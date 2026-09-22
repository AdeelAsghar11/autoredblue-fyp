"""Run the precision/recall + local-vs-cloud evaluation harness.

Compares `triaged_findings` against eval/ground_truth/ for DVWA and Juice
Shop, and (per docs/ARCHITECTURE.md's two-machine plan) is meant to be run
on both the dev and lab PCs to compare model tiers. No owner assigned yet,
see eval/__init__.py.
"""

from __future__ import annotations

# TODO: load eval/ground_truth/, run the graph against each target,
# compare triaged_findings to ground truth, compute precision/recall.


def main():
    """Run the evaluation harness and print/save precision/recall
    results.

    TODO
    """
    raise NotImplementedError


if __name__ == "__main__":
    main()
