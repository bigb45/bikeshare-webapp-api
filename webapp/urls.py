from django.urls import path
from webapp import views


urlpatterns = [

    path('bikeshare/', views.BikeShareDataAPIView.as_view(), name='bikeshare')
]
