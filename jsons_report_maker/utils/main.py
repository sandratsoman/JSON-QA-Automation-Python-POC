import os
from datetime import datetime
from fetch_data import source_target_path, check_path, get_data
from separate_folders import create_dir, matched_mismatched


path = os.getcwd()
abs_path=os.path.abspath(os.path.join(path, os.pardir))

source_store = input('Enter source stores folder name: \n')
target_store = input('Enter target stores folder name: \n')
src_file_folder=source_target_path(r"/source/"+source_store)
target_file_folder=source_target_path(r"/target/"+target_store)


source_data = get_data(src_file_folder)
target_data = get_data(target_file_folder)

report_path=check_path(r"\report")
if report_path=="path dont exist":
    report_path=create_dir(abs_path, "report")
        

report_folder_name="report_"+datetime.now().strftime("%Y_%m_%d_%H_%M")
report_folder = create_dir(report_path, report_folder_name)

matched_mismatched(source_data, target_data, report_folder)



