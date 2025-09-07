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
        if district.geometry:
            try:
                geometry = json.loads(district.geometry)
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
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Invalid geometry data'})
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
