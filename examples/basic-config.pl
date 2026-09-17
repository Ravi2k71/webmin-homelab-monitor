# Basic example configuration for Webmin Homelab Monitor

our %config = (

    # Dashboard
    dashboard_name        => 'My Homelab Monitor',
    dashboard_description => 'Basic Webmin monitoring dashboard',

    # GPU
    gpu_stats_command => '',

    # Storage
    storage_mount => '/mnt/storage',

    # Disable collectors not needed in this basic example
    raid_enabled      => 0,
    smart_enabled     => 0,
    backup_enabled    => 0,
    tailscale_enabled => 0,
    weather_enabled   => 0,

    # Network
    network_enabled   => 1,
    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    # Connectivity checks
    internet_target => '1.1.1.1',
    dns_test_host   => 'example.com',

    # Optional integrations
    docker_enabled => 1,
    ufw_enabled    => 1,

);

1;
