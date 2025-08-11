from deepdiff import DeepDiff
import json
import os
import logging

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

def matched_mismatched(source_data, target_data, output_dir):
    logger.info('Started separating folders')
    try:
        matched_folder= create_dir(output_dir, "matched")
        mismatched_folder= create_dir(output_dir, "mismatched")
        source_matched, source_mismatched= create_dir(matched_folder, "source_data"), create_dir(mismatched_folder, "source_data")
        target_matched, target_mismatched= create_dir(matched_folder, "target_data"), create_dir(mismatched_folder, "target_data")
        for (key1, value1) , (key2,value2) in zip(source_data.items(), target_data.items()):
            key1_path= create_dir(source_matched, key1)
            key2_path= create_dir(target_matched, key2)
            key3_path= create_dir(source_mismatched, key1)
            key4_path= create_dir(target_mismatched, key2)
            for (i,j) in zip(value1,value2):
                for (file1, content1) , (file2, content2) in zip(i.items(), j.items()):
                    if file1==file2:
                        result=get_diff(i[file1],j[file2])
                        if result==False:
                            with open(os.path.join(key1_path, file1), 'w') as f:
                                json.dump(content1, f, indent=4)
                            with open(os.path.join(key2_path, file2), 'w') as f:
                                json.dump(content2, f, indent=4)
                        if result==True:
                            with open(os.path.join(key3_path, file1), 'w') as f:
                                json.dump(content1, f, indent=4)
                            with open(os.path.join(key4_path, file2), 'w') as f:
                                json.dump(content2, f, indent=4)
    except Exception as e:
        logger.error('Separating folders interrupted due to error: ', e)