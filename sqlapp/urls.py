from django.conf.urls import url
from sqlapp import views

urlpatterns = [
    url(r'^fish/',views.fish),
    url(r'^login/',views.login),
    url(r'^login2/', views.login2),
    url(r'^register/', views.register),
    url(r'^finish/', views.finish),
    url(r'^finish2/', views.finish2),
    # url(r'^message/(.+)/', views.message),
    url(r'^buycom/',views.buycom),
    url(r'^shoppingcar/',views.shoppingcar),
    url(r'^shoppingdel/', views.shoppingdel),
    # url(r'^pay1/',views.pay1),

    url(r'^index2/',views.index2),
    url(r"^pay/$",views.pay),
    url(r"^check_pay/$", views.check_pay),

    url(r'^paysuccess/',views.paysuccess),
    url(r'^buy/(.+)/', views.buy),

    url(r'^insert/$',views.insert),
    url(r'^inserttijiao/$',views.inserttijiao),
    url(r'^upload/$',views.upload),
    url(r'^uploadtijiao/$',views.uploadtijiao),
    url(r'^mycoms/',views.mycoms),
    url(r'^searchcom/',views.searchcom),
    # url(r'^delsession/',views.delsession),
]