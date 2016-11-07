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


    Smorgasbord
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
        """ Object creation happens before character generation so it shouldn't
        be run again

        If you want to be able to extend characters after generation, please use
        a separate function and call it during character generation to ensure 
        new characters get those features.

        Customizable stats should be generated in character generation and can 
        be changed by in-game events.

        Improveable should be initialized in at_object_creation and changed by 
        in-game events.
        """
        super(Character, self).at_object_creation()

        # would be valuable to have a character_update_health function which 
        # manages max health and triggers death.
        self.db.health = 20
        self.db.max_health = 40

        class BodyPart(object):
            """ An object mixin to define a body part.

            Basic Features:
            Body parts should be contents of the character and should 
            have limited interactivity. For example, a player's arm
            could be 'grab'-able, and eye should be 'poke'-able.
            Allowing these features creates a pretty complex brawl
            system that is beyond the scope of this class though.

            The most important features will be rich verb locks and
            a responsive system for the body part 'responding' properly
            when a verb is available for interaction.

            Body Part vs. Inventory:
            A player is an object and can have both body parts and inventory
            items.  However, we don't want to put a player's body parts
            in their backpack.  A player also shouldn't have an ethereal
            'inventory'.  So a player should not be able to have items
            'inside' them, e.g. they should not be a container.
            THIS MEANS WE NEED TO BUILD A RICHER CONTAINER TYPE AND TURN
            IT OFF BY DEFAULT. CONTAINER COULD BE TURNED OFF BY USING 
            verb lock() OR IT COULD BE MANAGED AT A HIGHER LEVEL WITH A FLAG.
            If a character does not have the container type then they couldn't
            have body parts inside them, so they would need to be a restricted
            container, maybe with all locks turned on or whatever.

            If some limbs all have an 'on' slot, then you could do:
            > put backpack on back
            This would fill the 'on' slot of the back.
            This is different than an 'in' slot.
            For example, if you had a table you could put stuff 'on' or 'under'
            the table and each spot would be a different 'place' or 'container'.
            HOW TO MANAGE THIS DIFFERENCE IN PHILOSPHY ABOUT "CONTAINER SPACE"?

            Possible containers: on, in, under, behind...
            NOTE: Three of these are environmental orientations.
            NOTE: Not all containers would need to exist for all objects
            NOTE: Can the current 'in' default be replicated for the others?

            Body Part Slots:
            A body part could have a 'slot' used for holding an item.

            "You put the backpack on your back" would fill the 'back' slot.
            A view could then be built by assessing your limbs.

            
            Content Location Management:
            ============================

            Object has a sublocation tag property: 'on', 'in', 'under', 'behind'

            These sublocations are PREPOSITIONS!

            Views and gets should be managed using these prepositions.

            Receiving location must have the attempted sublocation tag available

            The object's tag can be set by the receiving object when it's
            location changes.  The object also resets its own property tag
            whenever its location changes.  The object reaction has to act first
            so the new tag is kept.


            Currently lock is just on the verb get, so it would not need
            to know anything about sublocation tagging to work.

            There should be some sort of advanced locking though. You can get a 
            photo on a safe but you cannot get a bag of gold in a safe.

            Views and gets can be filtered by sublocation tag. Sublocation tags
            could also be managed by locks. This is a bit more complex.


            14:27 < robbintt> from what i see, the contents management is pretty
                deep inside evennia core, so i will probably need to work out 
                some sort of contents tagging system
            14:28 < robbintt> it seems messy to add state every time something 
                is moved but it might work out
            14:29 < robbintt> for example, when an object is put 'on' the table,
                it gets an 'on' tag, and when you look table you might see 
                everything for all of the table's tags,
                but when you look on table you might see the filtered view
            14:29 < robbintt> then when the object is moved again, it wipes its 
                location tag and wherever it ends up might set a new one


            Using Tags with the built in search() method?
            =============================================

            search: https://github.com/evennia/evennia/blob/master/evennia/objects/objects.py#L270
            All objects can search in their location.
            Does this default search support some sort of tagging?

            01:28 < robbintt> i might be able to complete what i want by 
                chaining attribute_name searches
            01:29 < robbintt> say there is a vase on a table and i use the 
                command 'get vase on table'
            01:29 < robbintt> first it queries the table for a vase, then it 
                queries the resulting vases for one with the sublocation "on"

            How would chaining those queries go?


            Body Part Properties:
            =====================

            max_health:
            the health after which the body part is destroyed
            
            scarring: 
            this value is 'temporary lost max_hp'
            
            essential_to_live:
            if True, if the body part is destroyed, the player should die

            idea - tattoos:
            ==============
            This means you will be able to read someone's arm if the permissions
            are right and they have something there to read.
            

            Attacking a Body Part:
            ======================
            An attacker needs to be able to query a Character to see what they 
            can attack, what body parts exist.
            Then they can target that body part... That's pretty complex though.

            assess (person) could give a list of targets
            
            Then an attack should have a higher chance of hitting body parts in 
            proximity to that one...

            So body parts do need a proximity or something.
            Also smaller parts are harder to hit.
            But aiming for the eye shouldn't reduce the total to-hit, as the 
            head is a bigger target around the eye.

            But then what incentive is there to aim for anything but the eye? 
            Maybe the head is harder to hit than the body

            Also arms would be pretty hard to hit and chest might be considered
            the 'baseline' ease to hit.

            Limb Damage:
            ============

            Certain limb damage may turn off command sets for the player. 
            This needs handled in a smart way.

            Limb damage could also cause the player to drop items on that limb.
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
    



