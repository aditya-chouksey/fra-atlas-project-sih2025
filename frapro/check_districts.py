import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frapro.settings')
django.setup()

from main.models import District

print("Available districts:")
for district in District.objects.all():
    print(f"- {district.name} (State: {district.state.name})")
    print(f"  Geometry: {district.geometry}")
    print()