# Collectors Guide

Webmin Homelab Monitor gathers information through a set of small collectors.

Each collector is responsible for one area of the system, such as CPU usage, storage, RAID, networking, Docker, backups, or weather.

The project is intentionally modular.

You can:

- Enable collectors you need
- Disable collectors you do not use
- Modify existing collectors
- Add new collectors
- Replace collectors with alternatives that better match your environment

---

# Collector States

Most collectors return one of these states:

```text
Operational
Attention
N/A
Disabled
```

These states are used by the dashboard and overall health logic.

## Operational

The collector was able to run and the monitored component appears healthy.

## Attention

The collector detected a condition that may require review.

Examples:

- RAID array not clean
- Storage usage above the warning threshold
- Docker container not running
- Backup timer inactive
- Network connectivity failure
- Firewall disabled

## N/A

The collector is enabled, but the module could not determine a valid result.

Possible causes include:

- Missing software
- Incorrect device path
- Incorrect interface name
- Missing permissions
- Unexpected command output
- Service not installed

## Disabled

The collector was intentionally disabled in `config.pl`.

Disabled collectors are ignored by the overall health calculation.

---

# CPU Collector

The CPU collector reads:

```text
/proc/stat
```

twice with a short delay between samples.

It calculates CPU utilization based on the difference between total and idle CPU time.

The result is displayed as a percentage.

Example:

```text
CPU: 24%
```

The current health logic considers very high CPU utilization worthy of attention.

The threshold can be modified in `index.cgi`.

---

# Memory Collector

The memory collector reads:

```text
/proc/meminfo
```

and uses:

```text
MemTotal
MemAvailable
```

to estimate current memory utilization.

Example:

```text
Memory: 41%
```

The result is displayed as a percentage.

The current implementation treats very high memory utilization as an attention state.

---

# GPU Collector

GPU monitoring is handled through a configurable helper command.

Example configuration:

```perl
gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',
```

The command should return a single numeric percentage.

Example output:

```text
37
```

which the dashboard displays as:

```text
37%
```

If no command is configured:

```perl
gpu_stats_command => '',
```

the GPU result is displayed as:

```text
N/A
```

This design allows different GPU platforms to be supported without hardcoding one vendor.

Possible backends include:

- Intel GPU tools
- NVIDIA `nvidia-smi`
- AMD tools
- Custom scripts

---

# Uptime Collector

The uptime collector reads:

```text
/proc/uptime
```

and converts the result into:

```text
days
hours
minutes
```

Example:

```text
12d 4h 17m
```

This collector is informational and does not normally affect overall health.

---

# Storage Collector

The storage collector uses:

```bash
df -P -B1
```

against the configured mount point.

Example:

```perl
storage_mount => '/mnt/storage',
```

The collector reports:

- Capacity
- Used space
- Available space
- Percentage used
- Health state

Example:

```text
Capacity: 4.0 TB
Used: 1.2 TB
Available: 2.8 TB
Usage: 30%
```

If usage crosses the configured warning threshold, the collector reports:

```text
Attention
```

The default implementation monitors one filesystem.

It can be extended to support multiple mount points.

---

# RAID Collector

Enable RAID monitoring with:

```perl
raid_enabled => 1,
```

The collector is designed for Linux software RAID using `mdadm`.

Configuration example:

```perl
raid_array   => 'md0',
raid_devices => [qw(sda sdb)],
```

The collector reads RAID state from:

```text
/sys/block/<array>/md/
```

Examples:

```text
/sys/block/md0/md/array_state
/sys/block/md0/md/level
/sys/block/md0/md/raid_disks
```

It also checks configured member devices.

The collector reports information such as:

- Array state
- RAID level
- Number of expected disks
- Number of active/in-sync disks
- Overall RAID status

Example:

```text
RAID: Operational
Level: raid1
Devices: 2/2 active
Array state: clean
```

---

# RAID0 Warning

If the array level is:

```text
raid0
```

the dashboard displays:

```text
RAID0 provides no fault tolerance
```

This warning is informational.

A RAID0 array may still be functioning correctly while providing no redundancy.

---

# SMART Collector

Enable SMART monitoring with:

```perl
smart_enabled => 1,
```

Configure devices:

```perl
smart_devices => [qw(/dev/sda /dev/sdb)],
```

The collector runs:

```bash
smartctl -H
```

for each configured device.

Example:

```bash
smartctl -H /dev/sda
```

A passing SMART health result is displayed as:

```text
Operational
```

A failed health result becomes:

```text
Attention
```

If the collector cannot determine a result, it reports:

```text
N/A
```

SMART monitoring requires:

```text
smartmontools
```

---

# Docker Collector

Enable Docker monitoring with:

```perl
docker_enabled => 1,
```

The collector runs:

```bash
docker ps -a --format "{{.Names}}|{{.Status}}"
```

