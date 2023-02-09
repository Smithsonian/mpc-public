"""
mpc_orb/parse.py
 - Code to parse an mpc_orb json file
 - Expected to be used frequently to read the contents of an mpc_orb.json
 - Expected to be of use to the external community as well as to the MPC
 - ***THIS CODE IS STILL BEING DEVELOPED***

Author(s)
MJP
"""

# Import third-party packages
# -----------------------
import numpy as np

# local imports
# -----------------------
from . import interpret
from . import validate_mpcorb
from . import filepaths

# Class to parse JSONs
# -----------------------
class MPCORB():

    def __init__(self, arg=None ):
        self.schema_json = None
        
        """ If an argument is supplied at initiation, go ahead and parse ( & validate ) """
        if arg is not None:
            self.parse( arg)
            
    def parse(self, arg):
        """
        Parse the supplied argument and make various components of the
        input mpc_orb-dictionary available as attributes of this MPCORB object
        
        inputs:
        -------
        arg: dictionary or json-filepath
        
        action:
        --------
        populates MPCORB attributes
        
        """
        # interpret argument to allow filepaths as well as dicts as input)
        json_dict, input_filepath = interpret.interpret(arg)
        
        # validate supplied json-dict against schema
        validate_mpcorb.validate_mpcorb(json_dict)
        
        # provide useful quantities as attributes
        self._add_various_attributes(json_dict)
        
    def describe(self, variable_name):
        """
        Parse an individual variable/attribute of the MPCORB object
        
        Reads the "description" of a variable from the schema
        
        inputs:
        -------
        variable_name: string
        
        action:
        --------
        returns dictionary containing any available "descriptive" elements
        
        """
        if self.schema_json is None:
            self.schema_json = validate_mpcorb.load_schema()
                    
                    
        # Find the appropriate variable name to use to search for a description ...
        # (i) If variable_name is a top-level property such as 'designation_data', 'COM', etc
        if variable_name in self.schema_json['properties'].keys():
            return  {variable_name: {'description':self.schema_json['properties'][variable_name]['description'] }}

        if variable_name == 'schema_json':
            return {variable_name: {'filepath':filepaths.mpcorb_schema} }

        # (ii) If variable_name is one of the defined-schema variables
        if variable_name in self.schema_json['$defs']:
            def_var_name = variable_name
            
        # (iii) If variable_name is an attribute of COM
        elif variable_name in self.COM.__dict__:
            def_var_name = self.schema_json['properties']['COM']['properties']['coefficient_specification']['properties'][variable_name]['$ref'].replace('#/$defs/','')

        # (iv) If variable_name is an attribute of CAR
        elif variable_name in self.CAR.__dict__:
            def_var_name = self.schema_json['properties']['CAR']['properties']['coefficient_specification']['properties'][variable_name]['$ref'].replace('#/$defs/','')
        
        # (vi) Hopefully we never see this ...
        else:
            def_var_name = None
            
            
        # Extract a description
        return  {variable_name: None } if def_var_name is None else \
                {variable_name: self._clean(self.schema_json['$defs'][def_var_name])}
            

    def _clean(self,d):
        """ """
        return { k: self._clean(v) if isinstance(v, dict) else v for k,v in d.items() if k not in ['type']}
        

    
    def _add_various_attributes(self,json_dict):
        """
        expose various quantities from mpcorb.json as object attributes
        """
        
        # make top-level quantities available as object attributes (excluding CAR & COM)
        for k,v in json_dict.items():
            if k not in ["COM", "CAR"]:
                self.__dict__[k] = v

        # Create CAR & COM objects within MPCORB object:
        # - this ultimately allows you to evaluate M.COM.coefficient_values, etc
        for k in ["COM", "CAR"]:
            self.__dict__[k] = COORD(json_dict[k])
            
        # For convenience, expose individual "elements" (E.g. "x" or "e") from COORD in MPCORB
        # E.g. MPCORB.x == MPCORB.CAR.x
        # *** NOT exposing "bulk" quantities (e.g. "coefficient_values" array),
        # *** as they will conflict between COM & CAR
        for k in ["COM", "CAR"]:
            for name in self.__dict__[k].coefficient_names:
                self.__dict__[name] = self.__dict__[k].__dict__[name]
                    
        # Is there some other stuff we want to provide as convenient attributes?
        # - E.g. stats on N_Oppositions, N_Observations, etc ?
        
        return True



class COORD():
    """ Class to hold COM or CAR elements """

    def __init__(self, coord_dict ):
        """ """
        self._populate_coord_components(coord_dict)
        
    def _populate_coord_components(self,coord_dict):
        """ populate various components for COORD representation """

        # make top-level quantities available as object attributes
        # - E.g. 'coefficient_names', 'coefficient_values', 'coefficient_uncertainties', 'eigenvalues', 'covariance'
        for k,v in coord_dict.items():
            self.__dict__[k] = v

        # populate square CoV matricees
        self._generate_square_CoV(  )

        # populate element dictionary
        self._generate_element_dict(  )

        # populate individual coordinate dictionaries (e.g. COORD.x)
        self._generate_individual_element_dicts()

    def _generate_square_CoV(self, ):
        """ populate square array from triangular elements """
        num_params                        = len(self.__dict__['coefficient_values'])
        self.__dict__['covariance_array'] = np.empty( [num_params,num_params] )
        for i in range(num_params):
            for j in range(i,num_params):
                self.__dict__['covariance_array'][i,j] = \
                self.__dict__['covariance_array'][j,i] = \
                    self.__dict__['covariance']['cov%d%d' % (i,j)]
        
    def _generate_element_dict(self, ):
        """ turn element lists into dictionary
            N.B. Input JSON contains lists/arrays, so here we provide a dictionary as well
        """
        self.__dict__['element_dict'] =  \
            { k:{"val":v, "unc":u} for k,v,u in \
                    zip(    self.__dict__["coefficient_names"],\
                            self.__dict__["coefficient_values"],\
                            self.__dict__["coefficient_uncertainties"]) }
        
    def _generate_individual_element_dicts(self, ):
        """ turn element dictionary entries into object-attributes
            E.g. COORD.x == COORD
        """
        for k in self.__dict__['element_dict']:
            self.__dict__[k]=self.__dict__['element_dict'][k]
       



    '''
    *** TOO CLEVER : NOT SURE IF USEFUL ***
    def _recursive(self,k,v):
        """
        Add all levels of supplied json-dict data as class attributes
        E.g. if json_dict contains
        { ... , key1: { key2:{ key5:True, key6:False }, key3:[], key4:None}, ... }
        then all keys 1-6 will be available as attributes, with ...
        ... key1 & key2 having associated dictionary ,
        ... key3 having an associated list value,
        ... key4, key5 & key6 having single (non-iterable) values

        NB: Doing this requires unique "keys" across all dictionaries

        """

        # Add this attribute to the instance
        self.__dict__[k]=v

        # If dict, then descend
        if isinstance(v, dict):
            for k,_ in v.items():
                self._recursive(k,_)
    '''


