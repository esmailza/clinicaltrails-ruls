

import spacy
import scispacy

import pandas as pd

import en_core_sci_lg
#import en_core_sci_md
import en_ner_bc5cdr_md
# import en_ner_jnlpba_md
# import en_ner_craft_md
# import en_ner_bionlp13cg_md

from collections import OrderedDict,Counter
from pprint import pprint
from tqdm import tqdm
tqdm.pandas()
import re
import sys
import itertools

# time taken to read data


nlp = spacy.load("en_ner_bc5cdr_md")


def read_pkl_data(file_name:str):
    data = pd.read_pickle(file_name)
    return data


def clean_text(text:str):

    if isinstance(text, str):
        text = remove_brackets(text)
        text = text.replace('-', '.')
        text = ' '.join(re.sub(r'[^a-z0-9,.;\s-]', '', remove_brackets(normalize_text(text))).split())
        return text
    else:
        return 0

def remove_brackets(text:str):
    while re.search(r'{[^{}]*}', text):
        text = re.sub(r'{[^{}]*}', '', text)
    while re.search(r'\([^()]*\)', text):
        text = re.sub(r'\([^()]*\)', '', text)
    while re.search(r'\[[^][]*\]', text):
        text = re.sub(r'\[[^][]*\]', '', text)
    return ' '.join(text.split())

def normalize_text(text:str):
    tokens = text.lower().split()
    refine_tokens = []
    for token in tokens:
        if token.isalnum():
            refine_tokens.append(token)
        else:
            temp_str = ''
            for char in token:
                if char.isalnum() or char == "'" or char == '.':
                    temp_str += char
                else:
                    if temp_str:
                        refine_tokens.append(temp_str)
                    refine_tokens.append(char)
                    temp_str = ''
            if temp_str:
                refine_tokens.append(temp_str)
    return ' '.join(refine_tokens)

def entity_extractor(model:str, text:str):
    doc = nlp(text)
    print(list(doc.sents))
    print(doc.ents)


def display_entities(document:str):
    """ A function that returns a tuple of displacy image of named or unnamed word entities and
        a set of unique entities recognized based on scispacy model in use
        Args: 
            model: A pretrained model from spaCy or ScispaCy
            document: text data to be analysed"""
    
    doc = nlp(document)
    # displacy_image = displacy.render(doc, jupyter=True,style='ent')
    entity_and_label = set([(X.text, X.label_) for X in doc.ents])
    return   entity_and_label


def check_condition(condition:str, pattern:str):

    match = re.search(pattern, condition, flags=re.IGNORECASE)
    # Use re.search() to search for a match in the string

    if match:
        return True
    else:
        return False

def get_drugName(text:set):
    first_values = [pair[0] for pair in text]
    return first_values


def clean_intervention(text:str):
    drug = "Drug: "
    intervention = []
    if drug in text:    
        text = text.rstrip(" ,")
        list_text = text.split(' , ')
        num_int = len(list_text)
        for value in list_text:
            if drug in value:
                value = value.replace(drug, "")
                intervention.append(value)
                
        
    return intervention


def switch_case_label(phase, drug):
    res = False
#     print(phase, drug)
    if phase == 1:
        res = ((drug in drug_lst_phase_2) or
               (drug in drug_lst_phase_3 ) or
               (drug in drug_lst_phase_4))
        return res
    elif phase == 2:
        res = ((drug in drug_lst_phase_3 ) or
           (drug in drug_lst_phase_4))
        return res
    
    elif phase == 3:
        res = ((drug in drug_lst_phase_4))
        return res
    else:
        return False
    

