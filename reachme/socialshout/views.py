from django.contrib.messages.api import success
from django.shortcuts import render, redirect
from complaint.models import complaint_category, complaint_subcategory, complaint_user
from django.contrib import messages
from django.db import IntegrityError
from django.core.mail import send_mail
from datetime import datetime, timedelta
from django.http import JsonResponse
import pytz
import math
import random
import json
from django.views.decorators.csrf import csrf_exempt


def index(request):
    return render(request, 'socialshout/index.html')


def problems(request):
    categories = complaint_category.objects.all()
    params = {
        'categories': categories
    }
    return render(request, 'socialshout/problems.html', params)


def subproblems(request, subproblem_id):
    cat = complaint_category.objects.filter(id=subproblem_id)
    subcategories = complaint_subcategory.objects.filter(
        complaint_cat=subproblem_id).all()
    print(cat)
    params = {
        'subcategories': subcategories,
        'cat': cat[0].category
    }
    return render(request, 'socialshout/subproblems.html', params)


def registration(request, problem_id, problem, subproblem_id, subproblem):
    params = {
        'problem_id': problem_id,
        'problem': problem,
        'subproblem_id': subproblem_id,
        'subproblem': subproblem
    }
    return render(request, 'socialshout/registration.html', params)


def regform(request, problem_id, problem, subproblem_id, subproblem):
    if request.method == 'POST':
        fullname = request.POST['fullname']
        email1 = request.POST['email']
        inputaddress = request.POST['inputaddress']
        inputdetail = request.POST['inputdetail']
        contactno1 = request.POST['contactno1']
        contactno2 = request.POST['contactno2']
        aadharno = request.POST['aadharno']
        pincode = request.POST['pincode']
        inputcity = request.POST['inputcity']
        inputstate = request.POST['inputstate']
        upload_file1 = request.FILES['file1'] if 'file1' in request.FILES else False
        upload_file2 = request.FILES['file2'] if 'file2' in request.FILES else False
        #otp system
        digits = [i for i in range(0, 10)]
        random_str = ""
        for i in range(6):
            index = math.floor(random.random()*10)
            random_str += str(digits[index])
        try:
            send_mail('Verfiy Your Complaint by entering the OTP',
                      'Your OTP for Verfification of your Complaint is '+random_str+'.',
                      'khandelwalakshita882@gmail.com',
                      [email1],
                      fail_silently=False)
            user1 = complaint_user()
            user1.complaint_cat = complaint_category(problem_id)
            user1.complaint_subcat = complaint_subcategory(subproblem_id)
            user1.full_name = fullname
            user1.complaint_info = inputdetail
            user1.email = email1
            user1.address = inputaddress
            user1.phone = contactno1
            user1.alternative_phone = contactno2
            user1.aadhar_no = aadharno
            user1.pincode = pincode
            user1.city = inputcity
            user1.state = inputstate
            user1.complaint_aadhar = upload_file1
            user1.complaint_spotimage = upload_file2
            user1.otp_code = random_str
            user1.otp_created_at = datetime.now()
            user1.save()
            request.session['complaint_email'] = email1
            request.session['complaint_id'] = user1.id
            messages.success(
                request, "otp is successfully sent to your registered email-id.")
            return redirect("/verify/")
        except Exception as e:
            messages.error(request, e)
            return redirect("/problems/subproblems/registration/"+str(problem_id)+"/"+problem+"/"+str(subproblem_id)+"/"+subproblem)
    return render(request, 'socialshout/otp_verify.html')


def verify(request):
    complaint_email = request.session.get('complaint_email')
    complaint_id = request.session.get('complaint_id')
    if request.method == 'POST':
        otp = request.POST['otp']
        complaint_user_row = complaint_user.objects.get(id=complaint_id)
        time_limit = complaint_user_row.otp_created_at+timedelta(minutes=10)
        utc = pytz.UTC
        time_limit = time_limit.replace(tzinfo=utc)
        now_time = datetime.now()
        now_time = now_time.replace(tzinfo=utc)
        if time_limit >= now_time and otp == complaint_user_row.otp_code:
            complaint_user_row.is_otp_verify = True
            complaint_user_row.save()
            e_id = complaint_user_row.id
            e_priority = complaint_user_row.complaint_subcat.priority
            e_email=complaint_user_row.email
            messages.success(request, 'Your Complaint is successfully registered. Please note your complaint-id to trace the progress of your complaint. Id = %s.' %
                             e_id)
            send_mail('Complaint Registration Successful',
                      'Congratulations! Your Complaint is successfully registered. Please note your complaint-id ' + str(e_id) + ' to trace the progress of your complaint. your complaint will be solved within ' + str(
                          e_priority) + ' days. if not done then please contact us and do track your complaint regularly for ' + str(e_priority) + ' days. Thankyou!',
                      'khandelwalakshita882@gmail.com',
                      [e_email],
                      fail_silently=False)
            return redirect("/")
        elif time_limit <= now_time and otp == complaint_user_row.otp_code:
            messages.error(request, "Your OTP is expire.")
            return redirect("/verify/")
        elif otp != complaint_user_row.otp_code:
            messages.error(request, "Please enter correct otp.")
            return redirect("/verify/")
    params = {
        'complaint_email': complaint_email,
        'complaint_id': complaint_id,
    }
    return render(request, 'socialshout/otp_verify.html', params)


@csrf_exempt
def tracker(request):
    data = json.loads(request.body)
    custmer_id = int(data['cust_id'])
    try:
        complaint_row = complaint_user.objects.get(id=custmer_id)
        if complaint_row:
            complaint_dets = {'complaint_id': complaint_row.id,
                              'progress': complaint_row.progress,
                              'abort_reason': complaint_row.abort_reason
                              }

            complaintstatus = json.dumps(complaint_dets)
            return JsonResponse(complaintstatus, safe=False)
    except complaint_user.DoesNotExist:
        complaint_dets = {'complaint_id': 0,
                          'progress': 0,
                          'abort_reason': None
                          }
        complaintstatus = json.dumps(complaint_dets)
        return JsonResponse(complaintstatus, safe=False)
    except Exception as e:
        e = json.dumps(e)
        return JsonResponse(e, safe=False)
