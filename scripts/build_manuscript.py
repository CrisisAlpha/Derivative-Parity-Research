"""Build current LaTeX in an isolated output directory and verify the PDF.

Requires Tectonic 0.15.0 on PATH (or --tectonic PATH) and the manuscript extra.
Artifacts are for draft review, not publication. No handoff PDF is read.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
from xml.sax.saxutils import escape

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--tectonic", default="tectonic")
    args = parser.parse_args()
    output = ROOT / "outputs/manuscript-build"
    output.mkdir(parents=True, exist_ok=True)
    pdf = output / "main.pdf"
    # Stale success artifacts must never survive a failed rebuild.
    for name in ("main.pdf", "verification.json", "extracted.txt"):
        stale = output / name
        if stale.exists():
            stale.unlink()
    version = subprocess.check_output([args.tectonic, "--version"], text=True).strip()
    if not re.search(r"\b0\.15\.0\b", version):
        raise RuntimeError(f"Expected Tectonic 0.15.0; got {version}")
    inputs = [ROOT / "manuscript/main.tex", ROOT / "manuscript/references.bib",
              ROOT / "outputs/figures/transport_bound_comparison.png"]
    hashes = {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in inputs}
    command = [args.tectonic, "--keep-logs", "--keep-intermediates", "--outdir", str(output), "main.tex"]
    env = os.environ.copy()
    if os.name == "nt" and "FONTCONFIG_FILE" not in env:
        # The portable Windows release ships no system Fontconfig configuration.
        config = output / "fonts.conf"
        fonts = Path(env.get("WINDIR", "C:/Windows")) / "Fonts"
        config.write_text("<?xml version='1.0'?><fontconfig><dir>" +
                          escape(fonts.as_posix()) + "</dir><cachedir>" +
                          escape((output / "font-cache").as_posix()) +
                          "</cachedir></fontconfig>", encoding="utf-8")
        env["FONTCONFIG_FILE"] = str(config)
    proc = subprocess.run(command, cwd=ROOT / "manuscript", capture_output=True, text=True,
                          encoding="utf-8", errors="replace", env=env)
    transcript = f"Compiler: {version}\nCommand: {command!r}\n" + proc.stdout + proc.stderr
    transcript += f"\nCOMPILER EXIT STATUS: {proc.returncode}\n"
    (output / "build.txt").write_text(transcript, encoding="utf-8")
    print(transcript, flush=True)
    proc.check_returncode()
    if hashes != {str(p.relative_to(ROOT)).replace("\\", "/"): sha(p) for p in inputs}:
        raise RuntimeError("Manuscript inputs changed during compilation")
    log = (output / "main.log").read_text(encoding="utf-8", errors="replace")
    if re.search(r"(?:Citation|Reference).*undefined|There were undefined|Rerun to get cross-references right|Missing character:|^!", log, re.M):
        raise RuntimeError("Unresolved reference/citation, missing glyph or TeX error in final log")
    reader = PdfReader(pdf, strict=True)
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    if len(reader.pages) < 4 or any(not (page.extract_text() or "").strip() for page in reader.pages):
        raise RuntimeError("Unexpected empty or truncated manuscript PDF")
    for marker in ["infimum", "supremum", "Verification boundary", "full-support"]:
        if marker not in text:
            raise RuntimeError(f"Current-source marker absent from PDF: {marker}")
    images = 0
    for page in reader.pages:
        objects = page["/Resources"].get("/XObject")
        if objects is not None:
            images += sum(obj.get_object().get("/Subtype") == "/Image"
                          for obj in objects.get_object().values())
    if not images:
        raise RuntimeError("Comparison figure missing from generated PDF")
    report = {"compiler": version, "compiler_exit": proc.returncode, "pages": len(reader.pages),
              "embedded_images": images, "inputs_sha256": hashes, "pdf_sha256": sha(pdf),
              "source_commit": subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
              "working_tree_dirty": bool(subprocess.check_output(["git", "status", "--porcelain"], cwd=ROOT, text=True)),
              "verification": "PASS", "purpose": "draft PR review artifact, not publication"}
    (output / "verification.json").write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
    (output / "extracted.txt").write_text(text, encoding="utf-8")
    print(json.dumps(report, indent=2), flush=True)


if __name__ == "__main__":
    main()
