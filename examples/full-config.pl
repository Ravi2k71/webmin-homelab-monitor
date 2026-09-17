# Full example configuration for Webmin Homelab Monitor

our %config = (

    # Dashboard
    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Custom Webmin monitoring dashboard',

    # Storage
    storage_mount => '/mnt/storage',

    # RAID
    raid_array   => 'md0',
    raid_devices => [qw(sda sdb)],

    # SMART
    smart_devices => [qw(/dev/sda /dev/sdb)],

    # Network
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    # Connectivity checks
    internet_test_ip => '1.1.1.1',
    dns_test_host    => 'openai.com',

    # Weather
    weather_location  => 'Example City, FL',
    weather_latitude  => 28.0000,
    weather_longitude => -81.0000,

    # Backup
    backup_timer   => 'homelab-backup.timer',
    backup_service => 'homelab-backup.service',

    # Feature toggles
    enable_raid      => 1,
    enable_smart     => 1,
    enable_docker    => 1,
    enable_tailscale => 1,
    enable_ufw       => 1,
    enable_backup    => 1,
    enable_weather   => 1,

);

1;
