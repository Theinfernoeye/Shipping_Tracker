
from django.db import models

class Admin(models.Model):
    ID  = models.AutoField(primary_key=True)
    Email = models.TextField(blank=True, null=True)
    Password = models.TextField(blank=True, null=True)
    class Meta:
        db_table="admin_list"

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




def get_state_label(state_value):
    # Define a dictionary mapping integer values to corresponding labels
    state_labels = {
        0: "Being Packaged",
        1: "Leaving warehouse",
        2: "In Air",
        3: "On Sea",
        4: "In country",
        5: "Ready for pickup",
        6: "Returned"
    }

    # Return the label corresponding to the state value, or 'Unknown' if not found
    return state_labels.get(state_value)