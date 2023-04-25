import json
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.pdfgen import canvas
import textwrap

def get_string_for_dict( description, dict_to_parse , dict_of_strings , defs):
    """
    Function to extract key quantities from schema json/dict,
    returning a list-of-strings describing each componoent
    
    inputs:
    -------
    description: string
     - description of the dict_to_parse
    
    dict_to_parse: dictionary
     - containing schema definitions, properties, etc
     
    dict_of_strings: dictionary
     - reformated version of the data from dict_to_parse
     - populated by this function
     
    defs: dictionary
     - standard/common definitions extracted from schema
     - used to help dict_of_strings from dict_to_parse
    
    
    action:
    -------
    """
    
    # Initialize variables
    list_of_strings = []
    properties_dict = {}
    
    # Loop over the items in the dict_to_parse
    for key, value in dict_to_parse.items():
    
        # Collect keys & values into a list of strings
        if key == '$ref': # <<-- Some schema use standard/shared definitions: replace with data from "defs"
            def_key_str = value[8:]  # len('#/$defs/') == 8
            def_val = defs[def_key_str]
            this_string= f"{def_val['description']} [See below for detailed specification]"

        else: # <<-- Individually specified/definied schema entries
            key_str     = key if key not in ["properties","required"] else "Allowed Properties" if key == "properties" else "Required Properties"
            this_string = f"{key_str}: {value}" if key != "properties" else f"{key_str}: {list(value.keys())}"

        list_of_strings.append(this_string)
        
        # Keep track of any "child-properties" that we need to descend into ...
        if key == "properties":
            properties_dict = value
                
    # Populate the dict_of_strings for this dictionary
    dict_of_strings[f'{len(dict_of_strings):03}:{description}'] = list_of_strings
    
    # Descend into any child dictionaries (i.e. the properties_dict)
    for k, d in properties_dict.items():
        get_string_for_dict( k, d , dict_of_strings ,defs )



def create_mpc_orb_pdf():
    """
    Over all routine to create mpc_orb.pdf
    Key steps are:
    (a) Define PDF
    (b) Read & reformat schema data
    (c) Write data to PDF
    """

    # ---------- Format the pdf ------------------------
    # Create a new PDF document with margins of 0.5 inches
    pdf = canvas.Canvas('mpc_orb.pdf', pagesize=letter)

    # Define the page size and margins
    PAGE_HEIGHT = letter[1]
    PAGE_WIDTH = letter[0]
    LEFT_MARGIN = 72
    RIGHT_MARGIN = LEFT_MARGIN
    TOP_MARGIN = PAGE_HEIGHT - 72
    BOTTOM_MARGIN = 72


    # Set the font and font size for the document
    styles = getSampleStyleSheet()
    style = styles['Normal']
    style.fontName = 'Helvetica'
    style.fontSize = 12

    pdf.setTitle('MPC-ORB.JSON')

    
    
    # ---------- Read the data from the Schema ---------
    
    # Read the JSON file and extract the data
    with open('../mpc_orb/schema_json/mpcorb_schema_latest.json', 'r') as f:
        data = json.load(f)
        defs = data["$defs"]
        data = {k:v for k,v in data.items() if k != "$defs"}


    # Create a simplified "data" dictionary:
    # - Loop through the data and parse it in a structure manner
    description = "Top Level of MPC-ORB.JSON object"
    dict_of_strings = {}
    get_string_for_dict(description , data, dict_of_strings , defs)

    # Add the stuff from the defs dictionary
    # - Trying to do in a slightly different manner to that above, so that the unit-information stays together.
    for k,v in defs.items():
        dict_of_strings[f'{len(dict_of_strings):03}:{k}'] = [ f"{kk}: {vv}" for kk,vv in v.items() ]

    # Turns out to be (somewhat) easier to just turn the description into a list of text strings
    # Note the imposed maximum width
    text_lines = []
    for key, list_of_strings in dict_of_strings.items():
        text_lines.append(key)
        for s in list_of_strings:
            for n, word in enumerate(textwrap.wrap(s, width=75)):
                if n == 0 :
                    text_lines.append(f'    {word}')
                else:
                    text_lines.append(f'      {word}')
        text_lines.append('')


    # ---------- Populate the PDF with the description  -----------------
    # Write intro
    text_lines.insert(0,"This document describes the MPC_ORB.JSON format.")
    text_lines.insert(1,"This document is generated programatically from a schema file.")

    # Loop through the data and add it to the PDF document
    y = TOP_MARGIN  # Starting y-coordinate for the text
    for n , line in enumerate(text_lines):
        pdf.drawString(LEFT_MARGIN, y, line)
        y -= 20  # Adjust the line spacing as needed
        if y < BOTTOM_MARGIN or n == 1:
            pdf.showPage()
            y = TOP_MARGIN

    # Save the PDF document
    pdf.save()



if __name__ == '__main__':
    create_mpc_orb_pdf()
