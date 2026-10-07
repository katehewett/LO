#!/bin/bash

# These exports were completed for work for Larissa. so much. data.
# 2015 - 2025

LOe=/dat2/kmhewett/LO/extract/moor

python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2020.01.01 -1 2020.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs7.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2021.01.01 -1 2021.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs8.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2022.01.01 -1 2022.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs9.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2023.01.01 -1 2023.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs10.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2024.01.01 -1 2024.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs11.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2025.01.01 -1 2025.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs12.log
