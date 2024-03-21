
from django.db import models

class Admin(models.Model):
    ID  = models.AutoField(primary_key=True)
    Email = models.TextField(blank=True, null=True)
    Password = models.TextField(blank=True, null=True)
    class Meta:
        db_table="admin_list"

class Ship(models.Model):
    Shipping_id = models.AutoField(primary_key=True)
    Client_num = models.ForeignKey('User', on_delete=models.CASCADE)
    Location= models.TextField(blank=True, null=True)
    State= models.IntegerField(blank=True, null=True)
    Arrival_Date= models.IntegerField(blank=True, null=True)
    AirwayBill= models.TextField(blank=True, null=True)
    ShipBill= models.TextField(blank=True, null=True)

    class Meta:
        db_table="shipping_order"


class User(models.Model):
    Phone_number = models.AutoField(primary_key=True)
    First_name = models.TextField(blank=True, null=True)
    Last_name = models.TextField(blank=True, null=True)
    email = models.TextField(blank=True, null=True)
    Password = models.TextField(blank=True, null=True)
    class Meta:
        db_table="client_list"




