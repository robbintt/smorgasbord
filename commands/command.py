"""
Commands

Commands describe the input the player can do to the game.

"""

from evennia import Command as BaseCommand

from evennia import default_cmds, utils

# used by CmdGet which is plucked and modded from evennia.commands.default.general
from evennia import settings
COMMAND_DEFAULT_CLASS = utils.class_from_module(settings.COMMAND_DEFAULT_CLASS)

class Command(BaseCommand):
    """
    Inherit from this if you want to create your own command styles
    from scratch.  Note that Evennia's default commands inherits from
    MuxCommand instead.

    Note that the class's `__doc__` string (this text) is
    used by Evennia to create the automatic help entry for
    the command, so make sure to document consistently here.

    Each Command implements the following methods, called
    in this order (only func() is actually required):
        - at_pre_command(): If this returns True, execution is aborted.
        - parse(): Should perform any extra parsing needed on self.args
            and store the result on self.
        - func(): Performs the actual work.
        - at_post_command(): Extra actions, often things done after
            every command, like prompts.

    """
    pass

#------------------------------------------------------------
#
# The default commands inherit from
#
#   evennia.commands.default.muxcommand.MuxCommand.
#
# If you want to make sweeping changes to default commands you can
# uncomment this copy of the MuxCommand parent and add
#
#   COMMAND_DEFAULT_CLASS = "commands.command.MuxCommand"
#
# to your settings file. Be warned that the default commands expect
# the functionality implemented in the parse() method, so be
# careful with what you change.
#
#------------------------------------------------------------

#from evennia.utils import utils
#class MuxCommand(Command):
#    """
#    This sets up the basis for a MUX command. The idea
#    is that most other Mux-related commands should just
#    inherit from this and don't have to implement much
#    parsing of their own unless they do something particularly
#    advanced.
#
#    Note that the class's __doc__ string (this text) is
#    used by Evennia to create the automatic help entry for
#    the command, so make sure to document consistently here.
#    """
#    def has_perm(self, srcobj):
#        """
#        This is called by the cmdhandler to determine
#        if srcobj is allowed to execute this command.
#        We just show it here for completeness - we
#        are satisfied using the default check in Command.
#        """
#        return super(MuxCommand, self).has_perm(srcobj)
#
#    def at_pre_cmd(self):
#        """
#        This hook is called before self.parse() on all commands
#        """
#        pass
#
#    def at_post_cmd(self):
#        """
#        This hook is called after the command has finished executing
#        (after self.func()).
#        """
#        pass
#
#    def parse(self):
#        """
#        This method is called by the cmdhandler once the command name
#        has been identified. It creates a new set of member variables
#        that can be later accessed from self.func() (see below)
#
#        The following variables are available for our use when entering this
#        method (from the command definition, and assigned on the fly by the
#        cmdhandler):
#           self.key - the name of this command ('look')
#           self.aliases - the aliases of this cmd ('l')
#           self.permissions - permission string for this command
#           self.help_category - overall category of command
#
#           self.caller - the object calling this command
#           self.cmdstring - the actual command name used to call this
#                            (this allows you to know which alias was used,
#                             for example)
#           self.args - the raw input; everything following self.cmdstring.
#           self.cmdset - the cmdset from which this command was picked. Not
#                         often used (useful for commands like 'help' or to
#                         list all available commands etc)
#           self.obj - the object on which this command was defined. It is often
#                         the same as self.caller.
#
#        A MUX command has the following possible syntax:
#
#          name[ with several words][/switch[/switch..]] arg1[,arg2,...] [[=|,] arg[,..]]
#
#        The 'name[ with several words]' part is already dealt with by the
#        cmdhandler at this point, and stored in self.cmdname (we don't use
#        it here). The rest of the command is stored in self.args, which can
#        start with the switch indicator /.
#
#        This parser breaks self.args into its constituents and stores them in the
#        following variables:
#          self.switches = [list of /switches (without the /)]
#          self.raw = This is the raw argument input, including switches
#          self.args = This is re-defined to be everything *except* the switches
#          self.lhs = Everything to the left of = (lhs:'left-hand side'). If
#                     no = is found, this is identical to self.args.
#          self.rhs: Everything to the right of = (rhs:'right-hand side').
#                    If no '=' is found, this is None.
#          self.lhslist - [self.lhs split into a list by comma]
#          self.rhslist - [list of self.rhs split into a list by comma]
#          self.arglist = [list of space-separated args (stripped, including '=' if it exists)]
#
#          All args and list members are stripped of excess whitespace around the
#          strings, but case is preserved.
#        """
#        raw = self.args
#        args = raw.strip()
#
#        # split out switches
#        switches = []
#        if args and len(args) > 1 and args[0] == "/":
#            # we have a switch, or a set of switches. These end with a space.
#            switches = args[1:].split(None, 1)
#            if len(switches) > 1:
#                switches, args = switches
#                switches = switches.split('/')
#            else:
#                args = ""
#                switches = switches[0].split('/')
#        arglist = [arg.strip() for arg in args.split()]
#
#        # check for arg1, arg2, ... = argA, argB, ... constructs
#        lhs, rhs = args, None
#        lhslist, rhslist = [arg.strip() for arg in args.split(',')], []
#        if args and '=' in args:
#            lhs, rhs = [arg.strip() for arg in args.split('=', 1)]
#            lhslist = [arg.strip() for arg in lhs.split(',')]
#            rhslist = [arg.strip() for arg in rhs.split(',')]
#
#        # save to object properties:
#        self.raw = raw
#        self.switches = switches
#        self.args = args.strip()
#        self.arglist = arglist
#        self.lhs = lhs
#        self.lhslist = lhslist
#        self.rhs = rhs
#        self.rhslist = rhslist
#
#        # if the class has the player_caller property set on itself, we make
#        # sure that self.caller is always the player if possible. We also create
#        # a special property "character" for the puppeted object, if any. This
#        # is convenient for commands defined on the Player only.
#        if hasattr(self, "player_caller") and self.player_caller:
#            if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                # caller is an Object/Character
#                self.character = self.caller
#                self.caller = self.caller.player
#            elif utils.inherits_from(self.caller, "evennia.players.players.DefaultPlayer"):
#                # caller was already a Player
#                self.character = self.caller.get_puppet(self.session)
#            else:
#                self.character = None
#

