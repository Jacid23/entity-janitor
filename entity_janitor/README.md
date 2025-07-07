# Entity Janitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub Release](https://img.shields.io/github/release/home-assistant-user/entity-janitor.svg)](https://github.com/home-assistant-user/entity-janitor/releases)
[![License](https://img.shields.io/github/license/home-assistant-user/entity-janitor.svg)](LICENSE)

A Home Assistant custom integration for automated management of orphaned entities.

## Features

✅ **Automated Orphan Detection** - Automatically scans for entities without backing devices or integrations  
✅ **Safe Cleanup** - Backup entities before cleanup with full restore capability  
✅ **Configurable Filtering** - Exclude specific domains and entities from cleanup  
✅ **Dry Run Mode** - Preview what would be cleaned without making changes  
✅ **Integration Management** - Sensors, buttons, and switches for monitoring and control  
✅ **Service Integration** - Comprehensive services for automation and scripting  
✅ **Age-Based Filtering** - Only clean entities older than specified days  
✅ **Detailed Logging** - Complete audit trail of all cleanup operations  

## Installation

### HACS Installation (Recommended)

1. Open HACS in Home Assistant
2. Go to "Integrations" 
3. Click the 3-dot menu → "Custom repositories"
4. Add repository URL: `https://github.com/YOUR_USERNAME/entity-janitor`
5. Category: **Integration**
6. Click "Add"
7. Find "Entity Janitor" in HACS and install
8. Restart Home Assistant
9. Add the integration via Settings → Devices & Services → Add Integration

### Manual Installation

1. Download the latest release from [GitHub releases](https://github.com/home-assistant-user/entity-janitor/releases)
2. Extract to `custom_components/entity_janitor/` in your Home Assistant config directory
3. Restart Home Assistant
4. Add the integration via Settings → Devices & Services → Add Integration

## Configuration

Configure Entity Janitor through the Home Assistant UI:

1. Go to **Settings** → **Devices & Services** → **Add Integration**
2. Search for "Entity Janitor"
3. Configure your preferences:
   - **Auto Scan**: Enable automatic periodic scanning
   - **Scan Interval**: How often to scan (15-1440 minutes)
   - **Auto Clean**: Enable automatic cleanup (requires backup)
   - **Backup Before Clean**: Create backups before cleanup (recommended)
   - **Minimum Age**: Only clean entities older than X days
   - **Dry Run**: Preview mode without actual cleanup

## Usage

### Sensors
- `sensor.entity_janitor_orphan_count`: Number of orphaned entities
- `sensor.entity_janitor_total_entities`: Total entities in registry
- `sensor.entity_janitor_last_scan`: Last scan timestamp

### Buttons
- `button.entity_janitor_scan_orphans`: Trigger manual scan
- `button.entity_janitor_clean_orphans_dry_run`: Preview cleanup
- `button.entity_janitor_backup_orphans`: Create backup

### Switches
- `switch.entity_janitor_auto_scan`: Enable/disable auto scanning
- `switch.entity_janitor_auto_clean`: Enable/disable auto cleanup

### Services

#### `entity_janitor.scan_orphans`
Scan for orphaned entities.

#### `entity_janitor.clean_orphans`
Clean orphaned entities.
```yaml
service: entity_janitor.clean_orphans
data:
  entity_ids: [] # Optional: specific entities to clean
  dry_run: true # Optional: preview mode
  backup_before_clean: true # Optional: create backup
```

#### `entity_janitor.backup_entities`
Backup orphaned entities.
```yaml
service: entity_janitor.backup_entities
data:
  entity_ids: [] # Optional: specific entities to backup
```

## How It Works

The integration identifies orphaned entities by checking:

1. **Missing Devices**: Entities linked to non-existent devices
2. **Missing Config Entries**: Entities with invalid configuration entries
3. **Unloaded Integrations**: Entities from disabled/removed integrations
4. **Stale Entities**: Entities without active state

## Safety Features

- **Dry Run Mode**: Preview changes before applying
- **Automatic Backups**: JSON backups before cleanup
- **Age Filtering**: Only remove entities older than specified days
- **Domain Exclusions**: Skip critical entity types
- **Entity Exclusions**: Protect specific entities

## Backup Files

Backups are saved as JSON files in your Home Assistant configuration directory:
- `entity_janitor_backup_YYYYMMDD_HHMMSS.json`

Each backup contains:
- Timestamp
- Entity details (ID, domain, platform, etc.)
- Cleanup reason
- Total count

## Events

The integration fires events for automation:
- `entity_janitor_orphans_found`: When orphans are detected
- `entity_janitor_cleanup_complete`: When cleanup finishes

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Home Assistant is recent enough
2. **Permission Errors**: Check file system permissions
3. **Memory Issues**: Large entity registries may need patience

### Logs

Enable debug logging:
```yaml
logger:
  logs:
    custom_components.entity_janitor: debug
```

## Contributing

This integration is designed to be safe and conservative. Always test in a development environment first.

## License

This custom integration is provided as-is for educational and utility purposes.
