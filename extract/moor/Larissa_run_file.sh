#!/bin/bash

# These exports were completed for work for Larissa. so much. data.
# 2015 - 2025

LOe=/dat2/kmhewett/LO/extract/moor

python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2015.01.01 -1 2015.12.31 -job CEA_jobs -get_all True > Diaz_cea2.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2016.01.01 -1 2016.12.31 -job CEA_jobs -get_all True > Diaz_cea3.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2018.01.01 -1 2018.12.31 -job CEA_jobs -get_all True > Diaz_cea5.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2019.01.01 -1 2019.12.31 -job CEA_jobs -get_all True > Diaz_cea6.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2020.01.01 -1 2020.12.31 -job CEA_jobs -get_all True > Diaz_cea7.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2021.01.01 -1 2021.12.31 -job CEA_jobs -get_all True > Diaz_cea8.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2022.01.01 -1 2022.12.31 -job CEA_jobs -get_all True > Diaz_cea9.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2023.01.01 -1 2023.12.31 -job CEA_jobs -get_all True > Diaz_cea10.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2024.01.01 -1 2024.12.31 -job CEA_jobs -get_all True > Diaz_cea11.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2025.01.01 -1 2025.12.31 -job CEA_jobs -get_all True > Diaz_cea12.log

python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2018.03.01 -1 2019.09.22 -job anemone_jobs -get_all True > Diaz_anemone.log

python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2014.09.30 -1 2014.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs1.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2015.01.01 -1 2015.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs2.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2016.01.01 -1 2016.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs3.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2017.09.30 -1 2017.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs4.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2018.01.01 -1 2018.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs5.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2019.09.30 -1 2019.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs6.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2020.01.01 -1 2020.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs7.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2021.01.01 -1 2021.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs8.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2022.01.01 -1 2022.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs9.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2023.01.01 -1 2023.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs10.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2024.01.01 -1 2024.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs11.log
python3 $LOe/multi_mooring_driver.py -gtx cas7_t1_x11ab -ro 1 -lt average -0 2025.01.01 -1 2025.12.31 -job Hatchery_jobs -get_all True > Diaz_Hatchery_jobs12.log