It records:

- Container name
- Container status

Example:

```text
jellyfin: Up 5 days
database: Up 5 days
reverse-proxy: Up 5 days
```

If any container is not reported as running with a status beginning with:

```text
Up
```

the Docker collector reports:

```text
Attention
```

If no containers can be read, the collector may report:

```text
N/A
```

The Webmin process must have permission to access Docker.

---

# Tailscale Collector

Enable Tailscale monitoring with:

```perl
tailscale_enabled => 1,
```

The collector uses:

```bash
tailscale status
```

and:

```bash
tailscale ip -4
```

It can display:

- Tailscale IPv4 address
- Tailnet devices visible
- Tailscale state
- Funnel detection

Example:

```text
Server IP: 100.64.0.10
Tailnet devices visible: 3
Funnel: Enabled
```

If Tailscale is unavailable or not configured, the collector may report:

```text
N/A
```

---

# UFW Collector

Enable UFW monitoring with:

```perl
ufw_enabled => 1,
```

The collector runs:

```bash
ufw status verbose
```

and parses:

- Firewall state
- Logging level
- Default incoming policy
- Number of allow rules
- SSH exposure summary

Example:

```text
Status: Operational
Logging: on (low)
Default incoming: deny
Allow rules: 8
SSH exposure: Restricted
```

The SSH exposure logic attempts to recognize private-network and Tailscale-restricted rules.

The collector is intended as a summary.

It should not replace reviewing the actual firewall configuration.

---

# Backup Collector

Enable backup monitoring with:

```perl
backup_enabled => 1,
```

The collector is designed around systemd timers and services.

Example:

```perl
backup_timer   => 'homelab-backup.timer',
backup_service => 'homelab-backup.service',
```

The collector uses commands such as:

```bash
systemctl is-active
```

```bash
systemctl show
```

```bash
systemctl list-timers
```

It reports:

- Timer state
- Last service result
- Last completion time
- Next scheduled run
- Overall backup health

Example:

```text
Last result: success
Last completed: Sep 14, 2026 03:02
Next scheduled: Sep 21, 2026 03:00
Timer: active
```

The collector reports:

```text
Attention
```

if the timer is not active or the last service result is not successful.

---

# Network Collector

Enable network diagnostics with:

```perl
network_enabled => 1,
```

The collector performs several independent checks.

Configured values include:

```perl
network_interface => 'eth0',
gateway           => '192.168.1.1',
internet_target   => '1.1.1.1',
dns_test_host     => 'example.com',
```

---

# Interface State

The collector reads:

```text
/sys/class/net/<interface>/operstate
```

Example:

```text
/sys/class/net/eth0/operstate
```

If the interface state is:

```text
up
```

the collector reports:

```text
Operational
```

---

# LAN Address

The collector uses:

```bash
ip -4 addr show dev <interface>
```

to determine the interface IPv4 address.

Example:

```text
192.168.1.50
```

---

# Gateway Test

The configured gateway is tested with ping.

Example:

```bash
ping -c 1 -W 1 192.168.1.1
```

This helps determine whether the server can reach the local router or gateway.

---

# Internet Test

The collector pings the configured internet target.

Example:

```perl
internet_target => '1.1.1.1',
```

It uses the ping output to determine:

- Internet reachability
- Packet loss
- Approximate latency

Example:

```text
Internet: Operational
Latency: 18.4 ms
Packet loss: 0%
```

---

# DNS Test

The collector uses:

```bash
getent hosts <hostname>
```

Example:

```bash
getent hosts example.com
```

If resolution succeeds:

```text
DNS: Operational
```

If resolution fails:

```text
DNS: Attention
```

---

# Why the Network Checks Are Separate

The collector intentionally tests multiple layers.

Example:

```text
Interface: Operational
Gateway: Operational
Internet: Operational
DNS: Attention
```

This suggests a DNS-specific problem.

Another example:

```text
Interface: Operational
Gateway: Operational
Internet: Attention
DNS: Attention
```

may indicate an upstream internet problem.

And:

```text
Interface: Attention
Gateway: Attention
Internet: Attention
DNS: Attention
```

may indicate a local interface or physical network problem.

This makes the dashboard more useful for troubleshooting than a single internet status indicator.

---

# Weather Collector

Enable weather with:

```perl
weather_enabled => 1,
```

The collector uses Open-Meteo.

Example configuration:

```perl
weather_location  => 'Example City, FL',
weather_latitude  => 28.0000,
weather_longitude => -81.0000,
```

The collector requests:

- Current temperature
- Feels-like temperature
- Relative humidity
- Weather code
- Wind speed
- Daily high
- Daily low
- Maximum precipitation probability

It uses:

```bash
curl
```

and Perl:

```text
JSON::PP
```

to retrieve and parse the response.

