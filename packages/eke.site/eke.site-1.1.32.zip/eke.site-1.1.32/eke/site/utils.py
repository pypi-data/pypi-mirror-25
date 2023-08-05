# encoding: utf-8
# Copyright 2009 California Institute of Technology. ALL RIGHTS
# RESERVED. U.S. Government Sponsorship acknowledged.

'''
EKE Site: utilities
'''

def generateTitleFromNameComponents(components):
    '''Given a triple of (last name, first name, middle name), generate an appropriate object title.
    The form is "Last, First Middle" where middle may appear in first if the first is None and
    the comma disappears if both are None.'''
    last, first, middle = components
    given = first
    if not given:
        given = middle
    else:
        if middle:
            given += ' ' + middle
    if not given:
        return last
    else:
        return '%s, %s' % (last, given)
