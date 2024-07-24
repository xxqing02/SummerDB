from django.shortcuts import render,redirect
from . import models
from django.contrib.auth import logout
from django.http import JsonResponse
from django.db.models import Prefetch
from django.core import serializers
import random
from django.core.mail import send_mail
from django.utils import timezone
from datetime import timedelta

def home(request):
    return render(request,'home.html')

def userlogout(request):
    logout(request)
    return redirect('/entry/')


def entry(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        role = request.POST.get('role')
        
        if role == 'serviceAdvisor':
            man = models.ServiceAdvisor.objects.filter(name=username).first()
            if man and man.password == password:
                request.session['username'] = username
                print("Session set: ", request.session['username']) 
                return redirect('/service/entrust')
            else:
                context = {}
                if man:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)
    
        elif role == 'repairManager':
            man = models.RepairManager.objects.filter(name=username).first()
            if man and man.password == password:
                request.session['username'] = username
                return redirect('/repair_manage/work')
            else:
                context = {}
                if man:
                    context = {'password_error':'password_error'}
                else:
                    context = {'user_not_exist':'user_not_exist'}
                return render(request,'entry.html',context)

    return render(request,'entry.html')


def register(request):
    if request.method == 'GET':
        user_type = request.GET.get('role')

        if user_type == 'user':
            context = {'user_type':'user'}
            return render(request,'register.html',context)
        if user_type == 'serviceAdvisor': 
            context = {'user_type':'serviceAdvisor'}
            return render(request,'register.html',context)
        if user_type == 'repairMan':  
            context = {'user_type':'repairMan'}
            return render(request,'register.html',context)
        if user_type == 'repairManager': 
            context = {'user_type':'repairManager'}
            return render(request,'register.html',context)
        
    elif request.method == 'POST':
        user_type = request.POST.get('usertype')
        if user_type == 'user':
            username = request.POST.get('username')
            password = request.POST.get('password')
            phone = request.POST.get('phone')
            character = request.POST.get('character')
            models.User.objects.create(name=username,password=password,phone=phone)
            
        elif user_type == 'serviceAdvisor':
            username = request.POST.get('username')
            password = request.POST.get('password')
            models.ServiceAdvisor.objects.create(name=username,password=password)
            
        elif user_type == 'repairMan':
            username = request.POST.get('username')
            password = request.POST.get('password')
            worktype = request.POST.get('type')
            models.RepairMan.objects.create(name=username,password=password,job=worktype)

        elif user_type == 'repairManager':
            username = request.POST.get('username')
            password = request.POST.get('password')
            models.RepairManager.objects.create(name=username,password=password)

        return redirect('/entry/')
    
    return render(request,'register.html')



# Module: service advisor

def service(request):
    username = request.session.get('username')
    if request.method == 'POST':
        if request.POST.get('action') == 'changename':
            newname = request.POST.get('name')
            models.ServiceAdvisor.objects.filter(name=username).update(name=newname)
            request.session['username'] = newname
            return redirect('/service/')
        if request.POST.get('action') == 'changepassword':
            nowpassword = request.POST.get('currentPassword')
            newpassword = request.POST.get('newPassword')
            confirmpwd = request.POST.get('confirmPassword')
            context = {}
            storepwd = models.ServiceAdvisor.objects.filter(name=username).first().password
            if storepwd != nowpassword:
                context = {'password_error':'password error','username':username}
                return render(request,'serviceAdvisor/index.html',context)
            if newpassword != confirmpwd:
                context = {'confirm_error':'confirm error','username':username}
                return render(request,'serviceAdvisor/index.html',context)
            
            models.ServiceAdvisor.objects.filter(name=username).update(password=newpassword)
            return redirect('/logout/')
        
    return render(request,'serviceAdvisor/index.html',{'username':username})


