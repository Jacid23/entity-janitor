# Entity Janitor

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub](https://img.shields.io/badge/GitHub-Jacid23%2Fentity--janitor-blue.svg)](https://github.com/Jacid23/entity-janitor)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](https://github.com/Jacid23/entity-janitor/blob/main/LICENSE)
[![Version](https://img.shields.io/badge/Version-1.0.3-green.svg)](https://github.com/Jacid23/entity-janitor)

A professional Home Assistant custom integration for automated management of obsolete entities with ESPHome-style user controls.

## Features

✅ **Automated Obsolete Detection** - Automatically scans for entities without backing devices or integrations  
✅ **Safe Cleanup** - Backup entities before cleanup with full restore capability  
✅ **User-Friendly Controls** - ESPHome-style template switches and buttons for direct interaction  
✅ **Device Grouping** - All entities grouped under a single "Entity Janitor" device with custom icon  
✅ **Professional Terminology** - Uses "obsolete" instead of "orphan" throughout the interface  
✅ **Configurable Filtering** - Exclude specific domains and entities from cleanup  
✅ **Dry Run Mode** - Preview what would be cleaned without making changes  
✅ **Template Controls** - Interactive switches and buttons for monitoring and control  
✅ **Service Integration** - Comprehensive services for automation and scripting  
✅ **Age-Based Filtering** - Only clean entities older than specified days  
✅ **Detailed Logging** - Complete audit trail of all cleanup operations  

## Installation

### HACS Installation (Recommended)

1. **Open HACS** in Home Assistant
2. **Go to "Integrations"** 
3. **Click the 3-dot menu** → **"Custom repositories"**
4. **Add repository URL**: `https://github.com/Jacid23/entity-janitor`
5. **Category**: **Integration**
6. **Click "Add"**
7. **Find "Entity Janitor"** in HACS and click **"Download"**
8. **Restart Home Assistant**
9. **Add the integration**: Settings → Devices & Services → Add Integration → "Entity Janitor"

### Manual Installation

1. Download the latest release from [GitHub releases](https://github.com/Jacid23/entity-janitor/releases)
2. Extract the downloaded ZIP file
3. Copy the integration files to your `custom_components` directory:
   - If files are in `custom_components/entity_janitor/`, copy that folder
   - If files are in the root, create a new folder called `entity_janitor` in your `custom_components` directory and copy all files there
4. Copy `www/entity_janitor/icon.svg` to your `www/entity_janitor/` directory for the device icon
5. Your final structure should be: `custom_components/entity_janitor/manifest.json`
6. Restart Home Assistant
7. Add the integration via Settings → Devices & Services → Add Integration

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

## Device & Controls

All Entity Janitor entities are grouped under a single device with a custom icon. The device includes:

### Sensors
- `sensor.entity_janitor_obsolete_count`: Number of obsolete entities found
- `sensor.entity_janitor_total_entities`: Total entities in registry
- `sensor.entity_janitor_last_scan`: Last scan timestamp

### Template Switches (ESPHome-style)
- `switch.entity_janitor_backup_before_clean`: Enable/disable automatic backups
- `switch.entity_janitor_dry_run_mode`: Enable/disable dry run mode
- `switch.entity_janitor_notifications`: Enable/disable notifications
- `switch.entity_janitor_detailed_logging`: Enable/disable detailed logging

### Template Buttons (ESPHome-style)
- `button.entity_janitor_quick_scan`: Trigger manual scan for obsolete entities
- `button.entity_janitor_full_cleanup`: Perform full cleanup of obsolete entities
- `button.entity_janitor_export_report`: Export scan results to file
- `button.entity_janitor_reset_statistics`: Reset scan statistics

### Legacy Controls (Deprecated)
- `button.entity_janitor_scan_obsolete`: Trigger manual scan
- `button.entity_janitor_clean_obsolete_dry_run`: Preview cleanup
- `button.entity_janitor_backup_obsolete`: Create backup

## Services

### `entity_janitor.scan_obsolete`
Scan for obsolete entities.

### `entity_janitor.clean_obsolete`
Clean obsolete entities.
```yaml
service: entity_janitor.clean_obsolete
data:
  entity_ids: [] # Optional: specific entities to clean
  dry_run: true # Optional: preview mode
  backup_before_clean: true # Optional: create backup
```

### `entity_janitor.backup_entities`
Backup obsolete entities.
```yaml
service: entity_janitor.backup_entities
data:
  entity_ids: [] # Optional: specific entities to backup
```

## How It Works

The integration identifies obsolete entities by checking:

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
- **Template Controls**: User-friendly switches and buttons for safe operation

## Device Icon

The Entity Janitor device features a custom icon that combines:
- **Broom**: Represents cleaning/janitor functionality
- **Database elements**: Represents entity management
- **Sparkles**: Represents the optimization process
- **Professional colors**: Blue theme for a clean, professional look

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
- `entity_janitor_obsolete_found`: When obsolete entities are detected
- `entity_janitor_cleanup_complete`: When cleanup finishes
- `entity_janitor_scan_complete`: When scan completes

## Template Controls Usage

The template switches and buttons work like ESPHome entities:

### Switches
- **Toggle directly** in Home Assistant UI
- **Use in automations** for conditional logic
- **Monitor state** for dashboard displays

### Buttons
- **Press to trigger actions** immediately
- **Use in scripts** for batch operations
- **Monitor last pressed** for automation triggers

Example automation:
```yaml
automation:
  - alias: "Weekly Entity Cleanup"
    trigger:
      - platform: time
        at: "02:00:00"
    condition:
      - condition: time
        weekday:
          - sun
    action:
      - service: button.press
        target:
          entity_id: button.entity_janitor_quick_scan
      - delay: "00:01:00"
      - service: button.press
        target:
          entity_id: button.entity_janitor_full_cleanup
```

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure Home Assistant is version 2023.1 or newer
2. **Permission Errors**: Check file system permissions for backup directory
3. **Memory Issues**: Large entity registries may need patience during scans
4. **Device Icon Missing**: Ensure `www/entity_janitor/icon.svg` is copied correctly
5. **Template Controls Not Working**: Verify integration is properly configured

### Logs

Enable debug logging:
```yaml
logger:
  logs:
    custom_components.entity_janitor: debug
```

### Reset Integration

If issues persist:
1. Remove integration from Settings → Devices & Services
2. Restart Home Assistant
3. Re-add the integration

## Changelog

### Version 1.0.3
- **Professional Terminology**: Changed "orphan" to "obsolete" throughout
- **ESPHome-Style Controls**: Added template switches and buttons
- **Device Grouping**: All entities grouped under single device
- **Custom Icon**: Added professional device icon
- **Improved Safety**: Enhanced backup and dry-run capabilities
- **Better UX**: User-friendly controls and terminology

## Contributing

This integration is designed to be safe and conservative. Always test in a development environment first.

### Development Setup
1. Clone the repository
2. Install development dependencies
3. Run tests before submitting PRs
4. Follow the coding standards

### Bug Reports
Please include:
- Home Assistant version
- Entity Janitor version
- Relevant logs
- Steps to reproduce

## License

This custom integration is provided as-is under the MIT License for educational and utility purposes.

## Support

- **GitHub Issues**: Report bugs and feature requests
- **GitHub Discussions**: Ask questions and share experiences
- **Home Assistant Community**: Get help from the community

---

**⚠️ Important**: Always backup your Home Assistant configuration before using this integration. While designed to be safe, entity management operations should be performed carefully.
