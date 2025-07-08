# Entity Janitor - User-Facing Template Controls

## Overview
Entity Janitor now provides user-facing template switches and buttons similar to ESPHome's platform: template pattern, giving users direct control over the integration's behavior and actions.

## New Template Switches (entity_category: config)

### Configuration Switches
1. **Entity Janitor Backup Before Clean** (`switch.entity_janitor_template_backup_before_clean`)
   - Icon: `mdi:content-save-cog`
   - Automatically backup entities before cleaning
   - Default: ON

2. **Entity Janitor Dry Run Mode** (`switch.entity_janitor_template_dry_run_mode`)
   - Icon: `mdi:test-tube`
   - Test cleanup operations without actually removing entities
   - Default: OFF

3. **Entity Janitor Notifications** (`switch.entity_janitor_template_notifications_enabled`)
   - Icon: `mdi:bell-ring`
   - Send notifications when obsolete entities are found
   - Default: ON

4. **Entity Janitor Detailed Logging** (`switch.entity_janitor_template_detailed_logging`)
   - Icon: `mdi:text-box-search`
   - Enable detailed logging for troubleshooting
   - Default: OFF
   - Automatically adjusts logging level when toggled

### Operational Switches
5. **Entity Janitor Auto Scan** (`switch.entity_janitor_auto_scan`)
   - Icon: `mdi:magnify-scan`
   - Enable automatic scanning for obsolete entities
   - Category: config

6. **Entity Janitor Auto Clean** (`switch.entity_janitor_auto_clean`)
   - Icon: `mdi:delete-sweep`
   - Enable automatic cleanup of obsolete entities
   - Category: config

## New Template Buttons (entity_category: config)

### Quick Action Buttons
1. **Entity Janitor Quick Scan** (`button.entity_janitor_template_quick_scan`)
   - Icon: `mdi:magnify-scan`
   - Quickly scan for obsolete entities
   - Fires event: `entity_janitor_quick_scan_complete`

2. **Entity Janitor Full Cleanup** (`button.entity_janitor_template_full_cleanup`)
   - Icon: `mdi:delete-sweep`
   - Perform full cleanup with backup (respects dry run mode)
   - Fires event: `entity_janitor_full_cleanup_complete`

3. **Entity Janitor Export Report** (`button.entity_janitor_template_export_report`)
   - Icon: `mdi:file-export`
   - Export detailed JSON report of obsolete entities
   - Saves to: `config/entity_janitor_report_YYYYMMDD_HHMMSS.json`

4. **Entity Janitor Reset Statistics** (`button.entity_janitor_template_reset_stats`)
   - Icon: `mdi:refresh`
   - Reset statistics and clear cached data
   - Fires event: `entity_janitor_stats_reset`

### Existing Buttons
5. **Entity Janitor Scan Obsolete** (`button.entity_janitor_scan_obsolete`)
   - Icon: `mdi:magnify`
   - Scan for obsolete entities

6. **Entity Janitor Test Cleanup** (`button.entity_janitor_test_cleanup`)
   - Icon: `mdi:play-outline`
   - Test cleanup without removing entities

7. **Entity Janitor Backup Obsolete** (`button.entity_janitor_backup_obsolete`)
   - Icon: `mdi:content-save`
   - Backup currently found obsolete entities

## ESPHome-Style Features

### Similar to ESPHome Template Pattern
- **entity_category: config** - Groups controls in configuration section
- **Optimistic behavior** - Immediate UI feedback
- **Clear naming** - User-friendly names and descriptions
- **Appropriate icons** - Material Design icons for each function
- **Event firing** - Similar to ESPHome's event system
- **State attributes** - Extra information about each control

### Switch Behaviors
- **Immediate feedback** - Changes are applied immediately
- **Persistent state** - Settings are saved to config entry options
- **Action triggers** - Some switches trigger specific actions (like logging level changes)
- **State restoration** - Switches remember their state across restarts

### Button Behaviors
- **Single press actions** - Each button performs a specific action
- **Event generation** - Buttons fire events that can be used in automations
- **Status feedback** - Button actions are logged and provide feedback
- **Smart behavior** - Buttons respect current settings (dry run mode, etc.)

## Usage Examples

### Direct User Control
Users can now control Entity Janitor directly from the integration page:
1. Toggle dry run mode on/off
2. Enable/disable notifications
3. Perform quick scans
4. Export reports
5. Reset statistics

### Automation Integration
The fired events can be used in Home Assistant automations:
```yaml
automation:
  - alias: "Entity Janitor Scan Complete"
    trigger:
      - platform: event
        event_type: entity_janitor_quick_scan_complete
    action:
      - service: notify.mobile_app_phone
        data:
          message: "Found {{ trigger.event.data.obsolete_count }} obsolete entities"
```

### Configuration Management
Template switches provide an easy way to manage configuration:
- No need to edit YAML files
- Changes take effect immediately
- Settings are preserved across restarts
- Visual feedback in the UI

## Technical Implementation

### Switch Implementation
- Extends `CoordinatorEntity` and `SwitchEntity`
- Uses `entity_category: config` for proper grouping
- Implements `async_turn_on/off` with immediate state updates
- Saves settings to config entry options
- Provides extra state attributes for debugging

### Button Implementation
- Extends `CoordinatorEntity` and `ButtonEntity`
- Uses `entity_category: config` for proper grouping
- Implements `async_press` with specific actions
- Fires events for automation integration
- Provides descriptive state attributes

This implementation follows the ESPHome template pattern while being native to Home Assistant, providing users with direct, intuitive control over the Entity Janitor integration.
