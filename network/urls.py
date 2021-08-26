from django.urls import path
from django.views.generic import TemplateView

app_name = 'network'

urlpatterns = [
    path('home/', TemplateView.as_view(template_name='home.html')),
]