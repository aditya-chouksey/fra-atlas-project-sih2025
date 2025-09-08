import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frapro.settings')
django.setup()

from main.models import District

# Simple geometry data for districts
geometry_data = {
    "Balaghat": {
        "type": "Polygon",
        "coordinates": [[[79.5, 21.5], [80.5, 21.5], [80.5, 22.5], [79.5, 22.5], [79.5, 21.5]]]
    },
    "Bastar": {
        "type": "Polygon", 
        "coordinates": [[[81.0, 19.0], [82.0, 19.0], [82.0, 20.0], [81.0, 20.0], [81.0, 19.0]]]
    },
    "Komaram Bheem": {
        "type": "Polygon",
        "coordinates": [[[78.5, 19.0], [79.5, 19.0], [79.5, 20.0], [78.5, 20.0], [78.5, 19.0]]]
    }
    
}

print("Loading geometry data...")

for district_name, geometry in geometry_data.items():
    try:
        district = District.objects.get(name=district_name)
        district.geometry = json.dumps(geometry)
        district.save()
        print(f"Added geometry for {district_name}")
    except District.DoesNotExist:
        print(f"District {district_name} not found")

print("Geometry loading completed!")