# Webmin Homelab Monitor

A customizable Webmin dashboard for Linux homelabs. It provides a single-page view of system utilization, storage health, services, networking, security, backups, weather, and overall server health.

This repository is a reusable template derived from a real homelab deployment. Machine-specific values are kept in `config.pl`, which is intentionally excluded from Git.

## Features

- CPU, memory, GPU, and uptime
- Whole-server overall health summary
- Linux software RAID (mdadm) state
- Storage capacity and utilization
- SMART drive health
- Docker container status
- Tailscale status and Funnel detection
- UFW status and SSH exposure summary
- systemd backup-job status
- Network diagnostics: interface, LAN IP, gateway, internet, DNS, latency, packet loss
- Optional Open-Meteo weather panel

## Repository layout

```text
webmin-homelab-monitor/
├── README.md
├── .gitignore
├── module/
│   ├── index.cgi
│   ├── module.info
│   └── config.pl.example
├── docs/
│   ├── INSTALLATION.md
│   ├── CONFIGURATION.md
│   ├── COLLECTORS.md
│   ├── SECURITY.md
│   └── TROUBLESHOOTING.md
└── examples/
    ├── basic-config.pl
    └── full-config.pl
```

## Quick start

1. Install Webmin and the tools needed by the collectors you plan to enable.
2. Copy `module/` to `/usr/share/webmin/homelab-monitoring/`.
3. Copy `config.pl.example` to `config.pl` and edit it for your server.
4. Make `index.cgi` executable.
5. Allow your Webmin user to access the `homelab-monitoring` module.
6. Open **Homelab Monitoring** from Webmin.

See [Installation](docs/INSTALLATION.md) and [Configuration](docs/CONFIGURATION.md) for complete instructions.

## Important

This is a starting point, not a universal monitoring appliance. Linux distributions, device names, RAID layouts, backup jobs, Docker permissions, and firewall configurations vary. Review each collector before using it in production.

Never commit your real `config.pl`, private keys, passwords, tokens, certificates containing private keys, or other secrets.

## Requirements

Core:

- Linux
- Webmin
- Perl
- `iproute2`
- `ping`
- `getent`
- `df`

Depending on enabled collectors:

- `smartmontools`
- Docker CLI
- Tailscale CLI
- UFW
- `curl`
- Perl `JSON::PP`
- mdadm/Linux software RAID

## Customization

This project is designed to be adapted to your own homelab.

You can change the monitored services, storage layout, network configuration,
weather location, health thresholds, dashboard styling, collectors, and more.

See [CUSTOMIZATION.md](CUSTOMIZATION.md) for examples and guidance.

## License
Licensed under the GNU General Public License v3.0.
