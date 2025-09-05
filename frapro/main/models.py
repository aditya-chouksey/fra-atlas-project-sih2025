from django.db import models
from django.contrib.auth.models import User
from django.contrib.gis.db import models as gis_models

# Administrative Drawer - States and Districts
class State(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=10, unique=True)
    location = models.CharField(max_length=300, blank=True)
    geometry = gis_models.PolygonField(help_text="State boundary", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class District(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=10)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='districts')
    location = models.CharField(max_length=300, blank=True)
    geometry = gis_models.PolygonField(help_text="District boundary", null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['name', 'state']
    
    def __str__(self):
        return f"{self.name}, {self.state.name}"

# Performance Drawer - FRA Claim Statistics
class ClaimStatistics(models.Model):
    district = models.OneToOneField(District, on_delete=models.CASCADE, related_name='claim_stats')
    claims_filed = models.PositiveIntegerField(default=0)
    claims_approved = models.PositiveIntegerField(default=0)
    claims_rejected = models.PositiveIntegerField(default=0)
    claims_under_review = models.PositiveIntegerField(default=0)
    claims_pending = models.PositiveIntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.district.name} - {self.claims_filed} claims"

class FRAClaim(models.Model):
    CLAIM_STATUS = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
        ('under_review', 'Under Review'),
    ]
    
    claim_number = models.CharField(max_length=50, unique=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='fra_claims')
    status = models.CharField(max_length=20, choices=CLAIM_STATUS, default='pending')
    location = models.CharField(max_length=300, blank=True)
    geometry = gis_models.PolygonField(help_text="Claimed land boundary", null=True, blank=True)
    area_claimed = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    date_submitted = models.DateTimeField(auto_now_add=True)
    date_processed = models.DateTimeField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.claim_number} - {self.district.name}"

# Asset Drawer - Spatial Assets
class Asset(gis_models.Model):
    ASSET_TYPES = [
        ('water_bodies', 'Water Bodies'),
        ('forest_cover', 'Forest Cover'),
        ('agricultural_land', 'Agricultural Land'),
        ('homesteads', 'Homesteads'),
    ]
    
    name = models.CharField(max_length=200)
    asset_type = models.CharField(max_length=20, choices=ASSET_TYPES)
    location = models.CharField(max_length=300, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='assets', null=True, blank=True)
    geometry = gis_models.PolygonField(help_text="Spatial boundary of the asset", null=True, blank=True)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    identified_by_ai = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.get_asset_type_display()}"

# Beneficiary Drawer - Patta Holders
class PattaHolder(models.Model):
    GENDER_CHOICES = [
        ('M', 'Male'),
        ('F', 'Female'),
        ('O', 'Other'),
    ]
    
    name = models.CharField(max_length=200)
    father_name = models.CharField(max_length=200)
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES)
    age = models.PositiveIntegerField()
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField()
    location = models.CharField(max_length=300, blank=True)
    geometry = gis_models.PointField(help_text="Patta holder location", null=True, blank=True)
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='patta_holders')
    fra_claim = models.ForeignKey(FRAClaim, on_delete=models.CASCADE, related_name='patta_holders')
    patta_number = models.CharField(max_length=50, unique=True)
    land_area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Land area in acres")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.name} - {self.patta_number}"

# Scheme Recommendation System
class SchemeRecommendation(models.Model):
    SCHEMES = [
        ('MGNREGA', 'Mahatma Gandhi National Rural Employment Guarantee Act'),
        ('JAL_JEEVAN', 'Jal Jeevan Mission'),
        ('PMAY_G', 'Pradhan Mantri Awas Yojana - Gramin'),
        ('DDU_GKY', 'Deen Dayal Upadhyaya Grameen Kaushalya Yojana'),
        ('PM_KISAN', 'PM Kisan Samman Nidhi'),
        ('SWACHH_BHARAT', 'Swachh Bharat Mission'),
    ]
    
    district = models.ForeignKey(District, on_delete=models.CASCADE, related_name='scheme_recommendations')
    scheme = models.CharField(max_length=20, choices=SCHEMES)
    reason = models.TextField()
    priority_score = models.IntegerField(default=1, help_text="1-5 priority score")
    generated_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['district', 'scheme']
    
    def __str__(self):
        return f"{self.district.name} - {self.get_scheme_display()}"