No API key is required.

---

# Weather Condition Mapping

Open-Meteo weather codes are converted into labels such as:

```text
Clear
Mostly Clear
Partly Cloudy
Cloudy
Fog
Drizzle
Rain
Snow
Rain Showers
Snow Showers
Thunderstorm
```

Unknown codes are displayed as:

```text
Unknown
```

---

# Overall Health Collector

The overall health calculation combines individual collector states.

Possible overall values include:

```text
Healthy
Attention
Unknown
```

The logic works roughly as follows:

1. If any enabled collector reports `Attention`, overall health becomes:

```text
Attention
```

2. If no collector reports `Attention`, but an enabled collector reports `N/A`, overall health becomes:

```text
Unknown
```

3. If enabled collectors are operational, overall health becomes:

```text
Healthy
```

4. Collectors set to:

```text
Disabled
```

are ignored.

This is important because users are not expected to run every supported service.

---

# Disabled Collector Behavior

A collector that is intentionally disabled should return:

```text
Disabled
```

instead of:

```text
N/A
```

This distinction matters.

`N/A` means:

```text
The collector was expected to work, but its status could not be determined.
```

`Disabled` means:

```text
The user intentionally chose not to use this collector.
```

Disabled collectors do not reduce overall health.

---

# Adding a Collector

A collector can be added as a normal Perl function.

Example:

```perl
sub temperature_info {
    my $output = `your-temperature-command 2>/dev/null`;

    return ("N/A", "N/A")
        unless $output;

    chomp($output);

    return ("Operational", $output);
}
```

Call the collector:

```perl
my ($temperature_status, $temperature_value) =
    temperature_info();
```

Then render it:

```perl
print qq{
<div class="hlm-placeholder">
    <strong>Temperature:</strong>
    <div class="hlm-status @{[health_class($temperature_status)]}">
        $temperature_status
    </div>
    <div>
        $temperature_value
    </div>
</div>
};
```

---

# Adding a Feature Toggle

For optional collectors, add a toggle to `config.pl.example`.

Example:

```perl
temperature_enabled => 1,
```

Then begin the collector with:

```perl
return ("Disabled", "N/A")
    unless $config{temperature_enabled};
```

This makes the collector optional without causing overall health to become unknown.

---

# Collector Design Guidelines

When adding collectors, try to follow these principles.

## Fail Safely

If a command fails, return:

```text
N/A
```

instead of allowing the entire dashboard to crash.

## Respect Disabled Features

If a collector is disabled, return:

```text
Disabled
```

and avoid running unnecessary commands.

## Avoid Unnecessary Privileges

Do not require root access unless the monitored information genuinely requires it.

## Avoid Untrusted Input

Do not pass untrusted user input directly into shell commands.

Configuration values should still be validated where practical.

## Keep Collectors Focused

A collector should generally be responsible for one category of information.

Examples:

```text
RAID
SMART
Docker
Backups
Network
```

This makes the code easier to understand and customize.

## Return Predictable States

Prefer consistent states:

```text
Operational
Attention
N/A
Disabled
```

This makes integration with overall health much easier.

---

# Possible Future Collectors

The project can be extended with many additional collectors.

## Hardware

- CPU temperature
- GPU temperature
- Fan speed
- UPS battery state
- Power consumption

## Storage

- ZFS pool health
- Btrfs health
- NVMe wear
- Disk temperature
- Scrub status
- Snapshot age

## Security

- Failed SSH logins
- Fail2ban status
- CrowdSec status
- Certificate expiration
- Open ports
- Webmin authentication failures

## Maintenance

- Pending package updates
- Reboot required
- Kernel version
- OS version
- Last update
- Last reboot

## Services

- Jellyfin
- Plex
- Immich
- Nextcloud
- Home Assistant
- Pi-hole
- AdGuard Home
- Syncthing
- Proxmox
- Game servers
- Custom APIs

## Networking

- Interface throughput
- WAN IP
- VPN health
- Link speed
- VLAN state
- Packet-loss history
- Tailscale direct versus relayed connectivity

---

# Testing Collectors

Whenever you add or modify a collector, test the underlying command manually first.

Examples:

```bash
df -h
```

```bash
smartctl -H /dev/sda
```

```bash
docker ps -a
```

```bash
tailscale status
```

```bash
ufw status verbose
```

```bash
systemctl list-timers
```

```bash
ip addr
```

```bash
ping -c 2 1.1.1.1
```

Then validate the CGI:

```bash
perl -c index.cgi
```

or, after installation:

```bash
perl -c /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

A successful result should show:

```text
syntax OK
```

---

# Keep Collectors Adaptable

The included collectors are examples.

They are not intended to define how every homelab must work.

Replace, remove, or extend them as needed.

The goal is to provide understandable building blocks that can be adapted to different hardware, services, and network designs.
