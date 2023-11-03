import math
import csv
import numpy as np
import math3d
from scipy.spatial.transform import Rotation
import copy


new_array = []
cur_list = []
abc = []

def get_pose(position):
    # Desired end effector pose
    for i in range(len(position)):
    # for i in range(10):
        px, py, pz = position[i][0],position[i][1],position[i][2]  # Desired position (x, y, z)
        rx, ry, rz = np.deg2rad(position[i][3]), np.deg2rad(position[i][4]), np.deg2rad(0)  # Desired Euler angles (radians)

        # Create a rotation matrix from Euler angles
        r = Rotation.from_euler('XYZ', [rx, ry, rz])

        # Desired transformation matrix (position and orientation)
        desired_pose = np.identity(4)
        desired_pose[:3, :3] = r.as_matrix()  # Orientation
        desired_pose[:3, 3] = [px, py, pz]  # Position

        orient = r.as_matrix()
        pos = [px, py, pz]
        c = math3d.Transform(orient, pos)
        # print(c.pose_vector)
        cur_list.append(c.pose_vector)
    print(cur_list)

    # num = 1010
    # csv_file = f'new_xyz_data{num}.csv'
    # with open(csv_file, mode='w', newline='') as file:
    #     writer = csv.writer(file)
    #
    #     for i in range(len(cur_list)):
    #         writer.writerow(cur_list[i])

def cal_pose(r,num_waypoint):
    max_degree = 20
    for i in range(num_waypoint+1):
        deg = (math.pi * i / num_waypoint)
        x = round(r * math.cos(deg), 4)
        # y = round(r * math.sin(deg), 4)
        y = 0
        z = 0

        if i < num_waypoint/2:
            percent = i/(num_waypoint * 0.5)
            degree = max_degree * percent
            rx = round(degree,4)

            percent2 = ((num_waypoint * 0.5) - i)/(num_waypoint * 0.5)
            ry = max_degree * percent2
            ry = round(ry,4)

        else:
            percent = (i - (num_waypoint * 0.5))/(num_waypoint * 0.5)
            degree = max_degree * 1-percent
            rx = round(degree,4)

            percent2 = (i - (num_waypoint * 0.5))/(num_waypoint * 0.5)
            ry = max_degree * percent2 * -1
            ry = round(ry,4)

        rz = 0
        # print(rx)
        # pos_list = [x,y,z,rx,ry,rz]
        pos_list = [x]
        new_array.append(pos_list)
        print(f'circle  =  {new_array}')
    # reve = new_array.copy()
    # reve.reverse()
    # for j in range(len(reve)):
    #     new_array.append(reve[j])

    # print(new_array)
    return new_array

def pose_calculator(d,num_waypoint):
    r = d/2
    max_degree = 20
    num = math.floor(num_waypoint/2)
    for i in range(num + 1):
        deg = (math.pi * i) / num
        x = round(r * math.cos(deg), 4)
        y = z = rz = 0

        if i < (num+1)/2:
            percent = i/(num/2)
            degree = max_degree * percent
            rx = round(degree,4)

            percent2 = ((num/2) - i)/(num/2)
            ry = max_degree * percent2
            ry = round(ry,4)

        else:
            percent = (i - (num/2))/(num/2)
            degree = max_degree * (1-percent)
            rx = round(degree,4)

            percent2 = (i - (num/2))/(num/2)
            ry = max_degree * -percent2
            ry = round(ry,4)

        pos_list = [x,y,z,rx,ry,rz]
        abc.append(pos_list)
    # print(abc)

    first_half = abc[int(num/2):]
    second_half = abc[:int((num/2) + 1)]

    top2right = copy.deepcopy(first_half)
    for x in range(len(top2right)):
        top2right[x][4] = top2right[x][4] * -1
        top2right[x][0] = top2right[x][0] * -1

    right2btm = copy.deepcopy(second_half)
    for y in range(len(right2btm)):
        right2btm[y][3] = right2btm[y][3] * -1

    btm2left = copy.deepcopy(first_half)
    for z in range(len(btm2left)):
        btm2left[z][3] = btm2left[z][3] * -1

    left2top = copy.deepcopy(second_half)
    for w in range(len(left2top)):
        left2top[w][0] = left2top[w][0] * -1
        left2top[w][4] = left2top[w][4] * -1

    act_pose = []
    act_pose.extend(top2right)
    act_pose.extend(right2btm)
    act_pose.extend(btm2left)
    act_pose.extend(left2top)
    print(act_pose)
    print(len(act_pose))
    return act_pose

def save_file(posistion_list):
    num = 1
    csv_file = f'poslist{num}.csv'
    with open(csv_file, mode='w', newline='') as file:
        writer = csv.writer(file)

        for i in range(len(posistion_list)):
            writer.writerow(posistion_list[i])

# get =cal_pose(13.75,75)
# get_pose(get)
# print('done')

p1 = pose_calculator(30,32)  # only multiple of 4 can get 0 at start or end
save_file(p1)
print('done')

# test(pos,angleess)