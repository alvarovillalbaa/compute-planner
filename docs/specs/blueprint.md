# Inherited compute-planner blueprint

Last updated: 2026-11-10

Historical design extracted from [Lab at ba67e51](https://github.com/alvarovillalbaa/lab/blob/ba67e510bab2703b1042993744ce099490221c1f/docs/specs/steps.md). The component specification owns current scope. This text does not prove implementation, current provider facts, or executed research.

# 2. Compute strategy and realistic budget

Use the standard rough compute estimate:

[
\text{training FLOPs} \approx 6 \times \text{parameters} \times \text{tokens}
]

For minimal cost, use the Chinchilla-style rule as your baseline: roughly scale model size and training tokens together; in practical terms, many people use about **20 training tokens per parameter** as a planning anchor. The Chinchilla paper’s core result was that compute-optimal training scales model size and token count together, correcting the old habit of training models too large on too few tokens. ([arXiv][11])

Current public GPU prices vary constantly, but as a live public reference, RunPod lists H100 PCIe at **$2.89/hr**, H100 SXM at **$3.29/hr**, A100 PCIe at **$1.39/hr**, and RTX 4090 at **$0.69/hr** on its pricing page. ([Runpod][12])

These are optimistic compute-only estimates, assuming good utilization and excluding storage, failed jobs, idle time, data processing, evals, and retries. Multiply by **1.5–2.5×** for a real budget.

| Run                | Params | Tokens | Assumed hardware           | Approx compute-only GPU cost | Why                                          |
| ------------------ | -----: | -----: | -------------------------- | ---------------------------: | -------------------------------------------- |
| Smoke              |   124M |   2.5B | 1× RTX 4090                |             ~$7 raw GPU cost | proves codepath                              |
| Mini               |   350M |     7B | 8× RTX 4090                |            ~$60 raw GPU cost | data/filtering ablations                     |
| Public v0          |   1.3B |    26B | 8× H100                    |           ~$550 raw GPU cost | first serious end-to-end model               |
| Strong small       |     3B |    60B | 8× H100                    |          ~$2.9k raw GPU cost | credible public model                        |
| 7B compute-optimal |     7B |   140B | 64× H100 or 8× H100 longer |           ~$16k raw GPU cost | stretch                                      |
| 7B overtrained     |     7B |     1T | 64× H100 or longer         |          ~$110k raw GPU cost | closer to modern strong small-model practice |

The **1.3B and 3B runs** are the sweet spot. They are large enough to force you to solve real LLM-training problems, but small enough that mistakes do not bankrupt you.

---

# 15. Phase 11 — autonomous GPU workload allocation

This is another good innovation target.

The mistake most teams make: they optimize one training run. You should optimize the **entire research portfolio**.

## 15.1 Workload types

| Workload            | Hardware                 |
| ------------------- | ------------------------ |
| data cleaning       | CPU-heavy, cheap         |
| tokenization        | CPU or cheap GPU         |
| teacher generation  | cheap GPUs / spot        |
| evals               | cheap GPUs, batchable    |
| 124M/350M ablations | 4090/A100                |
| 1B/3B training      | homogeneous 8× H100/A100 |
| RL rollouts         | H100/A100 + vLLM         |
| serving benchmark   | target deployment GPU    |

Do not mix heterogeneous GPUs inside one tightly coupled pretraining job unless the framework explicitly supports it well. Use heterogeneity across the workload queue.

## 15.2 Scheduler objective

Your scheduler should maximize:

[
\frac{\text{expected information gain or eval improvement}}{\text{expected dollars} \times \text{risk}}
]

Each job gets:

```yaml
job_id: data_ablation_350m_quality_v05
gpu_type_options: [RTX4090, A100, H100]
min_gpus: 1
max_gpus: 8
preemptible_ok: true
checkpoint_interval_minutes: 15
expected_value: 0.73
expected_cost_usd: 120
deadline: none
risk: 0.2
```

## 15.3 Scheduler policies to compare

| Policy              | Description                                        |
| ------------------- | -------------------------------------------------- |
| FIFO                | baseline                                           |
| cheapest-first      | minimize cost                                      |
| fastest-first       | minimize wall time                                 |
| value-per-dollar    | your first real policy                             |
| Bayesian scheduler  | prioritizes uncertain high-upside experiments      |
| preemption-aware    | chooses spot only when checkpointing makes it safe |
| portfolio optimizer | balances data, training, eval, distillation jobs   |

## 15.4 Metrics

Track:

* GPU utilization
* idle GPU-hours
* failed GPU-hours
* preemption recovery time
* queue wait time
* cost per completed experiment
* cost per benchmark improvement
* wall-clock time to decision
* number of ablations completed per $1,000

This can become a legitimate systems paper/blog:

> “Cost-aware autonomous scheduling for LLM training research.”

---
