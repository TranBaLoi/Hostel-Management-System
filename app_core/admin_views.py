import base64
import io
from django.shortcuts import *
from matplotlib import pyplot as plt
import urllib
from .models import *
from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .models import Rent


def admin_home(request):
    requestss = Accomodation_Request.objects.all()
    context = {"requestss":requestss}
    return render(request, "admin_templates/admin_home.html", context)


def create_block(request):
    house_managers = House_Manager.objects.all()
    if request.method == "POST":
        house_manager = request.POST.get("house_manager")
        block_name = request.POST.get("block_name")
        house_manager_obj = House_Manager.objects.filter(id = house_manager).first()
        block = Block(house_manager = house_manager_obj, block_name = block_name)
        block.save()
        messages.success(request, "Success")
        return redirect(request.META.get("HTTP_REFERER"))
    context = {"house_managers":house_managers}
    return render(request, "admin_templates/create_block.html", context)


def create_manager(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name")
        email = request.POST.get("email")
        address = request.POST.get("address")
        phone_no = request.POST.get("phone_no")
        manager = House_Manager(full_name = full_name, email = email,  address = address, phone_no = phone_no)
        manager.save()
        messages.success(request, "Success")
        return redirect(request.META.get("HTTP_REFERER"))
    context = {}
    return render(request, "admin_templates/create_manager.html", context)


def create_room(request):
    blocks = Block.objects.all()
    if request.method == "POST":
        room_name = request.POST.get("room_name")
        room_tag = request.POST.get("room_tag")
        room_description = request.POST.get("room_description")
        room_charge = request.POST.get("room_charge")
        room_condition = request.POST.get("room_condition")
        block_name = request.POST.get("block_name")
        block_obj = Block.objects.filter(id = block_name).first()
        image1 = request.FILES["image1"]
        image2 = request.FILES["image2"]
        image3 = request.FILES["image3"]

        fs = FileSystemStorage()
        profile_image1_save = fs.save(image1.name, image1)
        profile_image2_save = fs.save(image2.name, image2)
        profile_image3_save = fs.save(image3.name, image3)

        image1_url = fs.url(profile_image1_save)
        image2_url = fs.url(profile_image2_save)
        image3_url = fs.url(profile_image3_save)

        room = Rooms(block=block_obj, room_name=room_name, room_tag=room_tag, description=room_description, condition=room_condition, charge=room_charge, image1=image1_url, image2=image2_url, image3=image3_url)
        room.save()
        messages.success(request, "Success!")
        return redirect(request.META.get("HTTP_REFERER"))
    context = {"blocks":blocks}
    return render(request, "admin_templates/create_room.html", context)


def manage_request(request):
    context = {}
    return render(request, "admin_templates/admin_home.html", context)


def manage_guest(request):
    guests = GuestStayRequest.objects.all()
    context = {"guests":guests}
    return render(request, "admin_templates/manage_guest.html", context)


def manage_transfer(request):
    transfers = RoomTransfer.objects.all()
    context = {"transfers":transfers}
    return render(request, "admin_templates/manage_transfer.html", context)


def manage_complaints(request):
    complaints = Complaints.objects.all()
    context = {"complaints":complaints}
    return render(request, "admin_templates/manage_complaint.html", context)


def manage_rule(request):
    if request.method == "POST":
        rule = request.POST.get("rule")
        guideline1 = request.POST.get("guideline1")
        guideline2 = request.POST.get("guideline2")
        guideline3 = request.POST.get("guideline3")
        guideline4 = request.POST.get("guideline4")
        guideline5 = request.POST.get("guideline5")
        guideline = Guideline(rule = rule, guideline1 = guideline1, guideline2=guideline2, guideline3=guideline3, guideline4=guideline4, guideline5=guideline5)
        guideline.save()
        messages.success(request, "Success")
        return redirect(request.META.get("HTTP_REFERER"))
    context = {}
    return render(request, "admin_templates/manage_rule.html", context)

def manage_rent(request):
    rooms= Rooms.objects.all()
    students= Student_Account.objects.all()
    if request.method == "POST":
        student_id = request.POST.get("student")
        room=request.POST.get("room")
        rent = request.POST.get("rent")
        electricbill = request.POST.get("electricbill")
        waterbill = request.POST.get("waterbill")
        service = request.POST.get("service")
        room_obj=Rooms.objects.filter(id=room).first()
        student_obj = Student_Account.objects.filter(id=student_id).first()
        rents = Rent(room=room_obj,rent=rent, electricity_bill=electricbill, water_bill=waterbill, service=service,student=student_obj)
        rents.save()
        messages.success(request, "Success")
        return redirect(request.META.get("HTTP_REFERER"))
    context = {"rooms":rooms,"students":students}
    return render(request, "admin_templates/manage_rent.html", context)

def approve_or_disapprove(request, ac_id):
    accomodation_req = Accomodation_Request.objects.filter(id = ac_id).first()
    if accomodation_req.approved == True:
        accomodation_req.approved = False
    else:
        accomodation_req.approved = True
    accomodation_req.save()
    return redirect(request.META.get("HTTP_REFERER"))



def complain_status(request, complain_id):
    complaint = Complaints.objects.filter(id = complain_id).first()
    if complaint.status == True:
        complaint.status = False
    else:
        complaint.status = True
    complaint.save()
    return redirect(request.META.get("HTTP_REFERER"))


def guest_status(request, guest_id):
    guest = GuestStayRequest.objects.filter(id = guest_id).first()
    if guest.status == True:
        guest.status = False
    else:
        guest.status = True
    guest.save()
    return redirect(request.META.get("HTTP_REFERER"))


def transfer_status(request, transfer_id):
    transfer = RoomTransfer.objects.filter(id = transfer_id).first()
    if transfer.approved == True:
        transfer.approved = False
    else:
        transfer.approved = True
    transfer.save()
    return redirect(request.META.get("HTTP_REFERER"))

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
    return render(request, 'admin_templates/admin_revenue.html', context)

def permission_denied_view(request):
    return render(request, 'admin_templates/permission_denied.html')

def generate_pie_chart(available_rooms, full_rooms):
    labels = ['Available Rooms', 'Full Rooms']
    sizes = [available_rooms, full_rooms]
    colors = ['#ff9999','#66b3ff']
    explode = (0.1, 0)  

    fig1, ax1 = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal') 

    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    return uri

def admin_dashboard(request):
    rooms = Rooms.objects.all()
    available_rooms = rooms.filter(is_available=True).count()
    full_rooms = rooms.filter(slot_available=0).count()

    pie_chart_uri = generate_pie_chart(available_rooms, full_rooms)

    context = {
        "available_rooms": available_rooms,
        "full_rooms": full_rooms,
        "pie_chart_uri": pie_chart_uri
    }
    return render(request, "admin_templates/admin_dashboard.html", context)



