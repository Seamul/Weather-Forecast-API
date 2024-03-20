from django.urls import path
from . import views

urlpatterns = [
    # path('hello/', update_forcast_data.HelloWorld.as_view(), name='hello_world'),
    path('update_forcast_data/', views.UpdateForcastData.as_view(), name='update_forcast_data'),
    
    
]