from django.urls import path

from . import views

urlpatterns = [
    
    path("land",views.index,name="index"),
    path("login",views.login_view,name="login"),
    path("logout",views.logout_view,name="logout"),
    path("",views.register,name="register"),
    path("user_register",views.user_register,name="user_register"),
    path("employee_register",views.employee_register,name="employee_register"),
    path("skill-update",views.skill_update,name="skill_update"),
    path("skill-delete",views.skill_delete,name="skill_delete"),
    path("exp-update",views.experience_update,name="exp_update"),
    path("job-post",views.job_post,name="job_post"),
    path("profile",views.user_profile,name="profile"),
    path("applied",views.applied_jobs,name="applied"),
    path("apply-for-job",views.apply_for_job,name="apply_for_job"),
    path("<int:job_id>",views.applicants,name="applicants")
    
]