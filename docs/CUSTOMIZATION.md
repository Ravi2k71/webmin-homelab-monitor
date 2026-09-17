# Customization Guide

Webmin Homelab Monitor is designed to be customized.

It is not intended to be a rigid monitoring appliance that requires every user to have the same hardware, network layout, storage configuration, services, or software.

The included setup is a starting point.

You can use only the parts that make sense for your homelab and modify the rest.

---

# What You Can Customize

Almost every part of the project can be changed.

Examples include:

- Dashboard name
- Dashboard description
- Storage mount points
- RAID array names
- RAID member devices
- SMART devices
- Network interfaces
- Default gateway
- Internet connectivity targets
- DNS test hosts
- Docker monitoring
- Tailscale monitoring
- UFW monitoring
- Backup jobs
- Weather location
- Health thresholds
- Status labels
- Dashboard layout
- Colors and styling
- Existing collectors
- Additional collectors

Your server does not need to match the example configuration.

---

# Feature Toggles

Major collectors can be enabled or disabled independently.

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

Use:

```perl
1
```

to enable a feature.

Use:

```perl
0
```

to disable it.

Example:

```perl
docker_enabled => 1,
```

enables Docker monitoring.

```perl
docker_enabled => 0,
```

disables Docker monitoring.

Disabled collectors do not negatively affect the overall health result.

This means a server that does not use RAID, Tailscale, Docker, UFW, automated backups, or weather monitoring can still use the dashboard normally.

---

# Start With `config.pl`

Most users should begin by customizing:

```text
config.pl
```

rather than editing `index.cgi`.

Copy the example file:

```bash
cp config.pl.example config.pl
```

Then edit it:

```bash
nano config.pl
```

A typical configuration may look like:

```perl
our %config = (

    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Custom Webmin monitoring dashboard',

    gpu_stats_command => '',

    storage_mount => '/mnt/storage',

    raid_enabled => 1,
    raid_array   => 'md0',
    raid_devices => [qw(sda sdb)],

    smart_enabled => 1,
    smart_devices => [qw(/dev/sda /dev/sdb)],

    network_enabled   => 1,
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    internet_target => '1.1.1.1',
    dns_test_host   => 'example.com',

    backup_enabled => 0,

    docker_enabled    => 1,
    tailscale_enabled => 0,
    ufw_enabled       => 1,

    weather_enabled => 0,

);

1;
```

The goal is to keep machine-specific settings outside the main CGI code whenever possible.

---

# You Do Not Need Every Feature

The dashboard should reflect your infrastructure.

Your infrastructure should not be changed just to satisfy the dashboard.

For example, if you do not use RAID:

```perl
raid_enabled => 0,
```

If you do not use Tailscale:

```perl
tailscale_enabled => 0,
```

If you do not use Docker:

```perl
docker_enabled => 0,
```

If you do not want weather information:

```perl
weather_enabled => 0,
```

This is expected and supported.

---

# Customize the Dashboard Name

Change:

```perl
dashboard_name => 'My Homelab Monitor',
```

to anything you want.

Examples:

```perl
dashboard_name => 'Home Server Dashboard',
```

```perl
dashboard_name => 'NAS Monitor',
```

```perl
dashboard_name => 'Lab Infrastructure',
```

```perl
dashboard_name => 'Server Health',
```

The description can also be customized:

```perl
dashboard_description => 'Monitoring dashboard for my home infrastructure',
```

---

# Customize Storage Monitoring

Set:

```perl
storage_mount => '/mnt/storage',
```

to the mount point you want monitored.

Examples:

```perl
storage_mount => '/srv/storage',
```

```perl
storage_mount => '/media/data',
```

```perl
storage_mount => '/mnt/nas',
```

You can also modify the storage collector in `index.cgi` if you want to monitor more than one filesystem.

For example, you could add separate cards for:

```text
/
```

```text
/mnt/media
```

```text
/mnt/backups
```

```text
/mnt/archive
```

---

# Customize RAID Monitoring

