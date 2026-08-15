# VFA-0.2 Construction Invariants

## 1. Causal object

\[
\boxed{\mathcal K_t=(R_t,F_t,D_t)}
\]

The treatment is restricted to `D_t`.

Required construction identity:

\[
\boxed{R_t^A=R_t^B,\qquad F_t^A=F_t^B,\qquad D_t^A\ne D_t^B.}
\]

## 2. Dormancy

The defining lineage invariant is

\[
\boxed{G=0\Rightarrow\frac{\partial T_{\rm forward}}{\partial D}=0.}
\]

Operationally, the forward subsystem receives no reserve handle, reserve path, arm identity, or dereference-capable interface while the gate is closed.

Behavioral equality is necessary but not sufficient; the implementation boundary is also statically audited.

## 3. Gate independence

\[
\boxed{G=g(E_{\rm insuff}),\qquad\frac{\partial G}{\partial D}=0.}
\]

The same external insufficiency evidence must produce the same gate value for both arms. The reserve cannot help decide whether the shared route failed.

## 4. Trace certificate

Define

\[
\boxed{\mathcal N(D_A,D_B)=1\iff\forall x\in\mathcal X_{\rm adapt}^{pre},\;T_A(x)\equiv_{\mathcal T_{\rm prereg}}T_B(x).}
\]

The frozen trace contains

\[
T=(I,A,C,\pi,E,S,M,L,\tau,R,O).
\]

`TRACE_EQUIVALENCE.json` defines the admissible relation. It is identity-only after deterministic canonicalization.

A single material reproducible mismatch is sufficient for failure:

\[
\exists x:T_A(x)\not\equiv T_B(x)\Rightarrow\texttt{D_PRE_ACTIVATION=FAIL}.
\]

No averaging can rescue a trace violation.

## 5. Three necessary certificates

The pre-activation D certificate is conjunctive:

\[
\boxed{D_{\rm pre}=PASS\iff\mathcal N=1\land Q_{\rm adapt}^A=Q_{\rm adapt}^B\land\operatorname{Sep}(\Phi_{\rm reserve}^A,\Phi_{\rm reserve}^B)=1}
\]

subject also to reserve-payload symmetry.

The clauses are independently necessary:

1. `N`: no pre-activation causal leakage into forward behavior or gate activation.
2. `Q_adapt`: exact equality on the frozen exhaustive pre-freeze surrogate universe.
3. `Sep(Phi_reserve)`: the treatment actually creates a dormant structural distinction.

## 6. Reserve quantity is not treatment

A/B reserve payloads must preserve:

- identical node payloads;
- identical node count;
- identical edge count;
- identical edge-kind multiset;
- identical canonical serialized byte length;
- identical ordinary forward machinery;
- identical compute/search budget before activation.

The current treatment changes only reserve relation bindings.

## 7. Reserve measurement

The current construction-side vector is

\[
\Phi_{\rm reserve}=(C_{\rm challenge},L_{\rm prov},A_{\rm preserve},R_{\rm reopen}).
\]

`A_preserve` is deliberately a presence/quantity measure here, not a binding-quality measure. Both arms retain one alternative edge per route, so it remains equal.

No scalar aggregation is permitted.

## 8. Adversarial leakage paths

The pre-activation suite attacks potential paths through:

- reserve serialization/order;
- dormant metadata and logging hints;
- candidate-identity contamination;
- memory reads/writes;
- operation-count/timing normalization;
- stopping behavior;
- gate activation;
- function signatures and static symbol references.

The intended architectural rule is stronger than “the solver happened not to use reserve”:

\[
\boxed{G=0\Rightarrow F_{\rm forward}\text{ has no dereference-capable path into }D.}
\]

## 9. Activation boundary

Only after shared external evidence satisfies the frozen gate may the reserve be dereferenced:

\[
E_{\rm insuff}\rightarrow G=1\rightarrow D\rightarrow\mathfrak C_{\rm correction}.
\]

The present construction audit does not execute that post-activation path and does not access a prospective future obligation.

## 10. Interpretation

A pre-activation PASS means only that the current implementation survived the specified construction-level noninterference attack.

It does **not** establish:

- future corrective benefit;
- benchmark authorization;
- adequacy of the full A-I audit;
- absence of all possible implementation confounds;
- a positive SSI result.

A future pre-activation leakage finding reopens this construction and localizes failure to the construction, not automatically to SSI theory.
