and_commute(p q: Prop): the and operator is commutative
show (p ∧ q → q ∧ p) ∧ (q ∧ p → p ∧ q)
  p_q_implies_q_p(p q: Prop): if p ∧ q, then q ∧ p
  q_p_implies_p_q(p q: Prop): if q ∧ p, then p ∧ q