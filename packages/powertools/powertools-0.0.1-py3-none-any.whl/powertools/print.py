#-- powertools.out

'''
pretty print functions
'''

#-------------------------------------------------------------------------------------------------#

from pprint import PrettyPrinter
_pprinter   = PrettyPrinter()
pprint      = _pprinter.pprint
pformat     = _pprinter.pformat


def add_pprint(cls):
    _pprinter._dispatch[cls.__repr__] = cls.__pprint__


#-------------------------------------------------------------------------------------------------#

from collections import namedtuple

#ToDo: 'tprint' - write to multiple streams

def dictprint( d, pfunc=print ) :
    list( pfunc( f'{str(key):<12}:', value ) for key, value in d.items( ) )

def listprint( l, pfunc=print ) :
    list( pfunc( value ) for value in l )

def rprint( struct, i=0, quiet=False, pfunc=print ) :
    #ToDo: return a string

    result = ""
    if isinstance( struct, list ) \
    or isinstance( struct, tuple):  # loop over list/tuple
        for value in struct :
            if isinstance( value, dict  ) \
            or isinstance( value, list  ) \
            or isinstance( value, tuple ) : # recurse on subsequence
                result += rprint( value, i + 2, quiet )

            else :
                line = ' '*i + "- " + str( value )
                result += line + "\n"
                pfunc( line ) if quiet is False else None

    elif isinstance( struct, dict ) : # loop over dict
        for (key, value) in struct.items( ) :
            line = ' '*i + "{:<12} ".format(str(key)+':')
            result += line
            pfunc( line, end='' ) if quiet is False else None

            if isinstance( value, dict  ) \
            or isinstance( value, list  ) \
            or isinstance( value, tuple ) : # recurse on subsequence
                pfunc( "" ) if quiet is False else None
                result += "\n"
                result += rprint( value, i + 2, quiet )

            else :
                result += str( value ) + "\n"
                pfunc( str( value ) ) if quiet is False else None

    return result


#-------------------------------------------------------------------------------------------------#

