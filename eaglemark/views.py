from django.http import HttpResponse
from django.shortcuts import render, redirect
from eaglemark.models import User, Ship
from eaglemark.models import Admin
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.db.models import Q


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
    print('user_num' in request.session)

    if 'user_num' in request.session:
        session_id = request.session['user_num']
        packages = Ship.objects.filter(Client_num=session_id)
    if not packages and request.method == "POST":
        search = request.POST.get('search')
        packages = Ship.objects.filter(Q(Shipping_id=search) | Q(AirwayBill=search) | Q(ShipBill=search))
        if not packages:
            message = "No packages found"
    if not packages and not message:
        message = "No package for you yet, call our local office if there is an issue "

    return render(request,"tracker.html",{'packages': packages,'message':message,'userLoggedIn': userLoggedIn})
def help(request):
    userLoggedIn = request.session.get('userLoggedIn', False)
    return render(request,"help.html",{'userLoggedIn': userLoggedIn})
def admin(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('pass')

        # Retrieve user from database
        try:
            user = Admin.objects.get(Email=email)
            if password == user.Password:
                messages.success(request, 'Login successful')
                return redirect('dashboard')
            else:
                messages.error(request, 'Incorrect password')
        except Admin.DoesNotExist:
            messages.error(request, 'User does not exist')

    # Get all messages
    messages_data = messages.get_messages(request)

    return render(request, "admin_login.html", {'messages_data': messages_data})
def dashboard(request):
    packages=Ship.objects.all()
    return render(request, "dashboard.html", {'packages': packages})

def add_package(request):
    if request.method == 'POST':
        packID = request.POST.get('Shipping_id')
        clientNum = request.POST.get('Client_num')
        abill = request.POST.get('AirwayBill')
        sbill = request.POST.get('ShipBill')
        state = request.POST.get('PackageState')
        locate = request.POST.get('Location')
        arive = request.POST.get('Arrival_Date')
        try:
            Ship.objects.create(
                packID=request.POST.get('Shipping_id'),
                clientNum = request.POST.get('Client_num'),
                locate=request.POST.get('Location'),
                state=request.POST.get('PackageState'),
                arive=request.POST.get('Arrival_Date'),
                abill = request.POST.get('AirwayBill'),
                sbill = request.POST.get('ShipBill')
            )
            messages.success(request, 'Package added')
            return redirect('add_package')
        except Exception as e:
            messages.error(request, f'failed: {str(e)}')
            return redirect('add_package')

    return render(request,"add_Package.html")

def package_list(request):
    packages = Ship.objects.all()
    return render(request, "package_List.html", {'packages': packages})