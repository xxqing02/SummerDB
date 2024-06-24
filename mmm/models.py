from django.db import models

class User(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20, unique=True)
    password = models.CharField(max_length=20)
    email = models.EmailField(max_length=254,null=True)
    phone = models.CharField(max_length=20)
    gender = models.CharField(max_length=10, null=True)
    birthday = models.DateField(null=True)
    
    
class MobilePhone(models.Model):
    id = models.AutoField(primary_key=True)
    imei = models.CharField(max_length=15,unique=True) # International Mobile Equipment Identifier
    model = models.CharField(max_length=20,null=True)
    color = models.CharField(max_length=20,null=True)
    price = models.FloatField(null=True)
    weight = models.FloatField(null=True)
    size = models.CharField(max_length=20,null=True)
    

class ServiceAdvisor(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20,unique=True)
    password = models.CharField(max_length=20)
    

class RepairMan(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    job = models.CharField(max_length=20)
    

class RepairManager(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=20)
    

class UserPhones(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    phone = models.ForeignKey(MobilePhone, on_delete=models.CASCADE)
    

class RepairCommission(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    serviceAdvisor = models.ForeignKey(ServiceAdvisor,on_delete=models.CASCADE)
    phone = models.ForeignKey(MobilePhone,on_delete=models.CASCADE)
    repairType = models.CharField(max_length=20,default='common') # common urgent
    faultInfo = models.CharField(max_length=100)
    materialCost  = models.FloatField(default=0)
    laborCost = models.FloatField(default=0)
    totalCost = models.FloatField(default=0)
    time = models.DateTimeField(auto_now_add=True)
    isCarried = models.BooleanField(default=False)
    isFinished = models.BooleanField(default=False)
    isPaid = models.BooleanField(default=False)


class RepairOrder(models.Model):
    id = models.AutoField(primary_key=True)
    project = models.CharField(max_length=20)
    repairMan = models.ForeignKey(RepairMan, on_delete=models.CASCADE)
    isFinished = models.BooleanField(default=False)
    repairCommission = models.ForeignKey(RepairCommission, on_delete=models.CASCADE)
    

class RepairProject(models.Model):
    id = models.AutoField(primary_key=True)
    projectName = models.CharField(max_length=20)
    laborCost = models.FloatField()
    materialCost = models.FloatField()
