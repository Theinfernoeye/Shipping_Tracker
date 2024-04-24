import csv
import io
from io import TextIOWrapper
from typing import TextIO

from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from eaglemark.models import User, Ship,get_Location
from eaglemark.models import Admin
from eaglemark.models import EagleDB
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Q
from datetime import datetime

def home(request):
    userLoggedIn = request.session.get('userLoggedIn', False)
    return render(request, "index.html",{'userLoggedIn': userLoggedIn})

def signup(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        email = request.POST.get('email')
        phnum = request.POST.get('numbers')
        pas = request.POST.get('pass')
        confpas = request.POST.get('confpass')

        if pas != confpas:
            messages.error(request, 'Passwords do not match')
            return redirect('signup')

        # Check password length
        if len(pas) < 8:
            messages.error(request, 'Password must be at least 8 characters long')
            return redirect('signup')

        # Check phone number length
        if len(phnum) != 8:  # Assuming phone number length should be 10 digits
            messages.error(request, 'Phone number must be 8 digits long dont add +267')
            return redirect('signup')

        # Hash the password before storing it
        hashed_password = make_password(pas)

        # Check if email already exists in the database
        if User.objects.filter(email=email).exists():
            messages.error(request, 'This email is already in use')
            return redirect('signup')
        if User.objects.filter(Phone_number=phnum).exists():
            messages.error(request, 'This Phone number is already in use')
            return redirect('signup')

        try:
            User.objects.create(
                First_name=fname,
                Last_name=lname,
                email=email,
                Phone_number=phnum,
                Password=hashed_password
            )
            messages.success(request, 'Successful signup')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Signup failed: {str(e)}')
            return redirect('signup')

    return render(request, "signup.html")

def login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        pas = request.POST.get('pass')
        remember_me = request.POST.get('rememberMe')

        try:
            user = User.objects.get(email=email)
            if check_password(pas, user.Password):
                request.session['user_num'] = user.Phone_number
                request.session['userLoggedIn'] = True  # Set userLoggedIn to True
                if remember_me:
                    response = redirect('home')
                    response.set_cookie('remembered_email', email)
                    response.set_cookie('remembered_password', pas)
                    return response
                else:
                    messages.success(request, 'Login successful')
                    return redirect('home')
            else:
                messages.error(request, 'Incorrect password')
                return redirect('login')
        except User.DoesNotExist:
            messages.error(request, 'User does not exist')

    messages_data = messages.get_messages(request)

    return render(request, "login.html", {'messages_data': messages_data})

def signout(request):
    if 'user_num' in request.session:
        del request.session['user_num']
    if 'userLoggedIn' in request.session:
        del request.session['userLoggedIn']
    return redirect('home')  # Redirect to the home page after sign out

def tracker(request):
    userLoggedIn = request.session.get('userLoggedIn', False)
    packages = None
    message = None
    bill = None  # Initialize bill variable here
    bill_list = []
    print('user_num' in request.session)

    if 'user_num' in request.session:
        session_id = request.session['user_num']
        packages = Ship.objects.filter(Client_num_id=session_id)
        for package in packages:
            # Translate the state value into a label
            package.state_label = get_Location(package.Location)

    if request.method == "POST":
        search = request.POST.get('search')
        packages = Ship.objects.filter(Q(Shipping_id=search) | Q(AirwayBill=search) | Q(ShipBill=search))
        if not packages:
            message = "No packages found"
        else:
            for package in packages:
                # Translate the state value into a label
                package.state_label = get_Location(package.State)

    if not packages and not message:
        message = "No package for you yet, call our local office if there is an issue "

    if packages is not None:
        for package in packages:
            if not package.AirwayBill:
                bill_list.append(package.AirwayBill)
            else:
                bill_list.append(package.ShipBill)
        bill = ', '.join(bill_list)
        print(bill)

    return render(request, "tracker.html", {'packages': packages, 'message': message, 'userLoggedIn': userLoggedIn, 'bill': bill})



def help(request):
    userLoggedIn = request.session.get('userLoggedIn', False)
    return render(request,"help.html",{'userLoggedIn': userLoggedIn})

def admin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')
        request.session['userLoggedIn'] = True

        # Retrieve user from database
        try:
            user = Admin.objects.get(Email=email)
            if password == user.Password:
                messages.success(request, 'Login successful')
                return redirect('package_list')
            else:
                messages.error(request, 'Incorrect password')
        except Admin.DoesNotExist:
            messages.error(request, 'User does not exist')

    # Get all messages
    messages_data = messages.get_messages(request)

    return render(request, "admin_login.html", {'messages_data': messages_data})

def admin_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if not request.session.get('userLoggedIn', False):
            # User is not logged in as admin, redirect to login page or any other page
            return redirect('admin')
        return view_func(request, *args, **kwargs)
    return _wrapped_view

@admin_required

def add_package(request):
    if request.method == 'POST':
        try:
            # Check if a CSV file is uploaded
            if 'excel_file' in request.FILES:
                csv_file = request.FILES['excel_file']
                if csv_file:
                    try:
                        # Check if the uploaded file is a CSV
                        if not csv_file.name.endswith('.csv'):
                            messages.error(request, 'Uploaded file is not a CSV')
                            return redirect('add_package')

                        # Read data from CSV file and create Ship objects
                        reader = csv.reader(io.TextIOWrapper(csv_file, encoding='utf-8'))
                        next(reader)  # Skip header row
                        for row in reader:
                            MARK, CUSTOMER, BALANCE = row[:3]
                            EagleDB.objects.create(
                                MARK=MARK,
                                CUSTOMER=CUSTOMER,
                                BALANCE=BALANCE
                            )
                        messages.success(request, 'Packages added successfully from CSV')
                        return redirect('add_package')
                    except Exception as e:
                        messages.error(request, f'Failed to add packages from CSV: {str(e)}')
                        return redirect('add_package')
                else:
                    messages.error(request, 'No file uploaded')
                    return redirect('add_package')
            else:
                # Check for manual input
                if all(request.POST.get(field) for field in ['Mark', 'Customer', 'Balance']):
                    try:
                        Date = request.POST.get('Date')
                        if Date:
                            Date = datetime.strptime(Date, '%Y-%m-%d').date()
                        else:
                            Date = None
                        EagleDB.objects.create(
                            MARK=request.POST.get('Mark'),
                            CUSTOMER=request.POST.get('Customer'),
                            BALANCE=request.POST.get('Balance'),
                            ID=request.POST.get('ID'),
                            LOCATION=request.POST.get('Location'),
                            Phone=request.POST.get('Phone'),
                            Date=Date

                        )
                        messages.success(request, 'Package added successfully')
                        return redirect('add_package')
                    except Exception as e:
                        messages.error(request, f'Failed to add package: {str(e)}')
                        return redirect('add_package')
                else:
                    messages.error(request, 'Please fill all required fields')
                    return redirect('add_package')
        except Exception as e:
            messages.error(request, f'Failed to add package: {str(e)}')
            return redirect('add_package')
    return render(request, "add_Package.html")

@admin_required
def package_list(request):
    packages = EagleDB.objects.all()
    for package in packages:
        # Translate the state value into a label
        package.state_label = get_Location(package.LOCATION)
    return render(request, "package_List.html", {'packages': packages})

@admin_required
def edit_package(request,mark):
    package = get_object_or_404(EagleDB, MARK=mark)
    return render(request, 'edit_package_form.html', {'package': package})

@admin_required
def delete_package(request, mark):
    if request.method == 'POST':
        package = get_object_or_404(EagleDB, MARK=mark)
        package.delete()
        return JsonResponse({'message': 'Package deleted successfully.'})
    else:
        return JsonResponse({'error': 'Invalid request method.'}, status=400)

@admin_required
def update_package(request, MARK):
    if request.method == 'POST':
        try:
            # Retrieve the package instance
            package = EagleDB.objects.get(MARK=MARK)

            # Update package fields based on form data
            package.Phone = request.POST.get('phone')
            package.Bill_ID = request.POST.get('bill_id')
            package.PAID = request.POST.get('paid') == 'on'  # Assuming 'paid' is a checkbox
            package.Location = request.POST.get('location')
            package.SIGNED = request.POST.get('picked_up') == 'on'  # Assuming 'picked_up' is a checkbox

            # Save the updated package
            package.save()

            # Return a success response
            return JsonResponse({'success': True, 'message': 'Package updated successfully'})

        except EagleDB.DoesNotExist:
            # Package not found
            return JsonResponse({'success': False, 'message': 'Package not found'}, status=404)

        except Exception as e:
            # Error occurred while updating package
            return JsonResponse({'success': False, 'message': f'Failed to update package: {str(e)}'}, status=500)

    # Method other than POST is not supported
    return JsonResponse({'success': False, 'message': 'Method not allowed'}, status=405)



