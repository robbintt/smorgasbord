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
        self.db.prepositions += ["behind", "under", "on"]


class Container(Object):
    """ Contains defaults for items that have an 'inside'
    """
    def at_object_creation(self):
        """
        """
        super(Container, self).at_object_creation()
        self.db.prepositions += ["in"]


class Bag(Container):
    """ A generic bag that doesn't have any special features or restrictions
    """
    pass

class FurnitureBag(Furniture, Container):
    """ A generic furniture that is also a container

    This won't quite work because at_object_creation will be taken from the
    first class, not both classes.
    """
    def at_object_creation(self):
        """
        """
        super(FurnitureBag, self).at_object_creation()


