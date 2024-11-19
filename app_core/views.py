from django.shortcuts import *
from django.contrib.auth import authenticate, login as dlogin, logout as dlogout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import *
from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test


def welcome_page(request):
    rooms = Rooms.objects.all()
    notifications = Notification.objects.filter(is_active = True).order_by('-created_at')


    # for room in rooms:
    #     print(room.image1.url)
    context = {
        # "rooms":rooms,
        "notifications" : notifications
        }
    return render(request, "home.html", context)


def login_page(request):
    context = {}
    return render(request, "login.html", context)


def login_user(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(username=username, password = password)
        if user is not None:
            dlogin(request, user)
            if username == "admin" or username == "admin_user":
                return redirect("admin-welcome-page")
            else:
                return redirect("welcome-page")
        messages.error(request, "Invalid Login Details")
        return redirect("login-page")
    else:
        return redirect("login-page")


def register_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = User.objects.create_user(username = username, password = password)
        user.save()
        return redirect("login-page")
    context = {}
    return render(request, "signup.html", context)


def view_rooms(request):
    rooms = Rooms.objects.all()
    context = {"rooms":rooms}
    return render(request, "view_rooms.html", context)


def logout_page(request):
    dlogout(request)
    return redirect("/")

def check_username(request):
    username = request.GET.get('username', None)
    data = {
        'is_taken': User.objects.filter(username__iexact=username).exists()
    }
    return JsonResponse(data)
def admin_required(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_active and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('permission-denied')
    return wrapper

@admin_required
def revenue_view(request):
    revenue_record, created = Revenue.objects.get_or_create(id=1)
    revenue_record.save()
    context = {
        'total_revenue': revenue_record.roomrevenue,
        'total_rent': revenue_record.rentroom,
        'total_electric': revenue_record.electric,
        'total_water': revenue_record.water,
        'total_service': revenue_record.service,
    }
    return render(request, 'admin_templates/revenue.html', context)

def permission_denied_view(request):
    return render(request, 'admin_templates/permission_denied.html')