from urllib import request
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib import messages
from django.db import IntegrityError
from django.contrib.auth.hashers import make_password
from .models import EmployeeRegistration, details 
from .models import UserRegistration
from django.contrib.auth.hashers import check_password
from django.http import JsonResponse
from .models import Booking 

def plumbers(request):

    plumbers = EmployeeRegistration.objects.filter(category='PLUMBER')

    return render(request,'plumbers.html',{'plumbers':plumbers})
def login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:
            user = UserRegistration.objects.get(email=email)

            if check_password(password, user.password):

                # Store user information in session
                request.session['user_id'] = user.id
                request.session['user_name'] = user.name


                return redirect("home")

            else:
                messages.error(request, "Invalid Password")

        except UserRegistration.DoesNotExist:
            messages.error(request, "Email does not exist")
    return render(request, 'login.html')
def signup(request):
    if request.method == "POST":

        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')
        mobile = request.POST.get('mobile')

        if password != confirm:
            messages.error(request, "Passwords do not match.")
            return render(request, "signup.html")

        
        if UserRegistration.objects.filter(email=email).exists():
            messages.error(request, "Email already registered.")
            return render(request, "signup.html")

        
        password = make_password(password)

        UserRegistration.objects.create(
            name=name,
            email=email,
            password=password,
            mobile=mobile
        )
        messages.success(request, "Registration successful!")
        return redirect('login')
    return render(request, 'signup.html')
def inveter(request):
    inveter = EmployeeRegistration.objects.filter(category='INVERTER')
    return render(request,'inveter.html',{'inveter':inveter})
def home(request):
    return render(request, 'Home.html')
def exploreus(request):
    return render(request, 'exploreus.html')
def aboutus(request):
    return render(request, 'aboutus.html')
def contactus(request):
    return render(request, 'contactus.html')
def ac(request):
    ac = EmployeeRegistration.objects.filter(category='AC')
    return render(request,'ac.html',{'ac':ac})
def booking(request):

    if 'user_id' not in request.session:
        messages.error(request, "Please login before booking a service.")
        return redirect('newlogin')

    user_id = request.session['user_id']

    try:
        user = UserRegistration.objects.get(id=user_id)
    except UserRegistration.DoesNotExist:
        request.session.flush()
        messages.error(request, "Please login again.")
        return redirect('newlogin')

    if request.method == "POST":

        customer_name = user.name
        email = user.email

        phone = request.POST.get("phone")
        address = request.POST.get("address")

        category = request.POST.get("category")
        worker_id = request.POST.get("worker")

        booking_date = request.POST.get("booking_date")
        booking_time = request.POST.get("booking_time")

        problem = request.POST.get("problem")
        payment_method = request.POST.get("payment_method")

        try:
            worker = EmployeeRegistration.objects.get(id=worker_id)
        except EmployeeRegistration.DoesNotExist:
            messages.error(request, "Selected worker does not exist.")
            return redirect("booking")

        Booking.objects.create(
            customer_name=customer_name,
            email=email,
            phone=phone,
            address=address,
            category=category,
            worker=worker,
            booking_date=booking_date,
            booking_time=booking_time,
            problem=problem,
            payment_method=payment_method,
            status="Pending"
        )

        return render(
            request,
            "bookingconfirmationpage.html"
        )

    return render(
        request,
        "booking.html"
    )
   
def electricalservices(request):
    electricalservices = EmployeeRegistration.objects.filter(category='ELECTRICAL')
    return render(request,'electricalservices.html',{'electricalservices':electricalservices})
def logout(request):
    request.session.flush()
    messages.success(request, "You have been logged out.")
    return redirect('newlogin')
