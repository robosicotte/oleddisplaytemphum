from enum import Enum

class BoundingBoxFormat(Enum):
    LEFT_RIGHT_TOP_BOTTOM=1
    CENTER_WIDTH_HEIGHT=2
    LEFT_TOP_WIDTH_HEIGHT=3

class TextBoundingBox:
    """
    class TextBoundingBox:
    An object for a text bounding box.
    Converts from tuple (from font.getbbox) to object
    """
    

    def __init__(self, bbox):
        """
        __init__: Initializes an object of type textBoundingBox

        :param bbox: (Tuple of 4 ints): The bounding box from getbbox
        """
        self.xleft, self.ytop, self.xright, self.ybottom=bbox

    def get_width(self):
        return self.xright-self.xleft
    
    def get_height(self):
        return self.ybottom-self.ytop
    
    def get_xleft(self):
        return self.xleft
    
    def get_ytop(self):
        return self.ytop
    
    def get_xright(self):
        return self.xright
    
    def get_ybottom(self):
        return self.ybottom
    
    def get_center(self):
        return ((self.xleft+self.xright)/2, (self.ytop+self.ybottom)/2)
    
    def get_bounding_box_format(self, format: BoundingBoxFormat):
        """
        get_bounding_box_format: Gets the bounding box formatted
        
        :param format: The format to return
        :type format: BoundingBoxFormat
        Returns:
        The formatted bounding box as a tuple of 4 floats/ints
        """
        format
        if format == BoundingBoxFormat.CENTER_WIDTH_HEIGHT:
            xc, yc=self.get_center()
            return (xc, yc, self.get_width(), self.get_height())
        elif format == BoundingBoxFormat.LEFT_RIGHT_TOP_BOTTOM:
            return (self.get_xleft(), self.get_xright(), self.get_ytop(), self.get_ybottom())
        elif format == BoundingBoxFormat.LEFT_TOP_WIDTH_HEIGHT():
            return (self.get_xleft(), self.get_ytop(), self.get_width(), self.get_height())
        else:
            print('Invalid format.')
            return None