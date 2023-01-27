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

# Class to parse JSONs
# -----------------------
class MPCORB():

    def __init__(self, arg=None ):
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
    

    
    def _add_various_attributes(self,json_dict):
        """
        expose various quantities from mpcorb.json as object attributes
        """
        
        # make top-level quantities available as object attributes
        for k,v in json_dict.items():
            self.__dict__[k] = v

        # These coord-types are both required in a valid input mpc_orb.json
        for coord_attr in ["COM", "CAR"]:
            self._populate_coord_components(coord_attr)
                    
        # Is there some other stuff we want to provide as convenient attributes?
        # - E.g. stats on N_Oppositions, N_Observations, etc ?
        
        
    def _populate_coord_components(self,coord_attr):
        """ populate various components for specific representation """
        
        # populate square CoV matricees
        self.__dict__[coord_attr]['covariance_array'] = self._generate_square_CoV( coord_attr )

        # populate element array
        self.__dict__[coord_attr]['element_array'] = self._generate_element_array( coord_attr )

        # provide uncertainty (CoV diag)
        # *** MJP:2023-01-24: Possibly unnecessary: I think "Uncertainty" already exists...
        self.__dict__[coord_attr]['uncertainty'] = self._generate_uncertainty( coord_attr )
    
    def _generate_square_CoV(self, coord_attr ):
        """ populate square array from triangular elements """
        num_params       = self.__dict__['orbit_fit_statistics']['numparams']
        covariance_array = np.empty( [num_params,num_params] )
        for i in range(num_params):
            for j in range(i,num_params):
                covariance_array[i,j] = covariance_array[j,i] = self.__dict__[coord_attr]['covariance']['cov%d%d' % (i,j)]
                
        return covariance_array

    def _generate_element_array(self,  coord_attr ):
        """ turn element dict into numpy array (with fixed ordering) """
        
        if 'element_order' in self.__dict__[coord_attr]:
            element_order = self.__dict__[coord_attr]['element_order']
        else:
            element_order = ['x','y','z','vx','vy','vz'] if coord_attr == 'CAR' else ['q','e','i','node','argperi','peri_time']
        return np.array( [ self.__dict__[coord_attr]['elements'][key] for key in element_order] )
        
    def _generate_uncertainty(self, coord_attr ):
        """ extract sqrt of diag elements in CoV-arry as uncertainty array
            *** MJP:2023-01-24: Possibly unnecessary: I think "Uncertainty" already exists...
        """
        return np.sqrt( self.__dict__[coord_attr]['covariance_array'].diagonal() )





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


