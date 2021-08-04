from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.models import User,auth
from django.contrib import messages
from app1.models import *
from datetime import datetime, date
from datetime import date
from datetime import timedelta
from django.http import JsonResponse
import json



#landing 
def index(request):
    return render(request, "index.html")
#login
def login(request):
    if request.user.is_authenticated:
        return redirect(dashboard)
        
    if request.method == "POST":
        username = request.POST['username'];
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)
            
        if user is not None:
            auth.login(request, user)
            messages.success(request,"Loged in ")
            return redirect(dashboard)
        else:
            messages.error(request,"username or password is wrong")
            return render(request, 'login.html')
        
    else:
        return render(request, 'login.html')

#dashboard
def dashboard(request):
    if request.user.is_authenticated:
        student =  StudentRegistration.objects.all().count()
        plans =  Plan.objects.all().count()
        expenses = Expense.objects.all().count()
        context = {'student':student,'plans':plans,'expenses':expenses}
        return render(request, 'dashboard.html',context)
    else:
        return redirect(login)
    
   

#plans
def plans(request):
     if request.user.is_authenticated:
         plans = Plan.objects.all()
         return render(request,'plans.html',{'plans':plans})
     else:
         return redirect(login)
   
#add plans
def add_plan(request):
    if request.user.is_authenticated:
        if request.method == "POST":
                plan  = Plan()
                plan.gender = request.POST['gender']
                plan.planName = request.POST['name']
                plan.price = request.POST['price']
                plan.registrationFee = request.POST['registration']
                plan.save()
                messages.success(request, 'Plan created succesfully')
                return redirect('plan')      
        else:
            return render(request, 'add_plan.html')
    else:
        return redirect('login')

#delete plans        
def delete_plan(request, id):
    if request.user.is_authenticated:
        plan = Plan.objects.get(id=id)  
        plan.delete()  
        messages.warning(request,"Plan deleted Successfully")
        return JsonResponse('plan_deleted',safe=False)
    else:
        return redirect('login')

#listing all student 
def student_list(request):
    if request.user.is_authenticated:
        students =  StudentRegistration.objects.all()
        return render(request, 'student_list.html',{"students":students})
    else:
        return redirect('login')

