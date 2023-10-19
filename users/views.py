from django.shortcuts import render, redirect
from django.http import HttpRequest,HttpResponse
from .forms import LoginForm, RegisterForm
from django.contrib.auth import login, authenticate
from django.contrib import messages
from django.forms.utils import ErrorList
from django.core.mail import send_mail
from django.http import JsonResponse
import random
from django.views.decorators.csrf import csrf_exempt
from users.check_invatation import check_invatation_code, delete_invatation_code


def index(request: HttpRequest):
    return render(
        request=request,
        template_name="users/index.html",
    )

@csrf_exempt
def log(request: HttpRequest):
    # action when request method is GET
    if request.method == "GET":
        register_form = RegisterForm()
        login_form = LoginForm()
        # context to render
        context = {
            "register_form": register_form,
            "login_form": login_form,
        }
    # action when request method is POST
    elif request.method == "POST":
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
                return redirect("chat:my")
            else:  # otherwise an error will be displayed
                context = {
                    "register_form": register_form,
                    "login_form": login_form,
                    "login_error": "Error email or Error password!",
                }
        else:
            invitation_code = request.POST["hidden_invitation_code"]
            if not check_invatation_code(invitation_code):
                context = {
                    "register_form": register_form,
                    "login_form": login_form,
                    "invatation_errors": "Wrong Invatation Code!",
                }            
                return render(
                    request=request, 
                    template_name='users/log.html', 
                    context = context
                )  
                
            # check whether regist success
            elif register_form.is_valid():
                email_code = register_form.cleaned_data.get("email_code")
                last_email_code = register_form.cleaned_data.get("last_email_code")          
                if email_code:
                    if email_code == last_email_code:
                        user = register_form.save()
                        delete_invatation_code(invitation_code)
                        login(request, user)
                        messages.success(
                            request, "Congratulations, you are now a registered user!"
                        )
                        return redirect("chat:my")
                    else:
                        email_code_errors = register_form.errors.get("email_code")
                        context = {
                            "register_form": register_form,
                            "login_form": login_form,
                            "email_code_errors": email_code_errors,
                        }
                else:
                    email_code_errors = register_form.errors.get("email_code")
                    context = {
                        "register_form": register_form,
                        "login_form": login_form,
                        "email_code_errors": email_code_errors,
                    }
            # collect errors
            else:
                # return errors for user
                username_errors = register_form.errors.get("username")
                email_errors = register_form.errors.get("email")
                password_errors = register_form.errors.get("password2")
                username_errors_show = None
                email_errors_show = None
                password_errors_show = None
                if(username_errors):
                    username_errors_show = ErrorList()
                    username_errors_show.append(username_errors[0])
                if(email_errors):
                    email_errors_show = ErrorList()
                    email_errors_show.append(email_errors[0])
                if(password_errors):
                    password_errors_show = ErrorList()
                    password_errors_show.append(password_errors[0])
                context = {
                    "register_form": register_form,
                    "login_form": login_form,
                    "username_errors": username_errors_show,
                    "email_errors": email_errors_show,
                    "password_errors":  password_errors_show,
                }            

    return render(
        request=request, 
        template_name='users/log.html', 
        context = context
    )



def sendemail(request: HttpRequest):
    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        to_email = request.POST.get("to_email")
        sms_code = "%06d" % random.randint(0, 999999)
        EMAIL_FROM = "1712471374@qq.com"  # 邮箱来自
        email_title = "邮箱激活"
        email_body = "您的邮箱注册验证码为：{0}, 该验证码有效时间为两分钟，请及时进行验证。".format(sms_code)
        try:
            send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
            return JsonResponse({"success": True, "sms_code": sms_code})
        except Exception as e:
            context = {
            }
            return JsonResponse({"success": False, "sms_code": sms_code})