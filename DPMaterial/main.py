import argparse
import json
import logging
import os
from typing import List, Optional
from dflow import Workflow
from DPMaterial.property.LAMMPS_flow import density
from typing import List, Optional
import argparse
import json
from dflow.plugins.dispatcher import DispatcherExecutor

def main_parser():
    parser = argparse.ArgumentParser(
        description="Workflow management",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers(
        title="Valid subcommands", dest="command")

    parser_submit = subparsers.add_parser(
        "submit",
        help="Submit a property calculation workflow",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_submit.add_argument("param_props", help="the path of the param_props file.")
    parser_submit.add_argument("machine", help="the path of the machine file.")

    parser_make = subparsers.add_parser(
        "make",
        help="Create a structure generation workflow",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser_make.add_argument("param_props", help="the path of the param_props file.")
    parser_make.add_argument("machine", help="the path of the machine file.")

    return parser

def parse_args(args: Optional[List[str]] = None):
    """Commandline options argument parsing."""
    parser = main_parser()
    parsed_args = parser.parse_args(args=args)
    if parsed_args.command is None:
        parser.print_help()
    return parsed_args

def main():
    args = parse_args()
    if args.command == "submit":
        with open(args.param_props, "r") as f:
            para = json.load(f)
            location = para.get("location")
        with open(args.machine, "r") as f:
            machine = json.load(f)
        dispatcher_executor = DispatcherExecutor(machine)
        wf = density(location, dispatcher_executor )
        wf.submit(location, dispatcher_executor)
    elif args.command == "make":
        with open(args.location, "r") as f:
            param = json.load(f)
        with open(args.machine, "r") as f:
            machine = json.load(f)


if __name__ == "__main__":
    main()