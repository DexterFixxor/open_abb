import json
from pyquaternion import Quaternion
import numpy as np

import abb

def generateHelix_target(x0, y0, p, radius, w, z):

    x = radius * np.cos(w*z + p) + x0
    y = radius * np.sin(w*z + p) + y0

    return x,y

def generateHelix_list(size_in_mm = 100, step_in_mm = 1):
    x0 = 400
    y0 = 0
    p = 0
    w = 3.14
    radius = 50
    start_z = 300 #in mm

    quat = Quaternion(axis=[0, 1, 0], degrees=180)

    target_list = []
    for z in range(start_z, size_in_mm + start_z, step_in_mm):
        x,y = generateHelix_target(x0, y0, p, radius, w, z/10)

        target_list.append([[x,y,300 + z], quat.q])

    return target_list



def init_robots(config: json):
    rob_dict = {}

    for robot in config["robots"]:
        name = robot["name"]
        ip = robot["ip"]
        port = robot["port"]
        toolData = robot["tool_data"]
        wobj = robot["wobj"]

        newRobot = abb.Robot(
            ip=ip,
            port_motion=port,
            port_logger=port + 1
        )

        newRobot.set_tool(toolData)
        newRobot.set_workobject(wobj)

        rob_dict[name] = newRobot

    return rob_dict


def main():
    file = open("config.json")
    config_json = json.load(file)
    robots = init_robots(config_json)

    xyz = [500, 0, 350]
    quat = Quaternion(axis=[0, 1, 0], degrees=180)
    #target = [xyz, quat.q]

    target_list = generateHelix_list()

    for target in target_list:
        for robot_name in robots:
            print(f"Controlling {robot_name}")
            # MoveL - zahteva samo Target. Brzina, zona, alat i wobj se postavljaju ranije
            robots[robot_name].set_cartesian(target)
            #robots[robot_name].buffer_set(target_list)
            #robots[robot_name].buffer_execute()


if __name__ == "__main__":
    main()
