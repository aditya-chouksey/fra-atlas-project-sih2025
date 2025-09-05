from django.contrib import admin
from .models import State, District, ClaimStatistics, FRAClaim, Asset, PattaHolder, SchemeRecommendation

admin.site.register(State)
admin.site.register(District)
admin.site.register(ClaimStatistics)
admin.site.register(FRAClaim)
admin.site.register(Asset)
admin.site.register(PattaHolder)
admin.site.register(SchemeRecommendation)
