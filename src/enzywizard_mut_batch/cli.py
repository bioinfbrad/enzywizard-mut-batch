from __future__ import annotations
import argparse

from .commands.mut_batch import add_mut_batch_parser


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="enzywizard-mut-batch",
        description="EnzyWizard-Mut-Batch: Run paired EnzyWizard analysis workflows for a wild-type protein and its mutant."
    )

    add_mut_batch_parser(parser)


    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()
    args.func(args)