def showProject(request):
    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            projectname = request.POST.get('project')
            person_cost = request.POST.get('labor_cost')
            material_cost = request.POST.get('material_cost')
            print(projectname,person_cost,material_cost)
            item = models.RepairProject.objects.create(projectName=projectname,
                                                        laborCost=person_cost,
                                                        materialCost=material_cost)

        if request.POST.get('action') == 'delete':
            projectid = request.POST.get('id')
            models.RepairProject.objects.filter(id=projectid).delete()

        if request.POST.get('action') == 'update':
            projectid = request.POST.get('id')
            person_cost = request.POST.get('labor_cost')
            material_cost = request.POST.get('material_cost')
            models.RepairProject.objects.filter(id=projectid).update(laborCost=person_cost,
                                                                          materialCost=material_cost)
        return redirect('/service/project')
    
    repair_project = models.RepairProject.objects.all()
    return render(request,'serviceAdvisor/project.html',{'repair_project':repair_project})


def entrust(request):
    service_name = request.session.get('username')
    print("service_name:",service_name)
    service_id = models.ServiceAdvisor.objects.filter(name=service_name).first().id
    user_list = models.User.objects.all()
    
    entrust_list = models.RepairCommission.objects.prefetch_related(
        Prefetch('phone', queryset=models.MobilePhone.objects.all()),
        Prefetch('user', queryset=models.User.objects.all())
    )
    
    entrust_data = []
    for entrust in entrust_list:
        entrust_info = {
            'id': entrust.id,
            'phone_id': entrust.phone.id if entrust.phone else 'No Mobilephone Info',
            'imei': entrust.phone.imei if entrust.phone else 'No Mobilephone Info',
            'user_name': entrust.user.name if entrust.user else 'No User Info',
            'fault_info': entrust.faultInfo,
            'repair_type': entrust.repairType,
            'material_cost': entrust.materialCost,
            'labor_cost': entrust.laborCost,
            'is_carried': entrust.isCarried,
            'is_finished': entrust.isFinished,
            'is_paid': entrust.isPaid,
        }
        entrust_data.append(entrust_info)

    entrust_data.sort(key=lambda x: x['repair_type'] != 'urgent')
    entrust_data.sort(key=lambda x: x['is_paid'] == True)
    info_list =  {'user_list':user_list,'entrust_data':entrust_data}

    if request.method == 'POST':
        if request.POST.get('action') == 'add':
            user_id = request.POST.get('customer_id')
            phone_id = request.POST.get('phone_id')
            error_info = request.POST.get('fault_description')
            repair_type = request.POST.get('repair_type')
            print(user_id,phone_id,error_info,repair_type)
            commission = models.RepairCommission.objects.create(user_id=user_id,
                                                                 serviceAdvisor_id=service_id,
                                                                 phone_id=phone_id,
                                                                 faultInfo=error_info,
                                                                 repairType=repair_type,
                                                                 )
            return redirect('/service/entrust')

    return render(request,'serviceAdvisor/entrust.html',info_list)


def entrust_delete(request):
    entrust_id = request.GET.get('id')
    models.RepairCommission.objects.filter(id=entrust_id).delete()
    return redirect('/service/entrust')

def entrust_pay(request):
    entrust_id = request.GET.get('id')
    models.RepairCommission.objects.filter(id=entrust_id).update(isPaid=True)
    return  redirect('/service/entrust')

def entrust_details(request):
    entrust_id = request.GET.get('id')
    entrust = models.RepairCommission.objects.filter(id=entrust_id).first()
    entrust_info = {
        'id': entrust.id,
        'phone_id': entrust.phone.id,
        'imei': entrust.phone.imei,
        'user_name': entrust.user.name,
        'fault_info': entrust.faultInfo,
        'material_cost': entrust.materialCost,
        'labor_cost': entrust.laborCost,
        'repair_type': entrust.repairType,
        'is_carried': entrust.isCarried,
        'is_finished': entrust.isFinished,
        'is_paid': entrust.isPaid
    }
    return render(request,'serviceAdvisor/details.html',entrust_info)

def get_phones(request):
    user_id = request.GET.get('customer_id')
    phone = models.UserPhones.objects.filter(user_id=user_id)
    phone_list = [{
            'id': item.phone_id,
            'imei': item.phone.imei,
            'model': item.phone.model
            } for item in phone.select_related('phone')]   
    return JsonResponse(phone_list,safe=False)



