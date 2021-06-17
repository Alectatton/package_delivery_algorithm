import copy
import datetime
import time

from importCSV import load_distances
from importCSV import load_packages
from importCSV import load_address
import math


packageHash = load_packages('packages.csv')
distanceList = load_distances('distances.csv')
addressList = load_address('address.csv')

# Create arrays and variables for package and order data
packages_on_one = [1, 2, 4, 5, 7, 8, 10, 11, 12, 17, 18, 21, 22, 23, 24, 33]
packages_on_two = [3, 13, 14, 15, 16, 19, 20, 26, 27, 29, 30, 31, 36, 38, 39, 40]
packages_on_three = [6, 9, 25, 28, 32, 34, 35, 37]

ordered_package_list = []


# Get address for location
def get_address(num):
    return packageHash.search(num).Address


# Get distance between two locations based on a row and column
def get_distance(row, column):
    distance = distanceList[row - 1][column - 1]
    if distance.strip() == '0.0':
        distance = 0.0
    else:
        distance = float(distance)
    return distance


# Get shortest distance from one point to
def get_shortest_distance(row):
    distance = get_distance(row, 0)
    for col in range(0, 27):
        if distanceList[row][col] < distance:
            distance = distanceList[row][col]

    return distance


# Find a location index on distances and address lists from a package number
def find_location_index(package_num):
    package_address = packageHash.search(package_num).Address
    for i in range(0, len(addressList) + 1):
        if package_address.strip() == addressList[i][2].strip():
            address_index = addressList[i][0]
            return int(address_index)


# Find a package number from an address number on distances list
def find_package_from_address(address):
    for i in range(0, 40):
        address_to_compare = addressList[i][2]
        if packageHash.search(address).Address.strip() == address_to_compare.strip():
            return i


# Greedy algorithm with recursion
# Takes a list of packages on a truck as an input, and the current package i.e. one that has just been delivered
def greedy_function(input_list, current_package):
    if len(input_list) == 0:
        pass
    else:
        distance = 100.0
        current_location = find_location_index(current_package)

        for i in range(1, len(input_list) + 1):
            if get_distance(current_location, find_location_index(input_list[i - 1])) <= distance:
                distance = get_distance(current_location - 1, find_location_index(i))
                current_location = find_location_index(i)
                next_order = input_list[i - 1];

        input_list.remove(next_order)
        ordered_package_list.append(next_order)
        greedy_function(input_list, next_order)

    return ordered_package_list


# Input a list and return an ordered list
def delivery_order(input_list):
    starting_location = 1
    ordered_list = copy.copy(greedy_function(input_list, starting_location))
    ordered_package_list.clear()
    return ordered_list


# Find amount of distance travelled for a package order
# List of packages in order for input
def route_distance(ordered_list):
    distance = 0.0
    for i in range(0, len(ordered_list) - 1):
        location_one = find_location_index(ordered_list[i])
        location_two = find_location_index(ordered_list[i + 1])
        distance += float(distance_between_packages(location_one, location_two))

    return round(distance, 1)


# Find distance between two addresses
def distance_between_packages(ad_one, ad_two):
    distance = float(distanceList[ad_one - 1][ad_two - 1])
    return distance


# Set status for truck 1 given a start time
# End time is used for lookup at given times
def update_delivery_times(input_list, start_time, end_time):
    total_distance = 0
    start_time_obj = datetime.datetime.strptime(start_time, '%H:%M:%S').time()
    end_time_obj = datetime.datetime.strptime(end_time, '%H:%M:%S').time()
    speed = 18.0  # 18 mph drive speed

    # Once this function is called, assume the truck has left to deliver packages
    for i in range(0, len(input_list) - 1):
        newPackage = packageHash.search(input_list[i])
        newPackage.Status = "En route"
        packageHash.insert(input_list[i], newPackage)

    # Find distances and delivery time for the next package in the list
    for i in range(0, len(input_list) - 1):

        location_one = find_location_index(input_list[i])
        location_two = find_location_index(input_list[i + 1])
        distance = float(distance_between_packages(location_one, location_two))
        total_distance += distance
        time_to_deliver = int(distance / speed * 3600)

        delivery_time_obj = datetime.datetime.combine(datetime.date.today(), start_time_obj) + datetime.timedelta(
            seconds=time_to_deliver)
        delivery_time_str = delivery_time_obj.strftime("%H:%M:%S")

        start_time_obj = delivery_time_obj.time()

        # Update packages with delivery time after they are delivered
        # If past the lookup time, do not update
        if start_time_obj < end_time_obj:
            newPackage = packageHash.search(input_list[i + 1])
            status_string = "Delivered at " + delivery_time_str
            newPackage.Status = status_string
            packageHash.insert(input_list[i + 1], newPackage)

        else:
            pass

    return packageHash


# Look up a packages status by package number
# Updates status for each object in the hash table at a given time
def look_up_by_package_num(package_num, lookup_time, ordered_one, ordered_two, ordered_three):
    update_delivery_times(ordered_one, "8:00:00", lookup_time)
    update_delivery_times(ordered_two, "9:05:00", lookup_time)
    three_leave_time = find_truck_three_leave_time(ordered_one)
    update_delivery_times(ordered_three, three_leave_time, lookup_time)
    return packageHash.search(package_num).Status


# Only two drivers, so one truck must return to the hub before three can depart
# Since truck one is leaving first, on return truck three will depart
def find_truck_three_leave_time(ordered_one):
    truck_one_distance = route_distance(ordered_one)
    last_package = ordered_one[len(ordered_one) - 1]
    return_distance = get_distance(find_location_index(last_package), 1)
    total_trip_time = (truck_one_distance + return_distance) / 18 * 3600

    start_time = "08:00:00"
    start_time_obj = datetime.datetime.strptime(start_time, '%H:%M:%S').time()

    leave_time_obj = datetime.datetime.combine(datetime.date.today(), start_time_obj) + datetime.timedelta(
        seconds=total_trip_time)
    leave_time_str = leave_time_obj.strftime("%H:%M:%S")

    return leave_time_str


def show_all_packages_at_time():
    return None
