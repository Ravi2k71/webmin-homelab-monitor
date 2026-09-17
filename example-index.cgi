#!/usr/bin/perl

# Webmin Homelab Monitor - example/template module
# Customize behavior through config.pl (copied from config.pl.example).

use strict;
use warnings;

use lib "/usr/libexec/webmin";
use lib "/usr/share/webmin";

use WebminCore;
use FindBin qw($Bin);

our %config;

init_config();

# Load local configuration. Keep config.pl out of version control if it contains
# private environment details. Start from config.pl.example.
my $config_file = "$Bin/config.pl";
if (!-f $config_file) {
    die "Missing config.pl. Copy config.pl.example to config.pl and customize it.\n";
}
require $config_file;


sub read_cpu {
    open(my $fh, '<', '/proc/stat') or return undef;
    my $line = <$fh>;
    close($fh);
    return undef unless defined $line;

    my @v = split(/\s+/, $line);
    shift @v;
    return undef unless @v >= 4;

    my ($user, $nice, $system, $idle, $iowait, $irq, $softirq, $steal) =
        map { $_ || 0 } @v[0..7];

    my $idle_all = $idle + $iowait;
    my $total = $user + $nice + $system + $idle_all + $irq + $softirq + $steal;

    return ($total, $idle_all);
}

