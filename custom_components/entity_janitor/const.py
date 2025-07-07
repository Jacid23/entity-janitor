"""Constants for the Entity Janitor integration."""
from homeassistant.const import Platform

DOMAIN = "entity_janitor"
PLATFORMS = [Platform.SENSOR, Platform.BUTTON, Platform.SWITCH]

# Configuration options
CONF_AUTO_SCAN = "auto_scan"
CONF_SCAN_INTERVAL = "scan_interval"
CONF_AUTO_CLEAN = "auto_clean"
CONF_BACKUP_BEFORE_CLEAN = "backup_before_clean"
CONF_EXCLUDED_DOMAINS = "excluded_domains"
CONF_EXCLUDED_ENTITIES = "excluded_entities"
CONF_MINIMUM_AGE_DAYS = "minimum_age_days"
CONF_DRY_RUN = "dry_run"

# Default values
DEFAULT_SCAN_INTERVAL = 60  # minutes
DEFAULT_MINIMUM_AGE_DAYS = 7
DEFAULT_EXCLUDED_DOMAINS = [
    "persistent_notification",
    "zone", 
    "person",
    "device_tracker",
    "automation",
    "script",
    "scene"
]

# Service names
SERVICE_SCAN_ORPHANS = "scan_orphans"
SERVICE_CLEAN_ORPHANS = "clean_orphans"
SERVICE_BACKUP_ENTITIES = "backup_entities"
SERVICE_RESTORE_ENTITIES = "restore_entities"

# Attributes
ATTR_ORPHAN_COUNT = "orphan_count"
ATTR_TOTAL_ENTITIES = "total_entities"
ATTR_LAST_SCAN = "last_scan"
ATTR_BACKUP_FILE = "backup_file"
ATTR_CLEANED_COUNT = "cleaned_count"
ATTR_SKIPPED_COUNT = "skipped_count"

# Events
EVENT_ORPHANS_FOUND = "entity_janitor_orphans_found"
EVENT_CLEANUP_COMPLETE = "entity_janitor_cleanup_complete"
