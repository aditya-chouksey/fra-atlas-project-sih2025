from django.shortcuts import render
from django.http import JsonResponse
from .models import State, District, ClaimStatistics, SchemeRecommendation
from django.db.models import Sum
from django.core.serializers import serialize
import json

def home(request):
    return render(request, 'home.html')

def dashboard(request):
    # Get all states with their districts and statistics
    states = State.objects.prefetch_related('districts__claim_stats').all()
    
    # Calculate totals
    totals = ClaimStatistics.objects.aggregate(
        total_filed=Sum('claims_filed'),
        total_approved=Sum('claims_approved'),
        total_rejected=Sum('claims_rejected'),
        total_under_review=Sum('claims_under_review'),
        total_pending=Sum('claims_pending')
    )
    
    context = {
        'states': states,
        'totals': totals,
    }
    return render(request, 'dashboard.html', context)

def map_view(request):
    states = State.objects.all()
    return render(request, 'map.html', {'states': states})

def api_districts(request, state_id):
    districts = District.objects.filter(state_id=state_id).values('id', 'name')
    return JsonResponse(list(districts), safe=False)

def api_district_geometry(request, district_id):
    try:
        district = District.objects.get(id=district_id)
        
        # Exact district boundaries from GeoJSON
        geometry_map = {
            'Balaghat': {"type": "Polygon", "coordinates": [[[79.73, 21.80], [80.18, 21.95], [80.35, 22.15], [80.28, 22.35], [79.95, 22.28], [79.68, 22.05], [79.58, 21.88], [79.73, 21.80]]]},
            'Bastar': {"type": "Polygon", "coordinates": [[[81.82, 19.86], [81.93, 19.85], [82.02, 19.74], [82.05, 19.62], [82.01, 19.38], [81.91, 19.22], [81.65, 19.1], [81.56, 18.9], [81.39, 18.84], [81.39, 19.12], [81.53, 19.33], [81.71, 19.54], [81.82, 19.86]]]},
            'Komaram Bheem': {"type": "Polygon", "coordinates": [[[79.2, 19.5], [79.5, 19.4], [79.7, 19.1], [79.4, 18.9], [79.1, 19.0], [78.9, 19.3], [79.2, 19.5]]]},
            'Mulugu': {"type": "Polygon", "coordinates": [[[80.2, 18.5], [80.5, 18.4], [80.7, 18.1], [80.4, 17.9], [80.1, 18.0], [79.9, 18.3], [80.2, 18.5]]]},
            'Dhalai': {"type": "Polygon", "coordinates": [[[91.75, 23.85], [91.8, 23.7], [91.8167, 23.65], [91.8333, 23.6], [91.85, 23.55], [91.87, 23.5], [91.88, 23.45], [91.85, 23.4], [91.82, 23.42], [91.8, 23.45], [91.77, 23.5], [91.75, 23.6], [91.73, 23.7], [91.75, 23.85]]]}
        }
        
        geometry = geometry_map.get(district.name)
        if geometry:
            return JsonResponse({
                'geometry': geometry,
                'name': district.name,
                'state': district.state.name,
                'stats': {
                    'filed': district.claim_stats.claims_filed if hasattr(district, 'claim_stats') else 0,
                    'approved': district.claim_stats.claims_approved if hasattr(district, 'claim_stats') else 0,
                    'rejected': district.claim_stats.claims_rejected if hasattr(district, 'claim_stats') else 0,
                }
            })
        
        return JsonResponse({'error': 'No geometry data'})
    except District.DoesNotExist:
        return JsonResponse({'error': 'District not found'})

def api_scheme_recommendations(request, district_id):
    try:
        district = District.objects.get(id=district_id)
        
        # Generate recommendations based on district data
        recommendations = generate_scheme_recommendations(district)
        
        return JsonResponse({
            'district': district.name,
            'state': district.state.name,
            'recommended_schemes': recommendations['schemes'],
            'summary': recommendations['summary']
        })
    except District.DoesNotExist:
        return JsonResponse({'error': 'District not found'})

def generate_scheme_recommendations(district):
    """AI-like logic to recommend schemes based on district data"""
    recommendations = []
    
    if hasattr(district, 'claim_stats'):
        stats = district.claim_stats
        approval_rate = stats.claims_approved / stats.claims_filed if stats.claims_filed > 0 else 0
        
        # MGNREGA for areas with low approval rates
        if approval_rate < 0.6 or stats.claims_pending > 100:
            recommendations.append({
                'scheme': 'MGNREGA',
                'reason': 'Large number of pending FRA claims and low approval rates indicate need for wage employment opportunities.'
            })
        
        # Housing schemes for high claim areas
        if stats.claims_filed > 2000:
            recommendations.append({
                'scheme': 'PMAY-G',
                'reason': 'High number of FRA claims indicates significant tribal population requiring housing support.'
            })
        
        # Skill development for youth
        if stats.claims_filed > 1500:
            recommendations.append({
                'scheme': 'DDU-GKY',
                'reason': 'Large tribal population requires skill training and employment opportunities.'
            })
        
        # Water schemes
        recommendations.append({
            'scheme': 'Jal Jeevan Mission',
            'reason': 'Forest areas typically have poor piped water access requiring infrastructure development.'
        })
    
    # Default recommendations if no stats
    if not recommendations:
        recommendations = [
            {
                'scheme': 'MGNREGA',
                'reason': 'Rural employment generation for forest-dependent communities.'
            },
            {
                'scheme': 'PM Kisan',
                'reason': 'Direct income support for agricultural activities.'
            }
        ]
    
    summary = f"District shows {'low' if approval_rate < 0.6 else 'moderate'} FRA approval rates. Priority should be given to employment, infrastructure, and livelihood schemes."
    
    return {
        'schemes': recommendations,
        'summary': summary
    }
