from django.urls import path, include
from .views import assignment_list, submit_assignment, submit_assignment, home, enroll, enroll_course
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('', home, name='home'),
    path("assignments/", assignment_list, name="assignment_list"),
    path("enroll-course/", enroll_course, name="enroll-course"),
    path('enroll/<int:course_id>/', enroll, name='enroll'),
     
    path("submit/<int:assignment_id>/", submit_assignment, name="submit_assignment"),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),
    path("accounts/", include("django.contrib.auth.urls")),
    
    
    path("enroll/<int:course_id>", enroll_course, name="course_detail"),
]
