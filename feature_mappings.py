# feature_mappings.py

peb_mapping = {
    'A++': 0, 'A+': 1, 'A': 2, 'B': 3, 'C': 4, 'D': 5, 'E': 6, 'F': 7, 'G': 8
}

state_of_building_mapping = {
    'New': 0, 'Good': 1, 'Fair': 2, 'Poor': 3, 'Needs Renovation': 4
}

type_of_property_mapping = {
    'House': 0, 'Apartment': 1, 'Villa': 2, 'Studio': 3
}

flooding_zone_mapping = {
    'CIRCUMSCRIBED_FLOOD_ZONE': 0, 'CIRCUMSCRIBED_WATERSIDE_ZONE': 1,
    'NON_FLOOD_ZONE': 2, 'POSSIBLE_FLOOD_ZONE': 3,
    'POSSIBLE_N_CIRCUMSCRIBED_FLOOD_ZONE': 4, 'POSSIBLE_N_CIRCUMSCRIBED_WATERSIDE_ZONE': 5,
    'RECOGNIZED_FLOOD_ZONE': 6, 'RECOGNIZED_N_CIRCUMSCRIBED_FLOOD_ZONE': 7,
    'RECOGNIZED_N_CIRCUMSCRIBED_WATERSIDE_FLOOD_ZONE': 8
}

# Varsayılan değerler
default_values = {
    'BathroomCount': 0,
    'ConstructionYear': 2000,    
    'MonthlyCharges': 0,
    'PEB': peb_mapping.get('Non-specific', 5),
    'PostalCode': 1000,
    'StateOfBuilding': state_of_building_mapping.get('New', 0),   
    'ToiletCount': 1,
    'TypeOfProperty': type_of_property_mapping.get('House', 0),
    'Kitchen_Numerical': 0,
    'FloodingZone_Numerical': 0,
   
    
}
