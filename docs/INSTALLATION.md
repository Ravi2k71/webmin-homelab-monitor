# Installation Guide

This guide walks through installing Webmin Homelab Monitor on a Linux server running Webmin.

The project is designed to be flexible, so you only need to enable the collectors that match your environment.

---

# Before You Begin

You should already have:

- A Linux server
- Webmin installed and working
- A Webmin user with permission to install or access modules
- Basic command-line access to the server
- Perl installed

Depending on which collectors you enable, you may also need:

- `smartmontools`
- `mdadm`
- Docker
- Tailscale
- UFW
- `curl`
- Perl `JSON::PP`
- systemd

You do not need every optional dependency.

Only install what your configuration actually uses.

---

# 1. Download the Repository

Clone the repository:

```bash
git clone https://github.com/Ravi2k71/webmin-homelab-monitor.git
```

Then enter the project directory:

```bash
cd webmin-homelab-monitor
```

If you do not use Git, you can also download the repository as a ZIP from GitHub and extract it manually.

---

# 2. Review the Module Files

The Webmin module is located in:

```text
module/
```

It should contain:

```text
module/
├── index.cgi
├── module.info
└── config.pl.example
```

These files serve different purposes:

- `index.cgi` — dashboard and collector logic
- `module.info` — Webmin module metadata
- `config.pl.example` — example user configuration

---

# 3. Create the Webmin Module Directory

A typical Webmin installation stores modules under:

```text
/usr/share/webmin/
```

Create the module directory:

```bash
sudo mkdir -p /usr/share/webmin/webmin-homelab-monitor
```

Then copy the module files:

```bash
sudo cp module/* /usr/share/webmin/webmin-homelab-monitor/
```

After copying, the directory should contain:

```text
/usr/share/webmin/webmin-homelab-monitor/
├── index.cgi
├── module.info
└── config.pl.example
```

---

# 4. Create Your Local Configuration

Change into the module directory:

```bash
cd /usr/share/webmin/webmin-homelab-monitor
```

Copy the example configuration:

```bash
sudo cp config.pl.example config.pl
```

Then edit it:

```bash
sudo nano config.pl
```

You should customize the values for your own server.

Example:

```perl
our %config = (

    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Custom Webmin monitoring dashboard',

    gpu_stats_command => '',

    storage_mount => '/mnt/storage',

    raid_enabled => 0,
    smart_enabled => 0,

    network_enabled   => 1,
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    internet_target => '1.1.1.1',
    dns_test_host   => 'example.com',

    backup_enabled => 0,

    docker_enabled    => 0,
    tailscale_enabled => 0,
    ufw_enabled       => 1,

    weather_enabled => 0,

);

1;
```

This is only an example.

Your own configuration may be much simpler or more detailed.

See:

```text
docs/CONFIGURATION.md
```

for full configuration documentation.

---

# 5. Make `index.cgi` Executable

Set the executable bit:

```bash
sudo chmod +x /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

You can verify it with:

```bash
ls -l /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

You should see executable permissions similar to:

```text
-rwxr-xr-x
```

---

# 6. Check Perl Syntax

Before opening the module in Webmin, validate the CGI:

```bash
perl -c /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

A successful result should look similar to:

```text
/usr/share/webmin/webmin-homelab-monitor/index.cgi syntax OK
```

If you see an error, fix it before continuing.

---

# 7. Verify Webmin's Perl Library Paths

The module currently loads Webmin libraries from common locations such as:

```text
/usr/libexec/webmin
/usr/share/webmin
```

Most standard Linux Webmin installations use one of these paths.

If your Webmin installation uses a different location, you may need to adjust the `use lib` lines near the top of:

```text
index.cgi
```

You can locate Webmin with commands such as:

```bash
which webmin
```

or inspect:

```text
/etc/webmin/
```

and:

```text
/usr/share/webmin/
```

---

# 8. Restart Webmin

Restart Webmin:

```bash
sudo systemctl restart webmin
```

Then verify that it is running:

```bash
sudo systemctl status webmin
```

You should see:

```text
active (running)
```

---

# 9. Allow Your Webmin User to Access the Module

Webmin can restrict modules by user or group.

If the module appears but gives an error such as:

```text
Access denied
```

open Webmin and review the permissions for the user or group you are using.

Make sure the user is allowed to access:

```text
Webmin Homelab Monitor
```

Do not disable Webmin's referer protection or CSRF protections just to bypass an access error.

Fix the module permissions instead.

---

# 10. Open the Dashboard

Log into Webmin.

Look for the module:

```text
Webmin Homelab Monitor
```

Open it.

If everything is configured correctly, the dashboard should begin displaying system data.

---

# 11. Install Optional Dependencies

Only install the tools needed by the collectors you actually enable.

---

## SMART Monitoring

If:

```perl
smart_enabled => 1,
```

install:

```bash
sudo apt install smartmontools
```

Test:

```bash
sudo smartctl -H /dev/sda
```

---

## RAID Monitoring

If:

```perl
raid_enabled => 1,
```

you may need:

```bash
sudo apt install mdadm
```

Check your arrays:

```bash
cat /proc/mdstat
```

and:

```bash
sudo mdadm --detail /dev/md0
```

---

## Docker Monitoring

If:

```perl
docker_enabled => 1,
```

make sure Docker is installed and running:

```bash
docker ps
```

If Webmin cannot read Docker state, review Docker permissions for the user or process running the module.

---

## Tailscale Monitoring

If:

```perl
tailscale_enabled => 1,
```

make sure Tailscale is installed and connected:

```bash
tailscale status
```

and:

```bash
tailscale ip -4
```

---

## UFW Monitoring

If:

```perl
ufw_enabled => 1,
```

verify:

```bash
sudo ufw status verbose
```

The dashboard expects UFW output in the standard format.

---

## Weather Monitoring

If:

```perl
weather_enabled => 1,
```

install `curl` if necessary:

```bash
sudo apt install curl
```

Then test Perl `JSON::PP`:

```bash
perl -MJSON::PP -e 'print "JSON::PP OK\n"'
```

You should see:

```text
JSON::PP OK
```

---

# 12. Test the Underlying Commands

If a dashboard section shows:

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

```bash
getent hosts example.com
```

This helps determine whether the issue is:

- Missing software
- Incorrect configuration
- Permissions
- Device naming
- Interface naming
- Service state
- Unexpected command output

---

# 13. Check Your Network Interface Name

The example configuration uses:

```perl
network_interface => 'eth0',
```

but many modern Linux systems use names such as:

```text
enp3s0
eno1
ens18
```

Check your system with:

```bash
ip link
```

or:

```bash
ip addr
```

Then update:

```perl
network_interface
```

to match your server.

---

# 14. Check Your Default Gateway

Find your gateway:

```bash
ip route
```

Look for something similar to:

```text
default via 192.168.1.1 dev eth0
```

Then configure:

```perl
gateway => '192.168.1.1',
```

using your actual gateway address.

---

# 15. Check Your Storage Mount

The default example uses:

```perl
storage_mount => '/mnt/storage',
```

Verify your actual mount points with:

```bash
df -h
```

or:

```bash
findmnt
```

Then configure the correct path.

Examples:

```perl
storage_mount => '/media/storage',
```

```perl
storage_mount => '/srv/data',
```

---

# 16. Check SMART Device Names

List block devices:

```bash
lsblk
```

Then set:

```perl
smart_devices => [qw(/dev/sda /dev/sdb)],
```

to the drives you want monitored.

Do not blindly copy the example device names.

---

# 17. Check RAID Device Names

If RAID is enabled, verify:

```bash
cat /proc/mdstat
```

Your array may be:

```text
md0
```

```text
md1
```

or another name.

Configure:

```perl
raid_array => 'md0',
```

accordingly.

---

# 18. Configure Backups

Backup monitoring expects a systemd timer and service.

Example:

```perl
backup_enabled => 1,
backup_timer   => 'homelab-backup.timer',
backup_service => 'homelab-backup.service',
```

List timers:

```bash
systemctl list-timers
```

Check the service:

```bash
systemctl status homelab-backup.service
```

Check the timer:

```bash
systemctl status homelab-backup.timer
```

If you do not use a systemd-based backup job:

```perl
backup_enabled => 0,
```

---

# 19. Configure Weather

If weather is enabled:

```perl
weather_enabled => 1,
```

set:

```perl
weather_location
weather_latitude
weather_longitude
```

Example:

```perl
weather_location  => 'Example City, FL',
weather_latitude  => 28.0000,
weather_longitude => -81.0000,
```

The location name is only a display label.

The latitude and longitude are used for the Open-Meteo request.

---

# 20. Configure GPU Monitoring

GPU monitoring is optional.

If you already have a helper command that returns a numeric utilization value:

```perl
gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',
```

If not:

```perl
gpu_stats_command => '',
```

The dashboard will display:

```text
N/A
```

for GPU usage.

---

# 21. Verify Disabled Features

If you do not use a feature, disable it.

For example:

```perl
raid_enabled      => 0,
smart_enabled     => 0,
backup_enabled    => 0,
docker_enabled    => 0,
tailscale_enabled => 0,
weather_enabled   => 0,
```

Disabled collectors are intentionally ignored by the overall health calculation.

This prevents unused services from causing:

```text
Overall Health: Unknown
```

---

# 22. File Permissions

A typical module directory might look similar to:

```bash
ls -la /usr/share/webmin/webmin-homelab-monitor
```

Example:

```text
-rw-r--r-- config.pl
-rw-r--r-- config.pl.example
-rwxr-xr-x index.cgi
-rw-r--r-- module.info
```

Your exact ownership and permissions may differ depending on your distribution and Webmin installation.

Avoid making files globally writable.

For example, do not use:

```bash
chmod 777
```

unless you have a very specific reason.

---

# 23. Security Notes

This module can display information about:

- Storage
- Network interfaces
- IP addresses
- Firewall state
- Services
- Backups
- Tailscale
- Docker
- Hardware

Treat it as an administrative interface.

Recommended practices include:

- Use HTTPS for Webmin
- Restrict Webmin access to trusted networks
- Use strong authentication
- Prefer SSH keys over password authentication where practical
- Disable direct root SSH login
- Keep firewall rules restrictive
- Keep Webmin's CSRF and referer protections enabled
- Do not expose Webmin directly to the public internet unless you understand the risks

---

# 24. Keep `config.pl` Private

Your actual:

```text
config.pl
```

may contain:

- Internal IP addresses
- Hostnames
- Device paths
- Storage paths
- Backup service names
- Location data
- Environment-specific settings

It should generally not be committed to Git.

The repository includes:

```text
config.pl.example
```

for public sharing.

Before committing changes, check:

```bash
git status
```

and review what is being added.

---

# 25. Updating the Module

If you pull a newer version from GitHub, back up your working installation first.

Example:

```bash
sudo cp -a \
/usr/share/webmin/webmin-homelab-monitor \
/usr/share/webmin/webmin-homelab-monitor.backup
```

Then copy the updated module files.

Do not overwrite your custom:

```text
config.pl
```

without reviewing the changes first.

After updating:

```bash
perl -c /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

