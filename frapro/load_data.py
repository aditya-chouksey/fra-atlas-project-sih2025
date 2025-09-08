import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'frapro.settings')
django.setup()

from main.models import State, District, ClaimStatistics

# Data to load
data = [
    ("Madhya Pradesh", "Balaghat", 2500, 1800, 400, 200, 100),
    ("Madhya Pradesh", "Chhindwara", 3200, 1600, 1200, 300, 100),
    ("Madhya Pradesh", "Dindori", 1800, 1500, 150, 100, 50),
    ("Madhya Pradesh", "Mandla", 2100, 900, 800, 300, 100),
    ("Madhya Pradesh", "Shahdol", 1500, 1250, 100, 100, 50),
    ("Madhya Pradesh", "Sheopur", 800, 200, 500, 50, 50),
    ("Chhattisgarh", "Bastar", 4500, 1500, 2000, 800, 200),
    ("Chhattisgarh", "Dantewada", 3000, 2200, 400, 300, 100),
    ("Chhattisgarh", "Kanker", 2800, 2100, 350, 250, 100),
    ("Chhattisgarh", "Korba", 3500, 1200, 1800, 400, 100),
    ("Chhattisgarh", "Raigarh", 1900, 1600, 100, 150, 50),
    ("Chhattisgarh", "Sukma", 2200, 1850, 150, 100, 100),
    ("Odisha", "Kalahandi", 5500, 2500, 2500, 400, 100),
    ("Odisha", "Kandhamal", 4800, 3800, 500, 300, 200),
    ("Odisha", "Koraput", 6200, 5500, 400, 200, 100),
    ("Odisha", "Malkangiri", 3100, 1100, 1500, 400, 100),
    ("Odisha", "Mayurbhanj", 7500, 6800, 300, 250, 150),
    ("Odisha", "Sundargarh", 4300, 3200, 600, 400, 100),
    ("Telangana", "Adilabad", 3800, 3100, 400, 200, 100),
    ("Telangana", "Bhadradri Kothagudem", 4100, 1800, 1900, 300, 100),
    ("Telangana", "Jayashankar Bhupalpally", 2900, 2400, 200, 200, 100),
    ("Telangana", "Komaram Bheem", 2500, 1200, 1000, 200, 100),
    ("Telangana", "Mulugu", 1800, 1550, 100, 100, 50),
]

print("Loading FRA data...")

for state_name, district_name, filed, approved, rejected, under_review, pending in data:
    # Create or get state
    state, created = State.objects.get_or_create(
        name=state_name,
        defaults={'code': state_name[:3].upper()}
    )
    if created:
        print(f"Created state: {state_name}")
    
    # Create or get district
    district, created = District.objects.get_or_create(
        name=district_name,
        state=state,
        defaults={'code': district_name[:3].upper()}
    )
    if created:
        print(f"Created district: {district_name}")
    
    # Create or update claim statistics
    stats, created = ClaimStatistics.objects.get_or_create(
        district=district,
        defaults={
            'claims_filed': filed,
            'claims_approved': approved,
            'claims_rejected': rejected,
            'claims_under_review': under_review,
            'claims_pending': pending,
        }
    )
    if not created:
        stats.claims_filed = filed
        stats.claims_approved = approved
        stats.claims_rejected = rejected
        stats.claims_under_review = under_review
        stats.claims_pending = pending
        stats.save()
    
    print(f"Loaded data for {district_name}, {state_name}")

# Add Tripura state and districts
tripura_districts = [
    ("Tripura", "Dhalai", 2550, 520, 1180, 200, 650),
    ("Tripura", "Gomati", 1820, 1350, 210, 50, 210),
    ("Tripura", "Khowai", 2200, 840, 310, 300, 750),
    ("Tripura", "North Tripura", 3150, 1680, 720, 200, 550),
    ("Tripura", "Sepahijala", 1230, 760, 160, 100, 210),
    ("Tripura", "South Tripura", 2890, 1150, 440, 350, 950),
    ("Tripura", "Unakoti", 950, 610, 110, 50, 180),
    ("Tripura", "West Tripura", 3510, 1950, 820, 300, 440),
]

for state_name, district_name, filed, approved, rejected, under_review, pending in tripura_districts:
    state, created = State.objects.get_or_create(
        name=state_name,
        defaults={'code': 'TR'}
    )
    if created:
        print(f"Created state: {state_name}")
    
    district, created = District.objects.get_or_create(
        name=district_name,
        state=state,
        defaults={'code': district_name[:3].upper()}
    )
    if created:
        print(f"Created district: {district_name}")
    
    stats, created = ClaimStatistics.objects.get_or_create(
        district=district,
        defaults={
            'claims_filed': filed,
            'claims_approved': approved,
            'claims_rejected': rejected,
            'claims_under_review': under_review,
            'claims_pending': pending,
        }
    )
    if not created:
        stats.claims_filed = filed
        stats.claims_approved = approved
        stats.claims_rejected = rejected
        stats.claims_under_review = under_review
        stats.claims_pending = pending
        stats.save()
    
    print(f"Loaded data for {district_name}, {state_name}")

print("Data loading completed!")
print(f"Total states: {State.objects.count()}")
print(f"Total districts: {District.objects.count()}")