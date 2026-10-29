import StaticCertificate
import TwoDateCertificate

/-!
Finite-state event parity, with no external axioms and no `sorry`.
The foundational statements below concern Boolean settlements and rational arithmetic.
Imported modules certify two specific finite instances over real-valued laws.
No solver implementation or general Kantorovich/MOT strong duality is formalized.
-/
namespace ParityOT

/-- A binary joint claim pays exactly when both events settle true. -/
def joint (a b : Bool) : Nat := if a && b then 1 else 0

/-- The three-way intersection, represented as a binary settlement. -/
def triple (a b c : Bool) : Nat := if a && b && c then 1 else 0

/-- Every pathwise three-way intersection is a subset of the A-C pair. -/
theorem triple_le_ac (a b c : Bool) : triple a b c ≤ joint a c := by
  cases a <;> cases b <;> cases c <;> decide

/-- Likewise it is a subset of A-B. -/
theorem triple_le_ab (a b c : Bool) : triple a b c ≤ joint a b := by
  cases a <;> cases b <;> cases c <;> decide

/-- The inclusion-exclusion lower hedge, pathwise on every settlement. -/
theorem lower_subhedge (a b c : Bool) :
    (joint a b : Int) + (joint b c : Int) - (if b then 1 else 0) ≤ triple a b c := by
  cases a <;> cases b <;> cases c <;> decide

/-- Pathwise order induces expectation order for nonnegative finite weights.
This is the finite-state weak-duality step used by all event-price bounds. -/
theorem weighted_bound {n : Nat} (weights payoff hedge : Fin n → Rat)
    (hweights : ∀ i, 0 ≤ weights i)
    (hpointwise : ∀ i, payoff i ≤ hedge i) :
    (∑ i : Fin n, weights i * payoff i) ≤
    (∑ i : Fin n, weights i * hedge i) := by
  apply Finset.sum_le_sum
  intro i _
  exact mul_le_mul_of_nonneg_left (hpointwise i) (hweights i)

/-- A sharp interval can be proved using pathwise bounds plus explicit
attaining feasible couplings; no general LP duality theorem is assumed. -/
theorem bound_with_attainment {n : Nat} (weightsLo weightsHi payoff : Fin n → Rat)
    (feasible : (Fin n → Rat) → Prop)
    (lo hi : Rat)
    (hLo : feasible weightsLo)
    (hHi : feasible weightsHi)
    (hEvery : ∀ q, feasible q →
      lo ≤ ∑ i : Fin n, q i * payoff i ∧
      (∑ i : Fin n, q i * payoff i) ≤ hi)
    (hAttainsLo : (∑ i : Fin n, weightsLo i * payoff i) = lo)
    (hAttainsHi : (∑ i : Fin n, weightsHi i * payoff i) = hi) :
    (∀ q, feasible q →
      lo ≤ ∑ i : Fin n, q i * payoff i ∧
      (∑ i : Fin n, q i * payoff i) ≤ hi) ∧
    (∃ q, feasible q ∧ (∑ i : Fin n, q i * payoff i) = lo) ∧
    (∃ q, feasible q ∧ (∑ i : Fin n, q i * payoff i) = hi) := by
  constructor
  · exact hEvery
  constructor
  · exact ⟨weightsLo, hLo, hAttainsLo⟩
  · exact ⟨weightsHi, hHi, hAttainsHi⟩

end ParityOT
