"""
Characters

Characters are (by default) Objects setup to be puppeted by Players.
They are what you "see" in game. The Character class in this module
is setup to be the "default" character type created by the default
creation commands.

"""
from evennia import DefaultCharacter
from objects import ExtendedDefaultObject, Object

class Character(DefaultCharacter, ExtendedDefaultObject):
    """
    The Character defaults to reimplementing some of base Object's hook methods with the
    following functionality:

    at_basetype_setup - always assigns the DefaultCmdSet to this object type
                    (important!)sets locks so character cannot be picked up
                    and its commands only be called by itself, not anyone else.
                    (to change things, use at_object_creation() instead).
    at_after_move - Launches the "look" command after every move.
    at_post_unpuppet(player) -  when Player disconnects from the Character, we
                    store the current location in the pre_logout_location Attribute and
                    move it to a None-location so the "unpuppeted" character
                    object does not need to stay on grid. Echoes "Player has disconnected" 
                    to the room.
    at_pre_puppet - Just before Player re-connects, retrieves the character's
                    pre_logout_location Attribute and move it back on the grid.
    at_post_puppet - Echoes "PlayerName has entered the game" to the room.


    Smorgasbord:
    There are a few categories of character attributes:
        1. Integral - limbs: arms, legs, etc. Equipment slots, etc.
        2. Customizable - blue eyes, long hair, blonde hair, etc.
        3. Improveable - skills trained, stats raised, levels, etc.

    Integral attributes are added as attributes of the Character class.
    Updating integral stats will change the way all characters behave.
    This means they update whenever the model is reloaded.
    """
    def basetype_setup(self):
        super(Character, self).basetype_setup()
        self.locks.add("put:false()")
        
    def at_object_creation(self):
        """ Object creation happens before character generation so it shouldn't be run again

        If you want to be able to extend characters after generation, please use a separate function
        and call it during character generation to ensure new characters get those features.

        Customizable stats should be generated in character generation and can be changed by in-game events.

        Improveable should be initialized in at_object_creation and changed by in-game events.
        """
        super(Character, self).at_object_creation()

        # would be valuable to have a character_update_health function which manages max health and triggers death.
        self.db.health = 20
        self.db.max_health = 40

        class BodyPart(object):
            """ A mixin for each body part as an Object

            This means you will be able to read someone's arm if the permissions are right and they have something there to read.

            An attacker needs to be able to query a Character to see what they can attack, what body parts exist.
            Then they can target that body part... That's pretty complex though.
            assess (person) could give a list of targets
            Then an attack should have a higher chance of hitting body parts in proximity to that one...
            So body parts do need a proximity or something.
            Also smaller parts are harder to hit.
            But aiming for the eye shouldn't reduce the total to-hit, as the head is a bigger target around the eye.
            But then what incentive is there to aim for anything but the eye? Maybe the head is harder to hit than the body
            Also arms would be pretty hard to hit and chest is obviously the 'baseline' ease to hit.

            Certain limb damage may also turn off command sets for the player. This needs handled in a smart way.
            """
            self.db.essential_to_live = False
            self.db.max_health = 10000
            self.db.health = self.db.max_health
            self.db.scarring = 0

            def health_changed(self, amount):
                """ Handle all logic up to and including death or full health.

                Damage - Amount is negative
                Healing - Amount is positive

                Player can be messaged with an effect according to the:
                    - direction, negative or positive
                    - magnitude absolute or percentage of total
                    - any resulting effects or cancelled effects
                    - initial or final state of the body part

                Where will status effects like poison, paralysis, be added?

                """
                self.db.health += change_amount


        class RightEye(Object, BodyPart):
            """
            """
            self.db.essential_to_live = False
            self.db.max_health = 2000
            self.db.scarring = 0
            self.db.health = self.db.max_health
    



