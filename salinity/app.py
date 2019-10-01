import click
from salinity import log_utils, parser


@click.command()
@click.option("-v", "--verbose", count=True)
@click.option("-q", "--quiet", count=True)
@click.argument("salt_log_file", type=click.File(mode="r"))
def main(verbose, quiet, salt_log_file):
    """
    Parses a file containing the logs printed out by salt-call during highstate and prints out a short report.

    SALT_LOG_FILE must be a file containing the logs printed by salt-call during a highstate.
    """
    log_utils.setup_logging(verbose, quiet)
    parsed_output = parser.parse(salt_log_file.read())
    changes = parsed_output["changes"]
    duration_sorted_changes = sorted(
        changes, key=lambda element: element["duration_ms"], reverse=True
    )
    click.echo("Top changes:")
    for i in range(0, min(10, len(changes))):
        change = duration_sorted_changes[i]
        click.echo(
            f"{i + 1}. {change['duration_ms']} ms: {change['function']}: {change['name']}"
        )