def employeeregistration(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        category = request.POST.get("category")
        experience = request.POST.get("experience")
        contact = request.POST.get("contact")
        address = request.POST.get("address")
        photo = request.FILES.get("photo")

        raw_password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        form_data = {
            "name": name,
            "email": email,
            "category": category,
            "experience": experience,
            "contact": contact,
            "address": address,
        }

        # Check password
        if raw_password != confirm_password:

            messages.error(request, "Passwords do not match.")

            return render(
                request,
                "employeeregistration.html",
                {
                    "form_data": form_data
                }
            )

        # Check email
        if EmployeeRegistration.objects.filter(email=email).exists():

            return render(
                request,
                "employeeregistration.html",
                {
                    "email_error": "This email already exists.",
                    "form_data": form_data,
                },
            )

        # Hash password
        password = make_password(raw_password)

        try:

            EmployeeRegistration.objects.create(
                name=name,
                email=email,
                category=category,
                experience=experience,
                contact=contact,
                address=address,
                photo=photo,
                password=password
            )

        except IntegrityError:

            return render(
                request,
                "employeeregistration.html",
                {
                    "email_error": "This email already exists.",
                    "form_data": form_data,
                },
            )

        messages.success(
            request,
            "Employee registration completed successfully. Please login."
        )

        return redirect("employee_login")

    return render(request, "employeeregistration.html")

def get_workers(request):
    category = request.GET.get('category')
    workers = EmployeeRegistration.objects.filter(category=category)
    data = []
    for worker in workers:
        data.append({
            'id': worker.id,
            'name': worker.name,
        })
    return JsonResponse(data, safe=False)
def bookingconfirmationpage(request):
    return render(request, 'bookingconfirmationpage.html')

def bookinghistorypage(request):

    # Check if customer is logged in
    if 'user_id' not in request.session:
        messages.error(request, "Please login to view your booking history.")
        return redirect('newlogin')

    user_id = request.session['user_id']

    try:
        user = UserRegistration.objects.get(id=user_id)
    except UserRegistration.DoesNotExist:
        request.session.flush()
        messages.error(request, "Please login again.")
        return redirect('newlogin')

    # Show only this customer's bookings
    bookings = Booking.objects.filter(
        email=user.email
    ).order_by("-created_at")

    return render(
        request,
        "bookinghistorypage.html",
        {
            "bookings": bookings
        }
    )
def cancelbookingpage(request, booking_id):

    if 'user_id' not in request.session:
        messages.error(request, "Please login first.")
        return redirect('newlogin')

    user_id = request.session['user_id']

    try:
        user = UserRegistration.objects.get(id=user_id)
    except UserRegistration.DoesNotExist:
        request.session.flush()
        return redirect('newlogin')

    try:
        booking = Booking.objects.get(
            id=booking_id,
            email=user.email
        )
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('bookinghistorypage')

    if request.method == "POST":

        booking.status = "Cancelled"

        booking.cancel_reason = request.POST.get("reason")

        booking.save()

        messages.success(
            request,
            "Your booking has been cancelled successfully."
        )

        return redirect("bookinghistorypage")

    return render(
        request,
        "cancelbookingpage.html",
        {
            "booking": booking
        }
    )
def newlogin(request):
    return render(request, 'newlogin.html')
def employee_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")

        try:

            employee = EmployeeRegistration.objects.get(email=email)

            if employee.password and check_password(
                password,
                employee.password
            ):

                # Employee-specific session
                request.session['employee_id'] = employee.id
                request.session['employee_name'] = employee.name

                return redirect("employee_dashboard")

            else:

                messages.error(
                    request,
                    "Invalid email or password."
                )

        except EmployeeRegistration.DoesNotExist:

            messages.error(
                request,
                "Employee account does not exist."
            )

    return render(request, "employee_login.html")
def employee_dashboard(request):
    if 'employee_id' not in request.session:
        messages.error(request, "Please login as an employee.")
        return redirect('newlogin')

    try:
        employee = EmployeeRegistration.objects.get(
            id=request.session['employee_id']
        )
    except EmployeeRegistration.DoesNotExist:
        request.session.flush()
        messages.error(request, "Please login again.")
        return redirect('newlogin')

    bookings = Booking.objects.filter(
        worker=employee
    ).order_by('-created_at')

    context = {
        'employee': employee,
        'bookings': bookings,

        'total_bookings': bookings.count(),

        'pending_count': bookings.filter(
            status='Pending'
        ).count(),

        'accepted_count': bookings.filter(
            status='Accepted'
        ).count(),

        'rejected_count': bookings.filter(
            status='Rejected'
        ).count(),

        'completed_count': bookings.filter(
            status='Completed'
        ).count(),

        'cancelled_count': bookings.filter(
            status='Cancelled'
        ).count(),
    }

    return render(
        request,
        'employee_dashboard.html',
        context
    )
def ourwork(request):
    return render(request, 'ourwork.html')

def accept_booking(request, booking_id):
    if 'employee_id' not in request.session:
        messages.error(request, "Please login as an employee.")
        return redirect('newlogin')

    try:
        employee = EmployeeRegistration.objects.get(
            id=request.session['employee_id']
        )
    except EmployeeRegistration.DoesNotExist:
        request.session.flush()
        return redirect('newlogin')

    try:
        booking = Booking.objects.get(
            id=booking_id,
            worker=employee
        )
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('employee_dashboard')

    booking.status = 'Accepted'
    booking.save()

    messages.success(
        request,
        "Booking accepted successfully."
    )

    return redirect('employee_dashboard')

def reject_booking(request, booking_id):
    if 'employee_id' not in request.session:
        messages.error(request, "Please login as an employee.")
        return redirect('newlogin')

    try:
        employee = EmployeeRegistration.objects.get(
            id=request.session['employee_id']
        )
    except EmployeeRegistration.DoesNotExist:
        request.session.flush()
        return redirect('newlogin')

    try:
        booking = Booking.objects.get(
            id=booking_id,
            worker=employee
        )
    except Booking.DoesNotExist:
        messages.error(request, "Booking not found.")
        return redirect('employee_dashboard')

    booking.status = 'Rejected'
    booking.save()

    messages.success(
        request,
        "Booking rejected."
    )

    return redirect('employee_dashboard')