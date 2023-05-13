"""
 This model is doing all the preprocessing task for the data.
"""

import pandas as pd
import re


# important columns from input (downloaded CSV from ClinicalTrials)
# that are used for output and calculating other fields (MMSE and etc.)
INPUT_COLUMNS = [ "Phases",
                    "Interventions",
                    "NCT Number",
                    "Status",
                    "Outcome Measures",
                    "Sponsor/Collaborators",
                    "Enrollment",
                    "Funded Bys",
                    "Start Date",
                    "Primary Completion Date",
                    "Completion Date",
                    "First Posted",
                    "Last Update Posted",
                    "Locations",
                    "Conditions",
                    ]


DATE_COLUMNS = ['FirstPosted',
                    'StartDate',
                    'CompletionDate',
                    'PrimaryCompletionDate',
                    'LastUpdatePostDate',]





# def generate_data(csv_name):
#     """
#         Generates the data that should be inserted into the database
#         for further usage. Does the followings procedure:

#             1. Load downloaded CSV file
#             2. Clean data
#             3. Build other fields based on available data

#         - Parameters
#         ============================
#         + csv_name :     String of downloaded csv file name

#         - Return
#         ============================
#         + pd.DataFrame : Generated data from CSV, similar to spreadsheet
#     """
#     data = pd.read_csv(settings.BASE_DIR + '/data/' + csv_name)
#     data = clean_data(data)
#     data = fill_null(data)
#     return data


def clean_data(data):
    """
        Removing irrelevant data from the dataframe

        - Parameters
        ============================
        + data:         Pandas dataframe

        - Return
        ============================
        + pd.DataFrame : Cleaned dataframe without irrelevant data
    """

    # required filters and data cleaning can be done here!

    return data
    



def text_preprocess(text):
    """
        Preprocess and normalize given text

        - Parameters
        ============================
        + text:         Sentence or paragraph that needs to be normalized

        - Return
        ============================
        + string :      Normalized text
    """
    text = str(text)
    text = text.strip()
    text = re.sub(r'\n+\s+\d+\. ', '. ', text)
    text = re.sub(r'\n+\s+- ', '. ', text)    
    
    text = text.replace('\n', ' ')  \
                .replace(' - ', ' ')\
                .replace('..', '.') \
                .replace(':.', '.') \
                .replace(',.', ',')
    
    # preprocess for MMSE
    text = text.replace('−', '-') \
                .replace('greater than', '>') \
                .replace('less than', '<') \
                .replace('≤', '<=') \
                .replace('≥', '>=')
    
    if re.search(r'<=\d+', text):
        text = re.sub('<=', '<= ', text)
        
    if re.search(r'>=\d+', text):
        text = re.sub('>=', '>= ', text)
    
    text = re.sub(r' {2,}', ' ', text)
    text = re.sub(r'[\.:]*\|+', '. ', text)
    return text


def extract_treatment_duration(text, time_unit='d'):
    """
        Finding treatment duration for an span of text in number
        of time unit

        - Parameters
        ============================
        + text:         Span of text mentioning treatment duration
        + time_unit:    The unit of extracted time. (d : days
                                                     w : weeks
                                                     m : months
                                                     y : years
                                                    )

        - Return
        ============================
        + int:          Treatment duration in time units
    """
    if isinstance(text, set):
        text = ' '.join(text)

    text = text.replace(', ', ' ')  \
                .replace('. ', ' ') \
                .replace('-', ' ') \
                .lower()            \
                .strip()

    time = re.findall(r'\d+ months?|\d+ weeks?|\d+ days?|\d+ years?', text)
    duration = 0
    if len(time) == 1:     # skipping time frames with more than one mentioned time
        t = time[0].lower().split()
        duration = int(t[0])
        if t[1][0] == 'w':      # to days
            duration *= 7
        elif t[1][0] == 'm':
            duration *= 31
        elif t[1][0] == 'y':
            duration *= 365

    # convert to asked unit from days
    unit = 1
    if time_unit == 'w':
        unit = 7
    elif time_unit == 'm':
        unit = 31
    elif time_unit == 'y':
        unit = 365

    return duration / unit


def fill_null(df):
    """
        Fill out every where that is null with None value
    """
    return df.where(pd.notnull(df), None)


