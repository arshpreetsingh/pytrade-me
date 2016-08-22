"""pypolo URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add an import:  from blog import urls as blog_urls
    2. Import the include() function: from django.conf.urls import url, include
    3. Add a URL to urlpatterns:  url(r'^blog/', include(blog_urls))
"""
from django.conf.urls import url
from django.contrib import admin
from history.views import nn_chart_view, profit_view, optimize_view, c_chart_view,start_trade,buy_sell

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^admin/buy_sell', buy_sell),
    url(r'^admin/nn_charts', nn_chart_view),
    url(r'^admin/c_charts', c_chart_view),
    url(r'^admin/profit', profit_view),
    url(r'^admin/optimize', optimize_view),
    url(r'^start_trade', start_trade),
]
