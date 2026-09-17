# Customizing Webmin Homelab Monitor

This project is designed to be a starting point, not a rigid appliance.

You are encouraged to modify the dashboard to match your own homelab, hardware, services, network layout, and preferences.

## What You Can Customize

Almost every part of the project can be changed, including:

- Dashboard name and description
- Storage mount points
- RAID array name and member drives
- Network interface and gateway
- Docker containers and services
- Backup timer and service names
- Tailscale monitoring
- UFW/firewall monitoring
- Weather location
- Health thresholds
- Status labels
- Colors and styling
- Dashboard layout
- Which collectors are enabled
- Additional custom collectors

You do not need to run the same services as the example configuration.

For example, you can remove PhotoPrism-specific monitoring and replace it with monitoring for services such as:

- Jellyfin
- Plex
- Immich
- Nextcloud
- Home Assistant
- Pi-hole
- AdGuard Home
- Syncthing
- Minecraft servers
- Virtual machines
- Other Docker containers or systemd services

## Start With the Configuration File

Copy the example configuration:

```bash
cp config.pl.example config.pl
```

Then edit `config.pl` for your own system.

The goal is to keep most machine-specific values outside the main `index.cgi` file.

Examples include:

```perl
storage_mount     => '/mnt/storage',
raid_array        => 'md0',
network_interface => 'eth0',
gateway           => '192.168.1.1',
weather_location  => 'Your City, ST',
backup_service    => 'your-backup.service',
```

## Remove Features You Do Not Need

You do not have to use every collector.

If your server does not use RAID, Tailscale, Docker, UFW, SMART monitoring, weather data, or automated backups, you can remove or disable those sections.

The dashboard should reflect **your infrastructure**, not force your infrastructure to match the dashboard.

## Add Your Own Collectors

The existing collectors are examples of how to gather system information and display it in Webmin.

You can add collectors for anything that can be checked from Perl or a command-line tool.

Examples:

- ZFS pool health
- Btrfs status
- UPS battery state
- CPU and disk temperatures
- Internet bandwidth
- Certificate expiration
- Failed SSH logins
- Webmin authentication failures
- Package updates
- Reboot-required state
- Virtual machine status
- Kubernetes workloads
- Proxmox nodes
- Game servers
- Custom application health checks

A typical collector pattern looks like:

```perl
sub example_info {
    my $output = `your-command 2>/dev/null`;

    return ("N/A", "N/A") unless $output;

    # Parse output here

    return ("Operational", $output);
}
```

Then call the collector before rendering the page and display its values inside a `print qq{ ... };` block.

## Change the Layout

The HTML and CSS in `index.cgi` can also be customized.

You can:

- Reorder sections
- Rename headings
- Change card sizes
- Add or remove cards
- Change status colors
- Create compact or expanded layouts
- Add additional sections
- Match the dashboard to your Webmin theme

When displaying Perl variables inside HTML, remember that:

```perl
print qq{
...
};
```

interpolates variables, while:

```perl
print <<'HTML';
...
HTML
```

does not.

This distinction is important when adding dynamic dashboard values.

## Make It Your Own

The included configuration and collectors are examples based on one homelab setup.

They are not requirements.

The project is intended to help you build a Webmin monitoring page that fits your own environment and can grow alongside your homelab.

Experiment, remove features, add new diagnostics, change the styling, and adapt the project however you find useful.

## Sharing Improvements

If you build a useful collector, improve compatibility, add documentation, or create a better layout, contributions and forks are welcome.

Because the project is licensed under GPL-3.0, you are free to study, modify, and redistribute the code under the terms of that license.
