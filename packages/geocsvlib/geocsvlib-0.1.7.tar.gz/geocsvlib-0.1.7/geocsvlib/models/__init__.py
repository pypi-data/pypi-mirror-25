"""Models Package

Holds Data Access Factories and Binds Factories to DAOs

Module Poem
-----------
What happens to a dream deferred?

Does it dry up
Like a raisin in the sun?

-Langston Hughes (Dream Deffered)
"""

from geocsvlib.models.connection_factory import ConnectionFactory
from geocsvlib.models.model_factory import ModelFactory

Model = ModelFactory.get_model()

__all__ = [
    'ConnectionFactory',
    'ModelFactory'
]