class CmdGet(COMMAND_DEFAULT_CLASS):
    """ Modified from standard CmdGet
    
    Modified version checks to see if self.args has " in ". If it does, then
    the location, arg2, is set as the location and the command proceeds.


    Standard CmdGet DocString:
    =================
    pick up something

    Usage:
      get <obj>

    Picks up an object from your location and puts it in
    your inventory.
    """
    key = "get"
    aliases = "take" # how do i do two aliases?
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "implements the command."

        caller = self.caller

        if not self.args:
            caller.msg("Get what?")
            return

        in_count = len([x for x in self.args.split() if x == "in"])
        if in_count > 1:
            caller.msg("Too many 'in' terms, please use 'in' once to retrieve from a container.")
            return

        elif in_count == 1:
            item, _, container = self.args.partition(" in ")
            location = caller.search(container, location=caller.location)
            if not location:
                caller.msg("Could not find {}".format(container))
                return
            caller_message = "You get {object} from {location}."
            location_message = "{caller} gets {object} from {location}."
        else:
            item = self.args
            location = caller.location
            caller_message = "You pick up {object}."
            location_message = "{caller} picks up {object}"


        # consider making this search silent and using the commented message if it is not found
        obj = caller.search(item, location=location)
        if not obj:
            # caller.msg("Get what?")
            return
        if caller == obj:
            caller.msg("You can't get yourself.")
            return
        if not obj.access(caller, 'get'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        message_data = { "object" : obj.name, "location" : location, "caller" : caller }
        obj.move_to(caller, quiet=True)
        caller.msg(caller_message.format(**message_data))
        caller.location.msg_contents(location_message.format(**message_data),
                                     exclude=caller)
        # calling hook method
        obj.at_get(caller)


class CmdPut(COMMAND_DEFAULT_CLASS):
    """ put X in Y command.

    This command should be expanded to support on, under, etc. - however, objets must have these things...
    
    Modified from custom CmdGet (in this file)

    FUTURE:
    'put' - put an object into another object
    The 'put' verb allows you to convey an object to a new location, generally
    inside a container.
    Mechanism: One object (generally character) conveys a second object into a
    third object. The third object must be able to contain other objects.
    Object1 - generally character
    Object2 - object being moved
    Object3 - container object
    
    HOW:
    1. Object1 (inside Location1) uses the 'put' verb on Object2 and Object3
    2. Object2 is searched for in: Object1, Location1
        - A custom search can be done later using search() method features
    3. (Object2 must be touched by Object1, so it must do a 'get' interaction)
        - Object2 would then be inside Object1...
        - IMPORTANT: So should this interaction be managed and completed???
    4. Object1 notifies Object2 and Object3:
        1. Object1 tells Object2 it wishes to put Object2 inside Object3.
            - The verb 'put' called from Object1 gives Object3 to Object2
            - 
        2. Object1 tells Object3 it wishes to put Object2 inside Object3.
        3. Either method may reject the interaction and give Object1 an error.
        4. At this point, Object2 may either be in Object1 or 
            at its original location? How are errors resolved?
    5. Object3 accepts Object2. Follow the Object2.move_to(Object3) pattern.
        - The Object2.at_moved() method interacts with Object1 and then Object3
        - This should happen in the Object3.at_received() method.
    6. Any tests are performed in at_moved() and at_receive()

    NOTE:
    In a sense this is already happening with search but location does not get
    a say in if the get and put command succeeds.
    BENEFIT:
    Locations can easily have item or weight limits or interact with with the
    player by acting differently when items are dropped or taken if this
    paradigm is generalized.
    """
    key = "put"
    locks = "cmd:all()"
    arg_regex = r"\s|$"

    def func(self):
        "implements the command."

        caller = self.caller

        if not self.args:
            caller.msg("Put what?")
            return

        in_count = len([x for x in self.args.split() if x == "in"])
        if in_count > 1:
            caller.msg("Too many 'in' terms, please use 'in' once to retrieve from a container.")
            return

        if in_count < 1:
            caller.msg("Put {} in what?".format(self.args))
            return

        elif in_count == 1:
            item, _, container = self.args.partition(" in ")
            # default to caller as location (in "hands") or however it works.
            # this is bad as it always defaults to caller first, so if caller has 3
            # backpacks and there are 3 on the ground, then you cannot access the 3 
            # on the ground.  other MUDs use 'my' to signify one in my inventory.
            # now i see why.
            destination = caller.search(container, location=caller, nofound_string=" ")
            if not destination:
                destination = caller.search(container, location=caller.location, nofound_string="Put it where?")
            if not destination:
                return
            caller_message = "You put {object} in {location}."
            location_message = "{caller} puts {object} in {location}."

        location = caller.location

        # consider making this search silent and using the commented message if it is not found
        obj = caller.search(item, location=caller, nofound_string=" ")
        if not obj:
            obj = caller.search(item, location=location, nofound_string="Put what?")
            if not obj:
                return
        if caller is obj:
            caller.msg("You can't think of a way to do that.")
            return
        if destination is obj:
            caller.msg("You cannot put something inside itself.")
            return
        if not obj.access(caller, 'put'):
            if obj.db.get_err_msg:
                caller.msg(obj.db.get_err_msg)
            else:
                caller.msg("You can't get that.")
            return

        message_data = { "object" : obj.name, "location" : destination, "caller" : caller }
        obj.move_to(destination, quiet=True)
        caller.msg(caller_message.format(**message_data))
        caller.location.msg_contents(location_message.format(**message_data),
                                     exclude=caller)
        # calling hook method
        obj.at_put(caller)


class CmdObjectInteraction(default_cmds.MuxCommand):
    """ middleware Class for any command in which 2 objects interact

    A number of commands follow the same model.
        1. parse command
        2. pass error messages to the caller
        3. The player is given a delay
        4. The target object's receiving `at_` function is triggered

    This is middleware for verbs that govern interaction between two objects.

    # The following variables are consumed by `func` for the particular action
    # example: 'read' verb
    key = "read"
    locks = "cmd:all()"
    caller_busy_error = "You are a little busy for that."
    caller_done_msg = "You finish reading the {}."
    object_notexist_error = "Read what?"
    # no object given defaults to the same error as if the object is not found
    no_object_given_error = object_notexist_error
    # at_caller will trigger the at_called method for the specific verb
    at_caller = 'at_read'
    
    FUTURE: 
    generalizing this for prepositions clears the way for both location
    specific searches and for three-way interactions like 'put' and 'get'.
    Can they fit in the same method?
    Under the 'read, focus, touch' paradigm, the object following the
    preposition defines the search() space.  Under the 'get, put' paradigm,
    the preposition defines the search space as well.  In fact, any of these
    verbs without a preposition defines the search space, too.  The question
    is whether we want the 'location' to have an opportunity to interact
    with the object activating the verb before the verb is completed.
    This is good news, I think.
    """
    def __init__(self):
        super(CmdObjectInteraction, self).__init__()
        
        # this does not belong here, it needs registered globally and imported.
        self.COMMAND_PREPOSITIONS = ["in", "under", "behind", "on"]
        
        # put other sane defaults here so they don't need redefined
        self.disallowed_prepositions = []
        self.error_preposition_disallowed = "You can't do that from here."
        self.error_too_many_prepositions = "Please use only one preposition from: {}".format(self.COMMAND_PREPOSITIONS)
        self.command_requires_preposition = False
        self.error_command_requires_preposition = "This command requires a location."
        self.error_location_notexist = "Can't find the location of the object."
        self.error_locationpreposition_notexist = "You can't seem to get there on that."
        self.caller_busy_error = "You are a little busy for that."


    def func(self):
        """ The method that handles any parsing and triggers the interaction

        getattr is used to get the response of the caller's at_ function. The
        function name is contained in the at_caller string.
        """
        
        if self.caller.ndb.busy:
            self.caller.msg(self.caller_busy_error)
            return
        
        if not self.args:
            self.caller.msg(self.no_object_given_error)
            return

        # parse args for prepositions received by location
        # we need to know the location to know if it accepts the preposition
        prepositions = [x for x in self.args.split() 
                                    if x in self.COMMAND_PREPOSITIONS]

        preposition_count = len(prepositions)
        if preposition_count > 1:
            caller.msg(self.error_too_many_prepositions)
            return
        
        # If a preposition is not necessary, this sets target from args
        elif preposition_count == 0:
            location = None  # not passed to search(), unnecessary 
            
            # some commands MUST have a preposition and a receiving object
            if self.command_requires_preposition:
                caller.msg(self.error_command_requires_preposition)
                return

            target = self.caller.search(self.args)
            if not target:
                self.caller.msg(self.object_notexist_error)
                return

        # If a preposition is necessary, this route handles args and errors
        elif preposition_count == 1:
            preposition = prepositions[0]
            target_object, _prep, target_location = self.args.partition(preposition)
            target_object = target_object.strip()
            target_location = target_location.strip()

            location = self.caller.search(target_location)
            if not location:
                self.caller.msg(self.error_location_notexist)
                return

            target = self.caller.search(target_object, location=location)
            if not target:
                self.caller.msg(self.object_notexist_error)
                return

            # don't continue if the preposition isn't valid in that location
            # this does require that containers have the 'in' location.
            # also, it may make a preposition a requirement for accessing a
            # container. Is this good enough?
            # things can be in things but inaccessible. good!
            if preposition not in location.db.prepositions:
                self.caller.msg(self.error_locationpreposition_notexist)
                return

            # disallowed_prepositions and error_preposition_disallowed should be
            # set in the child Command class. An example would be if you don't
            # want people to read a book while it is in something.
            if preposition in self.disallowed_prepositions:
                self.caller.msg(self.error_preposition_disallowed)
                return


        # update resulting messages to have the preposition if not Location
        # example: "You touch the blanket in the basket."


        # this needs to happen last so each object can delete itself
        at_caller_function = getattr(self.caller, self.at_caller)
        self.msg(at_caller_function(target, target_location=location))


class CmdRead(CmdObjectInteraction):
    """ Use middleware to provide CmdRead.
    """
    key = "read"
    locks = "cmd:all()"
    object_notexist_error = "Read what?"
    # no object given defaults to the same error as if the object is not found
    no_object_given_error = object_notexist_error
    # at_caller will trigger the at_called method for the specific verb
    at_caller = 'at_read'
    # optional, default is no disallowed prepositions
    disallowed_prepositions = ["in"]
    error_preposition_disallowed = "You can't read that from here."

class CmdFocus(CmdObjectInteraction):
    """ Use middleware to provide CmdFocus.
    """
    key = "focus"
    locks = "cmd:all()"
    object_notexist_error = "Focus on what?"
    # no object given defaults to the same error as if the object is not found
    no_object_given_error = object_notexist_error
    # at_caller will trigger the at_called method for the specific verb
    at_caller = 'at_focus'

class CmdTouch(CmdObjectInteraction):
    """ Use middleware to provide CmdTouch.
    """
    key = "touch"
    locks = "cmd:all()"
    object_notexist_error = "Touch what?"
    # no object given defaults to the same error as if the object is not found
    no_object_given_error = object_notexist_error
    # at_caller will trigger the at_called method for the specific verb
    at_caller = 'at_touch'