If you use Linux software RAID:

```perl
raid_enabled => 1,
```

Configure the array:

```perl
raid_array => 'md0',
```

and the member devices:

```perl
raid_devices => [qw(sda sdb)],
```

For a different array:

```perl
raid_array => 'md1',
```

For more disks:

```perl
raid_devices => [qw(sdb sdc sdd sde)],
```

If you do not use `mdadm`, disable the RAID collector:

```perl
raid_enabled => 0,
```

You could also replace the collector entirely with support for another storage technology.

Examples include:

- ZFS
- Btrfs
- LVM
- Storage Spaces through remote checks
- Hardware RAID controllers
- Ceph
- mergerfs

---

# Customize SMART Monitoring

Enable SMART monitoring:

```perl
smart_enabled => 1,
```

Then define your devices:

```perl
smart_devices => [qw(/dev/sda /dev/sdb)],
```

You can add additional drives:

```perl
smart_devices => [
    qw(
        /dev/sda
        /dev/sdb
        /dev/sdc
        /dev/sdd
    )
],
```

If SMART monitoring is not useful for your environment:

```perl
smart_enabled => 0,
```

You can also extend the collector to display more than pass/fail information.

Possible additions include:

- Drive temperature
- Power-on hours
- Reallocated sectors
- Pending sectors
- NVMe percentage used
- Media errors
- Drive model
- Serial number

Be mindful of whether you want serial numbers displayed or committed publicly.

---

# Customize Network Monitoring

Enable network diagnostics:

```perl
network_enabled => 1,
```

Set the primary network interface:

```perl
network_interface => 'eth0',
```

Your system may instead use:

```text
enp3s0
```

```text
eno1
```

```text
ens18
```

Set your gateway:

```perl
gateway => '192.168.1.1',
```

Set an internet test target:

```perl
internet_target => '1.1.1.1',
```

Set a DNS test host:

```perl
dns_test_host => 'example.com',
```

You can customize these tests for your own environment.

For example, you might test:

- Your router
- A local DNS server
- Pi-hole
- AdGuard Home
- A VLAN gateway
- A remote server
- A VPN endpoint
- An internal service

---

# Multiple Network Interfaces

The included collector is designed around one primary interface.

You can extend it to monitor multiple interfaces.

For example:

```text
eth0
wlan0
tailscale0
br0
docker0
```

Possible custom displays include:

- Interface state
- IPv4 address
- IPv6 address
- RX traffic
- TX traffic
- Link speed
- VLAN
- Bridge membership

---

# Customize Docker Monitoring

Enable Docker monitoring:

```perl
docker_enabled => 1,
```

The default collector displays containers returned by:

```bash
docker ps -a
```

You can modify it to monitor only specific containers.

For example:

```text
jellyfin
immich-server
homeassistant
nextcloud
postgres
mariadb
caddy
nginx
```

You could also group containers by service.

Example:

```text
Photo Services
  immich-server
  immich-machine-learning
  postgres

Media Services
  jellyfin

Network Services
  adguard
```

If your system does not use Docker:

```perl
docker_enabled => 0,
```

---

# Alternatives to Docker

The Docker collector can also serve as a model for other platforms.

You could create collectors for:

- Podman
- Kubernetes
- LXC
- Proxmox containers
- Virtual machines
- systemd services
- Nomad
- Docker Compose projects

---

# Customize Tailscale Monitoring

Enable Tailscale:

```perl
tailscale_enabled => 1,
```

Disable it:

```perl
tailscale_enabled => 0,
```

The included collector displays:

- Tailscale IPv4 address
- Tailnet devices visible
- Tailscale state
- Funnel detection

You could extend it to display:

- Exit node state
- Advertised routes
- Subnet routing
- Peer connectivity
- Direct versus relayed connections
- DERP region
- Tailscale SSH state

---

# Customize UFW Monitoring

Enable UFW monitoring:

```perl
ufw_enabled => 1,
```

Disable it:

