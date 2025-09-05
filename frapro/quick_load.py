import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frapro.settings')
django.setup()

from main.models import State, District, ClaimStatistics

# Sample data
data = [
    ("Madhya Pradesh", "Balaghat", 2500, 1800, 400, 200, 100),
    ("Madhya Pradesh", "Chhindwara", 3200, 1600, 1200, 300, 100),
    ("Chhattisgarh", "Bastar", 4500, 1500, 2000, 800, 200),
    ("Odisha", "Kalahandi", 5500, 2500, 2500, 400, 100),
]

print("Loading sample data...")

for state_name, district_name, filed, approved, rejected, under_review, pending in data:
    state, _ = State.objects.get_or_create(name=state_name, defaults={'code': state_name[:3].upper()})
    district, _ = District.objects.get_or_create(name=district_name, state=state, defaults={'code': district_name[:3].upper()})
    
    stats, _ = ClaimStatistics.objects.get_or_create(
        district=district,
        defaults={
            'claims_filed': filed,
            'claims_approved': approved,
            'claims_rejected': rejected,
            'claims_under_review': under_review,
            'claims_pending': pending,
        }
    )
    print(f"✓ Loaded {district_name}, {state_name}")

print("Sample data loaded! Check dashboard now.")