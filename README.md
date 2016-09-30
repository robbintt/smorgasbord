### Purpose

A smorgasbord of features to be mixed into a future game world.


### Goals

1. Player Body
    1. Player should have body parts
        1. For each body part zone there is an internal and external object
            - e.g. internal chest, external chest
        2. Player body parts should have both damage and scarring
            - Damage is HP per body part
            - Scarring reduces the body part's total HP
            - Bleeding begins at a certain ratio of hp/total_hp and thus happens faster on scarred parts
            - Bleeding reduces vitality at a fixed rate.
            - FUTURE: Scarring removes certain commands
    2. Player should have vitality
    3. Player should regenerate vitality slowly.
    4. If a hit is scored on a body part
        1. Damage Vitality
        2. Damage Body Part
    5. Implementation:
        1. There should be a body part class
        2. Body parts can inherit from that class and become persistent_attributes
    

2. Indefinite articles in 'touch' events.
    1. Need to manage "a", "an", "the", or "some", or no article
        - "a", "an" => words with leading consonants, an for words with leading vowels.
        - "the" => unique items
        - "some" => some water, something common place, some dirt.
        - no article => characters

3. Unique Item Tagging
    1. Use tags for unique items, this can be used to define the indefinite article.
    2. See [`tags` article](https://github.com/evennia/evennia/wiki/Tags)
    3. Then you can search the world for unique items.

4. 'focus' and 'touch'
    - The `at_focused` and `at_touched` currently emit player touch output after these events fire.
        - The effect is that an event like being poisoned fires before the touch is announced.

5. Add wearable item enables a global chat channel.
    - Disable all standard chat and broadcasting on Player
    - Add a local chat channel with a different magic item and consider how to use.
    - Use the 'think' verb for chatting.

6. First spell to implement - player viewer
    - Cast it on a player and you can view whatever they view
    - Needs discriminating mechanic for visions versus real sight

7. Player guild option similar to eve corps would be very nice

8. Concept of temporary experience or 'being sharp' at something
    - Core skills may build but then you have a modifier for what you've done lately

### Notes

- `rlwrap telnet localhost 4000` - for line history in telnet
- If evennia says it has hanging `pid` then go in the /server/ folder and remove the offending files.
- [Ainneve](https://github.com/evennia/ainneve) - A full sample game
- Admin can reload the server with `@reload`
- The server remembers admin's `prelogout_location` by default and puts admin back
    - Same for all characters? Probably. Where is this from?
- Persistent attributes: `prelogout_location`, `desc`, `health`, health_max`
    - Both health attributes are from my custom room, so it works.

The server database is not under source control.  If you wish to keep a server instance, back it up carefully.


### Resources

- [Tutorials](http://github.com/evennia/evennia/wiki/Tutorials)
- [Wiki](https://github.com/evennia/evennia/wiki)
- [Game Directory Overview](https://github.com/evennia/evennia/wiki/Tutorial%20World%20Introduction)
- [RP Mixins for Object, Room, Character](https://github.com/evennia/evennia/blob/master/evennia/contrib/rpsystem.py#L6)
    

### Default Readme Tips

You can delete this readme file when you've read it and you can
re-arrange things in this game-directory to suit your own sense of
organisation (the only exception is the directory structure of the
`server/` directory, which Evennia expects). If you change the structure
you must however also edit/add to your settings file to tell Evennia
where to look for things.

Your game's main configuration file is found in
`server/conf/settings.py` (but you don't need to change it to get
started). If you just created this directory (which means you'll already
have a `virtualenv` running if you followed the default instructions),
`cd` to this directory then initialize a new database using

    evennia migrate

To start the server, stand in this directory and run

    evennia start

This will start the server, logging output to the console. Make
sure to create a superuser when asked. By default you can now connect
to your new game using a MUD client on `localhost`, port `4000`.  You can 
also log into the web client by pointing a browser to
`http://localhost:8000`.