# Module: repair manager

def check_cost(request):
    commission_all = models.RepairCommission.objects.filter(isFinished=True,isPaid=False,totalCost=0).all()
    commission_list = []
    for commission in commission_all:
        labor_cost = material_cost = 0
        orders = models.RepairOrder.objects.filter(repairCommission=commission).all()
        for order in orders:
             labor_cost += models.RepairProject.objects.filter(projectName=order.project).first().laborCost
             material_cost += models.RepairProject.objects.filter(projectName=order.project).first().materialCost
        
        models.RepairCommission.objects.filter(id=commission.id).update(materialCost=material_cost,
                                                                          laborCost=labor_cost)
        
        imei = models.MobilePhone.objects.filter(id=commission.phone.id).first().imei
        info = {
            'id':commission.id,
            'imei':imei,
            'fault_info':commission.faultInfo,
            'material_cost':commission.materialCost,
            'labor_cost':commission.laborCost,
            'total_cost':commission.totalCost
        }
        commission_list.append(info)

    if request.method == 'POST':
        commission_id = request.POST.get('commission_id')
        material_cost = request.POST.get('material_cost')
        labor_cost = request.POST.get('labor_cost')
        total_cost = request.POST.get('total_cost')
        models.RepairCommission.objects.filter(id=commission_id).update(materialCost=material_cost,
                                                                          laborCost=labor_cost,
                                                                          totalCost=total_cost)
        return redirect('/repairManager/check_cost')
    
    return render(request,'repairManager/check_cost.html',{'commission_list':commission_list})


def manageIndex(request):
    username = request.session.get('username')
    if request.method == 'POST':
        if request.POST.get('action') == 'changename':
            newname = request.POST.get('name')
            models.RepairManager.objects.filter(name=username).update(name=newname)
            request.session['username'] = newname
            return redirect('/repair_manage/')
        if request.POST.get('action') == 'changepassword':
            nowpassword = request.POST.get('currentPassword')
            newpassword = request.POST.get('newPassword')
            confirmpwd = request.POST.get('confirmPassword')
            context = {}
            storepwd = models.RepairManager.objects.filter(name=username).first().password
            if storepwd != nowpassword:
                context = {'password_error':'password_error','username':username}
                return render(request,'repairManager/index.html',context)
            if newpassword != confirmpwd:
                context = {'confirm_error':'confirm_error','username':username}
                return render(request,'repairManager/index.html',context)
            
            models.RepairManager.objects.filter(name=username).update(password=newpassword)
            return redirect('/logout/')
        
    return render(request,'repairManager/index.html',{'username':username})


def manageTask(request):
    entrust_list = models.RepairCommission.objects.prefetch_related(
        Prefetch('phone', queryset=models.MobilePhone.objects.all()),
        Prefetch('user', queryset=models.User.objects.all())
        ).filter(isCarried=False).all()
    
    entrust_data = []
    for entrust in entrust_list:
        entrust_info = {
            'id': entrust.id,
            'user_name': entrust.user.name if entrust.user else 'No User Info',
            'imei': entrust.phone.imei if entrust.phone else 'No Phone Info',
            'phone_model': entrust.phone.model if entrust.phone else 'No Phone Info',
            'fault_info': entrust.faultInfo,
            'repair_type': entrust.repairType,
            'is_paid': entrust.isPaid,
        }
        entrust_data.append(entrust_info)
    
    entrust_data.sort(key=lambda x: x['repair_type'] != 'urgent') 
    
    repair_project = models.RepairProject.objects.all()
    repair_man = models.RepairMan.objects.all()
    repair_project_json = serializers.serialize('json', repair_project)
    repair_man_json = serializers.serialize('json', repair_man)

    data = {
        'entrust_data': entrust_data, 
        'repair_project': repair_project_json,
        'repair_man':repair_man_json
    }

    # 分配任务
    if request.method == 'POST':
        commission_id = request.POST.get('commission_id')
        projects = request.POST.getlist('projects[]')
        times = request.POST.getlist('times[]')
        men = request.POST.getlist('men[]')
        print(commission_id,projects,times,men)
        for project_id,time,man_id in zip(projects,times,men):
            man = models.RepairMan.objects.filter(id=man_id).first()
            projectname = models.RepairProject.objects.filter(id=project_id).first().projectName
            commission = models.RepairCommission.objects.filter(id=commission_id).first()
            order = models.RepairOrder.objects.create(project=projectname,
                                                        repairMan=man,
                                                        repairCommission=commission)
            
        models.RepairCommission.objects.filter(id=commission_id).update(isCarried=True) 
   
        return redirect('/repair_manage/work')

    return render(request,'repairManager/work.html',data)