#get plan gender wise while on student registration 
def get_plan(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            gender = request.POST['gender']
            plan = Plan.objects.filter(gender=gender)
            data_list= []
            for i in plan:
                pl = {'id':i.id,'name' :i.planName}
                data_list.append(pl)
            return JsonResponse({'plan':data_list})
    else:
        return redirect('login')

#getting plan price with plan wise 
def get_price(request):
    if request.user.is_authenticated:
        if request.method == "POST": 
            gender = request.POST['gender']
            plan = request.POST['plan']
            datas  = Plan.objects.filter(gender=gender).filter(id=plan)
            data_list= []
            for i in datas:
                data_list.append(i.price+i.registrationFee)
        # print(data_list)    
            return JsonResponse({'price':data_list})
    else:
        return redirect('login')

#registrating student after he choose the plan
def add_student(request):
    if request.user.is_authenticated:

        if request.method == "POST":        
            #posting to student registration model
            student = StudentRegistration()
            plan = Plan.objects.get(id=request.POST['plan'])
            student.plan  =  plan
            student.name  =  request.POST['name']
            student.phone =  request.POST['phone']
            student.address  = request.POST['address']
            student.age = request.POST['age']
            date = request.POST['joiningDate']
            student.joiningDate = date
            student.discription = request.POST['discription']
            if StudentRegistration.objects.filter(name = request.POST['name'],phone = request.POST['phone']).exists():
                messages.success(request, 'student already exist!')
                return redirect('student')
            else:
                print('hhyeyyeyey')
                student.save()
                #end student registration model
        
                #updating fees model also
                
                last_id = StudentRegistration.objects.latest('id')
                id = last_id.id
                student_id  = StudentRegistration.objects.get(id=id)
                fee = fees()
                fee.paidAmount = int(request.POST['paidAmount'])
                balance = int(request.POST['balanceAmount'])
               
                #status checking
                if balance == 0:
                    fee.feeStatus = True
                   
                else:
                    fee.feeStatus = False
                    
                fee.balance = balance
                fee.lastFeePaid = date
                
                fee.student = student_id
                fee.save() 
                messages.success(request, 'student added successfully')
                return redirect('student')
        return render(request, 'add_student.html')
    else:
        return redirect('login')

#edit student details
def edit_student(request,id):
    if request.user.is_authenticated:    
        student = StudentRegistration.objects.get(id=id)
        return render(request, 'edit_student.html',{'student':student})
    else:
        return redirect('login')

#updating student details
def update_student(request,id):
    if request.user.is_authenticated:
        student = StudentRegistration.objects.get(id=id)
        if request.method == "POST":
            plan = Plan.objects.get(id=request.POST['plan'])
            student.plan  =  plan
            student.name  =  request.POST['name']
            student.phone =  request.POST['phone']
            student.address  = request.POST['address']
            student.age = request.POST['age']
            student.joiningDate = request.POST['joiningDate']
            student.paidAmount = int(request.POST['paidAmount'])
            balance = int(request.POST['balanceAmount'])
            if balance == 0:
                student.feeStatus = True
                print('true')   
            else:
                student.feeStatus = False
            student.balance = balance    
            student.save()
            messages.warning(request, 'student updated successfully')
            return redirect('student')
    else:
        return redirect('login')

#deleting student 
def delete_student(request, id):
    if request.user.is_authenticated:  
        student = StudentRegistration.objects.get(id=id)  
        student.delete()  
        messages.info(request,"Deleted Successfully")
        return redirect('student')
    else:
        return redirect('login')


#fee  management start here 
def fee_payment_request(request,id):
    if request.user.is_authenticated:
        fee_payment = fees.objects.filter(student=id).latest('lastFeePaid')
        return render(request, 'fee_payment.html',{'fees':fee_payment})
    else:
        return redirect('login')
    
def fee_paid(request,id):
    if request.user.is_authenticated:
        if request.method == "POST":
            fee = fees()
            fee.paidAmount = int(request.POST['paid_amount'])
            balance = int(request.POST['balanceAmount'])
            fee.student = StudentRegistration.objects.get(id=id)
            if balance == 0:
                fee.feeStatus = True
            else:
                fee.feeStatus = False
            fee.balance = balance
            fee.lastFeePaid = request.POST['date']
            fee.save()
            return redirect('student')
    else:
        return redirect('login')
#fee management end here

#listing all fee paid student
def fee_paid1(request):
    if not request.user.is_authenticated:
        return redirect("login")
    date_range = date.today() - timedelta(days=30)
    data_list  = fees.objects.filter(lastFeePaid__gt=date_range,feeStatus=True)
    return render(request,'fee_paid.html',{'fees_paid':data_list})

#listing all fee unpaid student
def fee_unpaid(request):
  if request.user.is_authenticated:
        data_list= []
        today = date.today()
        fee_data = fees.objects.distinct("student")
        for j in fee_data:    
            student_last_paid_date = fees.objects.filter(student_id=j.student).latest("lastFeePaid")     
            if student_last_paid_date.feeStatus == True:
                out = today - student_last_paid_date.lastFeePaid
                time_between_insertion = date.today() - student_last_paid_date.lastFeePaid
                if  time_between_insertion.days>30:
                    data_list.append(student_last_paid_date)
                
            else:
                data_list.append(student_last_paid_date)
                out = today - student_last_paid_date.lastFeePaid
        # fee_data = fees.objects.all()
        
        return render(request,'fee_unpaid.html',{'fee_unpaid':data_list})
  else:
      return redirect('login')   


#listing all users
def user(request):
    if request.user.is_authenticated:   
        users = User.objects.all()
        context = {'users':users}
        return render(request, 'user_list.html',context)
    return redirect('login')

#delete existing user
def delete_user(request, id):
    if request.user.is_authenticated:   
        user = User.objects.get(id=id)
        user.delete()
        return redirect('user_list')
    return redirect('login')

#profiler
def profile(request,id):
    try:
        student = StudentRegistration.objects.get(id=id)
        fees_details = fees.objects.get(student=id)
        print(fees)
        return render(request, 'profile.html',{'students':student,'fees':fees_details})
    except Exception:
       return render(request, "404.html")



#logout
def logout(request):
    auth.logout(request)
    return redirect('login')

#page 404
def notFound(request):
    return render(request, '404.html')