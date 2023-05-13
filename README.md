# clinicaltrials_Knwldge_Grph

**python3 train.py generate-entities**
cleans Criteria column, split it into inclusion and exclusion criteria columns and extract its entities using Spacy library package.
store the column entities into a new column with string "_Ent" added to the column's name. Save the new dataframe into file "extrc_data_V2.pkl"


**python3 train.py select-disease**
Select the trials with that disease name in their condition. By defualt it is on breast cancer.

**python3 train.py labelling**
creates drug-phase pools and labels the data based on the efficiency of the drugs.



