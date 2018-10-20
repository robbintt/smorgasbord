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

        i think at_objput_from was originally intended to impact the 
        object that the item is in, to block the object from being moved

        as such the below feature should be moved

        there are evennia native homes for this such as:
        at_after_move
        at_object_receive

        i could use at_object_receive to run a crafting suite
        but i may want to trigger the crafting with a verb like
        'stoke fire' - causes any reactions to occur

        for example, putting bacon in a fire should delete the bacon
        and create a cooked bacon and a bacon fat
        """
        # this clause contains the trigger for spawning the object
        spawned_objects = []
        if target.name == 'raw bacon' or 'raw bacon' in target.aliases:

            # update the cooked bacon to have the proper location & sublocation
            # this could be done generically after the if statements
            spawned_objects.append(world_prototypes.COOKED_BACON)

        # this clause sets up the location, sublocation and spawns the object
        # set based on your needs
        for obj in spawned_objects:
            obj['location'] = self
            obj['sublocation'] = 'in'
            prototypes.spawner.spawn(obj)

class CookingPot(Container):
    ''' A food crafting object
    '''
    def at_stirred(self, stirrer):
        ''' Check for recipes in order and fill the first one
        '''
        try:
            stirrer_message = "As you stir the {}, it briefly bubbles."
            stirrer.msg(stirrer_message.format(self.get_display_name(stirrer)))
        except AttributeError:
            stirrer.msg(toucher_message.format(self.key))
        self.location.msg_contents(
            "The {item} briefly bubbles then returns to normal.", 
            exclude=stirrer,
            mapping={"item": self} )

        for item in self.contents:
            # this clause contains the trigger for spawning the object
            spawned_objects = []
            if item.name == 'raw bacon' or 'raw bacon' in item.aliases:
                spawned_objects.append(world_prototypes.COOKED_BACON)
                item.delete()

            # this clause sets up the location, sublocation and spawns the object
            # set based on your needs
            for obj in spawned_objects:
                obj['location'] = self
                obj['sublocation'] = 'in'
                prototypes.spawner.spawn(obj)

