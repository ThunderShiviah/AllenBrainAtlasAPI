"""Calls various functions on the Allen Brain Atlas API. 

NOTE: Docstrings start with a short description followed by the description listed on the
Allen Brain Atlas website: http://help.brain-map.org/display/api/Allen+Brain+Atlas+API 
"""

import sys

def main():
    """Main entry point for this script"""
    pass


def download_image():
    """Downloads an image from the Allen Brain Atlas.
    
    Download whole or partial two-dimensional images 
    from the Allen Institute with the SectionImage, AtlasImage
    and ProjectionImage Download Services.
    """
    
    pass
def download_SVG():
    """Downloads SVG annotations associated with Allen images.
    
    The SVG download service returns annotations associated with 
    the specified SectionImage as scalable vector graphics (SVG). 
    Examples of annotations that can be retrieved include hot spots
    and drawings of Structure boundaries on AtlasImages.
    Add the "groups=" parameter and specify one or more GraphicGroupLabel.id delimited
    by commas to filter the types of SVG returned.
    """
    pass

def image_to_reference_synchronization():
    """For a specified SectionImage and (x,y) location, 
    return the (x,y,z) location in the ReferenceSpace of the associated SectionDataSet.
    """
    
    


    
if __name__ == main():
    sys.exit(main())