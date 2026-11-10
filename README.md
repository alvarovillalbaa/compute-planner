# compute-planner

Last updated: 2026-11-10

Estimate training compute, rank jobs, and choose candidate providers without executing them.

**Status: implemented.** A standard-library Python 3.11+ library and CLI are present. Installation/build proof is recorded separately from source checks.

## Independent use

From this repository:

```sh
python3 -m pip install .
python3 -m compute_planner.cli estimate-cost examples/estimate.json
python3 examples/quickstart.py
```

No sibling checkout, GPU, account, database, or network service is needed for these examples.

## Ownership

The 6NT language-model estimate, ordered provider recommendations, FIFO, cheapest-first, and risk-adjusted value ordering.

Outside this component: Cloud allocation, provider credentials, live pricing, training, or budget enforcement.

## Compose

Use independently, or register a pinned version in [Lab](https://github.com/alvarovillalbaa/lab). A dependency on Lab is never required. Libraries connect through declared dependencies or explicit artifact/job interfaces.

[Specification and next work](docs/specs/README.md) · [Extraction provenance](docs/sources/lab-provenance.json)

MIT applies to the code and authored documentation in this repository. External datasets, model weights, provider services, and third-party projects retain their own terms.

`estimate_from_spec` supports token-based language-model GPU training only. CPU/MPS, serving workloads, and non-finite resource inputs are rejected. Estimates are not measured billing and do not enforce the supplied budget. Provider rankings are historical defaults, not current availability or pricing. `examples/routing.json` is checked against the library defaults.
