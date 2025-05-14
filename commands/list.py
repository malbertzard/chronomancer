import click
from datetime import datetime
from core.host import Host
from core.parser import parse_crontab_text
from core.models import CronEntryList

def parse_iso_datetime(value: str) -> datetime:
    """Parse a string as ISO 8601 datetime, with error handling."""
    try:
        return datetime.fromisoformat(value)
    except ValueError:
        raise click.BadParameter(
            f"Invalid datetime format: '{value}'. Use ISO 8601 format like '2025-05-14T15:30:00'."
        )

@click.command(help="""
List cron jobs that would have run in a given timeframe.

Examples:
  python script.py --from "2025-05-14T00:00:00" --to "2025-05-14T23:59:59"
  python script.py --from "2025-05-14T12:00:00" --format json
""")

@click.option(
    "--from", "from_time", required=True,
    help="Start time in ISO 8601 format (e.g., '2025-05-14T12:00:00')",
    callback=lambda ctx, param, value: parse_iso_datetime(value)
)

@click.option(
    "--to", "to_time", default=None,
    help="End time in ISO 8601 format (default: now)",
    callback=lambda ctx, param, value: parse_iso_datetime(value) if value else None
)

@click.option(
    "--format", type=click.Choice(["text", "json"]),
    default="text", show_default=True,
    help="Output format"
)

@click.option(
    "--user", default=None,
    help="User to read crontab for (default: current user)"
)

# SSH Connection
@click.option(
    "--connection", type=click.Choice(["local", "ssh"]),
    default="local", show_default=True,
    help="Connection type: local or ssh"
)
@click.option("--ssh-user", help="Username for SSH connection")
@click.option("--ssh-hostname", help="Hostname for SSH connection")
@click.option(
    "--ssh-option", multiple=True,
    help="Extra SSH options (can be repeated, e.g., --ssh-option='-i key.pem')"
)

def cli(from_time, to_time, format, user,
        connection, ssh_user, ssh_hostname, ssh_option):
    start = from_time
    end = to_time or datetime.now()

    if end < start:
        raise click.BadParameter("End time must be after start time.")

    try:
        host = Host(
            name=ssh_hostname or "localhost",
            connection=connection,
            user=ssh_user,
            hostname=ssh_hostname,
            ssh_options=list(ssh_option)
        )
    except ValueError as e:
        raise click.ClickException(str(e))

    try:
        crontab_text = host.read_crontab(user=user)
    except Exception as e:
        raise click.ClickException(f"Failed to read crontab: {e}")

    try:
        entries = parse_crontab_text(crontab_text, start, end)
    except Exception as e:
        raise click.ClickException(f"Failed to parse crontab: {e}")

    cron_list = CronEntryList(entries=entries)

    if format == "json":
        click.echo(cron_list.to_json(pretty=True))
    else:
        click.echo(cron_list.to_text())
