# Basic example configuration for Webmin Homelab Monitor

our %config = (

    dashboard_name => 'My Homelab Monitor',

    storage_mount => '/mnt/storage',

    network_interface => 'eth0',
    gateway           => '192.168.1.1',

    weather_location  => 'Example City, FL',
    weather_latitude  => 28.0000,
    weather_longitude => -81.0000,

);

1;
