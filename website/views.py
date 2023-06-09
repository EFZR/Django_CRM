from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import SignUpForm, AddRecordForm
from .models import Record
from Logging.Logger_Base import log

# Create your views here.


def home(request):
    records = Record.objects.all()
    # Check to see if login
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        # Authenticate
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'You have been logged in')
            log.info(f'The user {username} has logged in')
            return redirect('home')
        else:
            messages.warning(request, 'There was an error logging in')
            log.warning(f'There was an error logging with the user {username}')
            return redirect('home')
    else:
        return render(request, 'home.html', {'records': records})


def login_user(request):
    pass


def logout_user(request):
    logout(request)
    log.info('User has logout')
    messages.success(request, message='You have been logged out')
    return redirect('home')


def register(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            # Authenticate and Login
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            login(request=request, user=user)
            messages.success(request, 'You have succesfully Logged In')
            log.info(f'The user {username} was created and logged in Succesfully')
            return redirect('home')
    else:
        form = SignUpForm()
        return render(request, 'register.html', {'form': form})

    return render(request, 'register.html', {'form': form})


def record(request, pk):
    if request.user.is_authenticated:
        customer_record = Record.objects.get(id=pk)
        return render(request, 'record.html', {'record': customer_record})
    else:
        messages.success(request, 'You must be logged in to see the record')
        log.warning('Trying to see records without being logged in')
        return redirect('home')


def delete_record(request, pk):
    if request.user.is_authenticated:
        delete_it = Record.objects.get(id=pk)
        delete_it.delete()
        messages.success(request, 'Record deleted Succesfully')
        log.info(f'The user {request.user.username} has delete the record {delete_it}')
        return redirect('home')
    else:
        messages.success(request, 'You Must be logged in to do that')
        log.warning('Trying to see records without being logged in')
        return redirect('home')


def add_record(request):
    form = AddRecordForm(request.POST or None)
    if request.user.is_authenticated:
        if request.method == 'POST':
            if form.is_valid:
                add_record = form.save()
                messages.success(request, 'Record Added Succesfully')
                log.info(f'The user {request.user.username} add a new record')
                return redirect('home')
        else:
            return render(request, 'add_record.html', {'form': form})

    else:
        messages.success(request, 'You Must be logged in to do that')
        log.warning('Trying to see records without being logged in')
        return redirect('home')


def update_record(request, pk):
    if request.user.is_authenticated:
        current_record = Record.objects.get(id=pk)
        form = AddRecordForm(request.POST or None, instance=current_record)
        if form.is_valid():
            form.save()
            messages.success(request, 'Record Updated Succesfully')
            log.info(f'The user {request.user.username} update the record {current_record}')    
            return redirect('home')
        else:
            return render(request, 'update_record.html', {'form': form})
    else:
        messages.success(request, 'You Must be logged in to do that')
        log.warning('Trying to see records without being logged in')
        return redirect('home')
