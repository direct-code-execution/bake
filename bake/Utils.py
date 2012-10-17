''' 
 Utils.py
 
 This file stores the utility functions that are used by the different Bake
 modules.
''' 

import subprocess
from bake.Exceptions import TaskError
import os

def print_backtrace():
    """ Prints the full trace of the exception."""
     
    import sys
    import traceback
    trace = ""
    exception = ""
    
    exceptionHandling = True
    if(not sys.exc_info()[0] or not sys.exc_info()[1]):
        exceptionHandling = False
        
    if exceptionHandling: 
        traceback.extract_tb()
        exc_list = traceback.format_exception_only (sys.exc_info()[0],sys.exc_info()[1])

        for entry in exc_list:
            exception += entry
    
        tb_list = traceback.format_tb(sys.exc_info()[2])
    else:
        tb_list = traceback.format_stack()
        
    for entry in tb_list:
        trace += entry

    sys.stderr.write("%s\n%s" % (exception, trace))

def split_args(stringP):
    """ Split arguments respecting aggregate strings."""
    
    returnValue = []
    rawSplit = stringP.split()
    compensateElement=False
    elementStr = ''
    for element in rawSplit:
        if "'" in element :
            if element.count("'") % 2 != 0 :
                if compensateElement :
                    compensateElement = False
                    returnValue.append(elementStr + " " + str(element))
                    elementStr = ''
                    element = None
                elif element.find("'") == element.rfind("'") :
                    compensateElement = True
            
        if compensateElement :
            if len(elementStr) > 0 :
                elementStr = elementStr + " " + element
            else :
                elementStr = element 
        else : 
            if element :
                returnValue.append(element)
    
    return returnValue

class ModuleAttribute:
    """ Definition of the Bake attribute. An attribute is basically one of the 
    options the user can have to configure the Bake usage.
    """

    def __init__(self, name, value, help, mandatory):
        """ Initialization, all the fields are mandatory."""
        
        self._name = name
        self.value = value
        self._help = help
        self._mandatory = mandatory
        
    @property
    def name(self):
        """ Returns the stored name of the attribute."""
        
        return self._name
    
    @property
    def help(self):
        """ Returns the help string attached to the attribute."""
        return self._help
    
    @property
    def is_mandatory(self):
        """ Returns if the attribute is mandatory or not."""
        return self._mandatory


class ModuleAttributeBase(object):
    """ Definition of the Bake attribute structure. An attribute may be 
    organized in blocks, this structure stores this grouping of attributes.
    """
    
    def __init__(self):
        self._attributes = dict()
        self._children = []
        
    def children(self):
        """ Returns the children attributes attached to this attribute."""
        
        return self._children
    
    def add_child(self, child, name):
        """ Attach a child attribute to this attribute."""
        
        self._children.append([child, name])
        
    def add_attribute(self, name, value, help, mandatory = False):
        """ Creates a new attribute attached to this one."""
       
        assert not self._attributes.has_key(name)
        self._attributes[name] = ModuleAttribute(name, value, help, mandatory)
        
    def attributes(self):
        """ Returns the list of attributes attached to this attribute block."""
        
        return self._attributes.values()
    
    def attribute(self, name):
        """ Returns a specific attribute."""
        
        if not self._attributes.has_key(name):
            return None
        else:
            return self._attributes[name]

class ColorTool:
    """ Class responsible to handle the colored message printing."""
        
    OK = '\033[34m'
    WARNING = '\033[33m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

    def disable(self):
        """ Disables the color print. """
        
        self.WARNING = ''
        self.FAIL = ''
        self.ENDC = ''
    
    def cPrint(self,color, message):
        """ Print the message with the defined color. """
        
        print (color + message + self.ENDC)