sub cpu_usage {
    my @a = read_cpu();
    return "N/A" unless @a == 2;

    select(undef, undef, undef, 0.25);

    my @b = read_cpu();
    return "N/A" unless @b == 2;

    my $total_delta = $b[0] - $a[0];
    my $idle_delta  = $b[1] - $a[1];

    return "N/A" if $total_delta <= 0;

    my $usage = int((($total_delta - $idle_delta) * 100) / $total_delta);
    $usage = 0 if $usage < 0;
    $usage = 100 if $usage > 100;

    return $usage;
}

 sub raid_info {     my $array = $config{raid_array} || "md0"; my $base = "/sys/block/$array/md";      return ("N/A", "N/A", "N/A", 0, "Unknown", "") unless -d $base;      my $read_file = sub {         my ($name) = @_;         open(my $fh, "<", "$base/$name") or return undef;         my $value = <$fh>;         close($fh);         return undef unless defined $value;         chomp($value);         return $value;     };      my $state = $read_file->("array_state") // "N/A";     my $level = $read_file->("level") // "N/A";     my $disks = $read_file->("raid_disks") // "N/A";      my $active = 0;      if ($disks =~ /^\d+$/) {         for my $dev (@{$config{raid_devices} || []}) {             my $dev_state = $read_file->("dev-$dev/state");             $active++ if defined $dev_state && $dev_state =~ /\bin_sync\b/;         }     }      my $status = "Attention";      if ($state eq "clean" && $disks =~ /^\d+$/ && $active == $disks) {         $status = "Operational";     }      my $note = ($level eq "raid0") ? "RAID0 provides no fault tolerance" : "";      return ($state, $level, $disks, $active, $status, $note); } 
sub memory_usage {
    open(my $fh, '<', '/proc/meminfo') or return "N/A";

    my ($total, $available);

    while (my $line = <$fh>) {
        $total = $1 if $line =~ /^MemTotal:\s+(\d+)/;
        $available = $1 if $line =~ /^MemAvailable:\s+(\d+)/;
    }

    close($fh);

    return "N/A" unless defined $total && defined $available && $total > 0;

    my $used = $total - $available;
    my $percent = int(($used * 100) / $total);

    $percent = 0 if $percent < 0;
    $percent = 100 if $percent > 100;

    return $percent;
}

sub uptime {
    open(my $fh, '<', '/proc/uptime') or return "N/A";
    my $line = <$fh>;
    close($fh);

    return "N/A" unless defined $line;

    my ($seconds) = split(/\s+/, $line);
    return "N/A" unless defined $seconds;

    $seconds = int($seconds);

    my $days = int($seconds / 86400);
    $seconds %= 86400;

    my $hours = int($seconds / 3600);
    $seconds %= 3600;

    my $minutes = int($seconds / 60);

    return "${days}d ${hours}h ${minutes}m";
}

sub gpu_usage {
    return "N/A" unless $config{gpu_stats_command};
    my $cmd = $config{gpu_stats_command};
    my $output = `$cmd 2>/dev/null`;
    chomp($output);

    return "N/A" unless $output =~ /^\d+$/;

    my $value = int($output);
    $value = 0 if $value < 0;
    $value = 100 if $value > 100;

    return $value;
}

my $cpu = cpu_usage();
my $memory = memory_usage();
my $gpu = gpu_usage();
my $up = uptime();
my $cpu_status =
    ($cpu eq "N/A") ? "N/A" :
    ($cpu >= 90) ? "Attention" :
    "Operational";

my $memory_status =
    ($memory eq "N/A") ? "N/A" :
    ($memory >= 90) ? "Attention" :
    "Operational";

sub format_bytes {
    my ($bytes) = @_;

    return "N/A" unless defined $bytes && $bytes =~ /^\d+$/;

    my @units = ("B", "KB", "MB", "GB", "TB");
    my $i = 0;

    while ($bytes >= 1024 && $i < $#units) {
        $bytes /= 1024;
        $i++;
    }

    return sprintf("%.1f %s", $bytes, $units[$i]);
}

sub storage_info {
    my $mount = $config{storage_mount} || "/mnt/storage";

    open(my $fh, "-|", "df", "-P", "-B1", $mount)
        or return ("N/A", "N/A", "N/A", "N/A", "N/A");

    my @lines = <$fh>;
    close($fh);

    return ("N/A", "N/A", "N/A", "N/A", "N/A")
        unless @lines >= 2;

    my @fields = split(/\s+/, $lines[-1]);

    return ("N/A", "N/A", "N/A", "N/A", "N/A")
        unless @fields >= 6;

    my ($size, $used, $avail, $percent) =
        @fields[1, 2, 3, 4];

    $percent =~ s/%//;

    my $status = "Operational";

    if ($percent =~ /^\d+$/ && $percent >= 80) {
        $status = "Attention";
    }

    return ($size, $used, $avail, $percent, $status);
}
sub smart_health {
    my ($device) = @_;

    open(my $fh, "-|", "smartctl", "-H", $device)
        or return "N/A";

    my @lines = <$fh>;
    close($fh);

    for my $line (@lines) {
        if ($line =~ /overall-health.*:\s*(\S+)/i) {
            my $result = uc($1);

            return "Operational" if $result eq "PASSED";
            return "Attention";
        }
    }

    return "N/A";
}
sub docker_info {
    return ("N/A", []) unless $config{docker_enabled};
    open(my $fh, "-|", "docker", "ps", "-a", "--format", "{{.Names}}|{{.Status}}")
        or return ("N/A", []);

    my @containers;
    my $overall = "Operational";

    while (my $line = <$fh>) {
        chomp($line);
        next unless $line;

        my ($name, $status) = split(/\|/, $line, 2);
        push @containers, [$name, $status];

        if (!defined $status || $status !~ /^Up\b/) {
            $overall = "Attention";
        }
    }

    close($fh);

    return ("N/A", []) unless @containers;

    return ($overall, \@containers);
}
sub tailscale_info {
    return ("N/A", "N/A", 0, "N/A") unless $config{tailscale_enabled};
    my $status_output = `tailscale status 2>/dev/null`;
    my $ip = `tailscale ip -4 2>/dev/null`;

    chomp($ip);

    return ("N/A", "N/A", 0, "N/A")
        if !$status_output || !$ip;

    my $peer_count = 0;
    my $funnel = "Disabled";

    for my $line (split(/\n/, $status_output)) {
        $peer_count++ if $line =~ /^100\./;

        if ($line =~ /# Funnel on:/) {
            $funnel = "Enabled";
        }
    }

    my $status = "Operational";

    return ($status, $ip, $peer_count, $funnel);
}
sub ufw_info {
    return ("N/A", "N/A", "N/A", 0, "N/A") unless $config{ufw_enabled};
    my $output = `ufw status verbose 2>/dev/null`;

    return ("N/A", "N/A", "N/A", 0, "N/A")
        unless $output;

    my $status = "N/A";
    my $logging = "N/A";
    my $incoming = "N/A";
    my $allow_rules = 0;
    my $ssh_scope = "N/A";

    for my $line (split(/\n/, $output)) {
        $status = "Operational" if $line =~ /^Status:\s+active/i;
        $status = "Attention" if $line =~ /^Status:\s+inactive/i;

        $logging = $1 if $line =~ /^Logging:\s+(.+)$/i;

        if ($line =~ /^Default:\s+(\w+)\s+\(incoming\)/i) {
            $incoming = lc($1);
        }

        $allow_rules++ if $line =~ /\bALLOW IN\b/;

        if ($line =~ /^22\/tcp\s+ALLOW IN\s+192\.168\./ ||
            $line =~ /^22\/tcp on tailscale0\s+ALLOW IN/) {
            $ssh_scope = "Restricted";
        }
    }

    return ($status, $logging, $incoming, $allow_rules, $ssh_scope);
}
sub backup_info {
    my $timer = $config{backup_timer} || "homelab-backup.timer";
    my $service = $config{backup_service} || "homelab-backup.service";
    my $timer_active = `systemctl is-active $timer 2>/dev/null`;
    chomp($timer_active);

    my $result = `systemctl show $service -p Result --value 2>/dev/null`;
    chomp($result);

    my $last_run = `systemctl show $service -p InactiveExitTimestamp --value 2>/dev/null`;
    chomp($last_run);

    my $next_run = `systemctl list-timers $timer --no-legend 2>/dev/null`;
    chomp($next_run);

    my $status = "Operational";

    if ($timer_active ne "active" || $result ne "success") {
        $status = "Attention";
    }

    $last_run = "N/A" unless $last_run;

    my $next_display = "N/A";

    if ($next_run =~ /^(.+?\s+\S+\s+\S+\s+\S+)\s+\S+\s+/) {
        $next_display = $1;
    }

    return ($status, $last_run, $next_display, $result, $timer_active);
}
sub weather_code_text {
    my ($code) = @_;

    return "Clear" if $code == 0;
    return "Mostly Clear" if $code == 1;
    return "Partly Cloudy" if $code == 2;
    return "Cloudy" if $code == 3;
    return "Fog" if $code == 45 || $code == 48;
    return "Drizzle" if $code >= 51 && $code <= 57;
    return "Rain" if $code >= 61 && $code <= 67;
    return "Snow" if $code >= 71 && $code <= 77;
    return "Rain Showers" if $code >= 80 && $code <= 82;
    return "Snow Showers" if $code >= 85 && $code <= 86;
    return "Thunderstorm" if $code >= 95 && $code <= 99;

    return "Unknown";
}
sub weather_info {
    return ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A") unless $config{weather_enabled};
    my $lat = $config{weather_latitude};
    my $lon = $config{weather_longitude};

    my $url =
        "https://api.open-meteo.com/v1/forecast" .
        "?latitude=$lat" .
        "&longitude=$lon" .
        "&current=temperature_2m,apparent_temperature,relative_humidity_2m,weather_code,wind_speed_10m" .
        "&daily=temperature_2m_max,temperature_2m_min,precipitation_probability_max" .
        "&temperature_unit=fahrenheit" .
        "&wind_speed_unit=mph" .
        "&timezone=auto";

    my $json = `curl -fsS '$url' 2>/dev/null`;

    return ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
        unless $json;

    my $data;

    eval {
        require JSON::PP;
        $data = JSON::PP::decode_json($json);
    };

    return ("N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A")
        if $@ || !$data;

    my $temp     = $data->{current}->{temperature_2m} // "N/A";
    my $feels    = $data->{current}->{apparent_temperature} // "N/A";
    my $humidity = $data->{current}->{relative_humidity_2m} // "N/A";
    my $code     = $data->{current}->{weather_code} // "N/A";
    my $wind     = $data->{current}->{wind_speed_10m} // "N/A";

    my $high = $data->{daily}->{temperature_2m_max}->[0] // "N/A";
    my $low  = $data->{daily}->{temperature_2m_min}->[0] // "N/A";
    my $rain = $data->{daily}->{precipitation_probability_max}->[0] // "N/A";

    return ($temp, $feels, $humidity, $code, $wind, $high, $low, $rain);
}
sub network_info {
    my $interface = $config{network_interface} || "eth0";
    my $gateway = $config{gateway} || "192.168.1.1";
    my $internet_target = $config{internet_target} || "1.1.1.1";
    my $dns_test_host = $config{dns_test_host} || "example.com";

    my $link_state = `cat /sys/class/net/$interface/operstate 2>/dev/null`;
    chomp($link_state);

    my $ip_output = `/usr/sbin/ip -4 addr show dev $interface 2>/dev/null`;
    my $lan_ip = "N/A";

    if ($ip_output =~ /inet\s+(\d+\.\d+\.\d+\.\d+)/) {
        $lan_ip = $1;
    }

    my $gateway_test = `/usr/bin/ping -c 1 -W 1 $gateway 2>/dev/null`;
    my $gateway_status = ($gateway_test =~ /1 received/) ? "Operational" : "Attention";

    my $internet_test = `/usr/bin/ping -c 2 -W 1 $internet_target 2>/dev/null`;

    my $internet_status = "Attention";
    my $latency = "N/A";
    my $packet_loss = "N/A";

    if ($internet_test =~ /(\d+)% packet loss/) {
        $packet_loss = $1;
    }

    if ($internet_test =~ /rtt .* = [\d.]+\/([\d.]+)\//) {
        $latency = $1;
    }

    if ($packet_loss ne "N/A" && $packet_loss == 0) {
        $internet_status = "Operational";
    }

    my $dns_test = `/usr/bin/getent hosts $dns_test_host 2>/dev/null`;
    my $dns_status = $dns_test ? "Operational" : "Attention";

    my $interface_status =
        ($link_state eq "up") ? "Operational" : "Attention";

    return (
        $interface_status,
        $interface,
        $lan_ip,
        $gateway_status,
        $gateway,
        $internet_status,
        $dns_status,
        $latency,
        $packet_loss
    );
}
sub overall_health {
    my (@statuses) = @_;

    for my $status (@statuses) {
        return "Attention"
            if defined $status && $status eq "Attention";
    }

    for my $status (@statuses) {
        return "Unknown"
            if !defined $status || $status eq "N/A";
    }

    return "Healthy";
}
sub health_class {
    my ($value) = @_;
    return "unknown" if $value eq "N/A";
    return "warning" if $value eq "Attention";
    return "good";
}
my ($raid_state, $raid_level, $raid_disks, $raid_active, $raid_status, $raid_note) = raid_info();
my ($storage_size, $storage_used, $storage_avail, $storage_percent, $storage_status) = storage_info();
my @smart_results;
for my $device (@{$config{smart_devices} || []}) {
    push @smart_results, [$device, smart_health($device)];
}

my $smart_status = "N/A";
if (@smart_results) {
    $smart_status = "Operational";
    for my $entry (@smart_results) {
        if ($entry->[1] eq "Attention") { $smart_status = "Attention"; last; }
        if ($entry->[1] eq "N/A" && $smart_status ne "Attention") { $smart_status = "N/A"; }
    }
}
my $smart_html = join("<br>", map { $_->[0] . ": " . $_->[1] } @smart_results);
my ($docker_status, $docker_containers) = docker_info();
my $docker_html = "";

for my $container (@$docker_containers) {
    my ($name, $status) = @$container;
    $docker_html .= "$name: $status<br>";
}
my ($tailscale_status, $tailscale_ip, $tailscale_peers, $tailscale_funnel) = tailscale_info();
my ($ufw_status, $ufw_logging, $ufw_incoming, $ufw_allow_rules, $ufw_ssh_scope) = ufw_info();
my ($backup_status, $backup_last, $backup_next, $backup_result, $backup_timer) = backup_info();
my (
    $weather_temp,
    $weather_feels,
    $weather_humidity,
    $weather_code,
    $weather_wind,
    $weather_high,
    $weather_low,
    $weather_rain
) = weather_info();

my $weather_condition =
    ($weather_code eq "N/A")
    ? "N/A"
    : weather_code_text($weather_code);
my (
    $network_interface_status,
    $network_interface,
    $network_lan_ip,
    $network_gateway_status,
    $network_gateway,
    $network_internet_status,
    $network_dns_status,
    $network_latency,
    $network_packet_loss
) = network_info();


my $health = overall_health(
    $cpu_status,
    $memory_status,
    $raid_status,
    $storage_status,
    $smart_status,
    $docker_status,
    $tailscale_status,
    $ufw_status,
    $backup_status,
    $network_interface_status,
    $network_gateway_status,
    $network_internet_status,
    $network_dns_status
);

my $dashboard_name = $config{dashboard_name} || "Homelab Monitoring";
my $dashboard_description = $config{dashboard_description} || "Custom monitoring and health dashboard for a Linux homelab server.";
my $weather_location = $config{weather_location} || "Configured Location";
my $storage_mount_display = $config{storage_mount} || "/mnt/storage";
my $backup_label = $config{backup_label} || "Homelab Server Backup";

ui_print_header($dashboard_name, $dashboard_name, "", undef, 1, 1);

print <<'HTML';
<style>
.hlm-wrap {
    max-width: 1200px;
    margin: 0 auto;
}
.hlm-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(220px, 1fr));
    gap: 16px;
    margin: 20px 0;
}
.hlm-card {
    color: #222;
    color: #222;
    border: 1px solid #d8d8d8;
    border-radius: 10px;
    padding: 18px;
    background: #fff;
}
.hlm-card h3 {
    margin: 0 0 8px 0;
    font-size: 16px;
}
.hlm-value {
    font-size: 30px;
    font-weight: 600;
}
.hlm-status {
    font-weight: 600;
}
.hlm-good { color: #188038; }
.hlm-warning { color: #b06000; }
.hlm-unknown { color: #777; }
.hlm-section {
    margin-top: 28px;
}
.hlm-placeholder {
    border: 1px dashed #bbb;
    border-radius: 8px;
    padding: 16px;
    margin: 10px 0;
}
</style>
HTML

print qq{
<div class="hlm-wrap">
<h1>$dashboard_name</h1>
<p>$dashboard_description</p>

<div class="hlm-grid">
};

print qq{
<div class="hlm-card">
<h3>CPU</h3>
<div class="hlm-value">$cpu% </div>
<p>Current processor utilization</p>
</div>

<div class="hlm-card">
<h3>Memory</h3>
<div class="hlm-value">$memory% </div>
<p>Current memory utilization</p>
</div>

<div class="hlm-card">
<h3>GPU</h3>
<div class="hlm-value">$gpu% </div>
<p>Current GPU engine utilization</p>
</div>

<div class="hlm-card">
<h3>Uptime</h3>
<div class="hlm-value" style="font-size:24px">$up</div>
<p>Time since last boot</p>
</div>

<div class="hlm-card">
<h3>Overall Health</h3>
<div class="hlm-value hlm-status @{[health_class($health)]}">$health</div>
<p>Based on system, storage, services, security, backup, and network health</p>
</div>
</div>
};
print qq{
<div class="hlm-section">
<h2>Infrastructure Health</h2>

<div class="hlm-placeholder">
<strong>RAID:</strong>
<div class="hlm-status @{[health_class($raid_status)]}">
$raid_status
</div>
<div>
Level: $raid_level<br>
Devices: $raid_active/$raid_disks active<br>
Array state: $raid_state
</div>
};

if ($raid_note ne "") {
    print qq{
<div class="hlm-warning">$raid_note</div>
};
}
print qq{
<div class="hlm-placeholder">
<strong>Storage:</strong>
<div class="hlm-status @{[health_class($storage_status)]}">
$storage_status
</div>
<div>
Mount: $storage_mount_display<br>
Capacity: @{[format_bytes($storage_size)]}<br>
Used: @{[format_bytes($storage_used)]}<br>
Available: @{[format_bytes($storage_avail)]}<br>
Usage: $storage_percent%
</div>
</div>
};

print qq{
<div class="hlm-placeholder">
<strong>SMART:</strong>
<div class="hlm-status @{[health_class($smart_status)]}">
$smart_status
</div>
<div>
$smart_html
</div>
</div>
};

print qq{
<div class="hlm-placeholder">
<strong>Docker Services:</strong>
<div class="hlm-status @{[health_class($docker_status)]}">
$docker_status
</div>
<div>
$docker_html
</div>
</div>
};
print qq{
<div class="hlm-section">
<h2>Networking &amp; Security</h2>

<div class="hlm-placeholder">
<strong>Network Diagnostics:</strong>
<div>
Interface: $network_interface<br>
Interface status: $network_interface_status<br>
LAN IP: $network_lan_ip<br>
Gateway: $network_gateway ($network_gateway_status)<br>
Internet: $network_internet_status<br>
DNS: $network_dns_status<br>
Latency: $network_latency ms<br>
Packet loss: $network_packet_loss%
</div>
</div>

<div class="hlm-placeholder">
<strong>Tailscale:</strong>
<div class="hlm-status @{[health_class($tailscale_status)]}">
$tailscale_status
</div>
<div>
Server IP: $tailscale_ip<br>
Peers visible: $tailscale_peers<br>
Funnel: $tailscale_funnel
</div>
</div>

<div class="hlm-placeholder">
<strong>UFW Firewall:</strong>
<div class="hlm-status @{[health_class($ufw_status)]}">
$ufw_status
</div>
<div>
Logging: $ufw_logging<br>
Default incoming: $ufw_incoming<br>
Allow rules: $ufw_allow_rules<br>
SSH exposure: $ufw_ssh_scope
</div>
</div>

<div class="hlm-placeholder">
<strong>Backup Status:</strong>
<div class="hlm-status @{[health_class($backup_status)]}">
$backup_status
</div>
<div>
Job: $backup_label<br>
Last result: $backup_result<br>
Last completed: $backup_last<br>
Next scheduled: $backup_next<br>
Timer: $backup_timer
</div>
</div>

</div>

<div class="hlm-section">
<h2>Weather</h2>

<div class="hlm-placeholder">
<strong>$weather_location:</strong>
<div class="hlm-status good">
$weather_condition
</div>
<div>
Temperature: $weather_temp&deg;F<br>
Feels like: $weather_feels&deg;F<br>
Humidity: $weather_humidity%<br>
Wind: $weather_wind mph<br>
Today's high: $weather_high&deg;F<br>
Today's low: $weather_low&deg;F<br>
Rain chance: $weather_rain%
</div>
</div>

</div>
};

print <<'HTML';
</div>
HTML

ui_print_footer("", undef, 1);

1;
