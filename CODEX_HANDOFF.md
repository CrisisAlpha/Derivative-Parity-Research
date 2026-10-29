# Codex handoff — first implementation and Lean 4 review

## What is handed over
This archive is the **bridge** from a ChatGPT scientific-planning session to Codex. ChatGPT cannot inject its entire conversation or local sandbox into a Codex session automatically. This package therefore includes the source tree, `AGENTS.md` repository rules, `CODEX_TASK_PROMPT.txt` for the first Codex turn, and a claim-verification register.

The GitHub repository is `CrisisAlpha/Derivative-Parity-Research` (public). It was inspected and was empty in the preparatory session. Attempts to write through the *ChatGPT* GitHub integration produced HTTP 403; this does not imply Codex itself lacks GitHub rights.

## Recommended first-time bootstrap (Codex on desktop / local checkout)
1. Download the ZIP to your computer and **extract it**.
2. In Codex, open a local checkout (clone) of `https://github.com/CrisisAlpha/Derivative-Parity-Research`.
3. Put the CONTENTS of `Derivative-Parity-Research/` from the extracted archive directly in the checkout root. Do not put the folder itself one level down. The root should contain `AGENTS.md`, `LeanNotes.lean`, `pyproject.toml`, `manuscript/`, `src/`, and `tests/`.
4. Start a Codex chat on that folder. Paste `CODEX_TASK_PROMPT.txt` as the task. Ask Codex to run and record checks and open a **draft PR**, not to merge.
5. After that first push, GitHub is the common state for both ChatGPT and Codex. Start future tasks using Codex Cloud environments if desired, with the repository selected and authorized; this eliminates repeat ZIP handoffs.

Alternative: if the Codex interface supports attaching an archive directly, attach the ZIP and tell Codex to extract it into a checkout of the target repo. Verify the extracted files exist before proceeding. Cloud tasks do not automatically see ChatGPT's `/mnt/data` path or prior chat state.

## What belongs where
- **ChatGPT:** literature synthesis, critique of novelty, mathematical assumptions, experimental design, interpretation and manuscript review.
- **Codex:** edit Lean/Python/LaTeX, run pinned `lake build`, run numerical tests, assemble exact certificates, open and iterate on draft PRs.
- **GitHub:** durable single source of truth, CI logs, commits, issues and reviewer feedback.

## Initial milestone acceptance gates
- `lake build` has actually run successfully and Lean toolchain/version recorded; otherwise record a blocker.
- `python -m pytest -q` passes after correct installation, with test output recorded.
- Exact finite-state witness/dual certificates accompany sharp 3-event price bounds (preferably checked by Lean).
- Markdown/LaTeX never claims numerical experiments are formal theorems.
- `research/claim_registry.md` updated with evidence links and current statuses.
- A draft PR exists on GitHub, remains unmerged, and the user can review it.

**Not done yet:** no Lean compiler run was performed in ChatGPT's preparatory environment, no GitHub push succeeded from ChatGPT, and no draft PR was created there.
