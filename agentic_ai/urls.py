"""
URL configuration for agentic_ai project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path

import my_app.views as my_app_views

urlpatterns = [
    path("",my_app_views.home_page,name="home_page"),
    path("search",my_app_views.search_query,name="search"),
    path("ml-modals",my_app_views.answer_from_ML_modals,name="ml_modals"),
    path("predict-crop",my_app_views.predict_crop, name="predict_crop"),
    path('admin/', admin.site.urls),
]
