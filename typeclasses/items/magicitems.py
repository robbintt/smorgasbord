""" Magical object typeclasses
"""
from typeclasses.objects import Object
from evennia import utils


class DamageOrb(Object):
    """ An orb that deals damage when it is touched.
    """
    def at_object_creation(self):
        """
        """
        super(DamageOrb, self).at_object_creation()
        self.db.damage = 5
        self.locks.add("get:false()")
        self.locks.add("put:false()")
        self.locks.add("touch:all()")

    def at_touched(self, toucher):
        if toucher.db.health:
            # health needs to know when it is changed and ensure
            # it is between 0 and self.db.max)health
            toucher.db.health -= self.db.damage

        self.location.msg_contents(
            "Black smoke coughs upwards from {item}.", 
            mapping={"item": self} )

class HealingOrb(Object):
    """ An orb that removes damage when it is touched.
    """
    def at_object_creation(self):
        super(HealingOrb, self).at_object_creation()
        """
        """
        self.db.healing = 5
        self.db.focus_delay = 0
        self.locks.add("get:false()")
        self.locks.add("put:false()")
        self.locks.add("touch:all()")

    def at_touched(self, toucher):
        if toucher.db.health:
            # health needs to know when it is changed and ensure
            # it is between 0 and self.db.max)health
            toucher.db.health += self.db.healing


class MagicalWand(Object):
    """ A magical wand
    """
    def at_object_creation(self):
        """
        """
        super(MagicalWand, self).at_object_creation()
        self.db.charge = 0
        self.db.charge_max = 3
        self.db.focus_delay = 3
        self.db.touch_delay = 0
        self.db.touch_when_charged_delay = 5
        self.locks.add("get:all()")
        self.locks.add("touch:all()")
        self.locks.add("focus:all()")
        self.locks.add("put:all()")

    def at_touched(self, toucher):
        """
        """
        def local_remove_busy_flag(retval=None):
            """ Removes the busy flag from caller
            """
            del toucher.ndb.busy
            try:
                toucher_message = "The {} releases you from its grip."
                toucher.msg(toucher_message.format(self.get_display_name(toucher)))
            except AttributeError:
                toucher.msg(toucher_message.format(self.key))


        if self.db.charge >= self.db.charge_max:
            try:
                toucher_message = "As you touch the {}, a flash of light floods the area."
                toucher.msg(toucher_message.format(self.get_display_name(toucher)))
            except AttributeError:
                toucher.msg(toucher_message.format(self.key))
            self.location.msg_contents(
                "The {item} cracks and a flash of light floods the area.",
                exclude=toucher,
                mapping={"toucher" : toucher, "item": self} )

            if self.db.touch_when_charged_delay > 0:
                toucher.ndb.busy = True
                utils.delay(self.db.focus_delay, callback=local_remove_busy_flag, retval=None)


        elif self.db.charge > 0:
            try:
                toucher_message = "As you touch the {}, it glows weakly and abruptly goes dark."
                toucher.msg(toucher_message.format(self.get_display_name(toucher)))
            except AttributeError:
                toucher.msg(toucher_message.format(self.key))
            self.location.msg_contents(
                "The {item} glows weakly and abruptly goes dark.",
                exclude=toucher,
                mapping={"toucher" : toucher, "item": self} )
        else:
            pass

        self.db.charge = 0

    def at_focused(self, focuser):
        """
        """

        if self.db.charge < self.db.charge_max:
            self.db.charge += 1
            try:
                focuser_message = "As you focus on the {}, it glows faintly with a grey light."
                focuser.msg(focuser_message.format(self.get_display_name(focuser)))
            except AttributeError:
                focuser.msg(toucher_message.format(self.key))
            self.location.msg_contents(
                "The {item} glows faintly with a grey light.", 
                exclude=focuser,
                mapping={"item": self} )
        else:
            # this optionally could not run a timer, how do i implement that
            # it may actually be tested elsewhere
            try:
                focuser_message = "As you focus on the {}, it pulses briefly and seems to reject additional charge."
                focuser.msg(focuser_message.format(self.get_display_name(focuser)))
            except AttributeError:
                focuser.msg(toucher_message.format(self.key))
            self.location.msg_contents(
                "The {item} pulses briefly, indicating it is fully charged.", 
                exclude=focuser,
                mapping={"item": self} )


class SpellScroll(Object):
    """ Template for scrolls
    """
    def at_object_creation(self):
        """
        """
        super(SpellScroll, self).at_object_creation()
        self.locks.add("get:all()")
        self.locks.add("touch:all()")
        self.locks.add("focus:all()")
        self.locks.add("read:all()")
        self.locks.add("put:all()")

    def at_objectread(self, reader):
        """ Effects of reading the scroll

        By default the scroll will: 
            1. pass the spell to the player's active spell slot
            2. self destruct
        """
        self.delete()


class HealingSpellScroll(SpellScroll):
    """ Demo scroll for casting HealingSpell, a spell to improve player health
    """

