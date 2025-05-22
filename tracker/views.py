from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import JobApplication
from .forms import JobApplicationForm
from django.contrib import messages
from django.http import JsonResponse
from django.utils import timezone
import datetime

# Create your views here.

@login_required
def dashboard(request):
    jobs = JobApplication.objects.filter(user=request.user).order_by('-date_applied')
    # For filter modal options
    all_roles = jobs.values_list('role', flat=True).distinct()
    all_years = jobs.dates('date_applied', 'year').distinct()
    status_choices = ['applied', 'interviewing', 'offer', 'rejected']
    month_choices = [(str(i), '{:02d}'.format(i)) for i in range(1, 13)]
    # Get filter params
    roles = request.GET.getlist('role')
    statuses = request.GET.getlist('status')
    month = request.GET.get('month', '').strip()
    year = request.GET.get('year', '').strip()
    # Filtering
    if roles:
        jobs = jobs.filter(role__in=roles)
    if statuses:
        jobs = jobs.filter(status__in=statuses)
    # Only apply date filters if both month and year are provided, or just year
    if month and year:
        jobs = jobs.filter(date_applied__year=year, date_applied__month=month)
    elif year:
        jobs = jobs.filter(date_applied__year=year)
    # If neither month nor year is provided, show all applications
    add_form = JobApplicationForm()
    edit_form = None
    edit_job_id = None
    today_date = datetime.date.today().isoformat()
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        if 'delete_job_id' in request.POST:
            # AJAX delete
            job_id = request.POST.get('delete_job_id')
            job = get_object_or_404(JobApplication, id=job_id, user=request.user)
            job.delete()
            return JsonResponse({'success': True, 'job_id': job_id})
        elif 'job_id' in request.POST:
            # AJAX edit
            job_id = request.POST.get('job_id')
            job = get_object_or_404(JobApplication, id=job_id, user=request.user)
            edit_form = JobApplicationForm(request.POST, instance=job)
            if edit_form.is_valid():
                job = edit_form.save()
                return JsonResponse({'success': True, 'job': {
                    'id': job.id,
                    'role': job.role,
                    'company': job.company,
                    'date_applied': job.date_applied.strftime('%Y-%m-%d'),
                    'status': job.status,
                    'job_url': job.job_url or '',
                    'notes': job.notes or '',
                    'status_display': job.get_status_display(),
                }})
            else:
                return JsonResponse({'success': False, 'errors': edit_form.errors}, status=400)
        else:
            # AJAX add
            add_form = JobApplicationForm(request.POST)
            if add_form.is_valid():
                job = add_form.save(commit=False)
                job.user = request.user
                job.save()
                return JsonResponse({'success': True, 'job': {
                    'id': job.id,
                    'role': job.role,
                    'company': job.company,
                    'date_applied': job.date_applied.strftime('%Y-%m-%d'),
                    'status': job.status,
                    'job_url': job.job_url or '',
                    'notes': job.notes or '',
                    'status_display': job.get_status_display(),
                }})
            else:
                return JsonResponse({'success': False, 'errors': add_form.errors}, status=400)
    # GET or non-AJAX POST
    return render(request, 'tracker/dashboard.html', {
        'jobs': jobs,
        'add_form': add_form,
        'edit_form': edit_form,
        'edit_job_id': edit_job_id,
        'today_date': today_date,
        'all_roles': all_roles,
        'all_years': all_years,
        'status_choices': status_choices,
        'month_choices': month_choices,
        'filter_roles': roles,
        'filter_statuses': statuses,
        'filter_month': month,
        'filter_year': year,
    })

@login_required
def get_month_stats(request):
    year = request.GET.get('year')
    month = request.GET.get('month')
    if year and month:
        count = JobApplication.objects.filter(
            user=request.user,
            date_applied__year=int(year),
            date_applied__month=int(month)
        ).count()
    else:
        count = JobApplication.objects.get_month_stats()
    return JsonResponse({'count': count})

@login_required
def get_stats(request):
    jobs = JobApplication.objects.filter(user=request.user)
    return JsonResponse({
        'total': jobs.count(),
        'active': jobs.get_total_active(),
        'offers': jobs.get_total_offers(),
        'current_month': jobs.get_month_stats()
    })

@login_required
def profile_stats(request):
    user = request.user
    return JsonResponse({
        'total': user.jobapplication_set.count(),
        'monthly': user.jobapplication_set.get_month_stats(),
        'active': user.jobapplication_set.get_total_active(),
        'offers': user.jobapplication_set.get_total_offers(),
    })
