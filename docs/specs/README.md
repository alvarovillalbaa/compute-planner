# compute-planner specification

Last updated: 2026-11-10

Version 0.2.0 owns ordered provider recommendations, FIFO, cheapest-first, and
risk-adjusted value ordering. It does not require an economics package.

## Public interfaces

- `providers_for(job_type)`: ordered historical provider recommendations.
- `Job`: caller-supplied identity, type, expected value, expected cost, risk, and optional deadline.
- `fifo`, `cheapest_first`, `value_first`, `value_per_dollar`: pure ordering/scoring helpers.
- `compute-planner route JOB_TYPE`: route recommendations only.

Cost estimates and their template are owned by
[compute-economics](https://github.com/alvarovillalbaa/compute-economics).
The former costing imports and estimate-cost CLI were removed in 0.2.0.
A caller passes expected costs through values; no shared implementation or
runtime dependency is necessary.

## Next work

- Define a planning-to-runner handoff against a concrete execution consumer.
- Compare policies using the same frozen workload and cost assumptions.
- Keep provider capability and current availability explicit rather than inferred from defaults.

[Inherited blueprint](blueprint.md) and [inherited backlog](backlog.md) preserve
the original broader design. Their costing material is historical; current
economics ownership is separate. Existing dated receipts are not rewritten.

Source verification of 0.2.0 is recorded in the economics-extraction receipt.
Earlier 0.1.0 installed-package proof does not establish installation of 0.2.0.
