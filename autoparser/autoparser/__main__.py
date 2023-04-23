import sys

from .csv_mapping import main as csv_mapping_main
from .make_toml import main as make_toml_main


def main():
    if len(sys.argv) < 2:
        print(
            """autoparser: specify subcommand to run

Available subcommands:
  create-parser - Generate TOML parser from CSV mapping
  create-mapping - Create initial CSV mapping from data dictionary
"""
        )
        sys.exit(1)
    subcommand = sys.argv[1]
    if subcommand not in ["create-parser", "create-mapping"]:
        print("autoparser: unrecognised subcommand", subcommand)
        sys.exit(1)
    sys.argv = sys.argv[1:]
    if subcommand == "create-parser":
        make_toml_main()
    elif subcommand == "create-mapping":
        csv_mapping_main()
    else:
        pass


if __name__ == "__main__":
    main()
