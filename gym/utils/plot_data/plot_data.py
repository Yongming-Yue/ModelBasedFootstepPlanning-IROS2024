# 20241112 add filtered states
# 20241104 move to alip_1step, only sim
# 20240814 latest modified by YM
# 20250217 log rl data
# 20250625 plot observation and other data

import os
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from tile_figures import tileFigures

data_index = -1

display_monitor = 1
if display_monitor == 0:
    display_row = 7
    display_col = 6
    display_gap = 10
elif display_monitor == 1:
    display_row = 3
    display_col = 6
    display_gap = 10
elif display_monitor == 2:
    display_row = 8
    display_col = 6
    display_gap = 10

def rad2deg(input):
    return input / math.pi * 180
def deg2rad(input):
    return input / 180 * math.pi
def get_euler_xyz(q):
    x, y, z, w = q[:, 0], q[:, 1], q[:, 2], q[:, 3]
    # roll (x-axis rotation)
    sinr_cosp = 2.0 * (w * x + y * z)
    cosr_cosp = w * w - x * x - y * y + z * z
    roll = np.arctan2(sinr_cosp, cosr_cosp)

    # pitch (y-axis rotation)
    sinp = 2.0 * (w * y - z * x)
    pitch = np.where(np.abs(sinp) >= 1, np.sign(sinp) * np.pi/2.0, np.arcsin(sinp))

    # yaw (z-axis rotation)
    siny_cosp = 2.0 * (w * z + x * y)
    cosy_cosp = w * w + x * x - y * y - z * z
    yaw = np.arctan2(siny_cosp, cosy_cosp)

    return roll, pitch, yaw

if __name__ == '__main__':
    root = "../../../logs/Humanoid_Controller/analysis/"

    csv_files = [f for f in os.listdir(root) if os.path.isfile(os.path.join(root, f)) and f.lower().endswith(".csv")]

    if not csv_files:
        raise FileNotFoundError(f"no csv file in：{root}")

    csv_files = sorted(csv_files, key=lambda f: os.stat(os.path.join(root, f)).st_mtime, reverse=False)

    latest_file_name = csv_files[data_index]
    file_name = os.path.join(root, latest_file_name)
    # file_name = os.path.join(root, "Jul01_19-16-24_test.csv")
    print("plotting data:", file_name)

    data = pd.read_csv(file_name, index_col=False)

    ## load data
    ts = data["ts"].to_numpy()

    bp_x = data["bp_x"].to_numpy()
    bp_y = data["bp_y"].to_numpy()
    bp_z = data["bp_z"].to_numpy()
    
    bq_x = data["bq_x"].to_numpy()
    bq_y = data["bq_y"].to_numpy()
    bq_z = data["bq_z"].to_numpy()
    bq_w = data["bq_w"].to_numpy()
    roll, pitch, yaw = get_euler_xyz(np.stack([bq_x, bq_y, bq_z, bq_w], axis=1))

    bv_x = data["bv_x"].to_numpy()
    bv_y = data["bv_y"].to_numpy()
    bv_z = data["bv_z"].to_numpy()

    bw_x = data["bw_x"].to_numpy()
    bw_y = data["bw_y"].to_numpy()
    bw_z = data["bw_z"].to_numpy()  


    cmd_vx = data["cmd_vx"].to_numpy()
    cmd_vy = data["cmd_vy"].to_numpy()
    cmd_yaw = data["cmd_yaw"].to_numpy()
    
    contact_schedule = data["contact_schedule"].to_numpy()
    l_grf = data["l_grf"].to_numpy()
    r_grf = data["r_grf"].to_numpy()

    # plot data
    fig_num = 0

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, bp_x, 'r', label="bp_x [m]")
    plt.plot(ts, bp_y, 'g', label="bp_y [m]")
    plt.plot(ts, bp_z, 'b', label="bp_z [m]")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("pos")
    plt.xlabel("time [s]")
    plt.ylabel("pos [m]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(roll), 'r', label="roll [deg]")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("roll")
    plt.xlabel("time [s]")
    plt.ylabel("roll [deg]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(pitch), 'g', label="pitch [deg]")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("pitch")
    plt.xlabel("time [s]")
    plt.ylabel("pitch [deg]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(yaw), 'b', label="yaw [deg]")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("yaw")
    plt.xlabel("time [s]")
    plt.ylabel("yaw [deg]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(bw_x), 'r', label="wX_Base")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("wX_Base")
    plt.xlabel("time [s]")
    plt.ylabel("wX_Base [deg/s]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(bw_y), 'g', label="wY_Base")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("wY_Base")
    plt.xlabel("time [s]")
    plt.ylabel("wY_Base [deg/s]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, rad2deg(bw_z), 'b', label="wZ_Base")
    plt.plot(ts, contact_schedule, 'm', label="contact schedule")
    plt.title("wZ_Base")
    plt.xlabel("time [s]")
    plt.ylabel("wZ_Base [deg/s]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, bv_x, 'r', label="base_lin_vel_Base_x [m/s]")
    plt.plot(ts, cmd_vx, 'k', label="cmd_lin_vel_x [m/s]")
    plt.plot(ts, 1.5 + 1.5*contact_schedule, 'm', label="contact schedule")
    plt.title("base_lin_vel_Base")
    plt.xlabel("time [s]")
    plt.ylabel("base_lin_vel_x_Base [m/s]")
    plt.legend()
    plt.grid(True)


    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, bv_y, 'g', label="base_lin_vel_Base_y [m/s]")
    plt.plot(ts, cmd_vy, 'k', label="cmd_lin_vel_y [m/s]")
    plt.plot(ts, 0.5*contact_schedule, 'm', label="contact schedule")
    plt.title("base_lin_vel_Base")
    plt.xlabel("time [s]")
    plt.ylabel("base_lin_vel_y_Base [m/s]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, l_grf, 'b', label="left grf")
    plt.plot(ts, r_grf, 'r', label="right grf")
    plt.plot(ts, 150 + 150*contact_schedule, 'm', label="contact schedule")
    plt.title("grf")
    plt.xlabel("time [s]")
    plt.ylabel("grf [N]")
    plt.legend()
    plt.grid(True)

    fig_num = fig_num + 1
    plt.figure(fig_num)
    plt.plot(ts, bp_z, 'b', label="bp_z [m]")
    plt.plot(ts, 0.2*cmd_vx, 'r', label="0.2*cmd_lin_vel_x [m/s]")
    plt.plot(ts, 0.5 + 0.5*contact_schedule, 'm', label="contact schedule")
    plt.title("pos")
    plt.xlabel("time [s]")
    plt.ylabel("pos [m]")
    plt.legend()
    plt.grid(True)

    print("total figure: ", fig_num)

    tileFigures(fig_nums=fig_num, monitor_num=display_monitor, rows=display_row, cols=display_col, gap=display_gap)
