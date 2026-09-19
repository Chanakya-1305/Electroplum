from django.db import models

class details(models.Model):
    name = models.CharField(max_length=100)
    experience = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)


class UserRegistration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)
    mobile = models.CharField(max_length=15)

    def __str__(self):
        return self.name

class EmployeeRegistration(models.Model):

    CATEGORY_CHOICES = [
        ('AC', 'AC Service'),
        ('PLUMBER', 'Plumber Service'),
        ('ELECTRICAL', 'Electrical Service'),
        ('INVERTER', 'Inverter Service'),
    ]

    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    experience = models.PositiveIntegerField()
    contact = models.CharField(max_length=15)
    address = models.TextField()
    photo = models.ImageField(upload_to='workers/')
    password = models.CharField(max_length=128, blank=True, null=True)

    def __str__(self):
        return self.name
    
class Booking(models.Model):
        STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Accepted', 'Accepted'),
        ('Rejected', 'Rejected'),
        ('Completed', 'Completed'),
        ('Cancelled', 'Cancelled'),
        ]
        customer_name = models.CharField(max_length=100)
        email = models.EmailField()
        phone = models.CharField(max_length=10)
        address = models.TextField()

        category = models.CharField(max_length=20)

        worker = models.ForeignKey(
            'EmployeeRegistration',
            on_delete=models.CASCADE
        )

        booking_date = models.DateField()
        booking_time = models.TimeField()

        problem = models.TextField()

        payment_method = models.CharField(max_length=50)

        status = models.CharField(
            max_length=20,
            choices=STATUS_CHOICES,
            default="Pending"
        )

        cancel_reason = models.TextField(
            blank=True,
            null=True
        )

        created_at = models.DateTimeField(auto_now_add=True)

        def __str__(self):
            return self.customer_name