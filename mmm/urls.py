from django.urls import path,re_path
from . import views

app_name = 'mmm'

urlpatterns = [
    # web #
    path('', views.home, name='home'),
    path('entry/', views.entry, name='entry'), 
    path('register/', views.register, name='register'),
    path('logout/', views.userlogout, name='logout'),

    # Module: service advisor
    # path('service/', views.service,name='service'), # change service advisor name and password
    path('service/project',views.showProject,name='project'),
    path('service/entrust',views.entrust,name='entrust'),
    path('service/entrust_details',views.entrust_details,name='entrust_details'),
    
    # function
    path('service/entrust_pay',views.entrust_pay,name='entrust_pay'),
    path('service/entrust_delete',views.entrust_delete,name='entrust_delete'),
    path('service/get_phones/',views.get_phones,name='get_phones'),

    # Module: repair manager
    path('repair_manage/', views.manageIndex,name='repair_manager'),
    path('repair_manage/work',views.manageTask,name='manageTask'),
    path('repair_manage/check_cost',views.check_cost,name='check_cost'),
    
    # Wechat applet backend
    # Module: user
    path('user_login/',views.user_login,name="user_login"),
    path('user_managephone/',views.user_managephone,name='user_managephone'),
    path('user_commission/',views.commission,name='user_commission'),
    path('user_progressquery/',views.progressquery,name='user_progressquery'),
    path('user_commissionhistory/',views.get_commissionhistory,name='user_commissionhistory'),
    path('user_getuserinfo/',views.getUserInfo,name='user_getuserinfo'),
    path('user_setuserinfo/',views.setUserInfo,name='user_setuserinfo'),
    
    # Module: repair man
    path('repair_getorder/',views.get_order,name='getorder'),
    path('repair_finish/',views.repair_finsh,name='repair_finish'),
]