#Author: James Todaro
#Date: 08/26/2020
#Purpose: Implement a learning program using Q-learning and SARSA


import sys
import csv
import math
import copy
import random
import statistics

DELTA = 100


"""This function accepts a filename of a file which should be in csv format, and returns it as a list
"""
def read_data(filename):
    with open(filename, 'r') as csv_file:
        csv_reader = csv.reader(csv_file)
        data = []
        for row in csv_reader:
            data.append([str(v) for v in row])
    return data

def write_data(filename, data):
    f = open(filename, "a")
    for record in data:
        for index in range(len(record) - 1):
            f.write(str(record[index]) + ",")
        f.write(str(record[-1]) + "\n")
    f.close()

def get_key(xy, xy_acc):
    return str(xy[0]) + "_" + str(xy[1]) + "_" + str(xy_acc[0]) + "_" + str(xy_acc[1])

def get_sum_of_values(xy, xy_acc, action, v_of_s, track):
    x = xy[0]
    y = xy[1]
    x_acc = xy_acc[0]
    y_acc = xy_acc[1]

    new_x = x + x_acc + action[0] #80/20
    new_y = y + y_acc + action[1] #80/20
    
    if x_acc == 1: 
        new_x_prob = 0.8
        alt_x = x + x_acc
    else: new_x_prob = 1

    if y_acc == 1: 
        new_y_prob = 0.8
        alt_y = y + y_acc
    else: new_y_prob = 1

    v_of_s_vals = []
    #1 possible path
    path_of_car = car_path(x, y, new_x, new_y)
    points_moved_through = []

    for point in path_of_car:
        points_moved_through.append(track[point[1]][0][point[0]])

    if "F" in points_moved_through:
        finish = path_of_car[points_moved_through.index("F")]
        new_x = finish[0]
        new_y = finish[1]
        v_of_s_vals.append(v_of_s[get_key(new_x, new_y, x_acc, y_acc])
    elif "#" in points_moved_through:
        crash_point = points_moved_through.index("#")
        if (crash_point > 0) & big_crash:
            new_x = car_path[crash_point - 1][0]
            new_y = car_path[crash_point - 1][1]
            v_of_s_vals.append(v_of_s[get_key(new_x, new_y, 0, 0])
        else:
            new_x = x
            new_y = y
            v_of_s_vals.append(v_of_s[get_key(new_x, new_y, 0, 0])

        x_new_acc = 0
        y_new_acc = 0
    
    #2 possible path
        



""" run the value iteration algorithm
"""
def value_iteration(track):
    v_of_s = {}
    finish_line = get_start_and_finish_points(track)[1]
    coordinates = get_all_coordinates(track)
    acc_values = get_all_acc_values()
    actions = get_all_actions()
    
    #initalize v_of_s
    for xy in coordinates:
        for xy_acc in acc_values:
            v_of_s[get_key(xy, xy_acc)] = 0.5
    for xy in finish_line:
        for xy_acc in acc_values:
            v_of_s[get_key(xy, xy_acc)] = 0
    
    new_v_of_s = {}
    while True:
        for xy in coordinates:
            for xy_acc in acc_values:
                for action in actions:
                    new_v_of_s[get_key(xy, xy_acc)] = 1 + GAMMA * get_sum_of_states(xy, xy_acc, action, v_of_s)

""" returns all valid coordinate positions for a car for a given track
"""
def get_all_coordinates(track):
    coordinates = []
    for y in range(len(track)):
        for x in range(len(track[y][0])):
            if track[y][0][x] in 'S.':
                coordinates.append([x,y])
    return coordinates

""" returns a list of all possible x,y acceleration value pairs for a car state
"""
def get_all_acc_values():
    valid_acc_values = [-3, -2, -1, 0, 1, 2, 3]
    acc_values = []
    for x_acc in valid_acc_values:
        for y_acc in valid_acc_values:
            acc_values.append([x_acc, y_acc])
    return acc_values

""" creates list of all action pairs
"""
def get_all_actions():
    actions = []
    action_list = [-1, 0, 1]
    for a_x in action_list:
        for a_y in action_list:
            actions.append([a_x, a_y])
    return actions

""" returns the coordinates of the starting points (locations marked 'S' on the track)
"""
def get_start_and_finish_points(track):
    starting_points = []
    finishing_points = []
    for row_num in range(len(track)):
        for col_num in range(len(track[0][0])):
            if track[row_num][0][col_num] == 'S':
                starting_points.append([col_num, row_num])
            if track[row_num][0][col_num] == 'F':
                finishing_points.append([col_num, row_num]) 

    return [starting_points, finishing_points]

""" Dispays the track with an "X" in the location of the car
"""
def print_track(car_state, track):
    print(car_state)
    for row_num in range(len(track)):
        row = ""
        for col_num in range(len(track[0][0])):
            if (col_num == car_state[0]) & (row_num == car_state[1]):
                row += "X"
            else:
                row += track[row_num][0][col_num]
        print(row)

""" used in carpath.  Given a path it reverses the direction.
"""
def reverse(path):
    new_path = []
    for index in range(len(path) - 1, -1, -1):
        new_path.append(path[index])
    return new_path

""" used in carpath.  Given a path it will swap the x and y coordinates of each point.
"""
def swap_coords(path):
    new_path = []
    for point in path:
        new_path.append([point[1], point[0]])
    return new_path

""" used in carpath.  Given a path it reverses all the y coordinates.
"""
def swap_ys(path):
    new_path = []
    y_reverse = []
    for index in range(len(path)- 1, -1, -1):
        y_reverse.append(path[index][1])
    for index in range(len(path)):
        new_path.append([path[index][0], y_reverse[index]])
    return new_path

""" returns the coordinates that the car passes through from x1, y1 to x2, y2.  Does not include x1, x2
"""
def car_path(x1, y1, x2, y2): 
    path = []
    endpoint = [x2,y2]
    reversed = False
    swap_xy = False
    swap_y = False

    if x1 == x2: # undefined slope
        if y2 > y1:        
            for y in range (y1, y2 + 1):
                path.append([x1, y])
        else:
            for y in range (y1, y2 - 1, -1):
                path.append([x1, y])
        return path

    if x1 > x2: #left to right
        reversed = True
        x_temp = x2
        y_temp = y2
        x2 = x1
        y2 = y1
        x1 = x_temp
        y1 = y_temp
    
    if y1 > y2: #negative slope
        swap_y = True
        temp = y2
        y2 = y1
        y1 = temp

    if (y2 - y1)/(x2 - x1) > abs(1):
        swap_xy = True
        x2_temp = x2
        x1_temp = x1
        x2 = y2
        y2 = x2_temp
        x1 = y1
        y1 = x1_temp
        
    m_new = 2 * (y2 - y1)
    slope_error_new = m_new - (x2 - x1)
    y = y1
    path = []
    for x in range (x1, x2 + 1): 
        path.append([x, y])
        # Add slope to increment angle formed 
        slope_error_new += m_new

        # Slope error reached limit, time to 
        # increment y and update slope error. 
        if (slope_error_new >= 0):
            y += 1
            slope_error_new  -= 2 * (x2 - x1)
    
    if swap_y:
        path = swap_ys(path)

    if reversed:
        path = reverse(path)

    if swap_xy:
        path = swap_coords(path)
        if swap_y: path = reverse(path)

    path[-1] = endpoint
    return path[1:]

def get_new_xy (current, speed, track, is_x=True):
    max_val = len(track[0][0]) if is_x else len(track)
    speed = min(speed, 5)
    new = current + speed #max speed is 5
    
    if new >= max_val:
        new = max_val - 1
    if new < 0:
        new = 0
    print("X" if is_x else "Y", "- current:", current,"\tspeed:", speed, "\tnew:", new)
    return new


def start_race(starting_points, finishing_points, track):
    bad_crash = False
    crashed = False

    starting_line = starting_points[random.randint(0, len(starting_points)- 1)]
    time = 0
    car_location = [[starting_line[0], starting_line[1]]]
    points_moved_through = []
    car_state = [starting_line[0], starting_line[1], 0, 0] #x_t, y_t, a_x, a_y
    print("time =", time)
    print_track(car_state, track)
    while("F" not in points_moved_through):
        points_moved_through = []
        x_a = random.randint(-1, 1)
        y_a = random.randint(-1, 1)
        if x_a == 1:    
            if random.randint(1, 10) > 8: x_a = 0
        if y_a == 1:    
            if random.randint(1, 10) > 8: y_a = 0

        x_speed = 0 if (time == 0) | crashed else car_location[time][0] - car_location[time - 1][0]
        y_speed = 0 if (time == 0) | crashed else car_location[time][1] - car_location[time - 1][1]
        
        x_speed += x_a + car_state[2] #current x_acceleration
        y_speed += y_a + car_state[3] #current y_acceleration
        
        x_new = get_new_xy(car_state[0], x_speed, track)
        y_new = get_new_xy(car_state[1], y_speed, track, False)

        crashed = False
        path_of_car = car_path(car_state[0], car_state[1], x_new, y_new)
        
        for point in path_of_car:
            points_moved_through.append(track[point[1]][0][point[0]])
        
        if "#" in points_moved_through: # car hit a wall
            crashed = True
            car_state[2] = 0 # set x_a to 0
            car_state[3] = 0 # set y_a to 0
            if bad_crash:
                car_state[0] = starting_line[0]
                car_state[1] = starting_line[1]
            else:
                index_of_crash = points_moved_through.index("#")
                if index_of_crash > 0:
                    car_state[0] = path_of_car[index_of_crash - 1][0]
                    car_state[1] = path_of_car[index_of_crash - 1][1]
                else:
                    car_state[0] = car_location[time][0]
                    car_state[1] = car_location[time][1]
        else: #car did not hit a wall
            car_state[0] = x_new
            car_state[1] = y_new
            car_state[2] += x_a
            car_state[3] += y_a

        car_location.append([car_state[0], car_state[1]])
        time += 1
        print("time =", time)
        print(x_a, y_a)
        print(points_moved_through)
        print_track(car_state, track)
        input()


if __name__ == "__main__":
    
    track_name = "L-Track.txt"
    track_raw = read_data(track_name)
    num_rows = int(track_raw[0][0])
    num_cols = int(track_raw[0][1])
    track = track_raw[1:]
    start_and_finish_points = get_start_and_finish_points(track)
    #start_race(start_and_finish_points[0], start_and_finish_points[1], track)
    value_iteration(track)
    