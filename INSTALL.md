# Entity Janitor Installation Guide

## Prerequisites

- Home Assistant 2024.1.0 or later
- HACS (Home Assistant Community Store) installed (for HACS installation)

## Installation Methods

### Method 1: HACS (Recommended)

1. **Open HACS** in your Home Assistant instance
2. **Navigate to Integrations**
3. **Click the three dots** (⋮) in the top right corner
4. **Select "Custom repositories"**
5. **Add the repository**:
   - **URL**: `https://github.com/Jacid23/entity-janitor`
   - **Category**: Integration
   - **Click "Add"**
6. **Find Entity Janitor** in the integrations list
7. **Click "Download"**
8. **Restart Home Assistant**

### Method 2: Manual Installation

1. **Download the latest release** from [GitHub releases](https://github.com/Jacid23/entity-janitor/releases)
2. **Extract the files** to your Home Assistant `custom_components` directory
3. **Ensure proper structure**:
   ```
   custom_components/
   └── entity_janitor/
       ├── __init__.py
       ├── manifest.json
       ├── config_flow.py
       └── ... (other files)
   ```
4. **Restart Home Assistant**

## Configuration

### Initial Setup

1. **Go to Settings** → **Devices & Services**
2. **Click "Add Integration"**
3. **Search for "Entity Janitor"**
4. **Click to add the integration**
5. **Configure your preferences**:
   - **Auto Scan**: Enable automatic periodic scanning
   - **Scan Interval**: How often to scan (15-1440 minutes)
   - **Auto Clean**: Enable automatic cleanup (requires backup)
   - **Backup Before Clean**: Create backup files before removal
   - **Minimum Age**: Only consider entities older than X days
   - **Dry Run**: Preview changes without applying them

### Advanced Configuration

#### Excluded Domains
Skip entire entity domains (e.g., `automation`, `script`, `scene`):
```
automation, script, scene, zone, person
```

#### Excluded Entities
Protect specific entities from cleanup:
```
sensor.important_data, switch.critical_device
```

## Verification

After installation, verify the integration is working:

1. **Check Entities**: Look for Entity Janitor sensors in your entity list
2. **View Logs**: Check for any errors in the Home Assistant logs
3. **Test Scan**: Use the scan button to perform a manual scan
4. **Verify Backup**: Ensure backup files are created when enabled

## Troubleshooting

### Integration Not Appearing

1. **Check file structure** in `custom_components/entity_janitor/`
2. **Verify manifest.json** is present and valid
3. **Check Home Assistant logs** for loading errors
4. **Restart Home Assistant** completely

### Scan Not Finding Entities

1. **Verify minimum age** setting (entities may be too new)
2. **Check excluded domains** configuration
3. **Review entity registry** for actual orphaned entities
4. **Enable debug logging** for detailed information

### Backup Issues

1. **Check Home Assistant permissions** for writing files
2. **Verify storage space** availability
3. **Review backup file location** in configuration directory
4. **Check backup file format** (should be valid JSON)

## Debug Logging

Enable detailed logging by adding to your `configuration.yaml`:

```yaml
logger:
  logs:
    custom_components.entity_janitor: debug
```

## Support

For issues and questions:
- **GitHub Issues**: [Report bugs and request features](https://github.com/Jacid23/entity-janitor/issues)
- **Home Assistant Community**: [General discussion and help](https://community.home-assistant.io)
- **Documentation**: [README and guides](https://github.com/Jacid23/entity-janitor)

## Uninstallation

To remove Entity Janitor:

1. **Remove the integration** from Settings → Devices & Services
2. **Delete the folder** `custom_components/entity_janitor/`
3. **Restart Home Assistant**
4. **Clean up** any remaining backup files (optional)
