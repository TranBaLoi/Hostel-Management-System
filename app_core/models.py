from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.template.defaultfilters import truncatechars

class Student_Account(models.Model):
    user = models.OneToOneField(User, on_delete = models.CASCADE)
    first_name = models.CharField(max_length = 100)
    last_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    matric = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    is_student = models.BooleanField(default = True)
    wallet = models.IntegerField(default = 0, null = True)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class Deposit(models.Model):
    student = models.ForeignKey(Student_Account, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 200)
    card_number = models.CharField(max_length=20)
    bank = models.CharField(max_length = 10)
    date_submit = models.CharField(max_length = 100)
    amount = models.IntegerField()
    confirm = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def save(self, *args, **kwargs):
        if self.pk:  # Kiểm tra nếu khoản tiền gửi đã tồn tại
            old_deposit = Deposit.objects.get(pk=self.pk)
            if old_deposit.confirm is False and self.confirm is True:  # Xác nhận lần đầu
                self.student.wallet += self.amount
                self.student.save()
        super().save(*args, **kwargs)  # Gọi phương thức save "thật"

    def __str__(self):
        return self.student.user.username


class House_Manager(models.Model):
    full_name = models.CharField(max_length = 100)
    email = models.CharField(max_length = 100)
    address = models.CharField(max_length = 100)
    phone_no = models.CharField(max_length = 100)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.full_name


class Block(models.Model):
    house_manager = models.ForeignKey(House_Manager, on_delete = models.CASCADE)
    block_name = models.CharField(max_length = 50)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return self.block_name


class Rooms(models.Model):
    block = models.ForeignKey(Block, on_delete=models.CASCADE)
    room_name = models.CharField(max_length=50, null=True)
    room_tag = models.CharField(max_length=10, default="NEW")
    description = models.TextField()
    condition = models.TextField()
    charge = models.IntegerField()
    slot_available = models.IntegerField(default=2) # tối đa 10 giường 
    is_available = models.BooleanField(default=True)
    image1 = models.ImageField(upload_to="photos")
    image2 = models.ImageField(upload_to="photos")
    image3 = models.ImageField(upload_to="photos")
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def short_description(self):
        return truncatechars(self.description, 20)
    def admin_photo(self):
        return mark_safe('<img src ="{}" width = 100 />'.format(self.image1.url))
    admin_photo.short_description = "Image"
    admin_photo.allow_tag = True
    def __str__(self):
        return self.room_name

class Accomodation_Request(models.Model):
    student = models.OneToOneField(Student_Account, on_delete = models.CASCADE)
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    approved = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)


    def __str__(self):
        return f"{self.room.room_name} has been {self.approved} {self.student.first_name}"



class Complaints(models.Model):
    student = models.ForeignKey(Student_Account, on_delete = models.CASCADE)
    subject = models.CharField(max_length = 40)
    message = models.TextField()
    status = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.student.first_name} - {self.subject}"



class GuestStayRequest(models.Model):
    student = models.ForeignKey(Student_Account, on_delete = models.CASCADE)
    full_name = models.CharField(max_length = 40)
    address = models.CharField(max_length = 40)
    reason = models.TextField()
    status = models.BooleanField(default=False)
    date_from = models.DateField()
    date_to = models.DateField()
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.student.first_name} - {self.full_name}"


class RoomTransfer(models.Model):
    student = models.ForeignKey(Student_Account, on_delete=models.CASCADE)
    reason = models.TextField()
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE, related_name='new_room')  # phòng chuyển đến
    approved = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    # def save(self, *args, **kwargs):
    #     # Lấy thông tin phòng hiện tại của sinh viên trước khi cập nhật
    #     accommodation_request = Accomodation_Request.objects.get(student=self.student)
    #     current_room = accommodation_request.room

        # # Nếu việc chuyển phòng đã được duyệt và phòng mới khác phòng hiện tại
        # if self.approved and current_room != self.room:
        #     # Giảm số người ở phòng cũ
        #     current_room.cur_people = max(current_room.cur_people - 1, 0)
        #     current_room.save()

        #     # Tăng số người ở phòng mới
        #     self.room.cur_people = min(self.room.cur_people + 1, self.room.sum_people)
        #     self.room.save()

        #     # Cập nhật phòng mới cho student trong Accomodation_Request
        #     accommodation_request.room = self.room
        #     accommodation_request.save()

        # super(RoomTransfer, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.student.first_name} - {self.room.room_name}"




class Guideline(models.Model):
    rule = models.TextField()
    guideline1 = models.CharField(max_length = 250)
    guideline2 = models.CharField(max_length = 250)
    guideline3 = models.CharField(max_length = 250)
    guideline4 = models.CharField(max_length = 250)
    guideline5 = models.CharField(max_length = 250)
    created_at = models.DateTimeField(auto_now = True)
    updated_at = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return f"{self.rule[:20]}"
class Rent(models.Model):
    room = models.ForeignKey(Rooms, on_delete=models.CASCADE)
    rent = models.IntegerField()
    electricitybill = models.IntegerField()
    waterbill = models.IntegerField()
    service = models.IntegerField()
    is_paid = models.BooleanField(default=False)
    student = models.ForeignKey(Student_Account, on_delete=models.CASCADE)

    def __str__(self):
        return f'Rent of Room {self.room} by {self.student}'
    
    def total_bill(self):
        return self.rent + self.electricitybill + self.waterbill + self.service


class Notification(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=False)

    def __str__(self):
        return self.title

class Revenue(models.Model):
    roomrevenue = models.IntegerField(default=0)
    electric = models.IntegerField(default=0)
    water = models.IntegerField(default=0)
    service = models.IntegerField(default=0)

    def calculate_revenue(self):
        rents = Rent.objects.filter(is_paid=True) 
        self.roomrevenue = sum(rent.total_bill() for rent in rents)
        self.electric = sum(rent.electricitybill for rent in rents)
        self.water = sum(rent.waterbill for rent in rents)
        self.service = sum(rent.service for rent in rents)

    def save(self, *args, **kwargs):
        self.calculate_revenue()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Doanh thu: {self.roomrevenue}, Tiền điện: {self.electric}, Tiền nước: {self.water}, Dịch vụ: {self.service}"
