""" Magical object typeclasses
"""
from typeclasses.objects import Object
from evennia import prototypes

from world import prototypes as world_prototypes

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


class CampFire(FurnitureContainer):
    """ A fire 'crafting station'
    """

    def at_object_creation(self):
        """
        """
        super(CampFire, self).at_object_creation()

    def at_objput_from(self, putter=None, target=None, preposition=None):
        """ Define what happens to an object if it enters a fire

        for example, putting bacon in a fire should delete the bacon
        and create a cooked bacon and a bacon fat
        """
        print 'self = {}'.format(self)
        print 'putter = {}'.format(putter)
        print 'target = {}'.format(target)
        print 'target.name = {}'.format(target.name)
        if target.name == 'raw bacon' or 'raw bacon' in target.aliases:
            cooked_bacon = world_prototypes.COOKED_BACON
            cooked_bacon['location'] = self
            cooked_bacon['sublocation'] = 'in'
            prototypes.spawner.spawn(cooked_bacon)

