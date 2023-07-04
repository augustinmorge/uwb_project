from xpf2py.xpf2py import xpf2py
import os
import numpy as np

date = "28_06_2023"
filename = f'{date}_PH-2248_A_POSTPROCESSING-replay.xpf'
file_name = f"\\{date}\\{filename}"
current_directory = os.path.dirname(__file__)
file_path = current_directory + file_name

print(file_path)

xpf_content,py_fileOutPath = xpf2py(file_path)
print(xpf_content.keys())
print(xpf_content["data"].keys())
print(xpf_content["data"]["RANGE_KAL_MEAS"].keys())

date_s = xpf_content["data"]['RANGE_KAL_MEAS']["date"].astype(float)/10**7
print(date_s)
print(xpf_content["data"]['RANGE_KAL_MEAS']["lbl1DistOInnov"])

print("\n####\n")

print("Start of the data at ", xpf_content["data"]["UTC"])
utc_offset = (xpf_content["data"]["UTC"]["utcHour"].astype(float) + 2)*3600 + xpf_content["data"]["UTC"]["utcMinute"].astype(float)*60 + xpf_content["data"]["UTC"]["utcSecond"].astype(float)
print(utc_offset + date_s)