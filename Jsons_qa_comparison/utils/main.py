from jycm.helper import make_ignore_order_func
from jycm.jycm import YouchamaJsonDiffer
from helper_mod import dump_html_output, open_url
# from jycmm.helper_mod import dump_html_output, open_url
import os
from datetime import datetime
from fetch_data import source_target_path, check_path, get_data
from separate_folders import create_dir, matched_mismatched



path = os.getcwd()
abs_path=os.path.abspath(os.path.join(path, os.pardir))

source_store = input('Enter source stores folder name: \n')
target_store = input('Enter target stores folder name: \n')
src_file_folder=source_target_path(r"/source/"+source_store)
source_data = get_data(src_file_folder)

target_file_folder=source_target_path(r"/target/"+target_store)
target_data = get_data(target_file_folder)
          
    
ycm = YouchamaJsonDiffer(source_data, target_data, ignore_order_func=make_ignore_order_func([]))
ycm.diff()

report_path=check_path(r"\report")
if report_path=="path dont exist":
    report_path=create_dir(abs_path, "report")
        
diff_result = ycm.to_dict()
output_dir_name="jycm_output_"+datetime.now().strftime("%Y_%m_%d_%H_%M")
output_dir = os.path.join(report_path, output_dir_name)

url = dump_html_output(source_data, target_data, diff_result, output_dir, left_title='Source', right_title='Target')
open_url(url)

matched_mismatched(source_data, target_data, output_dir)