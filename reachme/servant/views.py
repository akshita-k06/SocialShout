from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.decorators import login_required
from django import forms
from django.contrib.auth.hashers import make_password, mask_hash
from django.contrib.auth.models import auth
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from django.contrib.messages.api import success
from django.db import IntegrityError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import Users
from django.core.mail import send_mail, BadHeaderError
from datetime import datetime, timedelta
import pytz
import math
import random
from django.template.loader import render_to_string
from django.db.models.query_utils import Q
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes

# Create your views here.


def register(request):
    if request.method == "GET":
        return render(
            request, "registration/register.html"
        )
    elif request.method == "POST":
        firstname = request.POST['firstname']
        lastname = request.POST['lastname']
        email = request.POST['email']
        aadharno = request.POST['aadharno']
        phoneno = request.POST['phoneno']
        user_role = request.POST['user_role']
        id_upload_aadhar = request.FILES['id_upload_aadhar'] if 'id_upload_aadhar' in request.FILES else False
        id_upload_id = request.FILES['id_upload_id'] if 'id_upload_id' in request.FILES else False
        role, remaining = user_role.split('-')
        role = int(role)
        try:
            servant1 = Users()
            servant1.first_name = firstname
            servant1.last_name = lastname
            servant1.email = email
            servant1.aadhar_no = aadharno
            servant1.user_role = role
            servant1.upload_aadhar = id_upload_aadhar
            servant1.upload_id = id_upload_id
            servant1.save()
            subject = "Password Reset Requested"
            email_template_name = "registration/password_reset_email.txt"
            c = {
                "email": servant1.email,
             			'domain': 'localhost:8000',
             			'site_name': 'Website Name',
             			"uid": urlsafe_base64_encode(force_bytes(servant1.pk)),
             			'token': default_token_generator.make_token(servant1),
             			'protocol': 'http',
            }
            email = render_to_string(email_template_name, c)
            send_mail(subject, email, 'verified_email_address',
                      [servant1.email], fail_silently=False)
            return redirect("/servant/accounts/password_reset/done/")
        except IntegrityError as e:
            messages.error(
                request, "Email is already used, please use new Email")
            return redirect('/servant/register/')
        except Exception as e:
            messages.error(request, e)
            return redirect('/servant/register/')
    return render(request, 'registration/')
def logout_view(request):
    logout(request)