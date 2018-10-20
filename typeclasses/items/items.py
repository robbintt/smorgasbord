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


class CookingPot(Container):
    ''' A food crafting object
    '''
    def at_stirred(self, stirrer):
        ''' Check for recipes in order and fill the first one
        '''
        if not "cooking" in self.location.attributes.get('crafting_types'):
            no_cooking_message = "The {} must be in a cooking location to stir it."
            stirrer.msg(no_cooking_message.format(self.get_display_name(stirrer)))
            return #abort
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

            #if hasattr(item, 'aliases') and item.name == 'raw bacon' or 'raw bacon' in item.aliases:
            # try to check aliases too so multiple items can have fill the same ingredient slot, e.g. various livers or whatever
            # try this way
            # if item.name == 'raw bacon' or 'raw bacon' in item.aliases.all():
            if item.name == 'raw bacon':
                spawned_objects.append(world_prototypes.COOKED_BACON)
                item.delete()

            # this clause sets up the location, sublocation and spawns the object
            # set based on your needs
            for obj in spawned_objects:
                obj['location'] = self
                obj['sublocation'] = 'in'
                prototypes.spawner.spawn(obj)

