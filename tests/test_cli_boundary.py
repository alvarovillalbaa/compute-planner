import importlib.util
import io
from contextlib import redirect_stdout, redirect_stderr
import unittest

import compute_planner
from compute_planner.cli import main


class CliBoundaryTests(unittest.TestCase):
    def test_route_command_retains_native_output(self):
        stdout = io.StringIO()
        with redirect_stdout(stdout):
            self.assertEqual(main(["route", "pretrain_smoke"]), 0)
        self.assertEqual(stdout.getvalue().splitlines(), ["local", "runpod", "lambda_cloud"])

    def test_economics_api_is_removed_without_a_forwarder(self):
        self.assertIsNone(importlib.util.find_spec("compute_planner.costing"))
        for name in ("CostEstimate", "estimate_from_spec", "format_estimate"):
            self.assertFalse(hasattr(compute_planner, name))
        stderr = io.StringIO()
        with redirect_stderr(stderr), self.assertRaises(SystemExit) as raised:
            main(["estimate-cost", "unread-fixture.json"])
        self.assertEqual(raised.exception.code, 2)
        self.assertIn("invalid choice", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
