'''
@Xuan Luo (xuanluo@lbl.gov)

'''
from subprocess import run
from multiprocessing import Pool
import os, sys, json

type_tags = {
			 'SSF': 'model_SSF_vin_6_cz_9-baseline', 
			 'LSF': 'model_LSF_vin_6_cz_9-baseline',
			 'MF': 'model_MF_vin_6_cz_9-baseline',
			 'LOffice': 'ASHRAE90.1_OfficeLarge_STD2010_SanDiego_new',
			 'MOffice': 'ASHRAE9012016_OfficeMedium_Denver', 
             'SOffice': 'ASHRAE90.1_OfficeSmall_STD2010_SanDiego_new',
             'SRetail': 'ASHRAE90.1_RetailStripmall_STD2010_SanDiego_new.idf', 
             'LRetail': 'ASHRAE9012016_RetailStandalone_Denver', 
             'SHotel': 'ASHRAE9012016_HotelSmall_Denver', 
             'LHotel': 'ASHRAE9012016_HotelLarge_Denver', 
             'Warehouse': 'ASHRAE9012016_Warehouse_Denver', 
             'SRestaurant': 'ASHRAE9012016_RestaurantSitDown_Denver', 
             'LRestaurant': 'ASHRAE9012016_RestaurantSitDown_Denver', 
             'School': 'ASHRAE9012016_School_Denver', 
             'Hospital': 'ASHRAE9012016_Hospital_Denver', 
             'None': 'model_LSF_vin_6_cz_9-baseline'
            }

wrf_id_list = list()
with open('bldg-wrf-mapping/wrf_to_bldgs.json', 'r') as f:
    data = json.load(f)
    wrf_id_list = data[type_tag]

NUM_OF_PROCESS = 24 

WRF_FOLDER = 'M02_EnergyPlus_Forcing_Historical'
WORK_FOLDER = 'ref_buildings'

def run_eplus(wrf_list):

	for wrf_id in wrf_list:
	    wrf_id = str(wrf_id)
	    for type_tag in type_tags:
		    model_name = type_tags[type_tag]

		    epw_name = os.path.join(WRF_FOLDER, 'wrf_epw', str(wrf_id) + '.epw')
		    if not os.path.exists(epw_name):
		    	continue
		    prefix = os.path.join(type_tag, wrf_id + '-' + type_tag)

		    if os.path.isdir(WORK_FOLDER):
                run(['python', 'run_eplus.py', model_name, WORK_FOLDER, epw_name, prefix])
                run(['mv', os.path.join(WORK_FOLDER, prefix, 'eplusout.csv'), os.path.join(WORK_FOLDER, prefix + '-out.csv')])
                run(['mv', os.path.join(WORK_FOLDER, prefix, 'eplustbl.xml'), os.path.join(WORK_FOLDER, prefix + '-tbl.xml')])
                run(['cp', os.path.join(WORK_FOLDER, prefix + '-out.csv'), os.path.join(WORK_FOLDER, 'results-base-csv', wrf_id + '-' + type_tag + '-out.csv')])
                run(['cp', os.path.join(WORK_FOLDER, prefix + '-tbl.xml'), os.path.join(WORK_FOLDER, 'results-base-xml', wrf_id + '-' + type_tag + '-tbl.xml')])
		    else:
		    	raise Exception('Error: ' + WORK_FOLDER + ' is not a directory')

if __name__ == '__main__':
	run_set = list()
	total_size = len(wrf_id_list)
	thread_size = int(total_size / NUM_OF_PROCESS) + 1

	end_num = 0
	for set_num in range(NUM_OF_PROCESS - 1):
	    start_num = set_num * thread_size
	    end_num = (set_num + 1) * thread_size
	    run_set.append(wrf_id_list[start_num: end_num])
	    
	run_set.append(wrf_id_list[end_num: ])

	pool = Pool(NUM_OF_PROCESS) 
	results = pool.map(run_eplus, run_set)

	pool.close() 
	pool.join()
