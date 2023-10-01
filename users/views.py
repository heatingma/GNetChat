from django.shortcuts import render, redirect
from django.http import HttpRequest
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages


def log(request: HttpRequest):
    # action when request method is GET
    if request.method == 'GET':
        register_form = RegisterForm()
        login_form = LoginForm()
        # context to render
        context = {
            "register_form": register_form,
            "login_form": login_form,
        }
    # action when request method is POST
    elif request.method == 'POST':
        # transform the request post to Forms 
        register_form = RegisterForm(request.POST)
        login_form = LoginForm(request.POST)
        # check whether login success
        if login_form.is_valid():
            email = login_form.cleaned_data["login_email"]
            password = login_form.cleaned_data["login_password"]
            # We check if the data is correct
            user = authenticate(email=email, password=password)
            if user:  # If the returned object is not None
                login(request, user)  # we connect the user
                return redirect('chat:my')
            else:  # otherwise an error will be displayed
                context = {
                    "register_form": register_form,
                    "login_form": login_form,
                    "login_error": "Error email or Error password!"
                }
        # check whether regist success
        elif register_form.is_valid():
            user = register_form.save()
            login(request, user)
            messages.success(request, "Congratulations, you are now a registered user!")
            return redirect('chat:my')
        # collect errors
        else:
            # return errors for user
            username_errors = register_form.errors.get('username')
            email_errors = register_form.errors.get('email')
            password_errors = register_form.errors.get('password2')
            context = {
                "register_form": register_form,
                "login_form": login_form,
                "username_errors": username_errors,
                "email_errors": email_errors,
                "password_errors":  password_errors,
            }            

    return render(
        request=request, 
        template_name='users/log.html', 
        context = context
    )