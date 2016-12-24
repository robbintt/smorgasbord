""" Magical object typeclasses
"""
from typeclasses.objects import Object
from evennia import utils

class Item(Object):
    def at_object_creation(self):
        """
        """
        super(Item, self).at_object_creation()
        self.locks.add("get:all()")
        self.locks.add("put:all()")
        self.locks.add("touch:all()")


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


class FurnitureContainer(Object):
    """ A generic furniture that is also a container
    """
    def at_object_creation(self):
        """
        """
        super(FurnitureContainer, self).at_object_creation()
        self.locks.add("get:false()")
        self.locks.add("put:false()")
        self.locks.add("touch:all()")
        self.db.prepositions += ["behind", "under", "on", "in"]


