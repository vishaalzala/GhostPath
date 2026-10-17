# Offline Suricata EVE and Zeek JSONL analysis

GhostPath evaluates *existing authorised* security event logs locally.
It does not capture, craft, transmit or inject network packets.

## Accepted formats
- Suricata EVE: newline-delimited JSON containing timestamp,
  event_type, proto, src_ip and optional flow-byte fields.
- Zeek JSON: newline-delimited JSON with ts, id.orig_h, proto and
  optional orig_bytes and resp_bytes.
- The traditional Zeek TSV log format is not supported in this version.

Files must be UTF-8 with extensions .jsonl, .json or .log.
Limits: up to 8 MiB, 20,000 events and 65,536 characters per event.
Mixed-format input is rejected.

## Usage

    ghostpath defense events --file /path/to/authorised-eve.jsonl --format eve --json
    ghostpath defense events --file /path/to/authorised-zeek.log --format zeek --json
    ghostpath defense events --file /path/to/events.jsonl --format auto --json

Outputs include per-minute event counts, flow-byte fields, an alert
count, protocol breakdown and pseudonymous source IDs. Raw IP addresses
are not returned.

## Limitations

Event count is not necessarily a request rate. The count depends on
which log types were enabled. A spike in logs does not prove malicious
traffic or a denial-of-service incident. Correlate with service error
rates and other independently verified indicators, and review false
positives.

Official documentation:
https://docs.suricata.io/en/latest/output/eve/eve-json-output.html
https://docs.zeek.org/en/current/log-formats.html
