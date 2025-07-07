# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-07-07

### Fixed
- **Version Display**: Fixed HACS showing commit hash instead of version number
- **Config Flow**: Fixed registration issues preventing integration from appearing in UI
- **Repository Structure**: Moved files to proper GitHub structure for easier downloads

### Documentation
- Added comprehensive GitHub setup and release guides
- Updated installation instructions for manual and HACS installation
- Created clean build folder structure

## [1.0.2] - 2025-07-07

### Fixed
- **Config Flow**: Fixed "Invalid handler specified" error
- **Class Definition**: Corrected ConfigFlow class structure
- **UI Integration**: Integration now appears properly in Home Assistant settings

### Documentation
- Added detailed troubleshooting guides
- Updated configuration examples

## [1.0.1] - 2025-07-07

### Added
- **Custom Logo**: Professional SVG logo with cleaning theme
- **HACS Compliance**: Full HACS integration support
- **Professional Documentation**: Complete README with badges and examples

### Fixed
- **HACS Structure**: Proper folder organization for HACS compatibility
- **Documentation Links**: Updated all URLs to point to correct repository

## [1.0.0] - 2025-07-07

### Added
- **Initial Release**: Complete Entity Janitor integration
- **Orphaned Entity Detection**: Automatically find entities without active devices
- **Safe Cleanup**: Backup entities before removal with dry-run mode
- **UI Integration**: Full Home Assistant configuration UI
- **Multiple Interfaces**: Sensors, buttons, switches, and services
- **Comprehensive Logging**: Detailed operation logs and debugging
- **Age-based Filtering**: Only process entities older than specified days
- **Domain/Entity Exclusions**: Protect critical entities from cleanup
- **Event System**: Fire events for automation integration
- **HACS Support**: Full HACS custom repository compatibility

### Features
- Auto-scan for orphaned entities
- Configurable scan intervals (15-1440 minutes)
- Automatic cleanup with safety checks
- JSON backup files with timestamps
- Dry-run mode for safe testing
- Comprehensive entity filtering options
- Home Assistant service integration
- Professional documentation and guides
