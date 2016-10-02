"""
Commands

Commands describe the input the player can do to the game.

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



class CmdTouch(default_cmds.MuxCommand):
    """ Supplies default behavior for 'touch'
    """

    key = "touch"
    locks = "cmd:all()"

    def func(self):
        """ This actually does things
        """
        if self.caller.ndb.busy:
            self.caller.msg("You are a little busy for that.")
        else:
            if not self.args:
                self.caller.msg("Touch what?")
            else:
                target = self.caller.search(self.args)
                if not target:
                    self.caller.msg("Touch what?")
                else:
                    if target.db.touch_delay > 0:
                        self.caller.ndb.busy = True
                        utils.delay(target.db.touch_delay, callback=self.remove_busy_flag, retval=target)
                    self.msg(self.caller.at_touch(target))

    def remove_busy_flag(self, retval):
        """ Removes the busy flag from caller

        This feature isn't used. The language would likely be object dependent
        this feature likely needs utils.delay to accept kwargs so you can generate
        a message in a way similar to the get_display_name api.
        """
        del self.caller.ndb.busy
        try:
            self.caller.msg("You finish touching the {}.".format(retval.get_display_name(self)))
        except AttributeError:
            self.caller.msg("You finish touching the {}.".format(retval.key))

        
class CmdFocus(default_cmds.MuxCommand):
    """ Supplies default behavior for 'focus'
    """

    key = "focus"
    locks = "cmd:all()"

    def func(self):
        """ This actually does things
        """
        # turn this into a decorator for all tasks that need a busy check
        if self.caller.ndb.busy:
            self.caller.msg("You are a little busy for that.")
        else:
            if not self.args:
                self.caller.msg("Focus on what?")
            else:
                target = self.caller.search(self.args)
                if not target:
                    self.caller.msg("Focus on what?")
                else:
                    if target.db.focus_delay > 0:
                        self.caller.ndb.busy = True
                        utils.delay(target.db.focus_delay, callback=self.remove_busy_flag, retval=target)
                    self.msg(self.caller.at_focus(target))

    def remove_busy_flag(self, retval):
        """ Removes the busy flag from caller
        """
        del self.caller.ndb.busy
        try:
            self.caller.msg("You finish focusing on the {}.".format(retval.get_display_name(self)))
        except AttributeError:
            self.caller.msg("You finish focusing on the {}.".format(retval.key))


class CmdRead(default_cmds.MuxCommand):
    """ Supplies default behavior for 'read'
    """

    key = "read"
    locks = "cmd:all()"

    def func(self):
        """ This actually does things
        """
        # turn this into a decorator for all tasks that need a busy check
        if self.caller.ndb.busy:
            self.caller.msg("You are a little busy for that.")
        else:
            if not self.args:
                self.caller.msg("Read what?")
            else:
                target = self.caller.search(self.args)
                if not target:
                    self.caller.msg("Read what?")
                else:
                    if target.db.read_delay > 0:
                        self.caller.ndb.busy = True
                        utils.delay(target.db.read_delay, callback=self.remove_busy_flag, retval=target)
                    self.msg(self.caller.at_read(target))

    def remove_busy_flag(self, retval):
        """ Removes the busy flag from caller
        """
        del self.caller.ndb.busy
        try:
            self.caller.msg("You finish reading the {}.".format(retval.get_display_name(self)))
        except AttributeError:
            self.caller.msg("You finish reading the {}.".format(retval.key))
