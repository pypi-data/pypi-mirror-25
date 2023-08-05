from .. import testing
from . import query

related_models = query.ORMRelatedModelsAdderFactory([
                    testing.Test3, testing.Test2, testing.Test4, testing.Test1])