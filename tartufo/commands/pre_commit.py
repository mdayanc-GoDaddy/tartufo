import pathlib
from typing import Tuple

import click

from tartufo import types, util
from tartufo.scanner import GitPreCommitScanner


@click.command("pre-commit")
@click.option(
    "--include-submodules/--exclude-submodules",
    is_flag=True,
    default=False,
    show_default=True,
    help="Controls whether the contents of git submodules are scanned",
)
@click.pass_obj
@click.pass_context
def main(
    ctx: click.Context, options: types.GlobalOptions, include_submodules: bool
) -> Tuple[str, GitPreCommitScanner]:
    """Scan staged changes in a pre-commit hook."""
    # Assume that the current working directory is the appropriate git repo
    repo_path = pathlib.Path.cwd()
    scanner = None
    try:
        scanner = GitPreCommitScanner(options, str(repo_path), include_submodules)
        scanner.scan()
    except types.ScanException as exc:
        util.fail(str(exc), ctx)
    return (str(repo_path), scanner)  # type: ignore
