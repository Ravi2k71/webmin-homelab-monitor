# Collectors

## CPU

Samples `/proc/stat` twice, approximately 250 ms apart, and calculates utilization from the delta.

## Memory

Reads `MemTotal` and `MemAvailable` from `/proc/meminfo` and reports percentage used.

## GPU

Runs a configurable local helper command expected to output a utilization percentage. This is intentionally hardware-specific because Linux GPU telemetry differs significantly between Intel, AMD, and NVIDIA.

## RAID

Reads Linux software RAID metadata from `/sys/block/<array>/md`. The collector checks array state, RAID level, configured disk count, and member `in_sync` state.

RAID is not a backup. RAID0 in particular provides no fault tolerance.

## Storage

Runs `df` against the configured mount and reports total, used, available, and percentage used. Usage at or above 80% is marked `Attention` by the template.

## SMART

Runs `smartctl -H` for each configured device. `PASSED` maps to `Operational`; failures map to `Attention`.

SMART health is useful but does not guarantee a drive will not fail. Consider adding temperature and attribute monitoring if desired.

## Docker

Runs `docker ps -a`. If every discovered container begins with status `Up`, Docker is considered `Operational`; stopped or failed containers produce `Attention`.

## Tailscale

Reads `tailscale status` and the node's IPv4 address. The template also detects the `Funnel on` section. Peer count includes devices visible in the status output and may include the local node.

## UFW

Parses `ufw status verbose` to report firewall state, logging, default incoming policy, allow-rule count, and a simple SSH-restriction indicator.

Review this logic for your own firewall conventions; it is a diagnostic summary, not a full firewall audit.

## Backup

Checks a configured systemd timer and oneshot service. The template reports timer state, last service result, last completion timestamp, and next timer occurrence.

## Weather

Uses Open-Meteo current and daily forecast data for configured coordinates. Weather codes are mapped to readable conditions.

## Network diagnostics

The network collector combines multiple checks so the dashboard can help identify *where* a failure occurs:

- Interface state: is the NIC logically up?
- LAN IP: what address is assigned?
- Gateway ping: can the server reach the local router?
- Internet ping: can the server reach an external IP without relying on DNS?
- DNS lookup: can the server resolve a hostname?
- Latency and packet loss: is connectivity degraded even when it is technically up?

Examples:

```text
Interface up + gateway up + internet down
=> likely upstream/ISP issue

Interface up + internet up + DNS down
=> likely DNS/resolver issue

Interface down + gateway down + internet down
=> investigate NIC, cable, switch, VLAN, or host networking
```

## Overall Health

Overall Health aggregates CPU, memory, RAID, storage, SMART, Docker, Tailscale, UFW, backup, and network status. Any `Attention` result makes the overall result `Attention`; otherwise an unavailable input can produce `Unknown`; all healthy inputs produce `Healthy`.
