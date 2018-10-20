"""
Object

The Object is the "naked" base class for things in the game world.

Note that the default Character, Room and Exit does not inherit from
this Object, but from their respective default implementations in the
evennia library. If you want to use this class as a parent to change
the other types, you can do so by adding this as a multiple
inheritance.

"""
from evennia import DefaultObject
from evennia import utils

class ExtendedDefaultObject(object):
    """ Mixin adds additional functionality across the board

    This object is mixed into: Room, Character, Object
    It should be listed first, overriding the default inheritance
    Should it go other places?
    """
    def at_object_creation(self):
        """ This overloads the DefaultObject at_object_creation, which is empty.

        weight: a arbitrary integer weight, something akin to ounces.
        prepositions: possible sublocations in this object, only used if container
        sublocation: a metadata 'orientation' 'inside' the object's container
                     may be better stated as 'orientation'
        """
        self.db.weight = 1
        self.db.prepositions = list()
        self.db.sublocation = None


    def get_object_article(self):
        """ return the appropriate article for a given object

        Note: 
        the exceptions list is exact object names. It is a very
        inefficent way to manage exceptions because each name needs added
        explicitly.  For example "idle hour" and "fast hour" both need to
        be added separately.

        Future: 
        1. change this exceptions list to only refer to the first word 
            of the tested object
        2. manage article using a global list of objects with 'an' prefixes
        3. the global list takes priority

        """
        article = "a"

        exceptions = ["hour"]
        vowels = ['a', 'e', 'i', 'o', 'u']

        if self.name[0] in vowels or self.name in exceptions:
            article = "an"

        return article
        

    def remove_busy_flag(self, retval):
        """ Removes the busy flag from the caller object

        The busy flag blocks many verbs.

        The caller needs some way to look at their busy flag. That isn't covered
        in this function, but it could be covered in the error in the future.

        This callback method can be used in at_touch or at_touched
        or any similar method.
        """
        caller_done_msg = retval[0]
        target = retval[1]

        del self.ndb.busy

        try:
            self.msg(caller_done_msg.format(target.get_display_name(self)))
        except AttributeError:
            self.msg(caller_done_msg.format(target.key))
            

    def at_get(self, target, target_location=None, preposition=None):
        """ Modelled after at_look and the original CmdGet.

        if the object is too hot to hold or something, the at_got method still 
        gets a chance to interact with everything.

        When does the location of the got object get to run its checks?
        - it needs to test the object preposition before or after search.
        - or include the object attribute in the search.
        - how can i chain search?
        """

        if target == self:
            self.msg("You can't get yourself!")
            return

        if target.location == self:
            self.msg("You already have that!")
            return

        # this messaging style is not used elsewhere... the Cmd where this
        # method is called tries to message the caller with the return value
        # but many other interactions in this at_caller style functions
        # message the account on their own and return nothing. Which pattern
        # is best to use?  at_caller functions here need refactored and
        # DRY'd out.
        if not target.access(self, "get"):
            try:
                return "You could not get the {}.".format(target.get_display_name(self),)
            except AttributeError:
                return "You could not get the {}.".format(target.key,)

        # location/room at_got_room() method performs checks
        # if any value is returned, abort before move
        # note that this returns an empty message:
        #     at_got_from must tell the character what happened.
        if target_location and target_location.at_got_from( getter=self, 
                                        target=target, 
                                        preposition=preposition):
            return
        
        # perform the move
        target.move_to(self, quiet=True)
        # this currently happens in at_get and at_put but it should probably
        # happen in a single location that detects the object has been moved
        # or is informed that the object is changing location and removes or
        # updates the sublocation accordingly
        target.db.sublocation = None

        # A different get delay can be defined and used in at_got
        get_done_message = "You finish getting the {}."
        if target.db.get_delay > 0:
            self.ndb.busy = True
            utils.delay(target.db.get_delay, 
                        callback=self.remove_busy_flag, 
                        retval=[get_done_message, target])
        
        # send custom messages to the room about the move
        # need to bring this data in from wherever it is
        if target_location:
            caller_message = "You get {object} from {location}."
            location_message = "{caller} gets {object} from {location}."
        else:
            caller_message = "You pick up {object}."
            location_message = "{caller} picks up {object}."
        message_data = { "object" : target.name, "location" : target_location, "caller" : self }
        self.msg(caller_message.format(**message_data))
        self.location.msg_contents(location_message.format(**message_data),
                                     exclude=self)
        
        target.at_got(getter=self)
        

    def at_got(self, getter=None):
        """ This is called whenever someone gets this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass


    def at_got_from(self, getter=None, target=None, preposition=None):
        """ This is called when 'get' is used on an object in this object.
        """
        pass


    def at_put(self, target, target_location=None, preposition=None):
        """ Modelled after at_look and the original CmdGet.
        """

        if target == self:
            self.msg("You can't put yourself!")
            return

        if not target_location:
            self.msg("Where do you want to put this?")
            return

        if target_location == self:
            self.msg("You can't quite figure out how to do that.")
            return

        # this messaging style is not used elsewhere... the Cmd where this
        # method is called tries to message the caller with the return value
        # but many other interactions in this at_caller style functions
        # message the account on their own and return nothing. Which pattern
        # is best to use?  at_caller functions here need refactored and
        # DRY'd out.
        if not target.access(self, "put"):
            try:
                return "You could not move the {}.".format(target.get_display_name(self),)
            except AttributeError:
                return "You could not move the {}.".format(target.key,)

        # location/room at_got_room() method performs checks
        # if any value is returned, abort before move
        # note that this returns an empty message:
        #     at_objput_from must tell the character what happened.
        # are these variable assignments right? is putter self?
        if target_location:
            # cannot short circuit - this function must run
            if target_location.at_objput_from( putter=self, 
                                        target=target, 
                                        preposition=preposition):
                # do not perform the move
                return
        
        # perform the move
        target.move_to(target_location, quiet=True)
        # this sublocation should aggressively clear whenever the object
        # is informed that it has moved. right now get/put move the object,
        # but it may make more sense to have a generic 'moved' detector.
        target.db.sublocation = preposition

        # A different put delay can be defined and used in at_objput
        put_done_message = "You finish putting the {}."
        if target.db.put_delay > 0:
            self.ndb.busy = True
            utils.delay(target.db.put_delay, 
                        callback=self.remove_busy_flag, 
                        retval=[put_done_message, target])
        
        # send custom messages to the room about the move
        # need to bring this data in from wherever it is
        if preposition:
            caller_message = "You put {object} {preposition} {location}."
            location_message = "{caller} puts {object} {preposition} {location}."
        message_data = { "object" : target.name, "location" : target_location, "caller" : self, "preposition": preposition }
        self.msg(caller_message.format(**message_data))
        self.location.msg_contents(location_message.format(**message_data),
                                     exclude=self)
        
        target.at_objput(putter=self)


    def at_objput(self, putter=None):
        """ This is called whenever someone puts this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass


    def at_objput_from(self, putter=None, target=None, preposition=None):
        """ This is called when an object is 'put' inside of this object

        note that 'into' and 'inside' would be aliases for the 'in'
        preposition (but are not implemented yet anyways)
        """
        pass

    
    def at_touch(self, target, target_location=None, preposition=None):
        """ Modelled after at_look, at_touch has its own lock: "touch"

        Ideally the multiple return control flow code pattern will be changed.
        it is from the default at_look.
        """

        if not target.access(self, "touch"):
            try:
                return "You could not touch the {}.".format(target.get_display_name(self),)
            except AttributeError:
                return "You could not touch the {}.".format(target.key,)
        
        self.location.msg_contents(
                "{toucher} touches {target}.", 
                exclude=self,
                mapping={"toucher": self, "target": target} )

        # A different touch delay can be defined and used in at_touched
        touch_done_message = "You finish touching the {}."
        if target.db.touch_delay > 0:
            self.ndb.busy = True
            utils.delay(target.db.touch_delay, 
                        callback=self.remove_busy_flag, 
                        retval=[touch_done_message, target])

        target.at_touched(toucher=self)

        try:
            return "You reach out and touch the {}.".format(target.get_display_name(self),)
        except AttributeError:
            return "You reach out and touch the {}.".format(target.key,)

    def at_touched(self, toucher=None):
        """ This is called whenever someone touches this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass


    def at_focus(self, target, target_location=None, preposition=None):
        """ Modelled after at_look, at_focus has its own lock: "focus"
        """
        if not target.access(self, "focus"):
            try:
                return "You could not focus on the {}.".format(target.get_display_name(self),)
            except AttributeError:
                return "You could not focus on the {}.".format(target.key,)
        
        self.location.msg_contents(
                "{focuser} concentrates on {target}.", 
                exclude=self,
                mapping={"focuser": self, "target": target} )

        # A different focus delay can be defined and used in at_focused
        focus_done_message = "You finish focusing on the {}."
        if target.db.focus_delay > 0:
            self.ndb.busy = True
            utils.delay(target.db.focus_delay, 
                        callback=self.remove_busy_flag, 
                        retval=[focus_done_message, target])

        target.at_focused(focuser=self)

        try:
            return "You focus your magical senses on {}.".format(target.get_display_name(self),)
        except AttributeError:
            return "You focus your magical senses on {}.".format(target.key,)

    def at_focused(self, focuser=None):
        """ This is called whenever someone focuses this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass

    def at_stir(self, target, target_location=None, preposition=None):

        target.at_stirred(stirrer=self)


    def at_stirred(self, stirrer=None):
        """ This is called whenever someone stirs this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass

    def at_read(self, target, target_location=None, preposition=None):
        """ Modelled after at_look, at_read has its own lock: "read"
        """
        if not target.access(self, "read"):
            try:
                response = "You could not read the {}.".format(target.get_display_name(self),)
            except AttributeError:
                response = "You could not read the {}.".format(target.key,)
        
        else: 
            self.location.msg_contents(
                    "{reader} reads {target}.", 
                    exclude=self,
                    mapping={"reader": self, "target": target} )

            try:
                response = "You read {}.".format(target.get_display_name(self),)
            except AttributeError:
                response = "You read {}.".format(target.key,)

        # A different read delay can be defined and used in at_readed
        read_done_message = "You finish reading the {}."
        if target.db.read_delay > 0:
            self.ndb.busy = True
            utils.delay(target.db.read_delay, 
                        callback=self.remove_busy_flag, 
                        retval=[read_done_message, target])

            target.at_objectread(reader=self)

        return response


    def at_objectread(self, reader=None):
        """ This is called whenever someone reads this object.

        Follows the same code pattern as at_desc, a function used by at_look
        """
        pass


    def at_look(self, target, target_location=None, preposition=None):
        """ arguments retrofitted for CmdObjectInteraction compatability

        the original code from evennia

        at_look and at_desc should be fully retrofitted to manage views
        there are numerous ideas on how to manage view interactions in:
        - README.md
        - this docstring
        
        # look can be retrofitted for the at_command style actions.
        # the code pattern used to filter visible objects may be helpful
        # for filtering by preposition/sublocation in the generic commands
        # the idea would be to first filter by sublocation then run a search
        # on the filtered list.

        # search() takes a list in its location, so we could technically build
        # a custom list then use the default search. this is the swiftest route.

        Called when this object performs a look. It allows to
        customize just what this means. It will not itself
        send any data.

        Args:
            target (Object): The target being looked at. This is
                commonly an object or the current location. It will
                be checked for the "view" type access.

        Returns:
            lookstring (str): A ready-processed look string
                potentially ready to return to the looker.

        """
        # handle empty target. this functionality is from the original CmdLook
        # the 'else' condition is probably not possible; defensive coding only
        if not target:
            if not self.location:
                return "You have no location to look at."
            else:
                return "Look at what?"

        if not target.access(self, "view"):
            try:
                return "Could not view '%s'." % target.get_display_name(self)
            except AttributeError:
                return "Could not view '%s'." % target.key

        description = target.return_appearance(self, preposition)

        # the target's at_desc() method.
        # this must be the last reference to target so it may delete itself when acted on.
        target.at_desc(self, preposition)

        return description


    def return_appearance(self, looker, preposition=None):
        """ This is still the default return_appearance from evennia

        Return appearance will probably be retrofitted for CmdObjectInteraction
        
        This formats a description. It is the hook a 'look' command
        should call.

        Args:
            looker (Object): Object doing the looking.
        """

        def enumerate_contents():
            ''' get and identify all objects
            '''
            visible = (obj for obj in self.contents 
                    if obj != looker and
                    obj.access(looker, "view"))

            exits, users, things = [], [], []

            # change these tests
            for obj in visible:
                if obj.destination:
                    exits.append(obj)
                elif obj.has_account:
                    users.append("%s" % obj)
                else:
                    things.append(obj)

            return exits, users, things


        if not looker:
            return

        # Assemble view components from appearance classes
        import inspect
        classes = [x.__name__ for x in inspect.getmro(self.__class__)]

        # if self is a room, keep the original display method 
        if "Room" in classes:

            exits, users, things = enumerate_contents()
            # get description, build string
            string = "%s\n" % self.get_display_name(looker)
            desc = self.db.desc

            if desc:
                string += "%s" % desc
            if exits:
                string += "\n{wExits:{n " + ", ".join([exit.get_display_name(looker) for exit in exits])
            if users or things:
                string += "\n{wYou see:{n " + ", ".join([thing.get_display_name(looker) for thing in users+things])
            return string

        # if self is a container, use the preposition display method 
        if preposition:

            exits, users, things = enumerate_contents()
            sublocation_things = [thing for thing in things if thing.db.sublocation == preposition]
            # get description, build string
            string = "%s\n" % self.get_display_name(looker)
            desc = self.db.desc
            if desc:
                string += "%s" % desc
            if things:
                string += "\n{wYou see:{n " + ", ".join([thing.get_display_name(looker) for thing in sublocation_things])
            return string


        # elif self is a character, use a character display method 

        # else use the simple "description only" display method
        else:
            desc = self.db.desc
            if desc:
                return str(desc)
            else:
                return "You see {} {}.".format(self.get_object_article(), str(self.get_display_name(looker)))


    def at_desc(self, looker=None, preposition=None):
        """
        This is called whenever someone looks at this object.

        looker (Object): The object requesting the description.

        """
        pass


class Object(ExtendedDefaultObject, DefaultObject):
    """
    This is the root typeclass object, implementing an in-game Evennia
    game object, such as having a location, being able to be
    manipulated or looked at, etc. If you create a new typeclass, it
    must always inherit from this object (or any of the other objects
    in this file, since they all actually inherit from BaseObject, as
    seen in src.object.objects).

    The BaseObject class implements several hooks tying into the game
    engine. By re-implementing these hooks you can control the
    system. You should never need to re-implement special Python
    methods, such as __init__ and especially never __getattribute__ and
    __setattr__ since these are used heavily by the typeclass system
    of Evennia and messing with them might well break things for you.


    * Base properties defined/available on all Objects

     key (string) - name of object
     name (string)- same as key
     aliases (list of strings) - aliases to the object. Will be saved to
                           database as AliasDB entries but returned as strings.
     dbref (int, read-only) - unique #id-number. Also "id" can be used.
                                  back to this class
     date_created (string) - time stamp of object creation
     permissions (list of strings) - list of permission strings

     account (Account) - controlling account (if any, only set together with
                       sessid below)
     sessid (int, read-only) - session id (if any, only set together with
                       account above). Use `sessions` handler to get the
                       Sessions directly.
     location (Object) - current location. Is None if this is a room
     home (Object) - safety start-location
     sessions (list of Sessions, read-only) - returns all sessions connected
                       to this object
     has_account (bool, read-only)- will only return *connected* accounts
     contents (list of Objects, read-only) - returns all objects inside this
                       object (including exits)
                       object (including exits)
     exits (list of Objects, read-only) - returns all exits from this
                       object, if any
     destination (Object) - only set if this object is an exit.
     is_superuser (bool, read-only) - True/False if this user is a superuser

    * Handlers available

     locks - lock-handler: use locks.add() to add new lock strings
     db - attribute-handler: store/retrieve database attributes on this
                             self.db.myattr=val, val=self.db.myattr
     ndb - non-persistent attribute handler: same as db but does not create
                             a database entry when storing data
     scripts - script-handler. Add new scripts to object with scripts.add()
     cmdset - cmdset-handler. Use cmdset.add() to add new cmdsets to object
     nicks - nick-handler. New nicks with nicks.add().
     sessions - sessions-handler. Get Sessions connected to this
                object with sessions.get()

    * Helper methods (see src.objects.objects.py for full headers)

     search(ostring, global_search=False, attribute_name=None,
             use_nicks=False, location=None, ignore_errors=False, account=False)
     execute_cmd(raw_string)
     msg(text=None, **kwargs)
     msg_contents(message, exclude=None, from_obj=None, **kwargs)
     move_to(destination, quiet=False, emit_to_obj=None, use_destination=True)
     copy(new_key=None)
     delete()
     is_typeclass(typeclass, exact=False)
     swap_typeclass(new_typeclass, clean_attributes=False, no_default=True)
     access(accessing_obj, access_type='read', default=False)
     check_permstring(permstring)

    * Hooks (these are class methods, so args should start with self):

     basetype_setup()     - only called once, used for behind-the-scenes
                            setup. Normally not modified.
     basetype_posthook_setup() - customization in basetype, after the object
                            has been created; Normally not modified.

     at_object_creation() - only called once, when object is first created.
                            Object customizations go here.
     at_object_delete() - called just before deleting an object. If returning
                            False, deletion is aborted. Note that all objects
                            inside a deleted object are automatically moved
                            to their <home>, they don't need to be removed here.

     at_init()            - called whenever typeclass is cached from memory,
                            at least once every server restart/reload
     at_cmdset_get(**kwargs) - this is called just before the command handler
                            requests a cmdset from this object. The kwargs are
                            not normally used unless the cmdset is created
                            dynamically (see e.g. Exits).
     at_pre_puppet(account)- (account-controlled objects only) called just
                            before puppeting
     at_post_puppet()     - (account-controlled objects only) called just
                            after completing connection account<->object
     at_pre_unpuppet()    - (account-controlled objects only) called just
                            before un-puppeting
     at_post_unpuppet(account) - (account-controlled objects only) called just
                            after disconnecting account<->object link
     at_server_reload()   - called before server is reloaded
     at_server_shutdown() - called just before server is fully shut down

     at_access(result, accessing_obj, access_type) - called with the result
                            of a lock access check on this object. Return value
                            does not affect check result.
     at_before_move(destination)             - called just before moving object
                        to the destination. If returns False, move is cancelled.
     announce_move_from(destination)         - called in old location, just
                        before move, if obj.move_to() has quiet=False
     announce_move_to(source_location)       - called in new location, just
                        after move, if obj.move_to() has quiet=False
     at_after_move(source_location)          - always called after a move has
                        been successfully performed.
     at_object_leave(obj, target_location)   - called when an object leaves
                        this object in any fashion
     at_object_receive(obj, source_location) - called when this object receives
                        another object

     at_traverse(traversing_object, source_loc) - (exit-objects only)
                              handles all moving across the exit, including
                              calling the other exit hooks. Use super() to retain
                              the default functionality.
     at_after_traverse(traversing_object, source_location) - (exit-objects only)
                              called just after a traversal has happened.
     at_failed_traverse(traversing_object)      - (exit-objects only) called if
                       traversal fails and property err_traverse is not defined.

     at_msg_receive(self, msg, from_obj=None, **kwargs) - called when a message
                             (via self.msg()) is sent to this obj.
                             If returns false, aborts send.
     at_msg_send(self, msg, to_obj=None, **kwargs) - called when this objects
                             sends a message to someone via self.msg().

     return_appearance(looker) - describes this object. Used by "look"
                                 command by default
     at_desc(looker=None)      - called by 'look' whenever the
                                 appearance is requested.
     at_get(getter)            - called after object has been picked up.
                                 Does not stop pickup.
     at_drop(dropper)          - called when this object has been dropped.
     at_say(speaker, message)  - by default, called if an object inside this
                                 object speaks

     """
    def at_object_creation(self):
        """
        """
        super(Object, self).at_object_creation()


