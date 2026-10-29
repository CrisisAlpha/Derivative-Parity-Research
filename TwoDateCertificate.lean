import Mathlib.Data.Real.Basic
import Mathlib.Algebra.BigOperators.Fin
import Mathlib.Algebra.BigOperators.Field
import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Tactic.FinCases
import Mathlib.Tactic.NormNum

/-! Two-date finite MOT certificate on the eight lexicographic price paths.
All real-valued laws are covered. Discounted tradability and the common pricing
measure are economic assumptions; the mathematical hypotheses are explicit
zero expected gains at EACH first-date history (90 and 110). -/
noncomputable section
namespace ParityOT.TwoDate

def high : Fin 8 → ℝ := ![0,0,0,0,1,1,1,1]
def d70 : Fin 8 → ℝ := ![1,0,0,0,1,0,0,0]
def d90 : Fin 8 → ℝ := ![0,1,0,0,0,1,0,0]
def d110 : Fin 8 → ℝ := ![0,0,1,0,0,0,1,0]
def d130 : Fin 8 → ℝ := ![0,0,0,1,0,0,0,1]
def gain90 : Fin 8 → ℝ := ![-20,0,20,40,0,0,0,0]
def gain110 : Fin 8 → ℝ := ![0,0,0,0,-40,-20,0,20]
def target : Fin 8 → ℝ := ![0,0,0,0,1,1,0,0]
def lowerHedge (i : Fin 8) : ℝ := high i / 3 - d110 i / 3 - gain110 i / 60
def upperHedge (i : Fin 8) : ℝ := d130 i - gain110 i / 20
def price (q f : Fin 8 → ℝ) : ℝ := ∑ i, q i * f i

def Feasible (q : Fin 8 → ℝ) : Prop :=
  (∀ i, 0 ≤ q i) ∧ (∑ i, q i) = 1 ∧
  price q high = 1/2 ∧ price q d70 = 1/4 ∧ price q d90 = 1/4 ∧
  price q d110 = 1/4 ∧ price q d130 = 1/4 ∧
  price q gain90 = 0 ∧ price q gain110 = 0

def qLo : Fin 8 → ℝ := ![1/6,1/4,0,1/12,1/12,0,1/4,1/6]
def qHi : Fin 8 → ℝ := ![1/4,0,1/4,0,0,1/4,0,1/4]

theorem pathwise (i : Fin 8) : lowerHedge i ≤ target i ∧ target i ≤ upperHedge i := by
  fin_cases i <;> norm_num [lowerHedge, upperHedge, target, high, d110, d130, gain110]

theorem qLo_feasible : Feasible qLo := by
  norm_num [Feasible, price, qLo, high, d70, d90, d110, d130, gain90, gain110,
    Fin.sum_univ_succ, Fin.forall_fin_succ]

theorem qHi_feasible : Feasible qHi := by
  norm_num [Feasible, price, qHi, high, d70, d90, d110, d130, gain90, gain110,
    Fin.sum_univ_succ, Fin.forall_fin_succ]

theorem qLo_attains : price qLo target = 1/12 := by
  norm_num [price, qLo, target, Fin.sum_univ_succ]

theorem qHi_attains : price qHi target = 1/4 := by
  norm_num [price, qHi, target, Fin.sum_univ_succ]

theorem hedge_costs (q : Fin 8 → ℝ) (hq : Feasible q) :
    price q lowerHedge = 1/12 ∧ price q upperHedge = 1/4 := by
  rcases hq with ⟨_, _, hh, _, _, hd110, hd130, _, hg⟩
  have lo : price q lowerHedge = price q high / 3 - price q d110 / 3 -
      price q gain110 / 60 := by
    simp only [price, lowerHedge, mul_sub, ← mul_div_assoc, Finset.sum_sub_distrib,
      ← Finset.sum_div]
  have hi : price q upperHedge = price q d130 - price q gain110 / 20 := by
    simp only [price, upperHedge, mul_sub, ← mul_div_assoc, Finset.sum_sub_distrib,
      ← Finset.sum_div]
  rw [lo, hi, hh, hd110, hd130, hg]
  norm_num

theorem all_feasible_bounds (q : Fin 8 → ℝ) (hq : Feasible q) :
    1/12 ≤ price q target ∧ price q target ≤ 1/4 := by
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

theorem sharp_bounds :
    (∀ q, Feasible q → 1/12 ≤ price q target ∧ price q target ≤ 1/4) ∧
    (∃ q, Feasible q ∧ price q target = 1/12) ∧
    (∃ q, Feasible q ∧ price q target = 1/4) := by
  exact ⟨all_feasible_bounds, ⟨qLo, qLo_feasible, qLo_attains⟩,
    ⟨qHi, qHi_feasible, qHi_attains⟩⟩

end ParityOT.TwoDate