if __name__ == "__main__":

        # new_columns = [ 'NCTID', 'Phase', 'Status', 'Allocation', 
    #    'Intervention_Model', 'Intervention', 'Conditions',
    #    'Date_start', 'Date_Completion',
    #     'Enrollment', 'ArmsNumber', 'has_dmc',
    #    'is_fda_regulated_drug', 'is_fda_regulated_device', 'Sponsors',
    #    'Age_Min', 'Age_Max', 'Gender', 'Countries', 'Mesh_Term', 
    #    'Inclusion_criteria', 'Exclusion_criteria', 'Inclusion_Ent', 'Exclusion_Ent']
    if sys.argv[1] =="generate-entities":

        pd.options.mode.chained_assignment = None

        data =pd.DataFrame( read_pkl_data("extracted_feature_data.pkl")).reset_index()
        del data['Primary_Purpose'], data['Title'],data['Summary_Detailed'], data['Summary_Brief'], data['Date_start'], data['Date_Completion']

        seperator= "Exclusion Criteria:"


        data[['Inclusion_Criteria', 'Exclusion_Criteria']] = data['Criteria'].str.split(seperator, n=1, expand=True)
        

        data['Inclusion_Criteria'].fillna(0, inplace=True)
        data['Exclusion_Criteria'].fillna(0, inplace=True)
        

        data['Inclusion_Criteria'] = data['Inclusion_Criteria'].apply(lambda x: clean_text(x) if (x is not None or x!=0 )else "None")
        data['Exclusion_Criteria'] = data['Exclusion_Criteria'].apply(lambda x: clean_text(x) if (x is not None or x!=0 )else "None")
       
        
        
        data['Inclusion_Ent'] = data['Inclusion_Criteria'].apply(lambda x: display_entities(x) if x != 0 else None)
        data['Exclusion_Ent'] = data['Exclusion_Criteria'].apply(lambda x: display_entities(x) if x != 0 else None)
        data['Intervention_Ent'] = data['Intervention'].apply(lambda x: display_entities(x) if x != 0 else None)
        data['Conditions_Ent'] = data['Conditions'].apply(lambda x: display_entities(x) if x != 0 else None)
        data['Mesh_Term_Ent'] = data['Mesh_Term'].apply(lambda x: display_entities(x) if x != 0 else None)

        data.to_pickle("extrc_data_V2.pkl")
    
    # Selecting data fo specific disease

    if sys.argv[1] == "select-disease":
        data = pd.read_pickle("extrc_data_V2.pkl")
        # print((data.head())['Conditions'])
        pattern = r'\b(breast\s?cancer|cancer\s?of\s?the\s?breast)\b'
        pattern2 = r'\b(breast\s?neoplasms|neoplasms\s?of\s?the\s?breast)\b'
        

        data['Conditions'].fillna(0, inplace = True)
        data['Select Disease'] = data['Conditions'].apply(lambda x: check_condition(x, pattern) if x!= 0 else False )
        data['Select Mesh'] = data['Mesh_Term']. apply(lambda x: check_condition(x, pattern2) if x!=0 else False)
        
        breast_data = (data[(data['Select Disease'] == True) | data['Select Mesh']  == True]).reset_index()
        del breast_data['level_0'], breast_data['index']
        del data['Select Mesh'], data['Select Disease']
        breast_data.to_pickle("breast_cancer.pkl")
        print(breast_data.shape[0])



    if sys.argv[1] == "labelling":
        data = pd.read_pickle("breast_cancer.pkl")
        pd.options.mode.chained_assignment = None

        data['Intervention_Ent'] = data['Intervention_Ent'].apply(get_drugName)
        data['Intervention'] = data['Intervention'].replace('', 0)

        #First filter, we remove 952 trials with intervention 0 (without set intervention)
        data = data[data['Intervention'] != 0]
        data["Intervention"] = data["Intervention"].apply(clean_intervention)

        # Second filter, we remove trials that their intervention is not drug type
        data = data[data['Intervention'].apply(lambda x: isinstance(x,list) and len(x) > 0)].reset_index()
        data = data.drop('index', axis=1)


        # replacing the drug name in the Intervention column with the drug name entity from the 
        # Interventuon_Ent column
        for index, row in data.iterrows():
            intervention = row["Intervention"]
            new_list = intervention
            
            for i in new_list:
                if i.lower() == "placebo":
                    new_list.remove(i)
                
            interven_ent = row["Intervention_Ent"]
            for ent in interven_ent:
                indices = [i for i, string in enumerate(intervention) if ent in string]
                for i in indices:
                    new_list[i] = str(ent)
            row["Intervention"] = new_list


            # Cleaning Phase:

        data['Phase'] = data['Phase'].replace('N/A',5)
        data['Phase'] = data['Phase'].replace('Phase 1', 1)
        data['Phase'] = data['Phase'].replace('Early Phase 1', 1)
        data['Phase'] = data['Phase'].replace('Phase 1/Phase 2', 2)
        data['Phase'] = data['Phase'].replace('Phase 2/Phase 3', 3)
        data['Phase'] = data['Phase'].replace('Phase 2', 2)
        data['Phase'] = data['Phase'].replace('Phase 3', 3)
        data['Phase'] = data['Phase'].replace('Phase 4', 4)

        # Creating phases drugs:
        drug_lst_phase_1 = list(itertools.chain.from_iterable(list(data[data['Phase'] == 1]['Intervention'])))
        drug_lst_phase_2 = list(itertools.chain.from_iterable(list(data[data['Phase'] == 2]['Intervention'])))
        drug_lst_phase_3 = list(itertools.chain.from_iterable(list(data[data['Phase'] == 3]['Intervention'])))
        drug_lst_phase_4 = list(itertools.chain.from_iterable(list(data[data['Phase'] == 4]['Intervention'])))
        data['Label'] = True

        failed_label=['Terminated', 'Withdrawn', 'Suspended']

        # Labelling trials
        for index, row in data.iterrows():
            drugs = row['Intervention']
            status = row['Status']
            phase = int(row['Phase'])
            result = []
            if status == "Completed":
                result = [switch_case_label(phase, drug) for drug in drugs]
                label = any(result)
                data.loc[index, 'Label'] = label

            if status in failed_label:
                data.loc[index, 'Label'] = False


        accepted_label = ['Terminated', 'Withdrawn', 'Suspended', 'Completed', 'Approved for marketing' ]
        data_filterd = data[data["Status"].isin(accepted_label)]
        data_filterd['Label'].value_counts()

        # Interventions are:
        print(data_filterd['Intervention_Ent'].value_counts(), "\n\n")
        print("Intervention_Model",data_filterd['Intervention_Model'].value_counts(), "\n\n")
        print("Status",data_filterd['Status'].value_counts(), "\n\n")
        print("Phase",data_filterd['Phase'].value_counts(), "\n\n")
        print("ArmsNumber",data_filterd['ArmsNumber'].value_counts(), "\n\n")
        print("is_fda_regulated_device",data_filterd['is_fda_regulated_device'].value_counts(), "\n\n")
        print("has_dmc \n",data_filterd['has_dmc'].value_counts(), "\n\n")
        print("is_fda_regulated_drug \n",data_filterd['is_fda_regulated_drug'].value_counts(), "\n\n")
        print("Inclusion_Ent \n",data_filterd['Inclusion_Ent'].value_counts(), "\n\n")
        


        



    

        

     
    








