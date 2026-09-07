"""Geographical distance and coordinate calculation utilities."""
import math
from src.config.constants import FACILITY_COORDS, BLOCK_COORDS

def haversine_km(lat1, lon1, lat2, lon2):
    """Calculate great-circle distance between two points on Earth (km)."""
    R = 6371.0  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))

def get_facility_coords(fac):
    """Get approximate coordinates for a facility from FACILITY_COORDS or location name."""
    name = fac.get("name", "")
    if name in FACILITY_COORDS:
        return FACILITY_COORDS[name]
    # Fall back to block-level coordinates from location field
    loc = fac.get("location", "").lower()
    if loc in BLOCK_COORDS:
        return BLOCK_COORDS[loc]
    return None

def facility_distance_km(fac, ref_lat, ref_lon):
    """Return approximate distance in km from reference point to facility, or None."""
    coords = get_facility_coords(fac)
    if not coords:
        return None
    return haversine_km(ref_lat, ref_lon, coords[0], coords[1])
