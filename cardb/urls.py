from django.urls import path
from . import views
from cardb.dash_apps.finished_apps import scatter_plots

urlpatterns = [
	path('', views.home, name='home'),
	path('cars/', views.CarListView.as_view(), name='cars'),
	path('car/<int:pk>', views.CarDetailView.as_view(), name='car-detail'),
]
