from django.shortcuts import render,redirect
from django.http import JsonResponse
from .models import complaint_category,complaint_subcategory,complaint_user
import json
# Create your views here.
def dashboard(request):
    pr=[]   
    complaints=[]
    complaintsubcategory = complaint_subcategory.objects.filter(servant_role=request.user.user_role)
    for i in complaintsubcategory: 
        val=complaint_user.objects.filter(complaint_subcat=i,is_otp_verify=True)
        complaints.append(val.all())
    params = {
        'complaintuser':complaints
    } 
    return render(request,"servant/servantpage.html",params)

def updateComplaint(request):
    data = json.loads(request.body)
    complaintId = int(data['complaintId'])
    complaintstatus = int(data['complaintstatus'])
    comp_status=complaint_user.objects.get(id = complaintId)
    comp_status.progress=complaintstatus
    if complaintstatus == -100: 
        complaintreason=str(data['reason'])
        comp_status.abort_reason=complaintreason
    comp_status.save()
    return JsonResponse('Complaint was updated', safe=False)
