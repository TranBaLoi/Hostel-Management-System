from django.contrib import admin
from django.urls import path
from .student_views import *
from app_core.admin_views import *
from .views import *


app_name = "app"


urlpatterns = [

    # Students Urls
    
    path("student_dashboard", student_dashboard, name = "student-dashboard"),
    path("student_register", student_register, name = "student-register"),
    path("room_details/<str:room_id>", room_details, name = "room-details"),
    path("payment", payment, name = "payment"),
    path("accomodation_request", accomodation_request, name = "accomodation-request"),
    path("room_transfer", room_transfer, name = "room-transfer"),
    path("guest_stay", guest_stay, name = "guest-stay"),
    path("complain", complaints, name = "complaints"),
    path('rents', view_rents, name='view-rents'),
    path('member_list', room_members_list, name='room-members'),
    path('pay_rent/<int:rent_id>/', pay_rent, name='pay_rent'),
    # Admin Urls
    path("revenue_view", revenue_view, name='admin-revenue'),
    path("manage_rent", manage_rent, name = "manage-rent"),
    path("create_block", create_block, name = "create-block"),
    path("create_manager", create_manager, name = "create-manager"),
    path("create_room", create_room, name = "create-room"),
    path("manage_request", manage_request, name = "manage-request"),
    path("manage_transfer", manage_transfer, name = "manage-transfer"),
    path("manage_guest", manage_guest, name = "manage-guest"),
    path("manage_complaints", manage_complaints, name = "manage-complaints"),
    path("manage_rule", manage_rule, name = "manage-rule"),
    path("approve_or_disapprove/<str:ac_id>", approve_or_disapprove, name = "approve_or_disapprove"),
    path("complain_status/<str:complain_id>", complain_status, name = "complain_status"),
    path("guest_status/<str:guest_id>", guest_status, name = "guest_status"),
    path("transfer_status/<str:transfer_id>", transfer_status, name = "transfer_status"),
    path("request_dashboard", request_dashboard, name = "request-dashboard"),
    path('admin-dashboard/', admin_dashboard, name='admin-dashboard'),

]
