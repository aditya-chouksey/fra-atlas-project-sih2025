import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frapro.settings')
django.setup()

from main.models import State, District

def load_simple_geometries():
    """Load district geometries as JSON text (not PostGIS geometry)"""
    
    geojson_file = "sample_districts.geojson"
    
    if not os.path.exists(geojson_file):
        print(f"GeoJSON file not found: {geojson_file}")
        return
    
    print(f"Loading geometries from {geojson_file}...")
    
    with open(geojson_file, 'r', encoding='utf-8') as f:
        geojson_data = json.load(f)
    
    features = geojson_data.get('features', [])
    
    for feature in features:
        properties = feature.get('properties', {})
        geometry = feature.get('geometry')
        
        state_name = properties.get('state')
        district_name = properties.get('district')
        
        if not state_name or not district_name or not geometry:
            continue
        
        try:
            # Find the district in database
            district = District.objects.filter(
                name__iexact=district_name,
                state__name__iexact=state_name
            ).first()
            
            if district:
                # Store geometry as JSON text in location field for now
                district.location = json.dumps(geometry)
                district.save()
                print(f"Updated location data for {district_name}, {state_name}")
            else:
                print(f"District not found: {district_name}, {state_name}")
                
        except Exception as e:
            print(f"Error processing {district_name}, {state_name}: {e}")
    
    print("Geometry loading completed!")

if __name__ == "__main__":
    load_simple_geometries()