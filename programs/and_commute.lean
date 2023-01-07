-- if p ∧ q, then q ∧ p
lemma p_q_implies_q_p(p q: Prop):

    p ∧ q → q ∧ p :=
begin
    intro h,
    cases h with hp hq,
    split,
        exact hq,
        exact hp,
end

-- Description: if p ∨ q, then q ∨ p
-- if q ∧ p, then p ∧ q
lemma q_p_implies_p_q(p q: Prop):

    (q ∧ p) → (p ∧ q) :=
begin
  intro h,
  split,
    exact h.right,
    exact h.left,
end

/-
  Theorem:
    If q ∧ p, then p ∧ q
-/
-- the and operator is commutative
lemma and_commute(p q: Prop):
  (p ∧ q → q ∧ p) ∧ (q ∧ p → p ∧ q) :=

begin
  apply and.intro,
  { apply p_q_implies_q_p },
  { apply q_p_implies_p_q }
end

-- Description: if p ∧ q, then p
-- Signature: p_and_q_implies_p(p q: Prop)

-- show (p ∧ q → q ∧ p) ∧ (q ∧ p → p ∧ q)


