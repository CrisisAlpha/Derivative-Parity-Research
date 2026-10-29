import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-! Exact finite static certificate. Weights range over all real distributions;
the attaining weights are explicit rational constants. The state index is the
binary integer 4*A + 2*B + C, matching Python's lexicographic Boolean states.
No martingale restriction is imposed on these events. -/
noncomputable section
namespace ParityOT.Static

def a : Fin 8 → ℝ := ![0,0,0,0,1,1,1,1]
def b : Fin 8 → ℝ := ![0,0,1,1,0,0,1,1]
def c : Fin 8 → ℝ := ![0,1,0,1,0,1,0,1]
def ab (i : Fin 8) : ℝ := a i * b i
def bc (i : Fin 8) : ℝ := b i * c i
def ac (i : Fin 8) : ℝ := a i * c i
def target (i : Fin 8) : ℝ := a i * b i * c i
def lowerHedge (i : Fin 8) : ℝ := ab i + bc i - b i
def upperHedge (i : Fin 8) : ℝ := ac i
def price (q f : Fin 8 → ℝ) : ℝ := ∑ i, q i * f i

def Feasible (q : Fin 8 → ℝ) : Prop :=
  (∀ i, 0 ≤ q i) ∧ (∑ i, q i) = 1 ∧
  price q a = 3/5 ∧ price q b = 11/20 ∧ price q c = 9/20 ∧
  price q ab = 2/5 ∧ price q bc = 3/10 ∧ price q ac = 11/50

def qLo : Fin 8 → ℝ := ![17/100, 8/100, 0, 15/100, 13/100, 7/100, 25/100, 15/100]
def qHi : Fin 8 → ℝ := ![10/100, 15/100, 7/100, 8/100, 20/100, 0, 18/100, 22/100]

theorem pathwise (i : Fin 8) : lowerHedge i ≤ target i ∧ target i ≤ upperHedge i := by
  fin_cases i <;> norm_num [lowerHedge, upperHedge, target, ab, bc, ac, a, b, c]

theorem qLo_feasible : Feasible qLo := by
  norm_num [Feasible, price, qLo, ab, bc, ac, a, b, c, Fin.sum_univ_succ,
    Fin.forall_fin_succ]

theorem qHi_feasible : Feasible qHi := by
  norm_num [Feasible, price, qHi, ab, bc, ac, a, b, c, Fin.sum_univ_succ,
    Fin.forall_fin_succ]

theorem qLo_attains : price qLo target = 3/20 := by
  norm_num [price, qLo, target, a, b, c, Fin.sum_univ_succ]

theorem qHi_attains : price qHi target = 11/50 := by
  norm_num [price, qHi, target, a, b, c, Fin.sum_univ_succ]

theorem hedge_costs (q : Fin 8 → ℝ) (hq : Feasible q) :
    price q lowerHedge = 3/20 ∧ price q upperHedge = 11/50 := by
  rcases hq with ⟨_, _, _, hb, _, hab, hbc, hac⟩
  constructor
  · have expand : price q lowerHedge = price q ab + price q bc - price q b := by
      simp [price, lowerHedge, mul_sub, mul_add, Finset.sum_add_distrib,
        Finset.sum_sub_distrib]
    rw [expand, hab, hbc, hb]
    norm_num
  · exact hac

theorem all_feasible_bounds (q : Fin 8 → ℝ) (hq : Feasible q) :
    3/20 ≤ price q target ∧ price q target ≤ 11/50 := by
  have lo : price q lowerHedge ≤ price q target := by
    apply Finset.sum_le_sum
    intro i _
    exact mul_le_mul_of_nonneg_left (pathwise i).1 (hq.1 i)
  have hi : price q target ≤ price q upperHedge := by
    apply Finset.sum_le_sum
    intro i _
    exact mul_le_mul_of_nonneg_left (pathwise i).2 (hq.1 i)
  rw [(hedge_costs q hq).1] at lo
  rw [(hedge_costs q hq).2] at hi
  exact ⟨lo, hi⟩

/-- Bounds for every real feasible law, with both endpoints attained. This is
instance-specific finite optimality, not general Kantorovich strong duality. -/
theorem sharp_bounds :
    (∀ q, Feasible q → 3/20 ≤ price q target ∧ price q target ≤ 11/50) ∧
    (∃ q, Feasible q ∧ price q target = 3/20) ∧
    (∃ q, Feasible q ∧ price q target = 11/50) := by
  exact ⟨all_feasible_bounds, ⟨qLo, qLo_feasible, qLo_attains⟩,
    ⟨qHi, qHi_feasible, qHi_attains⟩⟩

end ParityOT.Static
