"""Provider recommendations; workload economics has its own package."""
import argparse
import sys

from . import providers_for


def main(argv=None):
    parser = argparse.ArgumentParser(prog="compute-planner")
    sub = parser.add_subparsers(dest="command", required=True)
    sub.add_parser("route").add_argument("job_type")
    args = parser.parse_args(argv)
    try:
        print("\n".join(providers_for(args.job_type)))
    except KeyError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
