### ATTENTION

#### Migrate from 0.6 to 0.7 - DONE

- guide from griatch: https://groups.google.com/forum/#!category-topic/evennia/evennia-news/0JYYNGY-NfE

#### Migrate from 0.7 to 0.8 - dunno but I am using 0.8

- dunno!


#### Player was removed and the class i used was renamed to account

- i partially fixed this and used Griatch's find and replace script. I assume it's good now but could be wrong.


### Purpose

A smorgasbord of features to be mixed into a future game world. 

Consider making a CPF for this project. The sub-projects are becoming more clear.


### Reviewing Dragonrealms

The game this is surrogating actually requires a pretty custom UI to play. This is something I would love to avoid by using a system of buffers.

#### Special Features

Dragonrealms has tons of features outside its object management. Although most of dragonrealms is object management.

- crafting systems - we can do this easily, object synthesis/consumption
- Roundtime - cooldown after doing many tasks
- scaled training - a skills system that permanently improves things
- magic system
- combat system - both pc and npc-pc - what about npc-npc?


### Current Projects

A bunch of current projects as they come into focus. They can be broken out as tasks become deeper or more complex.

1. Characters Descriptions (PC and NPC identical)
    - Itemized description: eyes, hair, skin, face, height, build
    - visible status effects
    - demeanor
    - worn items
    - equipped items


2. Add inventory limits at some point. Move this task when necessary.
    1. limit options:
        - weight limit
        - volume limit
        - quantity limit
        - locks/permissions
    2. These limits COULD be used as an equip system


3. Implement 'my' adjective
    - Currently self locations override ground locations preventing (or confusing?) ground access on items with the same name as held items.
    - 'get my sword in my sheath' should be equivalent to 'get sword in my sheath'.
    - Consider implementing 'get my sword' which searches all your top level objects for the first sword.


4. De-abstraction: 'look' and 'put' are different grammars than CmdObjectInteraction.
    1. Extract 'look' from CmdObjectInteraction
        - Maintains most of the same code, but has these forms:
            1. 'look'
            2. 'look x'
            3. 'look x in y'
            4. 'look in y'
    2. Extract 'put' from CmdObjectInteraction
        - Maintains the same code, but switches the object and the location
        - Switching object and location here maintains the abstractions for:
            - at_put
            - at_objput
            - at_objput_from
    3. Notes pasted from elsewhere:
        1. Generalize the at_got and at_got_from 'style' of response function
        2. Some parts of this can be generic but a lot is customized.
            - put, get, and look all behave in very precise ways
            - the locations of both objects may need to be checked or given the ability to interject. This is already defined for get/put. 


5. Generalize the three response functions:
    1. Abstract the custom functions for all object interactions.
        - Since they all must be overridden, it is unclear how much abstraction is done.
        - It may be that every new registered CmdObjectInteraction 'command' will need to have its three response functions manually added to ExtendedDefaultObject.
        - WRITE: a howto for manually adding all parts of a new CmdObjectInteraction command.
    1. The following items should all have a say in how an object interaction goes:
        - Acting object, acted on object, object container
    2. What about the acting object's container?
    

6. Consider integrating the article function into the item description function

7. Game instances would need to be spawnable per character or something.
    1. Allows regulation of loot
        - one time instance versus repeating instance
        - shared locations on respawn timers?


### Done or Mostly Done Projects

1. Containers: get x in y, put x in y
    1. Override search language (maybe a silent or quiet flag on search with a custom caller.msg) 
        - In what cases do I want to override this language?
            -
    2. Add look_in to view stuff inside stuff. (DONE)
        - Add the grammar for this preposition (DONE)
        - Add special views when there is a prepositon in at_look and related response functions (DONE)
      
2. look: Reconstruct specialized object look methods
    1. Inside Items (anything with contents)
        - need special parsing for "look in X"
        - query each object for sublocation to build view based on preposition
        - Preposition/sublocation: "in", "under", "behind", "on"
        - Need specific view for each sublocation
        - Optional: comprehensive view (inspect object or something)
    2. Rooms
        - Detect if an object is a room and give a consistent view
    3. Items
        - Give a consistent, simple description


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
    6. Consider using container prepositions for body equip zones
    

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

4. 'focus' and 'touch' - event message order
    - The `at_focused` and `at_touched` currently emit player touch output after these events fire.
        - The effect is that an event like being poisoned fires before the touch is announced.

5. Add wearable item enables a global chat channel.
    - Disable all standard chat and broadcasting on Player
    - Add a local chat channel with a different magic item and consider how to use.
    - Use the 'think' verb for chatting.
    - consider using zones/tags on locations?

6. First spell to implement - player viewer
    - Cast it on a player and you can view whatever they view
    - Needs discriminating mechanic for visions versus real sight

7. Player guild option similar to eve corps would be very nice

8. Concept of temporary experience or 'being sharp' at something
    - Core skills may build but then you have a modifier for what you've done lately

9. Spell Management
    - For now lets just implement scrolls
    - When you read a scroll a memory uncurls like a snake behind your throat.
        - Or it could blossom like a rose
    - The spell is then in the character's active spell slot and can be cast.
        - As it sits in the active spell slot longer its chance of being cast increases
        - After a certain amount of time you lose the spell
            - Put a callback for like 180 seconds whenever you put a spell in your active slot
            - After this timer the callback empties the slot and the timer 
        - The player can manually forget to cancel the callback and empty the slot
        - If the player prepares another spell or reads another scroll then the player should become muddled and lose both

10. Dealing with item articles: 'a', 'an', 'the', 'some', and '' (empty)
    - The article would need referred to anywhere the item is explicitly broadcast to a room or individual.
    - Supply the article in the initalizer: `article = an`
    - If not supplied, provide a function for predicting:
        - `if not article: article = article_predictor()`
        - This function can exist in a base class somewhere
    - Rules:
        - Players get ''
        - items with `unique = True` or a unique tag maybe??? get `the`
        - otherwise 'a' and 'an' are based on the first letter.
        - 'some' is a special case, some beer, some water. A very vague one. 'a water' just will not do.


### Notes

- `rlwrap telnet 0.0.0.0 4000` - for line history in telnet, use 0.0.0.0 or `::` instead of localhost now
- Make a detached room: `@create My Room Name:rooms.DefaultRoom` `@tel/tonone My Room Name`
- (Griatch) The easiest way to do a global search for an object is to do `evennia.search_object("name")`
- If evennia says it has hanging `pid` then go in the /server/ folder and remove the offending files.
    - they will end in `pid` so you can use: `rm *.pid`
- [Ainneve](https://github.com/evennia/ainneve) - A full sample game
- Admin can reload the server with `@reload`
- The server remembers admin's `prelogout_location` by default and puts admin back
    - Same for all characters? Probably. Where is this from?
- Persistent attributes: `prelogout_location`, `desc`, `health`, health_max`
    - Both health attributes are from my custom room, so it works.
- The __server database is not under source control__.  If you wish to keep a server instance, back it up carefully.
- To Regenerate from git repository (only if cloning fresh)
    1. `evennia --initsettings`
    2. `mkdir server/logs`
    3. `evennia migrate`
    4. `evennia start`
    5. use a dev admin user/pass: admin / password@
- Reinitialize all objects - Potentially Destructive! - `@py for obj in evennia.ObjectDB.objects.all(): obj.at_object_creation()`
- Reinitialize a certain class of objects - Potentially Destructive! - `@py from typeclasses.objects import Heavy; [obj.at_object_creation() for obj in Heavy.objects.all()]`


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
