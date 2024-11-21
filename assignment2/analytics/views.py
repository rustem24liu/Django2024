
from django.db.models import Count
from django.shortcuts import render
from analytics.models import APIRequestLog

def get_usage_metrics(request):
    total_requests_per_user = (
        APIRequestLog.objects.values('user__username')
        .annotate(request_count=Count('id'))
        .order_by('-request_count')
    )

    most_active_users = total_requests_per_user[:5]

    context = {
        'total_requests_per_user': total_requests_per_user,
        'most_active_users': most_active_users,
    }
    return render(request, 'analytics/metrics.html', context)
