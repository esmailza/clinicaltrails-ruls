import bs4
from bs4 import BeautifulSoup
from lxml import etree as etree_lxml
import sys
import os
import re
sys.path.append('..')
from tools.BasicUtils import  my_write
import math




class XMLParser:
    """
        A class to the XML data downloaded from clinicaltrials.gov
        and build the corresponding Trial object to insert or update
        instances in the database
    """

    def __init__(self, xml: str, dist:str):
        self.xml = xml
        self.dist = dist
        self.soup = BeautifulSoup(xml, 'lxml')
        self.data = self._parse()
        # self.data['LocationsString'] = self.get_formatted_locations()

    
    def _tag_value(self, tag: str, node: bs4.element.Tag = None) -> str:
        """
            Retrieving value for a tag if the tag exists in the XML
        """
        if not node:
            node = self.soup

        if node.find(tag):
            return node.find(tag).text
        else:
            return None
    def _print(self):
        return self.data


    def _parse(self) -> dict:
        """
            The main function to yield resutls from the read XML file
        """
        data = {}

        data['NCTID'] = self.soup.nct_id.text
        data['Phase'] = self._tag_value('phase')
        data['Status'] = self.soup.overall_status.text

       
        data['Allocation'] = self._tag_value('allocation')
        data['Primary_Purpose'] = self._tag_value('primary_purpose')
        data['Intervention_Model'] = self._tag_value('intervention_model')

        intervention_text = ''
        for intervention in self.soup.find_all('intervention'):
            intervention_text += intervention.intervention_type.text  + ': '+   intervention.intervention_name.text  +' , '

        intervention_text = intervention_text.rstrip(',')
        data['Intervention'] = intervention_text

        data['Conditions'] = " , ".join ([c.get_text() for c in self.soup.find_all('condition')])
        data['Title'] = self._tag_value('official_title') or self._tag_value('brief_title')
        

        data['Date_start']= self._tag_value('start_date')
        data['Date_Completion'] = self._tag_value('completion_date')

        data['Summary_Brief'] = self._tag_value('brief_summary'),
        data['Summary_Detailed'] = self._tag_value('detailed_description'),

        data['Criteria'] = self._tag_value('textblock', self.soup.criteria) 
        data['Enrollment'] = self._tag_value('enrollment')
        data['ArmsNumber'] = self.soup.number_of_arms.text if self.soup.number_of_arms else None
        data['has_dmc'] = self._tag_value('has_dmc')
        data['is_fda_regulated_drug'] = self._tag_value('is_fda_regulated_drug')
        data['is_fda_regulated_device'] = self._tag_value('is_fda_regulated_device')
        



        sponsors_text = ''
        for spon in self.soup.sponsors.children:
            if spon.name:
                    if self._tag_value('agency_class', spon) is not None:
                
                        sponsors_text += self._tag_value('agency_class', spon) + ' , '
        
        sponsors_text.rstrip(' , ')      
   
        data['Sponsors'] = sponsors_text

        data['Age_Min'] = self._tag_value('minimum_age')
        data['Age_Max'] = self._tag_value('maximum_age')
     

        data['Gender'] = self._tag_value('gender')

        
        Locations = []
        for loc in self.soup.find_all('location'):
            if loc.find('facility'):
                facility = loc.facility
                information = {

                    'Country'  : self._tag_value('country', facility.address),
                
                }
                Locations.append(information)

        data['Countries'] =' , '.join(list( set([f['Country'] for f in Locations if f['Country'] != None])))
        data['Mesh_Term'] = self._tag_value('mesh_term')

        for key, value in data.items():
             if value is None:
                data[key] = 0
     
        return data


    def get_formatted_locations(self):
        """
            Returns the locations in a formatted string:
                Name, City, State, Country
        """
        result = []
        for l in self.data['Locations']:
            addr = ', '.join([v for k,v in l.items() if v != None and k != 'Status'])
            result.append(addr)
            
        return '\n'.join(result)



