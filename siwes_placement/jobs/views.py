from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.core.paginator import Paginator
from .models import Job, Company, Application
from .forms import JobForm, CompanyForm, ApplicationForm

def job_list(request):
    jobs = Job.objects.filter(is_active=True)
    search_query = request.GET.get('search')
    location_filter = request.GET.get('location')
    company_filter = request.GET.get('company')
    
    if search_query:
        jobs = jobs.filter(title__icontains=search_query)
    if location_filter:
        jobs = jobs.filter(location__icontains=location_filter)
    if company_filter:
        jobs = jobs.filter(company__name__icontains=company_filter)
    
    paginator = Paginator(jobs, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    return render(request, 'jobs/job_list.html', {
        'page_obj': page_obj,
        'search_query': search_query,
        'location_filter': location_filter,
        'company_filter': company_filter,
    })

def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    has_applied = False
    if request.user.is_authenticated:
        has_applied = Application.objects.filter(job=job, student=request.user).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'has_applied': has_applied})

@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, is_active=True)
    
    # Check if already applied
    if Application.objects.filter(job=job, student=request.user).exists():
        messages.warning(request, 'You have already applied for this job.')
        return redirect('job_detail', pk=pk)
    
    if request.method == 'POST':
        form = ApplicationForm(request.POST, request.FILES)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job
            application.student = request.user
            application.save()
            
            # Send email to company
            try:
                subject = f'New SIWES Application: {job.title}'
                message = f'''
Dear {job.company.name},

A new SIWES application has been received for the position: {job.title}

Student Details:
- Name: {request.user.get_full_name()}
- Email: {request.user.email}
- Institution: {request.user.institution}
- Course: {request.user.course_of_study}
- Year: {request.user.year_of_study}
- Phone: {request.user.phone_number}

Cover Letter:
{application.cover_letter}

Please find the student's resume attached or contact them directly.

Best regards,
SIWES Placement System
                '''
                
                send_mail(
                    subject,
                    message,
                    settings.EMAIL_HOST_USER,
                    [job.company.email],
                    fail_silently=False,
                )
                
                application.status = 'sent'
                application.save()
                messages.success(request, 'Your application has been sent to the company!')
                
            except Exception as e:
                messages.error(request, 'Application saved but email could not be sent. Please contact admin.')
            
            return redirect('job_detail', pk=pk)
    else:
        form = ApplicationForm()
    
    return render(request, 'jobs/apply_job.html', {'form': form, 'job': job})

@login_required
def my_applications(request):
    applications = Application.objects.filter(student=request.user).order_by('-applied_at')
    return render(request, 'jobs/my_applications.html', {'applications': applications})

@staff_member_required
def admin_dashboard(request):
    jobs_count = Job.objects.count()
    applications_count = Application.objects.count()
    companies_count = Company.objects.count()
    active_jobs = Job.objects.filter(is_active=True).count()
    
    context = {
        'jobs_count': jobs_count,
        'applications_count': applications_count,
        'companies_count': companies_count,
        'active_jobs': active_jobs,
    }
    return render(request, 'jobs/admin_dashboard.html', context)

@staff_member_required
def add_company(request):
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Company added successfully!')
            return redirect('admin_dashboard')
    else:
        form = CompanyForm()
    return render(request, 'jobs/add_company.html', {'form': form})

@staff_member_required
def add_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.created_by = request.user
            job.save()
            messages.success(request, 'Job posted successfully!')
            return redirect('admin_dashboard')
    else:
        form = JobForm()
    return render(request, 'jobs/add_job.html', {'form': form})

@staff_member_required
def manage_jobs(request):
    jobs = Job.objects.all().order_by('-created_at')
    return render(request, 'jobs/manage_jobs.html', {'jobs': jobs})

@staff_member_required
def toggle_job_status(request, pk):
    job = get_object_or_404(Job, pk=pk)
    job.is_active = not job.is_active
    job.save()
    status = "activated" if job.is_active else "deactivated"
    messages.success(request, f'Job {status} successfully!')
    return redirect('manage_jobs')