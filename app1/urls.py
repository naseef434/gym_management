from django.urls import path
from . import views
from datetime import timedelta

urlpatterns = [
 
    path('', views.index, name="index"),
    path('admin_login/', views.login, name="login"),
    path('dashboard/', views.dashboard, name="dashboard"),
    path('plan/', views.plans, name="plan"),
    path('add_plan/',views.add_plan, name="add_plan"),
    path('delete_plan/<int:id>/', views.delete_plan,name="delete_plan"), 
    path('student/', views.student_list,name="student"),
    path('add_student/', views.add_student, name="add_student"),
    path('get_plan/', views.get_plan, name="get_plan"),
    path('get_price/', views.get_price, name="get_price"),
    path('edit_student/<int:id>',views.edit_student,name="edit_student"),
    path('update_student/<int:id>',views.update_student,name="update_student"),
    path('delete_student/<int:id>', views.delete_student,name="delete_student"), 

    path('fee_payment_request/<int:id>',views.fee_payment_request,name="fee_payment_request"),
    
    path('fee_paid/<int:id>',views.fee_paid,name="fee_paid"),
    path('fee_paid1',views.fee_paid1,name="fee_paid1"),
    path('fee_unpaid',views.fee_unpaid,name="fee_unpaid"),
    path('expenses/', views.expenses, name="expenses"),
    path('add_expense', views.add_expense, name="add_expense"),
    path('delete_expense/<int:id>',views.delete_expense,name="delete_expense"), 
    # path('settings/',views.settings,name="settings"),
    path('user_list',views.user,name="user_list"),
    path('delete_user/<int:id>', views.delete_user,name="delete_user"), 

    path('logout',views.logout,name="logout"), 
    
]
