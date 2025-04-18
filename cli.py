import click
from commands import list as list_cmd

@click.group()
def cli():
    """cron-audit: Analyze and interact with crontabs."""
    pass

cli.add_command(list_cmd.cli, name="list")

if __name__ == "__main__":
    cli()
