import click
from datetime import datetime
from core.host import Host
from core.parser import parse_crontab_text
from core.models import CronEntryList

@click.command()
@click.option("--from", "from_time", required=True, help="Start time (ISO format or relative)")
@click.option("--to", "to_time", default=None, help="End time (default: now)")
@click.option("--format", type=click.Choice(["text", "json"]), default="text")
@click.option("--user", default=None, help="User to read crontab for")
def cli(from_time, to_time, format, user):
    """List cron jobs that would have run in a given timeframe."""
    start = datetime.fromisoformat(from_time)
    end = datetime.fromisoformat(to_time) if to_time else datetime.now()

    host = Host(name="localhost")
    crontab_text = host.read_crontab(user=user)

    entries = parse_crontab_text(crontab_text, start, end)
    cron_list = CronEntryList(entries=entries)

    if format == "json":
        click.echo(cron_list.to_json(pretty=True))
    else:
        click.echo(cron_list.to_text())