# wechat applet

def user_login(request):
    if request.method == "GET":
        username = request.GET.get('username')
        password = request.GET.get('password')

        user = models.User.objects.filter(name=username, password=password).first()
        if user:
            return JsonResponse({'status': 'success', 'message': '登录成功'})

        # 如果用户模型中未找到，尝试在维修人员模型中查找
        repairpeople = models.RepairMan.objects.filter(name=username, password=password).first()
        if repairpeople:
            return JsonResponse({'status': 'success', 'message': '登录成功'})

        # 未找到
        return JsonResponse({'status': 'fail', 'message': '用户名或密码错误'})



def sendVerificateCode(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(name=username).first()
    if not user:
        return JsonResponse({'status': 'fail', 'message': '用户名不存在'})

    userEmail = user.email
    code = random.randint(100000, 999999)
    send_mail(
        '国产之星维修端密码重置',
        f'尊敬的用户你好,你的验证码是{code},验证码10分种内有效。',
        'jovanwan6@gmail.com',
        [userEmail],
        fail_silently=False,
    )

    models.Verification.objects.filter(email=userEmail).delete()

    models.Verification.objects.create(
        email=userEmail,
        code=code,
        expiresAt=timezone.now() + timedelta(minutes=10)
    )

    return JsonResponse({'status': 'success', 'message': '验证码已发送，请查看您的邮箱'})


def resetUserPassword(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(name=username).first()
    if not user:
        return JsonResponse({'status': 'fail', 'message': '用户名不存在'})
    
    newpassword = request.GET.get('password')
    verificateCode = request.GET.get('verificateCode')

    verification = models.Verification.objects.filter(email=user.email).first()
    if not verification or verification.code != verificateCode:
        return JsonResponse({'status': 'fail', 'message': '验证码错误'})
    if verification.expires_at < timezone.now():
        return JsonResponse({'status': 'fail', 'message': '验证码已过期'})

    else:
        user.password = newpassword
        user.save()

        verification.delete()

        return JsonResponse({'status': 'success', 'message': '密码重置成功'})



def user_managephone(request):
    if request.method == "GET":
        action = request.GET.get('action')
        username = request.GET.get('username')
        if action == "inquire":
            user = models.User.objects.filter(name=username).first()
            user_phone = models.UserPhones.objects.filter(user=user).all()
            phone_list = [{ 'model': phone.phone.model,
                            'imei': phone.phone.imei,
                        } for phone in user_phone ]
            return JsonResponse(phone_list,safe=False)
        
        elif action == "add":
            model = request.GET.get('model')
            imei = request.GET.get('imei')
            phone = models.MobilePhone.objects.create(model=model,imei=imei)
            user = models.User.objects.filter(name=username).first()
            models.UserPhones.objects.create(user=user,phone=phone)
            return JsonResponse({'status': 'success', 'message': '添加成功'})
        
        elif action == "delete":
            imei = request.GET.get('imei')
            if models.RepairCommission.objects.filter(phone__imei=imei).first():
                return JsonResponse({'status': 'fail', 'message': '该手机维修中,无法删除'})
            models.MobilePhone.objects.filter(imei=imei).first().delete()
            return JsonResponse({'status': 'success', 'message': '删除成功'})
        

# details of commission
def commission(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(name=username).first()
    entrust = models.RepairCommission.objects.filter(user=user,isPaid=False).all()
    entrust_list = []
    for item in entrust:
        imei = models.MobilePhone.objects.filter(id=item.phone.id).first().imei
        model = models.MobilePhone.objects.filter(id=item.phone.id).first().model
        info = {
            'id':item.id,
            'imei':imei,
            'model':model,
            'fault_info':item.faultInfo,
            'material_cost': item.materialCost,
            'labor_cost':item.laborCost,
            'create_time':item.time,
            'is_carried':item.isCarried,
            'is_finshed':item.isFinished,
        }
        entrust_list.append(info)
    return JsonResponse(entrust_list,safe=False)

# inquire progress
def progressquery(request):
    entrust_id = request.GET.get('entrust_id')
    entrust = models.RepairCommission.objects.filter(id=entrust_id).first()
    orders = models.RepairOrder.objects.filter(repairCommission=entrust).all()
    numbers = len(orders)
    finished = orders.filter(isFinished=True).count()
    order_progress = []
    for order in orders:
        order_info = {
            'project': order.project,
            'progress':order.isFinished,
        }
        order_progress.append(order_info)
    progress = {
        'numbers': numbers,
        'finished': finished,
        'order_progress': order_progress
    }

    return JsonResponse(progress,safe=False)


def get_commissionhistory(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(name=username).first()
    entrust_list = models.RepairCommission.objects.filter(user=user,isPaid=True).all()
    entrust_data = []
    for item in entrust_list:
        entrust_info = {
            'id': item.id,
            'imei': models.MobilePhone.objects.filter(id=item.phone.id).first().imei,
            'fault_info': item.faultInfo,
            'material_cost': item.materialCost,
            'labor_cost': item.laborCost,
            'total_cost': item.totalCost,
            'time': item.time,
            'is_carried': item.isCarried,
            'is_finished': item.isFinished,
            'is_paid': item.isPaid
        }
        entrust_data.append(entrust_info)
    return JsonResponse(entrust_data,safe=False)


def getUserInfo(request):
    username = request.GET.get('username')
    user = models.User.objects.filter(name=username).first()
    info = {
        'name': user.name,
        'phone': user.phone,
        'password': user.password,
        'birthday': user.birthday,
        'email': user.email,
        'gender':user.gender
    }
    return JsonResponse(info,safe=False)
        
def setUserInfo(request):
    username = request.GET.get('name')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    password = request.GET.get('password')
    gender = request.GET.get('gender')
    birthday = request.GET.get('birthday')
    print(username,phone,email,gender,birthday)
    updated_count = models.User.objects.filter(name=username).update(
        phone=phone, email=email, password=password, gender=gender, birthday=birthday
    )

    if updated_count == 0:
        print("没有找到对应的用户")
        return JsonResponse({'status': 'error', 'message': '没有找到对应用户'})

    return JsonResponse({'status': 'success', 'message': '修改成功'})
                                                    
    
# repair_man
def get_order(request):
    username = request.GET.get('username')
    repair_man = models.RepairMan.objects.filter(name=username).first()
    task = models.RepairOrder.objects.filter(repairMan=repair_man).all()
    task_list = []
    for item in task:
        repair_commission = models.RepairCommission.objects.filter(id=item.repairCommission.id).first()
        phone = models.MobilePhone.objects.filter(id=repair_commission.phone.id).first()
        if item.isFinished:
            continue
        task_info = {
            'id': item.id,
            'project': item.project,
            'is_finished': item.isFinished,
            'model': phone.model,
        }
        task_list.append(task_info)
    return JsonResponse(task_list,safe=False)


def repair_finsh(request):
    id = request.GET.get('id')
    repair_order = models.RepairOrder.objects.filter(id=id).first()
    repair_order.isFinished=True
    repair_order.save()
    commission = models.RepairCommission.objects.filter(id=repair_order.repairCommission.id).first()
    orders = models.RepairOrder.objects.filter(repairCommission=commission)    
    all_finish = True
    for item in orders:
        if item.isFinished == False:
            all_finish=False
            break
    if all_finish:
        commission.isFinished=True
        commission.save()

    return JsonResponse({'status': 'success', 'message': '维修完成'})
