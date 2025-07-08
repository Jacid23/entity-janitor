# Entity Janitor for Home Assistant

[![hacs_badge](https://img.shields.io/badge/HACS-Custom-41BDF5.svg)](https://github.com/hacs/integration)
[![GitHub release (latest by date)](https://github.com/Jacid23/entity-janitor/releases/tag/v1.0.3)](https://github.com/homeassistant-user/entity-janitor/releases)
[![GitHub](https://img.shields.io/github/license/homeassistant-user/entity-janitor)](LICENSE)

A comprehensive Home Assistant custom integration for automatically detecting and managing orphaned entities.

## 🧹 What It Does

Entity Janitor automatically identifies and helps you clean up orphaned entities in your Home Assistant installation. These are entities that remain in your entity registry but are no longer connected to active devices or integrations.

## ✨ Features

- **🔍 Automatic Scanning**: Regularly scan for orphaned entities
- **🛡️ Safe Cleanup**: Backup entities before removal with dry-run mode
- **⚙️ Configurable Filters**: Exclude specific domains and entities
- **📊 Multiple Interfaces**: Sensors, buttons, switches, and services
- **⏰ Age-based Filtering**: Only consider entities older than specified days
- **📝 Comprehensive Logging**: Detailed logs for all operations
- **🔔 Event System**: Fire events for automation triggers

## 🚀 Installation

### HACS (Recommended)

1. Open HACS in your Home Assistant instance
2. Click on "Integrations"
3. Click the three dots in the top right corner
4. Select "Custom repositories"
5. Add this repository URL: `https://github.com/homeassistant-user/entity-janitor`
6. Select "Integration" as the category
7. Click "Add"
8. Find "Entity Janitor" in the list and click "Install"
9. Restart Home Assistant

### Manual Installation

1. Download the `entity_janitor` folder from this repository
2. Copy it to your `custom_components` directory
3. Restart Home Assistant
4. Go to Settings → Devices & Services
5. Click "Add Integration" and search for "Entity Janitor"

## 📋 Configuration

### Initial Setup

1. Go to Settings → Devices & Services
2. Click "Add Integration"
3. Search for "Entity Janitor"
4. Configure your preferences:
   - **Auto Scan**: Enable automatic scanning
   - **Scan Interval**: How often to scan (15-1440 minutes)
   - **Auto Clean**: Enable automatic cleanup (requires backup)
   - **Backup Before Clean**: Create backup files before removal
   - **Minimum Age**: Only consider entities older than X days
   - **Dry Run**: Show what would be cleaned without actually removing

### Advanced Options

- **Excluded Domains**: Entity domains to skip (e.g., automation, script)
- **Excluded Entities**: Specific entities to never remove

## 🎛️ Usage

### Sensors

- `sensor.entity_janitor_orphan_count`: Number of orphaned entities found
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

## 🔍 How It Works

The integration identifies orphaned entities by checking:

1. **Missing Devices**: Entities linked to non-existent devices
2. **Missing Config Entries**: Entities with invalid configuration entries
3. **Unloaded Integrations**: Entities from disabled/removed integrations
4. **Stale Entities**: Entities without active state

## 🛡️ Safety Features

- **Dry Run Mode**: Preview changes before applying
- **Automatic Backups**: JSON backups before cleanup
- **Age Filtering**: Only remove entities older than specified days
- **Domain Exclusions**: Skip critical entity types
- **Entity Exclusions**: Protect specific entities

## 📁 Backup Files

Backups are saved as JSON files in your Home Assistant configuration directory:
- `entity_janitor_backup_YYYYMMDD_HHMMSS.json`

Each backup contains:
- Timestamp
- Entity details (ID, domain, platform, etc.)
- Cleanup reason
- Total count

## 🔔 Events

The integration fires events for automation:
- `entity_janitor_orphans_found`: When orphans are detected
- `entity_janitor_cleanup_complete`: When cleanup finishes

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🐛 Issues

If you encounter any problems, please [open an issue](https://github.com/homeassistant-user/entity-janitor/issues) on GitHub.

## ⭐ Support

If you find this integration useful, please consider giving it a star on GitHub!

---

## 💡 Inspiration

This integration was created to address the common problem of orphaned entities accumulating in Home Assistant installations over time, especially after removing devices or changing integrations. It provides a safe, automated way to keep your entity registry clean and optimized.
