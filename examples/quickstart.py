from compute_planner import Job, providers_for, value_first
jobs = [Job("small", "evals", 1, 1, 1), Job("useful", "evals", 10, 2, 1)]
assert value_first(jobs)[0].job_id == "useful"
print(providers_for("pretrain_smoke"))
