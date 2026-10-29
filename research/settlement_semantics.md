# Settlement and execution semantics audit

## Contract identity

Record `venue`, `event_id`, `token_id`, precise resolution language and
`resolution_source`, market close vs event observation time, time zone,
threshold and inequality convention, and whether the event is monitored
continuously or only at a published timestamp. Two contracts are equivalent
only if payout semantics agree state by state.

## Cashflow identity

Record unit payout, collateral/quote currency, settlement lag, redemption
fees, potential oracle disputes, market suspensions, side-specific trading
restrictions, position transferability and conversion to cash. Any difference
may break the simple normalization `price = Q(event)`.

## Live market snapshots (future work, not run)

Required fields include UTC timestamp with subsecond precision, venue,
contract ID, event definition fingerprint, best bid, best ask, displayed depth
on both sides, tick size, maker/taker fee assumptions, funding/collateral
costs, venue outage flags and collection provenance. Take near-synchronous
snapshots of all legs. Verify whether bids/asks are actual executable orders.

## Conditional vs intersection

A token paying a dollar on `A AND B` has payoff `1_A 1_B`.
Its price under a normalized common measure is `Q(A AND B)`.
A conditional probability `Q(B | A)` equals `Q(A AND B) / Q(A)` if `Q(A)>0`.
This is an established identity awaiting Lean formalization, not a conjecture.
The event-specific `conditional_ratio_interval` API requires both payoff vectors
to be 0/1 indicators and the numerator event to be a subset of the conditioning
event on every state; a finite positive denominator cutoff is enforced. It is
not an optimizer for arbitrary payoff ratios. Its quote constraints and both
events must use the same settlement states and common pricing measure.
A digital claim conditional on `A` may instead void, refund or become
untradeable when `A` is false; this is a different payoff. Settlement code and
venue documentation, not naming conventions, determine the correct payoff.

## Dynamic hedge availability

A standard MOT dual has contingent positions in a dynamic underlying plus
static options. In prediction markets the analogue may not be executable:
traders may lack permission to short, markets may freeze when an event
resolves, and a state-dependent dynamic strategy can require impossible fills.
Such a dual is an analytical bound until executable venues and costs are shown.
