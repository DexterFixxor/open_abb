import json
from pyquaternion import Quaternion

import abb


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
    target = [xyz, quat.q]

    target_list = [target, target, target]
    for robot in robots:
        print(f"Controlling {robot}")
        robots[robot].set_cartesian(target)


if __name__ == "__main__":
    main()
