from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class UnactivationUser(models.Model):
    UserID = models.CharField(max_length = 100,primary_key=True)
    Password = models.CharField(max_length = 128)
    Userinf = models.ForeignKey(User, unique=True)
    Email = models.CharField(max_length = 100)
    ActivationCode = models.CharField(max_length = 128)

class Account(models.Model):
    UserID = models.CharField(max_length = 100, primary_key=True)
    Payword = models.CharField(max_length = 100)
    Challenge = models.CharField(max_length = 128)
    Balance = models.CharField(max_length = 20)

class TransactionRecord(models.Model):
    TransactionID = models.CharField(max_length = 100, primary_key=True)
    Date = models.CharField(max_length = 30)
    TransactionName = models.CharField(max_length = 100)
    Type = models.BooleanField()
    Money = models.CharField(max_length = 20)
    AnotherAccountID = models.CharField(max_length = 100)
    Account = models.ForeignKey(Account)
    State = models.CharField(max_length = 50)

class BankUser(models.Model):
    UserID = models.CharField(max_length = 100,primary_key=True)
    ActivationType = models.BooleanField(default=False)
    #Username = models.CharField(max_length = 100)
    Password = models.CharField(max_length = 128)
    Userinf = models.ForeignKey(User, unique=True)
    Random = models.CharField(max_length = 128)
    Email = models.CharField(max_length = 100)
    Phone = models.CharField(max_length = 20)
    Account = models.OneToOneField(Account)

class MyMessage(models.Model):
    UserID = models.CharField(max_length = 100,primary_key=True)
    Num = models.IntegerField()
    
class NewMessage(models.Model):
    Date = models.CharField(max_length = 30)
    Data = models.CharField(max_length = 500)
    Type = models.BooleanField(default=False)
    Belong = models.ForeignKey(MyMessage)