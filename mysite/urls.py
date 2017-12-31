"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
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
# also import the "include" module in the django.conf.urls
from django.conf.urls import include, url

from django.contrib import admin

# imports Django's login and logout views
from django.contrib.auth import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),

    # added a URL na galing sa blog app na imported login_required, it needs this.
    url(r'^accounts/login/$', views.login, name='login'),


    url(r'^accounts/logout/$', views.logout, name='logout', kwargs={'next_page': '/'}),
    # all urls will be presented here na nandun lahat sa blog/urls.py, maiinherit dito, because of the import module

    # and the include() function

    # not sure as to why pinagpapasa pasahan pa, para daw malinis (???) needs more studying

    # as for r'', it means "everything na pupunta sa 127.0.0.1 as is will be redirected lahat sa blog na django app."

    # it also means kung r'^blog/$' sana yan, dun mapupunta. hindi sa HUBAD na 127.0.0.1
    url(r'', include('blog.urls')),
]
