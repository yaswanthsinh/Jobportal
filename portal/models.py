from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class JobSeekerProfile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    experience = models.IntegerField(default=0)
    
    def __str__(self):
        return f"{self.user.first_name}"

class Skill(models.Model):
    name = models.CharField(max_length=64,unique=True)
    job_seeker = models.ForeignKey(JobSeekerProfile,on_delete=models.CASCADE,related_name="skills")

    def __str__(self):
        return f"{self.name}" 
    

class EmployeeProfile(models.Model):
    employee = models.OneToOneField(User,on_delete=models.CASCADE)
    role = models.CharField(max_length=64)
    company_name = models.CharField(max_length=64)
    
    def __str__(self):
        return f"{self.employee.first_name}"
    

class Job(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    location = models.CharField(max_length=64)
    salary = models.IntegerField(help_text='Enter salary in LPA (example: 2.3)')
    employer = models.ForeignKey(EmployeeProfile,on_delete=models.CASCADE, related_name="posts")

    def __str__(self):
        return f"{self.title}"
    
class Application(models.Model):
    job = models.ForeignKey(Job,on_delete=models.CASCADE,related_name="applications")
    seeker = models.ForeignKey(JobSeekerProfile,on_delete=models.CASCADE,related_name="applications")

    class Meta:
        unique_together = ('job','seeker')

    def __str__(self):
        return f"{self.seeker.user.first_name}"
 
   

    



    
    
    
    
    

    
    