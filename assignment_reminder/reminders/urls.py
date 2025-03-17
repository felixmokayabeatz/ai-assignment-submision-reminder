from django.urls import path, include
from .views import assignment_list, submit_assignment, submit_assignment, home, enroll, enroll_course, get_course_for_unit, chat_ai
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
    
    

    path('get_course_for_unit/<int:unit_id>/', get_course_for_unit, name='get_course_for_unit'),
    
    path("chat-ai/", chat_ai, name="chat-ai"),
]
