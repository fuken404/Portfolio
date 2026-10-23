from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register('skills', views.SkillViewSet)
router.register('projects', views.ProjectViewSet, basename='project')
router.register('experience', views.ExperienceViewSet)
router.register('education', views.EducationViewSet)
router.register('certifications', views.CertificationViewSet)

urlpatterns = [
    path('health/', views.health, name='health'),
    path('profile/', views.profile, name='profile'),
    path('contact/', views.ContactCreateView.as_view(), name='contact'),
    path('', include(router.urls)),
]
