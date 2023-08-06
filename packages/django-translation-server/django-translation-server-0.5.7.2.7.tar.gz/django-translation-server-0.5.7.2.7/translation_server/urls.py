"""django_simepar_translation_server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from translation_server.views import *
from rest_framework import routers

router = routers.DefaultRouter()
router.register(r'translation', TranslationViewSet, 'translations')
router.register(r'translation_type', TranslationTypeViewSet, 'translations_types')

urlpatterns = [
    url(r'^api/last_translation_tag/(?P<tag>\w+)[/]?$', LastTranslationTagView.as_view(),
        name='get_last_translation_tag'),
]
