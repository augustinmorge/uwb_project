import os
import numpy as np
# import pyproj
from xpf2py.xpf2py import xpf2py

# TEST = ['11_07_2023']
# TEST = ['17_07_2023_2']
TEST = ['26_07_2023']

current_directory = os.path.dirname(__file__)

for test in TEST:
    ref_std_10cm,_ = xpf2py(f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-navdiff-01.xpf")
    ref_std_50cm,_ = xpf2py(f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-navdiff-02.xpf")#['data']['NAV_DIFF']['horizontalSep']
    ref_std_adapt,_ = xpf2py(f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-navdiff-03.xpf")#['data']['NAV_DIFF']['horizontalSep']
    ref_std_1m, _ = xpf2py(f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-navdiff-04.xpf") 
    ref_std_adapt_2, _ = xpf2py(f"{current_directory}\\..\\{test}\\{test}_PH-2248_A_POSTPROCESSING-navdiff-05.xpf") 

    ref_std_10cm_date = ref_std_10cm['data']['NAV_DIFF']['date']/10**7
    ref_std_50cm_date = ref_std_50cm['data']['NAV_DIFF']['date']/10**7
    ref_std_adapt_date = ref_std_adapt['data']['NAV_DIFF']['date']/10**7
    ref_std_1m_date = ref_std_1m['data']['NAV_DIFF']['date'] / 10 ** 7
    ref_std_adapt_2_date = ref_std_adapt_2['data']['NAV_DIFF']['date'] / 10 ** 7

    if test == '11_07_2023':
        start_movement = 1110/60
        end_movement = 2400/60
    elif test == '17_07_2023':
        start_movement = 17
        end_movement = 46
    else:
        start_movement = 18 #min
        end_movement = 60 #min
    print(f"Crop from {start_movement}min to {end_movement}min")
    mask_ref_std_10cm_date = ((ref_std_10cm_date > start_movement*60) & (ref_std_10cm_date < end_movement*60))
    mask_ref_std_50cm_date = ((ref_std_50cm_date > start_movement*60) & (ref_std_50cm_date < end_movement*60))
    mask_ref_std_adapt_date = ((ref_std_adapt_date > start_movement*60) & (ref_std_adapt_date < end_movement*60))
    mask_ref_std_1m_date = ((ref_std_1m_date > start_movement * 60) & (ref_std_1m_date < end_movement * 60))
    mask_ref_std_adapt_2_date = ((ref_std_adapt_2_date > start_movement * 60) & (ref_std_adapt_2_date < end_movement * 60))

    ref_std_10cm_horizontalSep = ref_std_10cm['data']['NAV_DIFF']['horizontalSep'].astype(float)
    ref_std_50cm_horizontalSep = ref_std_50cm['data']['NAV_DIFF']['horizontalSep'].astype(float)
    ref_std_adapt_horizontalSep= ref_std_adapt['data']['NAV_DIFF']['horizontalSep'].astype(float)
    ref_std_1m_horizontalSep = ref_std_1m['data']['NAV_DIFF']['horizontalSep'].astype(float)
    ref_std_adapt_2_horizontalSep = ref_std_adapt_2['data']['NAV_DIFF']['horizontalSep'].astype(float)
    
    print(f"Mean for 10cm : {int(np.mean(ref_std_10cm_horizontalSep[mask_ref_std_10cm_date])*1000)/10}cm")
    print(f"Mean for 50cm : {int(np.mean(ref_std_50cm_horizontalSep[mask_ref_std_50cm_date])*1000)/10}cm")
    print(f"Mean for Adapt : {int(np.mean(ref_std_adapt_horizontalSep[mask_ref_std_adapt_date])*1000)/10}cm")
    print(f"Mean for 1m : {int(np.mean(ref_std_1m_horizontalSep[mask_ref_std_1m_date]) * 1000) / 10}cm")
    print(f"Mean for Adapt 2 : {int(np.mean(ref_std_adapt_2_horizontalSep[mask_ref_std_adapt_2_date]) * 1000) / 10}cm\n")

    print(f"std for 10cm : {int(np.std(ref_std_10cm_horizontalSep[mask_ref_std_10cm_date])*1000)/10}cm")
    print(f"std for 50cm : {int(np.std(ref_std_50cm_horizontalSep[mask_ref_std_50cm_date])*1000)/10}cm")
    print(f"std for Adapt : {int(np.std(ref_std_adapt_horizontalSep[mask_ref_std_adapt_date])*1000)/10}cm")
    print(f"std for 1m : {int(np.std(ref_std_1m_horizontalSep[mask_ref_std_1m_date]) * 1000) / 10}cm")
    print(f"std for Adapt 2 : {int(np.std(ref_std_adapt_2_horizontalSep[mask_ref_std_adapt_2_date]) * 1000) / 10}cm")
