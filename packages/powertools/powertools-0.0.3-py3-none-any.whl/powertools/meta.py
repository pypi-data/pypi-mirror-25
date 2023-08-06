#-- .meta

"""
higher order functions
"""

# todo: decorator that adds local variables in a function call as attributes of its object

# import sys
# from pprint import pprint
# import traceback

from contextlib import contextmanager

#----------------------------------------------------------------------#

# https://stackoverflow.com/questions/5189699/how-to-make-a-class-property
class ClassPropertyDescriptor( object ) :
    def __init__( self, fget, fset=None ) :
        self.fget = fget
        self.fset = fset

    def __get__( self, obj, klass=None ) :
        if klass is None :
            klass = type( obj )
        return self.fget.__get__( obj, klass )( )

    def __set__( self, obj, value ) :
        if not self.fset :
            raise AttributeError( "can't set attribute" )
        type_ = type( obj )
        return self.fset.__get__( obj, type_ )( value )

    def setter( self, func ) :
        if not isinstance( func, (classmethod, staticmethod) ) :
            func = classmethod( func )
        self.fset = func
        return self


################################
def classproperty( func ) :
    if not isinstance( func, (classmethod, staticmethod) ) :
        func = classmethod( func )

    return ClassPropertyDescriptor( func )


#----------------------------------------------------------------------#


@contextmanager
def assertion(exception:Exception):
    '''raise exception as if it came from the original assert statement'''
    try:
        yield
    except AssertionError as e:
        #tb = sys.exc_info()[2]

        #traceback.print_tb(tb)
        raise exception from None


#----------------------------------------------------------------------#