```perl
ufw_enabled => 0,
```

The included collector provides a basic overview.

You can extend it to display:

- Allowed ports
- Denied ports
- IPv6 rules
- Logging level
- Rule count by interface
- Public versus private exposure

If your server uses another firewall, you could replace the collector.

Examples:

- firewalld
- nftables
- iptables
- pfSense API checks
- OPNsense API checks

---

# Customize Backup Monitoring

Enable backup monitoring:

```perl
backup_enabled => 1,
```

Configure the label:

```perl
backup_label => 'Homelab Server Backup',
```

Configure the timer:

```perl
backup_timer => 'homelab-backup.timer',
```

Configure the service:

```perl
backup_service => 'homelab-backup.service',
```

You can use this for any backup job built around systemd.

Examples:

- Photo backups
- Database backups
- NAS backups
- rsync jobs
- Restic
- Borg
- Kopia
- rclone
- Custom scripts

You can also rewrite the collector for backup systems that do not use systemd.

---

# Customize Weather

Enable weather:

```perl
weather_enabled => 1,
```

Set the displayed location:

```perl
weather_location => 'Example City, FL',
```

Set latitude and longitude:

```perl
weather_latitude  => 28.0000,
weather_longitude => -81.0000,
```

The default implementation uses Open-Meteo.

No API key is required.

If you do not want weather:

```perl
weather_enabled => 0,
```

You can also remove the weather section entirely from the dashboard.

---

# Customize GPU Monitoring

GPU support is intentionally flexible because different GPU vendors expose statistics differently.

Set:

```perl
gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',
```

to a command that outputs a utilization percentage.

Example output:

```text
37
```

The dashboard will interpret this as:

```text
37%
```

If you do not want GPU monitoring:

```perl
gpu_stats_command => '',
```

Possible GPU backends include:

- Intel tools
- NVIDIA `nvidia-smi`
- AMD tools
- Custom scripts

---

# Customize Health Thresholds

The default dashboard uses simple thresholds.

For example, CPU or memory usage above a certain percentage may result in:

```text
Attention
```

You can modify these thresholds inside `index.cgi`.

For example, you might prefer:

```text
CPU warning: 85%
Memory warning: 90%
Storage warning: 80%
```

or:

```text
CPU warning: 95%
Memory warning: 95%
Storage warning: 90%
```

Choose thresholds that make sense for your hardware and workload.

---

# Customize Overall Health

The dashboard combines individual collector states into an overall status.

Typical states include:

```text
Healthy
Attention
Unknown
```

Disabled collectors are ignored.

You can modify the health logic if you want different behavior.

For example, you could add:

```text
Degraded
Critical
Maintenance
```

You could also assign different severity levels to different collectors.

For example:

```text
SMART failure     → Critical
RAID degraded     → Critical
Backup failure    → Attention
High CPU usage    → Warning
Weather failure   → Ignore
```

---

# Customize the Layout

The dashboard HTML and CSS live inside:

```text
index.cgi
```

You can modify:

- Card order
- Card size
- Section order
- Fonts
- Spacing
- Borders
- Colors
- Status indicators
- Headings
- Descriptions

You can also add new sections.

Examples:

```text
Hardware
Services
Networking
Security
Storage
Backups
Environment
Maintenance
```

---

# Adding a New Dashboard Card

A simple dynamic card might look like:

```perl
print qq{
<div class="hlm-card">
    <h3>Example Metric</h3>
    <div class="hlm-value">$example_value</div>
    <p>Description of the metric</p>
</div>
};
```

Because this uses:

```perl
qq{}
```

Perl variables are interpolated.

---

# Perl HTML Interpolation

When modifying the dashboard, be aware of the difference between:

```perl
print qq{
<p>$value</p>
};
```

and:

```perl
print <<'HTML';
<p>$value</p>
HTML
```

The first version interpolates:

```perl
$value
```

The second version outputs the text literally.

Use `qq{}` for sections containing dynamic Perl variables.

A quoted heredoc such as:

