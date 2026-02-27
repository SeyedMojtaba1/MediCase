"""
URL configuration for MediCaseBack project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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
from django.urls import include, path
from rest_framework.routers import DefaultRouter
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView
from django.conf import settings
from django.conf.urls.static import static

router = DefaultRouter()

urlpatterns = [
    path('admin/', admin.site.urls),
    path("api/registery/", include(router.urls)),
    path("api/registery/", include("registery.urls")),
    path("api/university/", include(router.urls)),
    path("api/university/", include("university.urls")),
    path("api/class/", include(router.urls)),
    path("api/class/", include("classroom.urls")),
    path("api/pulmonologyscenario/", include("pulmonology_scenario.urls")),
    path("api/tutorial/", include("tutorial.urls")),
    path("api/notification/", include("notification.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/schema/docs/", SpectacularSwaggerView.as_view(url_name="schema")),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
