# Entity Janitor Installation Guide

## Prerequisites

- Home Assistant 2023.3 or later
- Access to your Home Assistant configuration directory
- Basic understanding of Home Assistant integrations

## Installation Methods

### Method 1: Manual Installation (Recommended)

1. **Download the Integration**
   - Copy the entire `entity_janitor` folder to your `custom_components` directory
   - Path should be: `<config>/custom_components/entity_janitor/`

2. **Restart Home Assistant**
   ```bash
   # If using Docker
   docker restart homeassistant
   
   # If using systemd
   sudo systemctl restart home-assistant@homeassistant
   ```

3. **Add the Integration**
   - Go to Settings → Devices & Services
   - Click "Add Integration"
   - Search for "Entity Janitor"
   - Follow the configuration wizard

### Method 2: HACS (Future)

This integration is designed to be HACS-compatible but would need to be submitted to the HACS store.

## Initial Configuration

### Basic Setup

1. **Enable Integration**
   - Auto Scan: Start with `false` to control scanning manually
   - Scan Interval: 60 minutes (reasonable default)
   - Auto Clean: Keep `false` until you're comfortable
   - Backup Before Clean: Always keep `true`
   - Minimum Age: 7 days (protects new entities)
   - Dry Run: Keep `true` for testing

2. **First Scan**
   - Use the "Scan Orphans" button to do your first scan
   - Review the results in the sensor attributes
   - Check the logs for any issues

### Advanced Configuration

Access through Settings → Devices & Services → Entity Janitor → Configure

- **Excluded Domains**: Add domains you never want cleaned
- **Excluded Entities**: Protect specific entities by ID
- **Scan Interval**: Adjust based on your system size
- **Age Filtering**: Increase for more conservative cleanup

## Testing and Validation

### Step 1: First Scan
```yaml
# Call via Developer Tools → Services
service: entity_janitor.scan_orphans
```

### Step 2: Review Results
- Check `sensor.entity_janitor_orphan_count`
- Look at sensor attributes for entity list
- Review logs for any errors

### Step 3: Dry Run Cleanup
```yaml
service: entity_janitor.clean_orphans
data:
  dry_run: true
  backup_before_clean: true
```

### Step 4: Backup First
```yaml
service: entity_janitor.backup_entities
```

### Step 5: Real Cleanup (When Ready)
```yaml
service: entity_janitor.clean_orphans
data:
  dry_run: false
  backup_before_clean: true
```

## Monitoring and Maintenance

### Dashboard Setup
Add the provided Lovelace cards to monitor:
- Orphan count trends
- Last scan times
- Total entity counts

### Automation Setup
Use the example automations for:
- Weekly scanning
- Orphan alerts
- Automatic backups

### Log Monitoring
Enable debug logging to track operations:
```yaml
logger:
  logs:
    custom_components.entity_janitor: debug
```

## Safety Best Practices

1. **Always Backup First**
   - Create backups before any cleanup
   - Test restore procedures
   - Keep multiple backup generations

2. **Start Conservative**
   - Use high minimum age (14+ days)
   - Exclude critical domains
   - Test with small batches

3. **Monitor Results**
   - Check entity counts before/after
   - Verify functionality isn't affected
   - Review logs for errors

4. **Gradual Automation**
   - Start with manual operations
   - Enable auto-scan after validation
   - Only enable auto-clean after extensive testing

## Troubleshooting

### Common Issues

**Integration Won't Load**
- Check file permissions
- Verify directory structure
- Review Home Assistant logs

**Scan Failures**
- Check available memory
- Verify entity registry isn't corrupted
- Try smaller batches

**Cleanup Issues**
- Ensure backup location is writable
- Check for locked entity files
- Verify entity registry permissions

### Recovery Procedures

**Restore from Backup**
Currently manual restoration is required:
1. Locate backup file in config directory
2. Review backup contents
3. Manually re-add critical entities if needed

**Reset Integration**
1. Remove integration from UI
2. Restart Home Assistant
3. Re-add with fresh configuration

## Performance Considerations

### Large Installations
- Expect longer scan times with 10,000+ entities
- Consider increasing scan intervals
- Monitor memory usage during scans

### Storage Impact
- Backup files can be large with many entities
- Implement backup rotation
- Monitor disk space usage

## Support and Documentation

- Check logs first: `<config>/home-assistant.log`
- Review entity registry: `<config>/.storage/core.entity_registry`
- Backup files: `<config>/entity_janitor_backup_*.json`
