from django.db import models
from django.db.models.deletion import CASCADE



class complaint_category(models.Model):
    id = models.AutoField(primary_key=True)
    category=models.CharField(max_length=100,default=None,blank=True,null=True)
    def __str__(self):
        return str(self.id)+"-"+self.category
    
user_role_choices =  ( (1, "MSEB Chief Engineer"), 
   (2, "Health Department"), 
   (3, "Water Conservation officer"), 
   (4, "Municipal corporation"), 
   (5, "Department Safety Officer"), 
) 


class complaint_subcategory(models.Model):
    id = models.AutoField(primary_key=True)
    complaint_cat= models.ForeignKey(complaint_category,default=None,on_delete=models.CASCADE)
    subcategory=models.CharField(max_length=200,default=None,blank=True,null=True)
    priority=models.SmallIntegerField(default=1,blank=True,null=True)
    servant_role = models.SmallIntegerField(default=0,choices=user_role_choices) 
    def __str__(self):
        return str(self.id)+"-"+self.subcategory


class complaint_user(models.Model):
    id=models.AutoField(primary_key=True)
    complaint_cat=models.ForeignKey(complaint_category,default=None,on_delete=models.CASCADE)
    complaint_subcat=models.ForeignKey(complaint_subcategory,default=None,on_delete=models.CASCADE)
    full_name=models.CharField(max_length=250,default=None,null=True)
    complaint_info=models.TextField(default=None,blank=True,null=True)
    email = models.CharField(max_length=250, default=None)
    address = models.CharField(max_length=5000, default=None)
    phone = models.CharField(max_length=15, blank=True, null=True)
    alternative_phone = models.CharField(max_length=15, blank=True, null=True)
    pincode = models.IntegerField(default=None)
    aadhar_no = models.CharField(max_length=15,default=None)
    city = models.CharField(max_length=50, default=None)
    state = models.CharField(max_length=50, default=None)
    complaint_aadhar=models.ImageField(upload_to="media/complaint_aadhar")
    complaint_spotimage=models.ImageField(upload_to="media/complaint_spotimage")
    is_otp_verify=models.BooleanField(default=False)
    otp_code=models.CharField(max_length=6,blank=True,null=True)
    otp_created_at=models.DateTimeField(blank=True,null=True)
    created_at=models.DateTimeField(auto_now_add=True)
    progress=models.IntegerField(default=25)
    abort_reason=models.CharField(max_length=600,blank=True,null=True, default="No reason")

    def __str__(self):
        return str(self.id)+"-"+str(self.full_name)
    
