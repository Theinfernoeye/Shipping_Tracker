
from django.db import models

class Admin(models.Model):
    ID  = models.AutoField(primary_key=True)
    Email = models.TextField(blank=True, null=True)
    Password = models.TextField(blank=True, null=True)
    class Meta:
        db_table="admin_list"

class EagleDB(models.Model):

    MARK = models.TextField(primary_key=True)
    CUSTOMER = models.TextField(blank=True, null=True)
    BALANCE = models.TextField(blank=True, null=True)
    Date = models.DateTimeField(blank=True, null=True)
    Phone = models.IntegerField(blank=True,null=True)
    ID = models.TextField(blank=True, null=True)
    Bill_ID = models.TextField(blank=True, null=True)
    PAID = models.IntegerField(blank=True,null=True)
    SIGNED = models.IntegerField(blank=True,null=True)
    LOCATION = models.IntegerField(blank=True,null=True)

    class Meta:
        db_table="eaglemark"


class Ship(models.Model):
    Shipping_id = models.TextField(primary_key=True)
    Client_num_id = models.TextField(blank=True, null=True)
    Location= models.TextField(blank=True, null=True)
    State= models.IntegerField(blank=True, null=True)
    Arrival_Date= models.DateField(blank=True, null=True)
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




def get_Location(state_value):
    # Define a dictionary mapping integer values to corresponding labels
    state_labels = {
        0: "Botswana",
        1: "China",
        2: "Turkey"
    }

    # Return the label corresponding to the state value, or 'Unknown' if not found
    return state_labels.get(state_value)