Then restart Webmin if needed:

```bash
sudo systemctl restart webmin
```

---

# 26. Troubleshooting Checklist

If the module does not work, check these in order:

1. Does `index.cgi` exist?
2. Is `index.cgi` executable?
3. Does `config.pl` exist?
4. Does Perl syntax pass?
5. Is Webmin running?
6. Does your Webmin user have module access?
7. Are configured device names correct?
8. Is the configured network interface correct?
9. Are optional dependencies installed?
10. Can the underlying command run manually?
11. Does Webmin have permission to run it?

Useful commands:

```bash
perl -c /usr/share/webmin/webmin-homelab-monitor/index.cgi
```

```bash
sudo systemctl status webmin
```

```bash
ls -la /usr/share/webmin/webmin-homelab-monitor
```

```bash
ip addr
```

```bash
df -h
```

```bash
lsblk
```

```bash
docker ps
```

```bash
tailscale status
```

```bash
sudo ufw status verbose
```

---

# 27. Customize the Module

Once the basic module is working, you can customize it further.

See:

- [Configuration Guide](CONFIGURATION.md)
- [Customization Guide](CUSTOMIZATION.md)
- [Collectors Guide](COLLECTORS.md)

You can:

- Add collectors
- Remove collectors
- Change thresholds
- Change dashboard styling
- Add services
- Add hardware checks
- Add security checks
- Add maintenance information

The project is intended to be modified.

---

# Installation Complete

Once the dashboard loads successfully and your enabled collectors report valid information, the installation is complete.

From there, Webmin Homelab Monitor can be adapted to match your own server and homelab environment.