```perl
<<'HTML'
```

is useful for static HTML and CSS.

---

# Adding Your Own Collector

Collectors are normal Perl functions.

A basic collector might look like:

```perl
sub example_info {
    my $output = `your-command 2>/dev/null`;

    return ("N/A", "N/A")
        unless $output;

    chomp($output);

    return ("Operational", $output);
}
```

Then call it:

```perl
my ($example_status, $example_value) = example_info();
```

and display it:

```perl
print qq{
<div class="hlm-placeholder">
    <strong>Example:</strong>
    <div>$example_status</div>
    <div>$example_value</div>
</div>
};
```

---

# Collector Ideas

Possible custom collectors include:

### Hardware

- CPU temperature
- GPU temperature
- Disk temperature
- Fan speed
- Power consumption
- UPS battery state

### Storage

- ZFS pool health
- Btrfs health
- Drive temperature
- Drive age
- Drive wear
- Scrub status
- Snapshot count

### Networking

- Interface throughput
- WAN IP
- VPN state
- DNS server state
- Ping history
- Packet loss history
- Direct versus relayed Tailscale peers

### Security

- Failed SSH logins
- Webmin login failures
- Fail2ban jails
- CrowdSec state
- Certificate expiration
- Open ports
- Firewall rule changes

### Maintenance

- Pending package updates
- Reboot required
- Kernel version
- Operating system version
- Last package update
- Last reboot

### Services

- Jellyfin
- Plex
- Immich
- Nextcloud
- Home Assistant
- Pi-hole
- AdGuard Home
- Syncthing
- Minecraft
- Proxmox
- Virtual machines
- Custom APIs

---

# Remove Features You Do Not Want

You are not required to keep every section.

For example, if you do not want weather at all, you may:

```perl
weather_enabled => 0,
```

or remove the weather HTML entirely.

If you do not use Tailscale, you may disable it or remove its collector.

If you only want a simple server dashboard, you could reduce the project to:

```text
CPU
Memory
Uptime
Storage
Network
Overall Health
```

The project is intentionally flexible.

---

# Forking the Project

You are welcome to fork the repository and create your own version.

Your fork could focus on a particular use case.

Examples:

```text
Webmin NAS Monitor
Webmin Media Server Monitor
Webmin Proxmox Companion
Webmin Docker Dashboard
Webmin Home Server Dashboard
```

You can keep as much or as little of the original project as you find useful, subject to the project's license.

---

# Sharing Custom Collectors

If you create a useful collector, consider contributing it back to the project.

Examples of useful contributions include:

- ZFS support
- Btrfs support
- NVMe health
- UPS monitoring
- Proxmox monitoring
- Package updates
- Certificate expiration
- Service health checks
- Improved Docker support
- Additional firewall support

Reusable additions can make the project more useful for other homelab users.

---

# Security When Customizing

Custom collectors often execute system commands.

Review every command you add.

Avoid:

- Embedding passwords directly in the code
- Committing API tokens
- Committing SSH private keys
- Exposing unnecessary internal information
- Executing untrusted user input
- Running commands with more privileges than necessary

Keep your real:

```text
config.pl
```

out of Git if it contains environment-specific information.

---

# Test Changes Before Using Them

After modifying `index.cgi`, check Perl syntax:

```bash
perl -c index.cgi
```

You should see:

```text
syntax OK
```

If installed in Webmin:

```bash
perl -c /usr/share/webmin/homelab-monitoring/index.cgi
```

Then reload the module.

When making larger changes, keep a backup of the working version first.

For example:

```bash
cp index.cgi index.cgi.bak
```

---

# Make It Your Own

The example configuration and collectors in this repository are not requirements.

They exist to provide a working foundation.

Use what is useful.

Disable what is not.

Replace what does not fit your environment.

Add monitoring that matters to you.

The goal of Webmin Homelab Monitor is to make it easier to build a monitoring dashboard that reflects **your homelab**, rather than forcing your homelab to match someone else's setup.
