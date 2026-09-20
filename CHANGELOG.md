# Changelog

All notable changes to Webmin Homelab Monitor will be documented in this file.

The format is based on Keep a Changelog, and this project uses semantic versioning.

## [1.0.1] - 2026-09-18

### Added

- Initial installable Webmin module release
- CPU utilization monitoring
- Memory utilization monitoring
- GPU utilization support through a configurable helper command
- System uptime display
- Overall server health summary
- Linux software RAID monitoring
- SMART drive health monitoring
- Storage capacity and utilization monitoring
- Docker container monitoring
- Tailscale status monitoring
- Tailscale Funnel detection
- UFW firewall monitoring
- SSH exposure summary
- systemd backup timer/service monitoring
- Network interface status
- LAN IP detection
- Gateway connectivity testing
- Internet connectivity testing
- DNS resolution testing
- Latency measurement
- Packet-loss reporting
- Optional Open-Meteo weather panel
- Collector enable/disable toggles
- Native Webmin Module Config support
- Safe default configuration for fresh installs
- GitHub Pages static demo
- GitHub Actions build workflow
- Installable `.wbm.gz` release package
- GPL-3.0 license
- Installation, configuration, customization, and collector documentation

### Changed

- Migrated configuration from custom `config.pl` handling to Webmin's native module configuration system
- Standardized module ID and install path as `webmin-homelab-monitor`
- Improved disabled collector handling so unused features do not reduce overall health

### Fixed

- Fresh installs no longer fail because of a missing `config.pl`
- Fixed configuration path issues under Webmin
- Fixed duplicate and inconsistent configuration-loading logic
- Fixed outdated example configuration keys
- Fixed GitHub Actions Node.js 20 deprecation warnings
- Fixed module version detection in the build workflow
