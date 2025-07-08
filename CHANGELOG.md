# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.3] - 2025-07-07

### Fixed
- **Version Display**: Fixed HACS showing commit hash instead of version number
- Created proper GitHub release structure for version management
- Updated manifest.json to v1.0.3 for proper release tagging

### Documentation
- Added VERSION_FIX_GUIDE.md for GitHub release management
- Updated instructions for creating proper releases

## [1.0.2] - 2025-07-07

### Fixed
- **Critical**: Fixed "Config flow could not be loaded: Invalid handler specified" error
- Corrected config flow class registration with proper domain parameter
- Updated config flow imports and class structure for Home Assistant compatibility

## [1.0.1] - 2025-07-07

### Added
- Custom logo icon (icon.svg) for better visual identification
- Updated installation instructions prioritizing HACS
- Logo information documentation

### Changed
- Updated manifest with correct repository URLs (@Jacid23)
- Enhanced README with clearer HACS installation steps
- Version bump to 1.0.1 for logo and documentation updates

### Fixed
- HACS repository structure compliance achieved
- Corrected documentation URLs in manifest.json

## [1.0.0] - 2025-07-07

### Added
- Initial release of Entity Janitor integration
- Automatic orphaned entity detection and cleanup
- Safe backup system before cleanup operations
- Configurable filtering by domain and entity ID
- Age-based filtering for entity cleanup
- Dry-run mode for preview functionality
- Multiple platform support (sensors, buttons, switches)
- Comprehensive service API
- Event system for automation triggers
- Full configuration UI with options flow
- Extensive documentation and examples

### Features
- **Sensors**: Track orphan count, total entities, and last scan time
- **Buttons**: Manual scan, dry-run cleanup, and backup creation
- **Switches**: Toggle auto-scan and auto-clean functionality
- **Services**: Programmatic control of all operations
- **Safety**: Backup system with JSON export/import
- **Automation**: Event-driven automation support
- **Logging**: Comprehensive logging for all operations

### Safety Features
- Dry-run mode prevents accidental deletions
- Automatic backups before cleanup operations
- Age-based filtering protects new entities
- Domain exclusions protect critical entity types
- Entity-specific exclusions for custom protection
- Comprehensive logging for audit trails

### Configuration
- User-friendly setup wizard
- Advanced options for power users
- Configurable scan intervals
- Flexible filtering options
- Safe defaults for new installations
