
#Create a package class
from typing import Any


class Package:
    def __init__(self, ID, Address, Deadline, City, Zip, Weight, Status):
        self.ID = ID
        self.Address = Address
        self.Deadline = Deadline
        self.City = City
        self.Zip = Zip
        self.Weight = Weight
        self.Status = Status

