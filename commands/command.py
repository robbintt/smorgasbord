"""
Commands

Commands describe the input the account can do to the game.

"""

from evennia import Command as BaseCommand

from evennia import default_cmds, utils

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
#        # if the class has the account_caller property set on itself, we make
#        # sure that self.caller is always the account if possible. We also create
#        # a special property "character" for the puppeted object, if any. This
#        # is convenient for commands defined on the Account only.
#        if hasattr(self, "account_caller") and self.account_caller:
#            if utils.inherits_from(self.caller, "evennia.objects.objects.DefaultObject"):
#                # caller is an Object/Character
#                self.character = self.caller
#                self.caller = self.caller.account
#            elif utils.inherits_from(self.caller, "evennia.accounts.accounts.DefaultAccount"):
#                # caller was already an Account
#                self.character = self.caller.get_puppet(self.session)
#            else:
#                self.character = None
#


class CmdObjectInteraction(default_cmds.MuxCommand):
    """ middleware Class for any command in which 2 objects interact

    A number of commands follow the same model.
        1. parse command
        2. pass error messages to the caller
        3. The account is given a delay
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
    # override as necessary in each command
    arg_regex = r"\s|$"
    locks = "cmd:all()"

    def __init__(self):
        """
        Override init as necessary
        """
        super(CmdObjectInteraction, self).__init__()

        # this does not belong here, it needs registered globally and imported.
        # we also need preposition aliases aka "in" can be "into" "inside"
        self.COMMAND_PREPOSITIONS = ["in", "under", "behind", "on"]
        
        # put other sane defaults here so they don't need redefined
        self.disallowed_prepositions = []
        self.error_preposition_disallowed = "You can't do that from here."
        self.error_too_many_prepositions = "Please use only one preposition from: {}".format(self.COMMAND_PREPOSITIONS)
        self.command_requires_preposition = False
        self.error_command_requires_preposition = "This command requires a location."
        self.error_location_notexist = "You cannot locate that."
        self.error_locationpreposition_notexist = "Nothing could fit there."
        self.caller_busy_error = "You are a little busy for that."
        self.targetless_allowed = False
        self.target = None


    def func(self):
        """ The method that handles any parsing and triggers the interaction

        getattr is used to get the response of the caller's at_ function. The
        function name is contained in the at_caller string.
        """
        # ensure target is at least set from default
        # in the future it may be helpful to rebuild this control flow so
        # that different targets take precedence
        # right now the target is inferred by the control flow below
        target = self.target
        
        # a default variable check here could make busy optional. 
        # maybe there is a better place though.
        if self.caller.ndb.busy:
            self.caller.msg(self.caller_busy_error)
            return
        
        if not self.args:
            if self.targetless_allowed:
                # use the location as a target, this may not solve all cases...
                # make sure that at_(whatever) can manage target=None
                # in the case that the character has no location
                target = self.caller.location
            else:
                self.caller.msg(self.no_object_given_error)
                return

        # parse args for prepositions received by location
        # we need to know the location to know if it accepts the preposition
        prepositions = [x for x in self.args.split() 
                                    if x in self.COMMAND_PREPOSITIONS]

        preposition_count = len(prepositions)
        if preposition_count > 1:
            self.caller.msg(self.error_too_many_prepositions)
            return
        
        # If a preposition is not necessary, this sets target from args
        elif preposition_count == 0:
            preposition = None 
            location = None
            
            # some commands MUST have a preposition and a receiving object
            if self.command_requires_preposition:
                self.caller.msg(self.error_command_requires_preposition)
                return

            # only try to set the target if it is not already set
            # currently it would only have been set if the command was
            # sent 'empty' and the command is allowed to be empty
            if not target:
                target = self.caller.search(self.args)
            # if a target still isn't found
            if not target:
                self.caller.msg(self.object_notexist_error)
                return

        # If a preposition is necessary, this route handles args and errors
        elif preposition_count == 1:
            # hack: add a leading space to self.args so that if the preposition is the
            # first argument, it can be easily found. All spaces are stripped later.
            self.args = " " + self.args

            preposition = prepositions[0]
            preposition_parsed = " " + preposition + " "
            target_object, _prep, target_location = self.args.partition(preposition_parsed)
            target_object = target_object.strip()
            target_location = target_location.strip()
            
            location = self.caller.search(target_location)
            if not location:
                self.caller.msg(self.error_location_notexist)
                return
            contents = [obj for obj in location.contents 
                    if obj.access(self.caller, self.key)
                    and obj.db.sublocation == preposition]

            # switch the location and the source if the command is a 'put'
            # would prefer to separate this functionality
            if self.key == "put":
                # optionally the location could be the caller
                # this would turn off 'put' from the ground
                target = self.caller.search(target_object)
                
            # look has a special case of lacking target_object
            # in other words, 'look in y' is valid
            elif self.key == "look" and not target_object:
                # retarget a look command of the form 'look in y'
                # (look command with no target_object)
                target = location
                location = None
                
            # the default object interaction 'touch x in y'
            else:
                # contents is location.contents filtered by preposition
                target = self.caller.search(target_object, candidates=contents)
            if not target:
                self.caller.msg(self.object_notexist_error)
                return

            # don't continue if the preposition isn't valid in that location
            # this does require that containers have the 'in' location.
            # also, it may make a preposition a requirement for accessing a
            # container. Is this good enough?
            # things can be in things but inaccessible. good!
            if (location and preposition not in location.db.prepositions) or \
                (not location and preposition not in target.db.prepositions):
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
        # note that if the target is the location then the target=target_location
        at_caller_function = getattr(self.caller, self.at_caller)
        self.msg(at_caller_function(
            target, 
            target_location=location, 
            preposition=preposition))


class CmdRead(CmdObjectInteraction):
    """ Use middleware to provide CmdRead.
    """
    key = "read"
    at_caller = "at_read"
    def __init__(self):
        super(CmdRead, self).__init__()
        self.object_notexist_error = "Read what?"
        self.no_object_given_error = self.object_notexist_error
        # optional, default is no disallowed prepositions
        self.disallowed_prepositions += ["in"]
        self.error_preposition_disallowed = "You can't read that from here."

class CmdFocus(CmdObjectInteraction):
    """ Use middleware to provide CmdFocus.
    """
    key = "focus"
    at_caller = "at_focus"
    def __init__(self):
        super(CmdFocus, self).__init__()
        self.object_notexist_error = "Focus on what?"
        self.no_object_given_error = self.object_notexist_error

class CmdTouch(CmdObjectInteraction):
    """ Use middleware to provide CmdTouch.
    """
    key = "touch"
    at_caller = "at_touch"
    def __init__(self):
        super(CmdTouch, self).__init__()
        self.object_notexist_error = "Touch what?"
        self.no_object_given_error = self.object_notexist_error

class CmdStir(CmdObjectInteraction):
    """ Use middleware to provide CmdStir
    """
    key = "stir"
    at_caller = "at_stir"
    def __init__(self):
        super(CmdStir, self).__init__()
        self.object_notexist_error = "Stir what?"
        self.no_object_given_error = self.object_notexist_error

class CmdGet(CmdObjectInteraction):
    """ Use middleware to provide CmdGet.

    A number of convenience aliases could exist for get.
    'get first|second|1|2|last in bag' - get the positional item in a bag
    positional gets would not require specifying what item it is. are 
    objects stored in a list in containers currently? it should be for inv mgmt.
    """
    key = "get"
    aliases = ["take"]
    at_caller = "at_get"
    def __init__(self):
        super(CmdGet, self).__init__()
        self.object_notexist_error = "Get what?"
        self.no_object_given_error = self.object_notexist_error

class CmdPut(CmdObjectInteraction):
    """ Use middleware to provide CmdPut.
    """
    key = "put"
    at_caller = "at_put"
    def __init__(self):
        super(CmdPut, self).__init__()
        self.object_notexist_error = "Put what?"
        self.no_object_given_error = self.object_notexist_error

class CmdLook(CmdObjectInteraction):
    """ Use middleware to provide CmdPut.
    """
    key = "look"
    aliases = ["l", "ls", "look at"]
    at_caller = "at_look"
    # this currently changes the target to the room
    def __init__(self):
        super(CmdLook, self).__init__()
        self.object_notexist_error = "Look at what?"
        self.no_object_given_error = self.object_notexist_error
        self.targetless_allowed = True
