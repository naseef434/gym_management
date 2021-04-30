from django.db import models
from datetime import date
from datetime import datetime

class Plan(models.Model):
    gender = models.CharField(max_length=10)
    planName = models.CharField(max_length=30)
    price  = models.BigIntegerField()
    registrationFee = models.BigIntegerField(default= 0)
    date = models.DateTimeField(default=datetime.now)
    
    def __str__(self):
        return self.planName

class StudentRegistration(models.Model):
    #joinId = models.CharField(max_length=20)
    name = models.CharField(max_length=30)
    phone  = models.BigIntegerField()
    age  = models.IntegerField()
    discription  = models.CharField(max_length=200)
    address= models.CharField(max_length=100,null=True)
    joiningDate = models.DateField(default=datetime.now)
    plan = models.ForeignKey(Plan,on_delete = models.CASCADE)
    
    # def __str__(self):
    #     return self.name
    
class fees(models.Model):
    student = models.ForeignKey(StudentRegistration,on_delete=models.CASCADE)
    paidAmount = models.BigIntegerField()
    balance  = models.BigIntegerField()
    lastFeePaid = models.DateField(default=datetime.now)
    feeStatus = models.BooleanField(default=False)

class Expense(models.Model):
    name = models.CharField(max_length=100,null=False)
    amount = models.BigIntegerField(null=False)
    date = models.DateField(default=datetime.now)