# Chronomancer

This CLI tool lists cron jobs that would have executed within a specified time range. It supports both local and SSH-based connections to retrieve crontab entries and provides output in text or JSON format.

## Installation

Clone the repository and install the required dependencies:

```bash
git clone https://github.com/malbertzard/Chronomancer.git
```

> Make sure you have Python 3.7+ installed.

---

## Usage

```bash
python script.py --from "2025-05-14T00:00:00" --to "2025-05-14T23:59:59"
```

Or with a different output format:

```bash
python script.py --from "2025-05-14T12:00:00" --format json
```

### Example over SSH:

```bash
python script.py \
  --from "2025-05-14T00:00:00" \
  --to "2025-05-14T23:00:00" \
  --connection ssh \
  --ssh-user ubuntu \
  --ssh-hostname example.com \
  --ssh-option="-i ~/.ssh/key.pem"
```

## Options
	
 --from
	**(Required)** Start time in ISO 8601 format (e.g. 2025-05-14T12:00:00)
--to
	End time in ISO 8601 format (default: now)
--format
	Output format: (default: text) or json
--user
	User whose crontab to read (default: current user)
--connection
	(default: local) or ssh
--ssh-user
	Username for SSH connection
--ssh-hostname 
	Hostname for SSH connection
--ssh-option
	Additional SSH options (e.g. `-i key.pem`) Repeatable.


## Example Output

### Text Format

```
[2025-05-14 01:00:00] /usr/bin/backup.sh
[2025-05-14 15:00:00] /usr/local/bin/cleanup
```

### JSON Format

```json
[
  {
    "time": "2025-05-14T01:00:00",
    "command": "/usr/bin/backup.sh"
  },
  {
    "time": "2025-05-14T15:00:00",
    "command": "/usr/local/bin/cleanup"
  }
]
```

## Error Handling

* **Invalid datetime format**: Must follow ISO 8601, e.g., `2025-05-14T12:00:00`.
* **Time range error**: End time must be after start time.
* **SSH connection failure**: Ensure SSH options and credentials are correct.
* **Crontab parsing failure**: Malformed or unsupported crontab entries may cause this.

