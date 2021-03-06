"""
Room

Rooms are simple containers that has no location of their own.

"""

from evennia import DefaultRoom
from objects import ExtendedDefaultObject

class Room(ExtendedDefaultObject, DefaultRoom):
    """
    Rooms are like any Object, except their location is None
    (which is default). They also use basetype_setup() to
    add locks so they cannot be puppeted or picked up.
    (to change that, use at_object_creation instead)

    See examples/object.py for a list of
    properties and methods available on all Objects.
    """
    def basetype_setup(self):
        super(Room, self).basetype_setup()
        self.locks.add("put:false()")


class CharacterGeneratorRoom(Room):
    """
    This is the base room type for character generation
    """

    def at_object_receive(self, character, source_location):
        """
        Assign properties on characters
        """

        health = self.db.char_health or 20

        if character.has_account:
            character.db.health = health
            character.db.health_max = health
        
        if character.is_superuser:
            string = "-"*78 + "YOU ARE SUPERUSER" + "-"*78
            character.msg("%s" % string.format(name=character.key, quell="@quell"))
