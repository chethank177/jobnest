from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Count

class JobApplicationManager(models.Manager):
    def get_month_stats(self, year=None, month=None):
        if year is None or month is None:
            today = timezone.now()
            year = today.year
            month = today.month
        return self.filter(date_applied__year=year, date_applied__month=month).count()

    def get_status_counts(self):
        return self.values('status').annotate(count=Count('id'))

    def get_available_months(self):
        dates = self.dates('date_applied', 'month', order='DESC')
        return [(d.year, d.month, d.strftime('%B %Y')) for d in dates]

    def get_total_active(self):
        """Returns count of applications that are either in applied or interviewing status"""
        return self.filter(status__in=['applied', 'interviewing']).count()

    def get_total_offers(self):
        """Returns count of applications with offer status"""
        return self.filter(status='offer').count()

    def get_total_rejected(self):
        """Returns count of applications with rejected status"""
        return self.filter(status='rejected').count()

    def this_month(self):
        today = timezone.now()
        return self.filter(date_applied__year=today.year, date_applied__month=today.month)

    def status(self, status_type):
        return self.filter(status=status_type)

class JobApplication(models.Model):
    APPLIED = 'applied'
    INTERVIEWING = 'interviewing'
    OFFER = 'offer'
    REJECTED = 'rejected'
    STATUS_CHOICES = [
        (APPLIED, 'Applied'),
        (INTERVIEWING, 'Interviewing'),
        (OFFER, 'Offer'),
        (REJECTED, 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=200)
    company = models.CharField(max_length=200)
    date_applied = models.DateField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=APPLIED)
    job_url = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    objects = JobApplicationManager()

    def __str__(self):
        return f"{self.role} at {self.company}"

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    class Meta:
        ordering = ['-date_applied']
