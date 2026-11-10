import json
import unittest
from pathlib import Path

from compute_planner import Job, cheapest_first, fifo, providers_for, value_first


class SchedulingTests(unittest.TestCase):
    def test_policy_order_and_fifo_input(self):
        cheap = Job("cheap", "evals", 1, 1, 1)
        valuable = Job("valuable", "evals", 10, 2, 1)
        jobs = [valuable, cheap]
        self.assertEqual(cheapest_first(jobs), [cheap, valuable])
        self.assertEqual(value_first(jobs), [valuable, cheap])
        self.assertEqual(fifo(jobs), jobs)
        self.assertIsNot(fifo(jobs), jobs)
        self.assertEqual(jobs, [valuable, cheap])

    def test_route_example_matches_defaults(self):
        routes = json.loads((Path(__file__).resolve().parents[1] / "examples/routing.json").read_text())
        for key, value in routes.items():
            self.assertEqual(providers_for(key), value)
        with self.assertRaises(KeyError):
            providers_for("unknown")


if __name__ == "__main__":
    unittest.main()
