from deepdiff import DeepDiff
import json
import os
import logging
from jycm.helper import make_ignore_order_func
from jycm.jycm import YouchamaJsonDiffer
from helper_mod import dump_html_output, open_url

logging.basicConfig(format='%(asctime)s %(message)s', datefmt='%m/%d/%Y %I:%M:%S %p')
logger=logging.getLogger()  
logger.setLevel(logging.INFO) 

def create_dir(file_path, dir_name):
    path = os.path.join(file_path, dir_name)
    os.mkdir(path)
    return path

def get_diff(data1, data2):
    ddiff = DeepDiff(data1, data2)
    if ddiff:
        return True
    else:
        return False

def dump_to_json(key, file, content):
    with open(os.path.join(key, file), 'w') as f:
        json.dump(content, f, indent=4)


def dump_to_report(file, folder, content1, content2):
    output_dir_name=file
    output_dir_report = os.path.join(folder, output_dir_name)    
    ycm = YouchamaJsonDiffer(content1, content2, ignore_order_func=make_ignore_order_func([]))
    ycm.diff()
    diff_result = ycm.to_dict()
    url = dump_html_output(content1, content2, diff_result, output_dir_report, left_title='Source', right_title='Target')

def matched_mismatched(source_data, target_data, output_dir):
    matched_folder= create_dir(output_dir, "matched")
    mismatched_folder= create_dir(output_dir, "mismatched")
    source_matched, source_mismatched= create_dir(matched_folder, "source_data"), create_dir(mismatched_folder, "source_data")
    target_matched, target_mismatched= create_dir(matched_folder, "target_data"), create_dir(mismatched_folder, "target_data")
    html_reports_matched, html_reports_mismatched = create_dir(matched_folder, "html_reports"), create_dir(mismatched_folder, "html_reports")
    for (key1, value1) , (key2,value2) in zip(source_data.items(), target_data.items()):
        key1_path= create_dir(source_matched, key1)
        key2_path= create_dir(target_matched, key2)
        key3_path= create_dir(source_mismatched, key1)
        key4_path= create_dir(target_mismatched, key2)

        report_store_matched, report_store_mismatched = create_dir(html_reports_matched, key2), create_dir(html_reports_mismatched, key2)
        for (i,j) in zip(value1,value2):
            for (file1, content1) , (file2, content2) in zip(i.items(), j.items()):
                if file1==file2:
                    result=get_diff(i[file1],j[file2])
                    if result==False:
                        dump_to_report(file1, report_store_matched, content1, content2)
                        dump_to_json(key1_path, file1, content1)
                        dump_to_json(key2_path, file2, content2)
                        
                    if result==True:
                        dump_to_report(file1, report_store_mismatched, content1, content2)
                        dump_to_json(key3_path, file1, content1)
                        dump_to_json(key4_path, file2, content2)
                       