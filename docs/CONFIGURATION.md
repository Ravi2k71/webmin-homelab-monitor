# Configuration

Copy:

```bash
cp config.pl.example config.pl
```

`config.pl` is excluded by `.gitignore` so local environment details do not need to be published.

## Branding

```perl
dashboard_name        => 'Homelab Monitoring',
dashboard_description => 'Custom monitoring and health dashboard for a Linux homelab server.',
```

## GPU

```perl
gpu_stats_command => '/usr/local/sbin/webmin-gpu-stats',
```

The project expects the helper to print a single integer from 0 to 100. Set it to an empty string to disable GPU collection.

## RAID

```perl
raid_array   => 'md0',
raid_devices => [qw(sda sdb)],
```

This collector reads `/sys/block/<array>/md` and is intended for Linux software RAID/mdadm arrays.

## Storage

```perl
storage_mount => '/mnt/storage',
```

This is the filesystem shown in the Storage section.

## SMART

```perl
smart_devices => [qw(/dev/sda /dev/sdb)],
```

Each device is checked using `smartctl -H`.

## Backup monitoring

```perl
backup_label   => 'Homelab Server Backup',
backup_timer   => 'homelab-backup.timer',
backup_service => 'homelab-backup.service',
```

The collector assumes a systemd timer triggers a oneshot service. A completed oneshot service being `inactive (dead)` is normal; the dashboard checks the timer and service result rather than requiring the service to remain running.

## Network diagnostics

```perl
network_interface => 'eth0',
gateway           => '192.168.1.1',
internet_target   => '1.1.1.1',
dns_test_host     => 'example.com',
```

Choose an internet ping target and DNS hostname appropriate for your environment.

## Weather

```perl
weather_enabled   => 1,
weather_location  => 'Your City, ST',
weather_latitude  => 00.0000,
weather_longitude => -00.0000,
```

Weather uses Open-Meteo and does not require an API key for the basic endpoint used by this template. Set `weather_enabled => 0` to disable collection.

## Optional integrations

```perl
tailscale_enabled => 1,
ufw_enabled       => 1,
docker_enabled    => 1,
```

Set an integration to `0` if you do not use it.
