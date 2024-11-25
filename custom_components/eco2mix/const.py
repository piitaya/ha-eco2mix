"""Constants for the éCO2mix integration."""
from datetime import timedelta

DOMAIN = "eco2mix"
DEFAULT_SCAN_INTERVAL = 5  # minutes
MIN_SCAN_INTERVAL = 1  # minutes
SCAN_INTERVAL = timedelta(minutes=DEFAULT_SCAN_INTERVAL)

POWER_MEGA_WATT = "MW"

# Sources definition for aggregates
RENEWABLE_SOURCES = ["wind", "solar", "hydraulic", "bioenergy"]
LOW_CARBON_SOURCES = RENEWABLE_SOURCES + ["nuclear"]
ALL_PRODUCTION_SOURCES = LOW_CARBON_SOURCES + ["gas", "coal", "fuel"]

# Default sensors to enable
DEFAULT_SENSORS = [
    "consumption",
    "total_production",
    "renewable_percentage",
    "low_carbon_percentage",
    "last_update"
]

# Sensors definition with their names and icons
SENSOR_TYPES = {
    # Production sensors (power)
    "consumption": ("Consommation", "mdi:flash"),
    "nuclear": ("Production Nucléaire", "mdi:atom"),
    "wind": ("Production Éolienne", "mdi:wind-turbine"),
    "solar": ("Production Solaire", "mdi:solar-power"),
    "hydraulic": ("Production Hydraulique", "mdi:hydro-power"),
    "bioenergy": ("Production Bioénergies", "mdi:leaf"),
    "gas": ("Production Gaz", "mdi:fire"),
    "coal": ("Production Charbon", "mdi:factory"),
    "fuel": ("Production Fioul", "mdi:oil"),
    "total_production": ("Production Totale", "mdi:lightning-bolt"),
    
    # Aggregate sensors (power)
    "renewable": ("Production Renouvelable", "mdi:leaf-circle"),
    "low_carbon": ("Production Bas Carbone", "mdi:molecule-co2"),
    
    # Grid exchange sensors (power)
    "pumping": ("Pompage", "mdi:pump"),
    "import": ("Import", "mdi:import"),
    "export": ("Export", "mdi:export"),
    
    # Percentage sensors
    "nuclear_percentage": ("Pourcentage Nucléaire", "mdi:atom"),
    "wind_percentage": ("Pourcentage Éolien", "mdi:wind-turbine"),
    "solar_percentage": ("Pourcentage Solaire", "mdi:solar-power"),
    "hydraulic_percentage": ("Pourcentage Hydraulique", "mdi:hydro-power"),
    "bioenergy_percentage": ("Pourcentage Bioénergies", "mdi:leaf"),
    "gas_percentage": ("Pourcentage Gaz", "mdi:fire"),
    "coal_percentage": ("Pourcentage Charbon", "mdi:factory"),
    "fuel_percentage": ("Pourcentage Fioul", "mdi:oil"),
    "renewable_percentage": ("Pourcentage Renouvelable", "mdi:leaf-circle"),
    "low_carbon_percentage": ("Pourcentage Bas Carbone", "mdi:molecule-co2"),
    
    # Timestamp
    "last_update": ("Dernière mise à jour", "mdi:clock")
}

STORAGE_VERSION = 1
STORAGE_KEY = "eco2mix_cache"
