from django.urls import path
from . import views

urlpatterns = [
    # path('hello/', update_forcast_data.HelloWorld.as_view(), name='hello_world'),
    path('update_forcast_data/', views.UpdateForcastData.as_view(), name='update_forcast_data'),
    path('get_average_temperature/', views.GetLowestAverageTemperatures.as_view(), name='get_average_temperature'),
    path('compare_temperature/', views.CompareTemperature.as_view(), name='compare_temperature'),
    
]