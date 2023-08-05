'''Given a JSON file, attempts to clone the given repositories.
Requires Python 3!
'''
import argparse
from .program import Program

def main():
	'''Entry point for program.
	'''

	parser = argparse.ArgumentParser(prog="gittools",
	description="Batches common Git operations.")
	parser.add_argument("-d", "--debug",
						action="store_true",
						help=("Show debug entries in standard output."
						"Result logs always include debug info."))
	parser.add_argument("--dryrun",
						action="store_true",
						help=("List actions that would be performed, but"
						"do not actually perform them if they would"
						"affect the filesystem."))
	parser.add_argument("-v", "--verbose",
						action="store_true",
						help=("Include timecodes in standard output"
						"and show verbose output that would normally be hidden."))

	#Add subparsers:
	subparsers = parser.add_subparsers(dest="command")
	#clone command
	cloneParser = subparsers.add_parser("clone",
	help=("Reconstructs the directory tree described in a JSON"
	"file, cloning all Git repositories listed and adding any"
	"listed remotes."))
	cloneParser.add_argument("target",
	help="Path to a JSON file describing the repositories to clone.")
	cloneParser.add_argument("-o", "--out", default=".",
	help="Path to the output directory.")
	#validate command
	validateParser = subparsers.add_parser("validate",
	help=("Checks that the given JSON"
	"file is valid for use in `gittools clone`."))
	validateParser.add_argument("target",
	help="Path to a JSON file describing the repositories to clone.")
	#TODO: Can this be removed?
	validateParser.set_defaults(out=".")
	#pull command
	pullParser = subparsers.add_parser("pull",
	help=("Performs `git pull origin` on all Git repositories"
	"recursively below the given directory. Does not"
	"recurse on repository directories."))
	pullParser.add_argument("target",
	help="Path to the top of the directory tree to update.")
	#export command
	exportParser = subparsers.add_parser("export",
	help=("Exports all Git repositories"
	"recursively below the given directory to a JSON dictionary."
	"Does not recurse on repository directories."))
	exportParser.add_argument("target",
	help="Path to the top of the directory tree to export.")
	exportParser.add_argument("-o", "--out",
	help=("Path to the output dictionary file. If omitted, writes"
	"to the current working directory."))
	exportParser.add_argument("-f", "--force",
	action="store_true",
	help=("Overwrites the output dictionary file if it already "
	"exists."))
	#get-branches command
	getBranchesParser = subparsers.add_parser("getbranches",
	help=("Lists the current branch of all Git repositories"
	"recursively below the given directory."
	"Does not recurse on repository directories."))
	getBranchesParser.add_argument("target",
	help="Path to the top of the directory tree to list.")

	args = parser.parse_args()
	if not args.command:
		args = parser.parse_args(["--help"])
	Program(args).run()

if __name__ == "__main__":
	main()
