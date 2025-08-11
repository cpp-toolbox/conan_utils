import argparse
from main import interactively_create_conanfile, generate_conanfile_from_required_packages

# NOTE: this is very bad glue, instead we need to use c++ for everything, then meta parser the file we want to make available to the user, then we create a fuzzy matcher or abbreviation based function calling, this automates CLI's and now I hate CLI's becuase they're just bad glue every time.
def main():
    parser = argparse.ArgumentParser(description="Conanfile utility CLI")
    subparsers = parser.add_subparsers(dest="command", required=True)

    # Subcommand: interactive
    parser_interactive = subparsers.add_parser("interactive", help="Interactively create a conanfile")
    parser_interactive.add_argument("directory", nargs="?", default=".", help="Target directory")

    # Subcommand: generate
    parser_generate = subparsers.add_parser("generate", help="Generate a conanfile from required packages")
    parser_generate.add_argument("directory", nargs="?", default=".", help="Target directory")
    parser_generate.add_argument("output", nargs="?", default="conanfile.txt", help="Output conanfile path")

    args = parser.parse_args()

    if args.command == "interactive":
        interactively_create_conanfile(args.directory)
    elif args.command == "generate":
        generate_conanfile_from_required_packages(args.directory, args.output)

if __name__ == "__main__":
    main()
