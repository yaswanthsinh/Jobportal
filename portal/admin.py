from django.contrib import admin 
from .models import EmployeeProfile, Job, JobSeekerProfile

# Register your models here.

admin.site.register(EmployeeProfile)
admin.site.register(JobSeekerProfile)
admin.site.register(Job)
