import os.path
import json
import logging

def check_path(dir_path):
    path = os.getcwd()
    abs_path=os.path.abspath(os.path.join(path, os.pardir))
    final_path= abs_path+dir_path
    isdir = os.path.isdir(final_path)
    if isdir==True:
        return final_path
    if isdir==False:
        return "path dont exist"

def sortedDeep(d):
    def makeTuple(v): return (*v,) if isinstance(v,(list,dict)) else (v,)
    if isinstance(d,list):
        return sorted( map(sortedDeep,d) ,key=makeTuple )
    if isinstance(d,dict):
        return { k: sortedDeep(d[k]) for k in sorted(d)}
    return d

def source_target_path(dir_path):
    final_path=check_path(dir_path)
    if final_path== "path dont exist":
        dir_name=os.path.split(dir_path)[0]
        final_path = input(fr"Enter the path of {dir_name} directory: ")
        return final_path
    else:
        return final_path

def get_data(folder_name):
    logging.info("Started fetching data from the folders")
    try:
        store_dir = os.listdir(folder_name)
        output={}
        for store_name in store_dir:
            store_path=folder_name+"\\"+store_name
            store_coupons= os.listdir(store_path)
            data_info=[]
            
            for filename in store_coupons:
                with open(os.path.join(store_path, filename), 'r') as f:
                    data = json.load(f)
                    data= sortedDeep(data)
                data_info.append({filename:data})
            output[store_name]=data_info       
    except Exception as e:
        logging.error("Fetching data interrupted due to error: ", e)
    return output
