from django.urls import path
from . import views   

app_name = 'edm_calibration'

urlpatterns = [
    path('', views.edm_calibration_home, name = 'edm_calibration_home'),
    path('calibrate1/<slug:id>', views.calibrate1, name = 'calibrate1'),
    path('calibrate2/', views.calibrate2, name = 'calibrate2'),
    path('calibrate3/', views.calibrate3, name = 'calibrate3'),
    path('clear_cache/', views.clear_cache, name='clear_cache'),
    path('calibrate/', views.calibrate, name = 'calibrate'),
    path('guide_form/', views.guide_form, name='guide_form'),
    path('step_by_step_guide/', views.step_by_step_guide, name='step_by_step_guide'),
    
]