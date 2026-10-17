# GhostPath v2 — Offline Zeek JSON log reader

Use this module only with Zeek connection logs collected on systems
you own or have permission to administer.

GhostPath accepts existing UTF-8 newline-delimited Zeek JSON connection
logs with the extension .json, .jsonl, or .log. Ordinary Zeek TSV logs
are not supported; Zeek supports JSON-format log output separately.

## Usage

    ghostpath defense zeek --file /path/to/owned-conn.log --json

The tool summarises protocols, connection states, event counts grouped
by hour and the aggregate payload-byte fields. It excludes raw
source/destination IP addresses, hostnames and network identifiers.

## Limitations

- The log must be 8 MB or less and contain up to 50,000 JSON events.
- A log record describes a connection/event, not a request/packet flood.
- Network intrusion, capture, packet transmission and traffic generation
  are not implemented by this feature.
- These summaries cannot verify that a DDoS attack has occurred.
- Do not upload unredacted Zeek logs to public GitHub issues.

Zeek logging documentation:
https://docs.zeek.org/en/current/tutorial/logs.html
