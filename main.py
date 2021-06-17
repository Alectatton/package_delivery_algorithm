# Alec Tatton ID: 001469164


import importCSV
import algorithms
from algorithms import delivery_order
from algorithms import packages_on_one
from algorithms import packages_on_two
from algorithms import packages_on_three

# Create an instance of hash table
packageHash = importCSV.load_packages('packages.csv')
distanceList = importCSV.load_distances('distances.csv')

ordered_list_truck_one = delivery_order(packages_on_one)
ordered_list_truck_two = delivery_order(packages_on_two)
ordered_list_truck_three = delivery_order(packages_on_three)

# print(algorithms.update_delivery_times(ordered_list_truck_one, '8:00:00', '15:00:00'))
print(algorithms.look_up_by_package_num(33, '15:00:00', ordered_list_truck_one, ordered_list_truck_two, ordered_list_truck_three))



print(ordered_list_truck_one)
print(ordered_list_truck_two)
print(ordered_list_truck_three)


print("Distance for truck one is " + str(algorithms.route_distance(ordered_list_truck_one)) + " miles. ")
print("Distance for truck two is " + str(algorithms.route_distance(ordered_list_truck_two)) + " miles. ")
print("Distance for truck three is " + str(algorithms.route_distance(ordered_list_truck_three)) + " miles. ")


