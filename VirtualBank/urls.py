from django.conf.urls import patterns, url

#from django.contrib import admin
#admin.autodiscover()

from myBank import views

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'VirtualBank.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    #url(r'^admin/', include(admin.site.urls)),
    url(r'css/(?P<path>.*)','django.views.static.serve',{'document_root':'./myBank/TEMPLATE/css'}),
    url(r'script/(?P<path>.*)','django.views.static.serve',{'document_root':'./myBank/TEMPLATE/script'}),
    url(r'js/(?P<path>.*)','django.views.static.serve',{'document_root':'./myBank/TEMPLATE/js'}),
    url(r'images/(?P<path>.*)','django.views.static.serve',{'document_root':'./myBank/TEMPLATE/images'}),
    #url(r'^captcha/', include('captcha.urls')),
    #url(r'^getcheckcodeimage/$', views.get_check_code_image),
    url(r'^$', views.homepage),
    url(r'^register/$', views.register),
    url(r'^activation/([^/]+)/$', views.activation),
    url(r'^login/$', views.login),
    url(r'^logout/$', views.logout),
    url(r'^querybalance/$', views.querybalance),
    url(r'^querybill/$', views.querybill),
    url(r'^payset/$', views.payset),
    url(r'^payset/set-password/$', views.setpassword),
    url(r'^payset/set-payword/$', views.setpayword),
    url(r'^myaccount/$', views.myaccount),
    url(r'^transfer/$', views.transfer),
    url(r'^saveorwithdrew/$', views.saveorwithdrew),
    url(r'^saveorwithdrew/save/$', views.saveorwithdrew_save),
    url(r'^saveorwithdrew/withdraw/$', views.saveorwithdraw_withdrew),
    url(r'^newmessage/$', views.newmessage),
    url(r'^cashierdesk/([^/]+)/$', views.cashierdesk),
    url(r'^test/$', views.test),
)