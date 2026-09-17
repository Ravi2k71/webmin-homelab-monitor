# Full example configuration for Webmin Homelab Monitor

our %config = (

    # Dashboard
    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Custom Webmin monitoring dashboard',

    # GPU
    # Set to '' if GPU monitoring is not needed.
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
