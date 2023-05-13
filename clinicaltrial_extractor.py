""" 
This code goal is to open the XML files and extract and the required data columns from thesm save it to a pkl file. 

"""

import sys
import os
import re
sys.path.append('..')
from tools.parser import  XMLParser
# from tools.BasicUtils import MyMultiProcessing, my_write
import tqdm
import pandas as pd
from tools.preprocessing import text_preprocess

clinicalData_dir = '/home/esmailza/Mina/clinicaltrails/clinicaltrials_Knwldge_Grph/extract_clinical/data'
extract_clinical_path = 'extract_clinical/'
save_path = extract_clinical_path + 'clinical_collect'
test_path = '/home/esmailza/Mina/clinicaltrails/code/extract_clinical/data/NCT0328xxxx/NCT03289039.xml'



def get_content(file_name:str, file_dist:str):

    data = {}
    # print("we are here")
    with open(file_name, 'r') as f_in:
         data = XMLParser(f_in, file_dist)
         return data._print()      
                


if __name__ == '__main__':

    if sys.argv[1] == 'generate_data':



        if not os.path.exists(extract_clinical_path):
            os.mkdir(extract_clinical_path)

        if not os.path.exists(save_path):
            os.mkdir(save_path)



        sub_folders = [sub for sub in os.listdir(clinicalData_dir)]
        save_sub_folders = []
        save_sub_folders = [os.path.join(save_path, sub) for sub in sub_folders]
        clinical_sub_folders = [os.path.join(clinicalData_dir, sub) for sub in sub_folders]


        wiki_files = []
        save_sent_files = []

        for i in range(len(clinical_sub_folders)):
            files = [f for f in os.listdir(clinical_sub_folders[i])]
            wiki_files += [os.path.join(clinical_sub_folders[i], f) for f in files]

            save_sent_files += [os.path.join((save_sub_folders[i]), (f.rstrip(".xml"))+'.dat') for f in files]


        for save_dir in save_sub_folders:
            if not os.path.exists(save_dir):
                os.mkdir(save_dir)

        print('collect_sent_and_cooccur')

        appended_data = []

        for i in range(len(wiki_files)):
            temp = pd.DataFrame.from_dict((get_content(wiki_files[i], save_sent_files[i])))
            appended_data.append(temp)
        appended_data = pd.concat(appended_data)
        appended_data.to_pickle('extracted_feature_data.pkl')

        # clinical_trials = [(wiki_files[i], save_sent_files[i]) for i in range(len(wiki_files))]
        # print("sub folders:", clinical_trials)
        # p = MyMultiProcessing(10)
        # output = p.run(get_content, clinical_trials)




    elif sys.argv[1] == 'preprocessing':

        data = pd.read_pickle("extracted_feature_data.pkl")
        data['Criteria'] = text_preprocess(data['Criteria'])

        # data.to_pickle("extracted_feature_data.pkl")
        print(data['mesh_term'])
        

