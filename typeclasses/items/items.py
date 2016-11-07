""" Magical object typeclasses
"""
from typeclasses.objects import Object
from evennia import utils

class Furniture(Object):
    """ Contains defaults for items used to furnish a room.
    """
    def at_object_creation(self):
        """
        """
        super(Furniture, self).at_object_creation()
        self.locks.add("get:false()")
        self.locks.add("put:false()")
        self.locks.add("touch:all()")
        self.prepositions += ["behind", "under"]


class Container(Object):
    """ Contains defaults for items that have an 'inside'
    """
    def at_object_creation(self):
        """
        """
        super(Container, self).at_object_creation()
        self.prepositions += ["in"]


class Bag(Container):
    """ A generic bag that doesn't have any special features or restrictions
    """
    pass

class FurnitureBag(Furniture, Container):
    """ A generic furniture that is also a container
    """
    pass


