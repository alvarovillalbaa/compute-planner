# compute-planner

Last updated: 2026-11-10

Rank jobs and choose candidate providers without executing them.
Version **0.2.0** contains standard-library Python 3.11+ routing and scheduling
primitives. Economics is an independently usable component.

## Independent use

From this repository:

```sh
python3 -m pip install .
compute-planner route pretrain_smoke
python3 -m compute_planner.cli route pretrain_smoke
python3 examples/quickstart.py
```

No sibling checkout, compute-economics installation, GPU, account, database, or
network service is needed for these examples.

## Ownership

This package owns ordered provider recommendations, FIFO, cheapest-first, and
risk-adjusted value ordering. `Job.expected_cost_usd` is an estimate supplied
by the caller; it can come from compute-economics, another estimator, or an
explicit experimental assumption.

Cloud allocation, provider credentials, live pricing, workload cost models,
training, and budget enforcement are outside this component. Provider rankings
are historical defaults, not current availability or prices.
`examples/routing.json` is checked against the library defaults.

## Economics API change in 0.2.0

The costing implementation, cost example, native cost tests, and cost-ledger
template moved to [compute-economics](https://github.com/alvarovillalbaa/compute-economics).
Import `CostEstimate`, `estimate_from_spec`, and `format_estimate` from
`compute_economics`. Use `compute-economics estimate-cost SPEC.json`.
The old compute-planner costing module, exports, and estimate-cost command
are removed; no forwarding copy or mandatory economics dependency remains.

## Compose and proof

Use independently, or register a pinned version in [Lab](https://github.com/alvarovillalbaa/lab).
A dependency on Lab is never required. Connect estimates, jobs, and execution
through explicit values and interfaces.

[Specification](docs/specs/README.md) ·
[Initial Lab provenance](docs/sources/lab-provenance.json) ·
[Economics migration and source checks](docs/results/2026/11-10/economics-extraction.json)

The earlier installed receipt belongs to 0.1.0. Source checks for this 0.2.0
change do not establish fresh-install or wheel acceptance. Historical receipts
and blueprints remain unchanged. MIT terms and third-party input terms apply.
