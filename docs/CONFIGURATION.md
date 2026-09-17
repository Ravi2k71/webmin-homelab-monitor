# Configuration Guide

Webmin Homelab Monitor is designed to be customized through a local `config.pl` file.

The main dashboard logic lives in:

```text
module/index.cgi
```

Machine-specific settings should normally be kept in:

```text
config.pl
```

The repository includes:

```text
config.pl.example
```

as a safe starting point.

---

## Creating Your Configuration

After installing the module, copy the example configuration:

```bash
cd /usr/share/webmin/homelab-monitoring
sudo cp config.pl.example config.pl
```

Then edit it:

```bash
sudo nano config.pl
```

Your real `config.pl` should remain local to your server.

Do not commit it to Git if it contains private or environment-specific information.

---

# Example Configuration

A typical configuration may look like:

```perl
our %config = (

    # Dashboard
    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Custom Webmin monitoring and health dashboard',

    # GPU
    gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',

    # Storage
    storage_mount => '/mnt/storage',

    # RAID
    raid_enabled => 1,
    raid_array   => 'md0',
    raid_devices => [qw(sda sdb)],

    # SMART
    smart_enabled => 1,
    smart_devices => [qw(/dev/sda /dev/sdb)],

    # Network
    network_enabled   => 1,
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    # Connectivity checks
    internet_target => '1.1.1.1',
    dns_test_host   => 'example.com',

    # Weather
    weather_enabled   => 1,
    weather_location  => 'Example City, FL',
    weather_latitude  => 28.0000,
    weather_longitude => -81.0000,

    # Backup
    backup_enabled => 1,
    backup_label   => 'Homelab Server Backup',
    backup_timer   => 'homelab-backup.timer',
    backup_service => 'homelab-backup.service',

    # Optional integrations
    docker_enabled    => 1,
    tailscale_enabled => 1,
    ufw_enabled       => 1,

);

1;
```

---

# Feature Toggles

Most major collectors can be enabled or disabled independently.

Use:

```perl
1
```

to enable a collector and:

```perl
0
```

to disable it.

For example:

```perl
raid_enabled => 1,
```

enables RAID monitoring.

```perl
raid_enabled => 0,
```

disables RAID monitoring.

Available toggles include:

```perl
raid_enabled
smart_enabled
network_enabled
backup_enabled
docker_enabled
tailscale_enabled
ufw_enabled
weather_enabled
```

Disabled collectors are treated as intentionally unavailable and do not cause the overall server health status to become `Unknown`.

This allows the dashboard to work on systems that do not use every supported feature.

---

# Dashboard Settings

## Dashboard Name

```perl
dashboard_name => 'My Homelab Monitor',
```

Controls the main dashboard title shown in Webmin.

You can change this to anything you want.

Examples:

```perl
dashboard_name => 'Home Server Monitor',
```

```perl
dashboard_name => 'NAS Health Dashboard',
```

```perl
dashboard_name => 'Lab Infrastructure',
```

---

## Dashboard Description

```perl
dashboard_description => 'Custom Webmin monitoring and health dashboard',
```

Controls the description shown below the dashboard title.

---

# GPU Monitoring

GPU monitoring uses a configurable helper command:

```perl
gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',
```

The command should return a single numeric utilization value between:

```text
0
```

and:

```text
100
```

For example:

```text
42
```

would be displayed as:

```text
42%
```

If you do not want GPU monitoring, set:

```perl
gpu_stats_command => '',
```

The dashboard will then display:

```text
N/A
```

for GPU utilization.

Because GPU monitoring varies significantly between Intel, AMD, and NVIDIA hardware, the helper command is intentionally customizable.

---

# Storage Configuration

Set the filesystem or mount point you want the dashboard to monitor:

```perl
storage_mount => '/mnt/storage',
```

Examples:

```perl
storage_mount => '/media/storage',
```

```perl
storage_mount => '/srv/data',
```

```perl
storage_mount => '/mnt/nas',
```

The dashboard uses `df` to determine:

- Total capacity
- Used space
- Available space
- Percentage used

Storage usage at or above the configured internal warning threshold will appear as needing attention.

---

# RAID Monitoring

Enable RAID monitoring with:

```perl
raid_enabled => 1,
```

Disable it with:

```perl
raid_enabled => 0,
```

---

## RAID Array

Set the Linux software RAID array name:

```perl
raid_array => 'md0',
```

This corresponds to:

```text
/dev/md0
```

Another system might use:

```perl
raid_array => 'md1',
```

---

## RAID Devices

List the devices that belong to the array:

```perl
raid_devices => [qw(sda sdb)],
```

For example:

```perl
raid_devices => [qw(sdb sdc sdd)],
```

The collector checks Linux RAID information under:

```text
/sys/block/
```

and verifies how many configured devices are currently in sync.

---

## RAID0 Warning

If the detected RAID level is:

```text
raid0
```

the dashboard displays:

```text
RAID0 provides no fault tolerance
```

This is informational and does not automatically mean the array itself is malfunctioning.

---

# SMART Monitoring

Enable SMART monitoring:

```perl
smart_enabled => 1,
```

Disable it:

```perl
smart_enabled => 0,
```

Configure the drives to check:

```perl
smart_devices => [qw(/dev/sda /dev/sdb)],
```

Examples:

```perl
smart_devices => [qw(/dev/sdb /dev/sdc)],
```

or:

```perl
smart_devices => [qw(/dev/nvme0n1)],
```

SMART monitoring requires:

```text
smartmontools
```

On Debian/Ubuntu-based systems:

```bash
sudo apt install smartmontools
```

You can test a device manually with:

```bash
sudo smartctl -H /dev/sda
```

---

# Network Monitoring

Enable network diagnostics:

```perl
network_enabled => 1,
```

Disable them:

```perl
network_enabled => 0,
```

---

## Network Interface

Set the primary network interface:

```perl
network_interface => 'eth0',
```

Modern Linux systems may use names such as:

```text
enp3s0
```

```text
eno1
```

```text
ens18
```

You can find your interfaces with:

```bash
ip addr
```

or:

```bash
ip link
```

Then configure the correct one:

```perl
network_interface => 'enp3s0',
```

---

## Gateway

Set your network's default gateway:

```perl
gateway => '192.168.1.1',
```

The dashboard pings this address to help determine whether local network connectivity is working.

You can find your gateway with:

```bash
ip route
```

Look for a line similar to:

```text
default via 192.168.1.1 dev eth0
```

---

# Internet Connectivity Test

The dashboard can test connectivity to an external IP:

```perl
internet_target => '1.1.1.1',
```

Another common option is:

```perl
internet_target => '8.8.8.8',
```

This test is used to determine:

- Internet connectivity
- Packet loss
- Approximate latency

The target should normally be a reliable IP address that responds to ICMP ping.

---

# DNS Test

Configure a hostname for DNS testing:

```perl
dns_test_host => 'example.com',
```

The dashboard uses `getent` to verify that hostname resolution is functioning.

You may use another reliable domain:

```perl
dns_test_host => 'openai.com',
```

or:

```perl
dns_test_host => 'github.com',
```

---

# Why Network Tests Are Separate

The network collector checks several stages independently:

```text
Network interface
        ↓
Local gateway
        ↓
Internet connectivity
        ↓
DNS resolution
```

This helps distinguish different failure types.

For example:

```text
Interface: Operational
Gateway: Operational
Internet: Attention
DNS: Attention
```

may indicate an upstream internet connection problem.

While:

```text
Interface: Operational
Gateway: Operational
Internet: Operational
DNS: Attention
```

may indicate a DNS-specific issue.

---

# Docker Monitoring

Enable Docker monitoring:

```perl
docker_enabled => 1,
```

Disable it:

```perl
docker_enabled => 0,
```

When enabled, the dashboard runs:

```bash
docker ps -a
```

and displays container names and current status.

A running container normally appears similar to:

```text
Up 5 days
```

Containers that are stopped or otherwise not running may cause Docker health to show:

```text
Attention
```

The Webmin environment must have permission to communicate with Docker.

---

# Tailscale Monitoring

Enable Tailscale monitoring:

```perl
tailscale_enabled => 1,
```

Disable it:

```perl
tailscale_enabled => 0,
```

When enabled, the dashboard checks:

```bash
tailscale status
```

and:

```bash
tailscale ip -4
```

The dashboard can display:

- Tailscale IPv4 address
- Tailnet devices visible
- Tailscale status
- Funnel detection

Tailscale must already be installed and configured on the server.

---

# UFW Monitoring

Enable UFW monitoring:

```perl
ufw_enabled => 1,
```

Disable it:

```perl
ufw_enabled => 0,
```

The dashboard checks:

```bash
ufw status verbose
```

and displays information including:

- Firewall status
- Logging state
- Default incoming policy
- Number of allow rules
- SSH exposure summary

For security, a typical server configuration uses:

```text
Default incoming: deny
```

with specific services explicitly allowed.

The monitor should not be used as a replacement for reviewing your actual firewall rules.

---

# Backup Monitoring

Enable backup monitoring:

```perl
backup_enabled => 1,
```

Disable it:

```perl
backup_enabled => 0,
```

Backup monitoring is designed around systemd timers and services.

---

## Backup Label

The displayed name can be customized:

```perl
backup_label => 'Homelab Server Backup',
```

Examples:

```perl
backup_label => 'Photo Backup',
```

```perl
backup_label => 'Nightly NAS Backup',
```

---

## Backup Timer

Configure the systemd timer:

```perl
backup_timer => 'homelab-backup.timer',
```

You can check your timers with:

```bash
systemctl list-timers
```

---

## Backup Service

Configure the associated service:

```perl
backup_service => 'homelab-backup.service',
```

The dashboard checks information such as:

- Whether the timer is active
- Last service result
- Last completion time
- Next scheduled run

You can inspect the service manually with:

```bash
systemctl status homelab-backup.service
```

and:

```bash
systemctl status homelab-backup.timer
```

---

# Weather Monitoring

Enable weather:

```perl
weather_enabled => 1,
```

Disable weather:

```perl
weather_enabled => 0,
```

Weather information is retrieved from Open-Meteo.

No API key is required.

---

## Weather Location Name

The location displayed on the dashboard:

```perl
weather_location => 'Example City, FL',
```

This text is only used as a label.

---

## Latitude and Longitude

Set coordinates for your location:

```perl
weather_latitude  => 28.0000,
weather_longitude => -81.0000,
```

The dashboard uses these coordinates when requesting weather information from Open-Meteo.

The weather panel currently displays:

- Current temperature
- Feels-like temperature
- Humidity
- Weather condition
- Wind speed
- Daily high
- Daily low
- Rain probability

If you publish your configuration publicly, consider whether you want to expose highly precise location coordinates.

---

# Disabled Features

When a collector is disabled, the dashboard treats that collector as:

```text
Disabled
```

rather than:

```text
N/A
```

A disabled collector does not negatively affect the overall health calculation.

For example:

```perl
docker_enabled => 0,
```

does not cause:

```text
Overall Health: Unknown
```

simply because Docker is not installed.

This allows Webmin Homelab Monitor to work with many different homelab designs.

---

# Overall Health

The dashboard combines the enabled health checks into an overall status.

Possible overall states include:

```text
Healthy
Attention
Unknown
```

### Healthy

Enabled collectors are reporting normal operation.

### Attention

At least one enabled collector reports a condition that requires attention.

### Unknown

At least one enabled collector cannot determine its status.

Disabled collectors are ignored when calculating overall health.

---

# Minimal Configuration

You do not need to enable everything.

A simpler server might use:

```perl
our %config = (

    dashboard_name        => 'Home Server',
    dashboard_description => 'Basic server monitoring',

    gpu_stats_command => '',

    storage_mount => '/mnt/storage',

    raid_enabled  => 0,
    smart_enabled => 0,

    network_enabled   => 1,
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    internet_target => '1.1.1.1',
    dns_test_host   => 'example.com',

    backup_enabled    => 0,
    docker_enabled    => 1,
    tailscale_enabled => 0,
    ufw_enabled       => 1,
    weather_enabled   => 0,

);

1;
```

This is perfectly valid.

Your homelab does not need to use RAID, Tailscale, automated backups, or weather monitoring.

---

# Larger Configuration

A more complete server might enable everything:

```perl
raid_enabled      => 1,
smart_enabled     => 1,
network_enabled   => 1,
backup_enabled    => 1,
docker_enabled    => 1,
tailscale_enabled => 1,
ufw_enabled       => 1,
weather_enabled   => 1,
```

The dashboard is intended to support both simple and more complex environments.

---

# Keeping Configuration Private

Your actual:

```text
config.pl
```

should generally not be committed to Git.

The included `.gitignore` should contain:

```gitignore
config.pl
```

Public examples should use:

```text
config.pl.example
```

or files under:

```text
examples/
```

Before committing changes, check:

```bash
git status
```

to make sure your real configuration is not being added accidentally.

---

# Testing Configuration Changes

After changing `config.pl`, first check the main CGI syntax:

```bash
perl -c /usr/share/webmin/homelab-monitoring/index.cgi
```

You should see:

```text
syntax OK
```

Then reload the dashboard in Webmin.

If a collector displays:

```text
N/A
```

test the corresponding command manually.

Examples:

```bash
df -h
```

```bash
smartctl -H /dev/sda
```

```bash
docker ps
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

This can help determine whether the issue is with:

- Configuration
- Permissions
- Missing software
- Device naming
- Service state
- Collector parsing

---

# Customizing Beyond `config.pl`

`config.pl` handles the most common machine-specific settings.

The project is also intended to be modified at the code level.

You can:

- Add new collectors
- Remove collectors
- Change health thresholds
- Change status behavior
- Add additional services
- Modify dashboard styling
- Reorganize sections
- Add additional diagnostic information

See:

[Customization Guide](CUSTOMIZATION.md)

and:

[Collectors Guide](COLLECTORS.md)

for more information.

---

# Important

The example configuration is not intended to match every Linux system automatically.

Before enabling a collector, verify:

- The required software is installed
- The configured device exists
- The configured interface exists
- Webmin has permission to run the required command
- Service and timer names are correct
- File paths match your system

Webmin Homelab Monitor is designed to adapt to your infrastructure rather than requiring your infrastructure to match the example configuration.
