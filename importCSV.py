# Package to import csv tables

import csv
import hash
import packages


# Function to load the packages into the hash table
# Use utf-8-sig encoding to remove BOM from csv
def load_packages(filename):
    with open(filename, encoding='utf-8-sig') as packageFile:
        packageData = csv.reader(packageFile, delimiter=',')

        packageHash = hash.ChainingHashTable()

        for package in packageData:
            packageID = int(package[0])
            Address = package[1]
            City = package[2]
            Zip = package[4]
            Deadline = package[5]
            Weight = package[6]
            Status = "At hub"

            package = packages.Package(packageID, Address, Deadline, City, Zip, Weight, Status)

            packageHash.insert(packageID, package)

        return packageHash


# Function to load distances from distance.csv
# Use utf-8-sig encoding to remove BOM from csv
def load_distances(filename):
    with open(filename, encoding='utf-8-sig') as distanceFile:
        data = csv.reader(distanceFile, delimiter=',')
        return list(data)


# Function to load address names from address.csv
# Use utf-8-sig encoding to remove BOM from csv
def load_address(filename):
    with open(filename, encoding='utf-8-sig') as addressFile:
        data = csv.reader(addressFile, delimiter=',')
        return list(data)