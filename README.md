# Webmin Homelab Monitor

A customizable monitoring and health dashboard for Linux homelab servers, built as a Webmin module.

Webmin Homelab Monitor provides a single-page view of system utilization, storage health, services, networking, security, backups, weather, and overall server health.

This repository is a reusable template derived from a real homelab deployment. Machine-specific settings are separated from the main dashboard code so the project can be adapted to different servers, networks, storage layouts, and services.

---

## Live Demo

Want to see the dashboard before installing it?

**[View the live demo](https://ravi2k71.github.io/webmin-homelab-monitor/)**

The demo uses fictional example data and does **not** connect to a real server.

---
## Download

The latest installable Webmin module is available from the GitHub Releases page.

**[Download the latest release](https://github.com/Ravi2k71/webmin-homelab-monitor/releases/latest)**

Download the file ending in:

```text
.wbm.gz

## Features

The dashboard can monitor and display:

- CPU utilization
- Memory utilization
- GPU utilization
- System uptime
- Whole-server overall health summary
- Linux software RAID (`mdadm`) status
- Storage capacity and utilization
- SMART drive health
- Docker container status
- Tailscale status
- Tailscale Funnel detection
- UFW firewall status
- SSH exposure summary
- systemd backup-job status
- Network interface status
- LAN IP address
- Default gateway connectivity
- Internet connectivity
- DNS resolution
- Network latency
- Packet loss
- Optional Open-Meteo weather information

The project is intentionally modular. You do not need to use every collector.

---

## Designed to Be Customized

This project is a **starting point**, not a rigid monitoring appliance.

You are encouraged to modify it for your own homelab.

You can change:

- Dashboard branding
- Storage mount points
- RAID arrays
- SMART devices
- Network interfaces
- Gateways
- Connectivity tests
- Docker services
- Backup jobs
- Weather location
- Health thresholds
- Dashboard layout
- Colors and styling
- Status labels
- Existing collectors
- Which collectors are enabled
- Additional custom collectors

Your server does **not** need to match the example environment.

For example, you could adapt the dashboard to monitor services such as:

- Jellyfin
- Plex
- Immich
- Nextcloud
- Home Assistant
- Pi-hole
- AdGuard Home
- Syncthing
- Proxmox
- Virtual machines
- Game servers
- Kubernetes workloads
- UPS devices
- ZFS pools
- Btrfs filesystems
- Custom systemd services

See [Customization](docs/CUSTOMIZATION.md) for more information.

---

## Repository Layout

```text
webmin-homelab-monitor/
├── README.md
├── LICENSE
├── .gitignore
│
├── module/
│   ├── index.cgi
│   ├── module.info
│   └── config.pl.example
│
├── docs/
│   ├── index.html
│   ├── INSTALLATION.md
│   ├── CONFIGURATION.md
│   ├── CUSTOMIZATION.md
│   └── COLLECTORS.md
│
└── examples/
    ├── basic-config.pl
    └── full-config.pl
```

### `module/`

Contains the actual Webmin monitoring module.

- `index.cgi` — main dashboard and collector logic
- `module.info` — Webmin module metadata
- `config.pl.example` — example user configuration

### `docs/`

Contains project documentation and the static GitHub Pages demo.

### `examples/`

Contains example configurations showing how the monitor can be adapted to different homelab environments.

---

## Requirements

### Core Requirements

- Linux
- Webmin
- Perl
- `iproute2`
- `ping`
- `getent`
- `df`

### Optional Requirements

Depending on which collectors you enable, you may also need:

- `smartmontools`
- `mdadm`
- Docker CLI
- Tailscale CLI
- UFW
- `curl`
- Perl `JSON::PP`
- systemd

You only need to install the tools required by the features you plan to use.

---

## Quick Start

### 1. Install Webmin

Install Webmin using the installation method recommended for your Linux distribution.

Make sure you can successfully log in before installing the monitoring module.

---

### 2. Copy the Module

Copy the contents of the `module/` directory to your Webmin installation.

A typical location is:

```bash
/usr/share/webmin/webmin-homelab-monitor/
```

For example:

```bash
sudo mkdir -p /usr/share/webmin/webmin-homelab-monitor
sudo cp module/* /usr/share/webmin/webmin-homelab-monitor/
```

---

### 3. Create Your Configuration

Copy the example configuration:

```bash
cd /usr/share/webmin/webmin-homelab-monitor/
sudo cp config.pl.example config.pl
```

Then edit it:

```bash
sudo nano config.pl
```

Change the example values to match your server.

Example:

```perl
our %config = (

    dashboard_name => 'My Homelab Monitor',

    storage_mount => '/mnt/storage',

    raid_array   => 'md0',
    raid_devices => [qw(sda sdb)],

    smart_devices => [qw(/dev/sda /dev/sdb)],

    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    weather_location  => 'Example City, FL',
    weather_latitude  => 28.0000,
    weather_longitude => -81.0000,

    backup_timer   => 'homelab-backup.timer',
    backup_service => 'homelab-backup.service',

);

1;
```

Your actual values will depend on your system.

---

### 4. Make the CGI Executable

```bash
sudo chmod +x /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

---

### 5. Verify Perl Syntax

Before opening the module in Webmin, verify the CGI file:

```bash
perl -c //usr/share/webmin/webmin-homelab-monitor/index.cgi
```

A successful result should look similar to:

```text
syntax OK
```

---

### 6. Restart Webmin

If needed:

```bash
sudo systemctl restart webmin
```

---

### 7. Allow Your Webmin User to Access the Module

Webmin modules can be restricted by user permissions.

If you receive an error such as:

```text
Access denied
```

check the Webmin user or group permissions and allow access to the Homelab Monitoring module.

Do **not** disable Webmin's referer or CSRF protections just to make the module accessible.

---

### 8. Open the Dashboard

Log into Webmin and open:

**Webmin Homelab Monitor**

The dashboard should begin displaying information collected from your server.

---

## Configuration

Most environment-specific values should be stored in:

```text
config.pl
```

rather than being hardcoded into `index.cgi`.

The repository includes:

```text
config.pl.example
```

as a safe template.

Your real configuration may include values such as:

```perl
storage_mount
raid_array
raid_devices
smart_devices
network_interface
gateway
weather_location
weather_latitude
weather_longitude
backup_timer
backup_service
```

See [Configuration](docs/CONFIGURATION.md) for more information.

---

## Example Configurations

Two example configurations are included.

### Basic Configuration

```text
examples/basic-config.pl
```

Useful for a simpler system with only basic monitoring enabled.

### Full Configuration

```text
examples/full-config.pl
```

Shows a larger configuration with storage, RAID, SMART, networking, backups, weather, and additional monitoring options.

These are examples only.

You should adapt them to your own infrastructure.

---

## Collectors

The dashboard uses individual collectors to gather information from the operating system and installed tools.

Examples include:

- CPU utilization
- Memory utilization
- GPU utilization
- RAID state
- Filesystem capacity
- SMART health
- Docker container state
- Tailscale state
- UFW firewall state
- systemd backup state
- Network connectivity
- DNS resolution
- Weather information

The collectors are intended to be understandable and modifiable.

You can remove collectors you do not need or write your own.

See [Collectors](docs/COLLECTORS.md) for additional information.

---

## Adding Your Own Collector

You can extend the dashboard with additional Perl functions.

A very simple collector might look like:

```perl
sub example_info {
    my $output = `your-command 2>/dev/null`;

    return ("N/A", "N/A") unless $output;

    return ("Operational", $output);
}
```

You can then call the collector and display its result inside the dashboard.

Possible additions include:

- CPU temperature
- Disk temperature
- UPS battery state
- ZFS health
- Certificate expiration
- Failed SSH logins
- Available package updates
- Reboot-required status
- Internet bandwidth
- Virtual machine health
- Application-specific health checks

---

## Modifying the Dashboard

The HTML and CSS are contained within the CGI dashboard and can be modified.

You can:

- Reorder cards
- Rename headings
- Add new sections
- Remove unused sections
- Change card sizes
- Change styling
- Add additional status indicators
- Add more detailed diagnostics

When working with dynamic Perl-generated HTML, remember the difference between:

```perl
print qq{
    <p>$variable</p>
};
```

and:

```perl
print <<'HTML';
    <p>$variable</p>
HTML
```

`qq{}` performs Perl variable interpolation.

A single-quoted heredoc such as `<<'HTML'` does not.

This is important when adding dynamic dashboard values.

---

## Security

A monitoring dashboard often interacts with system utilities and infrastructure information, so security should be considered when modifying or deploying the module.

Recommended practices include:

- Keep Webmin access restricted
- Use HTTPS for Webmin
- Use strong authentication
- Use SSH keys instead of password authentication where practical
- Disable direct root SSH login
- Keep firewall rules restrictive
- Limit administrative interfaces to trusted networks or VPNs
- Keep Webmin's CSRF and referer protections enabled
- Avoid exposing Webmin directly to the public internet
- Review commands used by custom collectors
- Never place secrets directly inside the public repository

If using Tailscale or another private networking solution, Webmin can be limited to trusted private connectivity instead of public exposure.

---

## Security Notes

This project may display system and network information from your server.

Before publishing your configuration or modifications:

- Do not commit passwords, API tokens, SSH private keys, or private key material
- Keep your real `config.pl` out of Git
- Review hostnames, IP addresses, storage paths, and service names before publishing
- Keep Webmin protected with HTTPS and appropriate access controls
- Review any custom commands or collectors you add

The included `.gitignore` is intended to help keep local configuration files out of the repository.

---

## Demo Site

The GitHub Pages demo is located in:

```text
docs/index.html
```

It contains fictional example data and exists only to demonstrate the appearance and functionality of the dashboard.

It does not communicate with:

- A real Webmin server
- A real homelab
- Tailscale
- Docker
- Your network
- Your storage devices
- Any private API

Live demo:

**https://ravi2k71.github.io/webmin-homelab-monitor/**

---

## Troubleshooting

### Dashboard Does Not Appear in Webmin

Check:

```bash
ls -la /usr/share/webmin/webmin-homelab-monitor/
```

Verify that the directory contains:

```text
index.cgi
module.info
config.pl
```

---

### CGI Is Not Executable

Run:

```bash
sudo chmod +x /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

---

### Perl Syntax Error

Run:

```bash
perl -c /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

Correct any reported syntax errors before restarting Webmin.

---

### A Collector Shows `N/A`

This can mean:

- The required command is not installed
- The configured device does not exist
- The collector is disabled
- The Webmin process cannot access the resource
- The command output differs from what the collector expects

Test the command manually from the server first.

---

### SMART Information Is Missing

Install:

```bash
sudo apt install smartmontools
```

Then test a disk manually:

```bash
sudo smartctl -H /dev/sda
```

---

### RAID Information Is Missing

Check:

```bash
cat /proc/mdstat
```

and:

```bash
sudo mdadm --detail /dev/md0
```

Adjust the configured RAID array if necessary.

---

### Docker Information Is Missing

Check:

```bash
docker ps
```

Make sure Docker is installed and that the Webmin environment has permission to access it.

---

### Weather Does Not Load

Verify that:

- `curl` is installed
- Perl `JSON::PP` is available
- The server has internet connectivity
- Latitude and longitude are configured correctly

Test:

```bash
perl -MJSON::PP -e 'print "JSON::PP OK\n"'
```

---

## Project Philosophy

Webmin Homelab Monitor is meant to provide a useful foundation for people who want a lightweight monitoring interface inside Webmin without deploying a large monitoring platform.

It is not intended to replace tools such as:

- Grafana
- Prometheus
- Zabbix
- Nagios
- Uptime Kuma
- Netdata

Instead, it provides a convenient overview directly inside the server administration interface many homelab users already use.

The goal is to make the project:

- Understandable
- Customizable
- Lightweight
- Useful for small homelabs
- Easy to extend

---

## Contributions

Contributions, improvements, forks, and custom collectors are welcome.

Useful contributions could include:

- New collectors
- Additional Linux distribution support
- Improved error handling
- Better hardware detection
- Additional storage technologies
- Improved responsive styling
- Accessibility improvements
- Documentation improvements
- Installation scripts
- Webmin packaging improvements

If you modify the project for your own environment, consider sharing reusable improvements with the community.

---

## Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Configuration Guide](docs/CONFIGURATION.md)
- [Customization Guide](docs/CUSTOMIZATION.md)
- [Collectors](docs/COLLECTORS.md)
- [Live Demo](https://ravi2k71.github.io/webmin-homelab-monitor/)

---

## Disclaimer

This project is provided as a configurable example and should be reviewed before use on a production system.

Every homelab is different.

Commands, device paths, interfaces, permissions, distributions, storage layouts, firewall configurations, and services may differ from the examples in this repository.

Test changes carefully and keep backups before modifying production systems.

---

## License

This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.

You are free to use, study, modify, and redistribute the project under the terms of that license.

See [LICENSE](LICENSE) for the full license text.
