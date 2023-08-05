from zope import interface
from zope import component
from zope.interface.common.sequence import IFiniteSequence
from . import ISAQuery

@interface.implementer(IFiniteSequence)
@component.adapter(ISAQuery)
class ModelSequenceForQuery(object):
    
    def __init__(self, query):
        self.query = query
    
    #IMinimalSequence
    def __getitem__(self, index):
        """Slice object supported"""
        if isinstance(index, slice):
            start = index.start if index.start else 0
            stop = index.stop if index.stop else 0
            step = index.step if index.step else 1
            if stop >= start and start >= 0 and step == 1:
                return self.query.slice(index.start, index.stop).all()
        #default.  might be slow
        return self.query.all()[index]

    #IFiniteSequence
    def __len__(self):
        """`x.__len__()` <==> `len(x)`"""
        return self.query.count()
    
    #Some Helpers
    def __iter__(self):
        for v in self.query:
            yield v