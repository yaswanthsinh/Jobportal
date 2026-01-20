from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render
from django.http import HttpResponseRedirect, Http404, JsonResponse
from django.urls import reverse
from .models import Application, JobSeekerProfile, EmployeeProfile, Skill, Job
from django.db.models import Q

# Create your views here.

def index(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    else:

        if hasattr(request.user,"jobseekerprofile"):
            query = request.GET.get("q","").strip()

            seeker = JobSeekerProfile.objects.get(user=request.user)
            jobs = Job.objects.all()

            if query:
                jobs = jobs.filter(
                    Q(title__icontains = query) | Q(location__icontains = query) | Q(employer__company_name__icontains = query)
                )
            

            for job in jobs:
                job.salary = job.salary / 100000

            first = seeker.user.first_name
            last = seeker.user.last_name
           
            return render(request,"portal/user.html",{
                "first":first,
                "last":last,
                "jobs":jobs,
                "query":query
            })
        
        
        employee = EmployeeProfile.objects.get(employee=request.user)
        first = employee.employee.first_name
        last = employee.employee.last_name
        posts = employee.posts.all()
        company = employee.company_name


        for post in posts:
            post.salary = post.salary / 100000

        
        context = {

                "first":first,
                "last":last,
                "posts":posts,
                "company":company
            }

        return render(request,"portal/employee.html",context)

def user_profile(request):


    seeker = JobSeekerProfile.objects.get(user=request.user)

    skills = seeker.skills.all()
    experience = seeker.experience
    first = seeker.user.first_name
            
    return render(request,"portal/seeker.html",{
        "first":first,
        "seeker_skills":skills,
        "experience":experience
    })

    
def login_view(request):
    
    if request.method == "POST":

        username = request.POST["username"].strip()
        password = request.POST["password"].strip()

        user = authenticate(request,username=username,password=password)

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request,"portal/login.html",{
                "message":"Invalid Credentials"
            })
    
    return render(request,"portal/login.html")


def logout_view(request):

    logout(request)
    return render(request,"portal/login.html",{
        "message":"You'r logged out"
    })

def register(request):
    return render(request,"portal/main.html")


def user_register(request):

    if request.method == 'POST':

        first = request.POST["first"].strip()
        last = request.POST["last"].strip()
        username = request.POST["username"].strip()
        password = request.POST["password"].strip()
        email = request.POST["email"].strip()

        user = User.objects.create_user(username=username,email=email,password=password)
        user.first_name = first
        user.last_name = last
        user.save()

        seeker = JobSeekerProfile(user=user)
        seeker.save()

        if user:
            login(request,user)
            return HttpResponseRedirect(reverse("index"))
        else:
            raise Http404("Registration failed")

    return render(request,"portal/user_register.html")

def employee_register(request):

    if request.method == "POST":
        
        first = request.POST["first"].strip()
        last = request.POST["last"].strip()
        username = request.POST["username"].strip()
        email = request.POST["email"].strip()
        password = request.POST["password"].strip()
        company_name = request.POST["company"].strip()
        role = request.POST["role"].strip()

        user = User.objects.create_user(username=username,email=email,password=password)
        user.first_name = first
        user.last_name = last
        user.save()

        employee = EmployeeProfile(employee=user,role=role,company_name=company_name)
        employee.save()

        if employee:
            login(request,user)
            return HttpResponseRedirect(reverse('index'))
        
        else:
            raise Http404("Employee registration failed.")

    return render(request,"portal/employee_register.html")


def skill_update(request):

    if request.method == 'POST':

        skill = request.POST["skills"].strip().title()
       
        seeker = JobSeekerProfile.objects.get(user=request.user)
        j_skill, created = Skill.objects.get_or_create(name=skill,job_seeker=seeker)
        j_skill.save()
        seeker_skills = list(seeker.skills.values("id","name"))

        if not created:
            return JsonResponse({
                "success":False
            })

        return JsonResponse({
            "skills":seeker_skills,
            "success":True
        })
    
def skill_delete(request):

    if request.method == "POST":
        skill_id = int(request.POST["skill_id"])

        seeker = JobSeekerProfile.objects.get(user=request.user)
        Skill.objects.filter(pk=skill_id,job_seeker=seeker).delete()
       
        skills = list(seeker.skills.values("id","name"))

        return JsonResponse({
            "success":True,
            "skills":skills
        })

        


def experience_update(request):

    if request.method == "POST":

        EXPERIENCE = int(request.POST["experience"].strip())
        
        seeker = JobSeekerProfile.objects.get(user=request.user)
        seeker.experience = EXPERIENCE
        seeker.save()

        exp = seeker.experience

        return JsonResponse({
            "experience":exp,
            "status":True
        })

def job_post(request):

    if request.method == "POST":

        title = request.POST["title"]
        location = request.POST["location"]
        salary = request.POST["salary"]
        description = request.POST["description"]

        salary = float(salary) * 100000
        print(salary)

        employer = EmployeeProfile.objects.get(employee=request.user)
        job = Job( 
            title=title,
            description=description,
            location=location,
            salary= salary ,
            employer=employer,
        )
        job.save()
        return HttpResponseRedirect(reverse("index"))


    return render(request,"portal/job_post.html")


def applied_jobs(request):

    seeker = JobSeekerProfile.objects.get(user=request.user)
    applications = seeker.applications.all()

    for application in applications:
        application.job.salary = application.job.salary / 100000
        
    first_name = seeker.user.first_name
    return render(request,"portal/applied_jobs.html",{
        "applications":applications,
        "first":first_name
    })

def apply_for_job(request):

    if request.method == "POST":

        job_id = int(request.POST["job_id"])

        job = Job.objects.get(pk=job_id)
        seeker = JobSeekerProfile.objects.get(user=request.user)

        application, created = Application.objects.get_or_create(seeker=seeker,job=job)
        application.save()

        if not created:
            return JsonResponse({
                "message":"You've already applied for this job",
                "status":False
            })

        return JsonResponse({
            "message":"Application Successfully Submitted",
            "status":True
        })


def applicants(request,job_id):

    job = Job.objects.get(pk=job_id)

    applications = job.applications.all()

    return render(request,"portal/applicants.html",{
        "applicants":applications
    })





            
    
