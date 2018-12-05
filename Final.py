###########################################
# Class: CST-205
# Module 06, Lab13
# Group: VASC9
# Members:
#  - Victor Ramirez
#  - Aboubacar Diawara
#  - Juan Sebastian Delgado
#  - Cristian Palomo-Ramirez
###########################################

#  _____________
# |             |
# | Laboratory  |
# |             |
# |             |
# |______\__/___|___________________________
# |               |                         |
# |              \|                         |
# | Library         Ballroom                |
# |              /|                         |
# |               |                         |
# |______\   /____|________________\  /_____|
#    |          |            |              |
#    | hallway  |            |              |
#    |          |            |              |
#    |          |            |              |
#    |          | Courtyard  | Foyer        |
#  __|___\  /___|            |              |
# |             |            |              |
# | bedroom     |/           |/             |/
# |                                         | EXIT
# |             |\           |\             |\
# |_____________|____________|______________|

import os
import tempfile
import urllib

title = """
####
# Mansion Tour!
####

Welcome to Mansion Tour!
"""

instructions = """Enter the command you want to execute. Possible options, actions, and
directions are highlighted for you with uppercase words.

You can execute a command, by typing the verb followed by a noun,
for example 'MOVE NORTH' will move the user to the room north.

If you don't know what to do, you can 'EXAMINE' the place, object
or yourself to get information about it or type 'HELP' to display
this message.

Common actions are 'MOVE', 'TAKE', 'PUT' and 'USE'.

You must find your way out in 50 moves or less!"
"""

introduction = """You wake up, in an unknown space... Your head hurts. You look around,
but nothing looks familiar to you. You're dressed in formal
wear. You try to get your bearings, you EXAMINE the room.
"""

houseLayout = {
  "bedroom" : {
    'examine' : """=========== The Bedroom ===========
A plain looking room with a messy bed, a night stand, a desk and a chair.
The light of the moon shines through the westside window.
A door to leading to a NORTH hallway is wide open. There
is also a door open in the EAST side leading to a courtyard.
""",
    'move' : {
      'north' : 'hallway',
      'east'  : 'courtyard',
    },
    'items' : ['handle']
  },

  "courtyard" : {
    'examine' : """=========== The Courtyard ===========
An wide square courtyard full of flowers and a bench. The center of the
courtyard leads splits into different paths: WEST is the
bedroom, EAST is the foyer
""",
    'move' : {
      'west' : 'bedroom',
      'east' : 'foyer'
    },
    'items' : [],
    'events' : []
  },

  'hallway' : {
    'examine' : """=========== The Hallway ===========
The long, narrow hallway. The wall paper decoration is clearly dated
and the boards creek as you walk. The light of a room
shines dimly at the NORTH end of the passageway. SOUTH is a
bedroom you're familiar with but can't remember how.
""",
    'move' : {
      'south' : 'bedroom',
      'north' : 'library',
    },
    'items' : [],
    'events' : []
  },

  'library' : {
    'examine' : """=========== The Library ===========
This library could belong to a university! The old smell of ink, paper,
and wine overwhelmes your senses. A sofa and a low table.
The arch on the EAST side seem to open into a ballroom.
""",
    'move' : {
      'east'  : 'ballroom',
      'south' : 'hallway',
    },
    'items' : ['coffee', 'bookshelf'],
    'events' : ['eventLibrary']
  },

  'ballroom' : {
    'examine': """=========== The Ballroom ===========
The grand ballroom! It's already setup for the party, lined with tables,
decorations and soft music playing. You can see the wide
doors to the library WEST and the foyer SOUTH.
""",
    'move' : {
      'west' : 'library',
      'south' : 'foyer'
    },
    'items' : ['teeth']
  },

  'foyer' : {
    'examine' : """=========== The Foyer ===========
The entrance is a wide, long room with marble floors, and a large chandelier
lighting every corner. You can see the ballroom just
NORTH and WEST the famous courtyard. The main door is
locked by a skeleton key.
""",
    'move' : {
      'north' : 'ballroom',
      'west' : 'courtyard'
    },
    'items' : ['book'],
    'events' : []
  },
  'laboratory' : {
    'examine' : """=========== The Laboratory ===========
A laboratory fool of beakers, and burners. It feels stuffy here!
The passageway SOUTH leads to the library.
""",
    'move' : {
      'south' : 'library'
    },
    'items' : ['neck']
  }
}

items = {
  'handle' : {
    'examine' : "The HANDLE of a key... It looks like it's missing the NECK and TEETH",
    'take' : "You gently place the HANDLE in your pocket.",
    'location' : "You see a round loop like a HANDLE. Maybe you can TAKE it."
  },
  'neck' : {
    'examine' : "The NECK of a key. A long and shiny bronze bar. Maybe you can TAKE it.",
    'take' : "You gently place the NECK in your pocket.",
    'location' : "The NECK of a key seems to be resting at your reach."
  },
  'teeth' : {
    'examine' : "The TEETH of a key. They seem to fit perfectly a skeleton lock.",
    'take' : "You gently place the TEETH in your pocket.",
    'location' : "You can see the TEETH of a key shinning."
  },
  'book' : {
    'examine' : "A heavy, wornout book. The title reads: Experiments.",
    'take': "You take the book...",
    'put': "You gently place the book...",
    'location': "You notice a BOOK that reads 'Experiments'."
  },
  'coffee' : {
    'examine' : "A cup of coffee. Steam indicates the cup still warm. It looks like you can DRINK it",
    'drink' : "You take a sip. What a delicious cup of coffee!",
    'location' : 'A still warm cup of COFFEE fills the room with a sweet scent.'
  },
  'bookshelf' : {
    'examine' : "The bookshelf is full of books about science, biology and physics... There is a gap. Something can be PUT here.",
    'location' : "A BOOKSHELF lines the north wall from floor to celing."
  },
  'key' : {
    'examine' : "A shiny skeleton key. It would fit nicely in a door. But where can you USE it?",
    'use' : "you USE the key and jiggle it."
  }
}

hero = {
  'location' : 'bedroom',
  'inventory' : [],
  'moves' : 50,
  'name' : ''
}

def start():
  """This is the main loop that starts the game.
  First, it will print the instructions to the user and the introduction.
  Then, it will examine current room and ask for user input
  """

  # Print all initial information for the user.
  showInformation(title + instructions)
  showInformation(introduction)
  examine(houseLayout, items, hero)

  # Start the main loop.
  hero['state'] = 'playing'
  while(hero['state'] == 'playing'):
    
    # Prompt user for a name until one is provided.
    if not hero['name']:
      name = requestString("Please enter your name: ").strip().capitalize()
      hero['name'] = name
      continue

    # Process user inputs.
    user_response = requestString("What would like to do? ")
    if user_response == None:
      printNow("Please enter an action or QUIT to exit")
      continue
      
    user_response = user_response.lower().strip()
    if len(user_response) == 0:
      printNow("Please enter an action or QUIT to exit")
      continue
      
    printNow("\n>>>You entered: "+user_response+"\n")
    args = user_response.split()

    # Game logic.
    if args[0] == "help": 
      showInformation(instructions)
    elif args[0] ==  "quit":
      hero['state'] = 'quit'
      break
    else:
      # Ensure there is a second argument.
      if len(args) < 2:
        args.append(False)
      
      # Count the moves.
      if args[0] == "move":
        hero['moves'] = hero['moves'] -1
        if hero['moves'] == 0:
          hero['state'] == "fail"
          break

      # Execute action.
      doAction(args[0], args[1], houseLayout, items, hero)

  if  hero['state'] == "success":
    printNow("%s! You have finally made out of the house! You have won the game, %s!" % (hero['name'], hero['name']))
  elif  hero['state'] == "quit":
    printNow("Thank you for playing, %s. Please come again!" % hero['name'])
  else:
    printNow("Sorry %s! You have run out of moves, please try again!" % hero['name'])
      
def doAction(action, object, house, items, hero):
  """ Performs an action on an object or room based on user input.
  Args: 
    action (string): The action to be performed.
    object (string): The object the action is to be performed on, if it exists.
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
  """
  heroRoom = house[hero['location']]

  # Action logic
  if action == 'move':
    move(house, object, hero)
  elif action == 'examine':
    examine(house, items, hero, object)
  elif action == 'put':
    put(house, items, hero, object)
  elif action == 'take':
    take(house, items, hero, object)
  elif action == 'use':
    use(house, items, hero, object)
  else:
    # Execute actions based on wether they can be
    # performed in the room or an object.
    if not object and action in heroRoom:
      printNow(heroRoom[action])
    elif object in heroRoom['items'] and action in items[object]: 
      printNow(items[object][action])
    elif object in hero['inventory'] and action in items[object]: 
      printNow(items[object][action])
    else:
      # This action cannot be performed.
      printNow("%s, you don't know how to %s that object" % (hero['name'], action.upper()))

  checkEvents(house, items, hero)

def checkEvents(house, items, hero):
  """ Loops over all the actions available
  in the current room, and triggers the events as necessary.
  Additionally, executes global events.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
  """
  
  heroRoom = house[hero['location']]
  
  if 'events' in heroRoom:
    for event in heroRoom['events']:
      if 'eventLibrary' == event:
        eventLibrary(house, items, hero)
      elif 'eventOpenExit' == event:
        eventOpenExit(house, items, hero)
  eventMakeKey(house, items, hero)

def move(house, direction, hero):
  """Moves the hero from a location to another in the house.
  The hero can only move if the direction is allowed.
  Args:
    house (dictionary): The house layout.
    direction (string): The direction the user wishes to move.
    hero (dictionary):  The hero that needs to move.
  """

  heroRoom = hero['location']
  validDirections = house[heroRoom]['move'] 

  if direction in validDirections:

    if validDirections[direction] == 'exit':
      #you win the game    
      hero['state'] = 'success'
      return

    newRoom = validDirections[direction]
    hero['location'] = newRoom
    examine(houseLayout, items, hero)
  else:
    #Invalid direction entered
    if direction:
      printNow("%s, you cannot move in the %s direction from this room." % (hero['name'], direction.upper()))
    printNavigation(house[heroRoom])

def printNavigation(room):
  """Utility Function
  Prints the different directions and destinations for a room.
  Args:
    room (dictionary): The room to print directions of.
  """
  navigation = room['move']
  if len(navigation) > 1:
    printNow("You can see a few places you can MOVE to:")
  elif len(navigation) == 1:
    printNow("You can only MOVE")
  else:
    printNow("What? How is it possible?! You're trapped... No place to MOVE!")

  for direction, room in navigation.items():
    printNow("  %s to the %s" % (direction.upper(), room.capitalize()))

def examine(house, items, hero, object = False):
  """Action:
  Look at an object (room, item, etc.), and print the description.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
    object (string): The object the action is to be performed on, if it exists.
  """
  # Not an object, this is a room.
  location = hero['location']
  heroRoom = house[location]
  if not object or object == 'room':
    examineRoom(heroRoom, items)
    return

  # Examine the hero.
  if object == 'me':
    examineMe(hero)
    return

  # Check if the room or user have the object.
  
  if object in hero['inventory'] or object in heroRoom['items']:
    if 'examine' in items[object]:
      printNow(items[object]["examine"])
      return

  printNow("Strange... you cannot examine that.")

def examineMe(hero):
  """Action:
  Examine the hero, and print all relevant information.
  Args:
    hero (dictionary): The hero to examine..
  """
  printNow("\nYou're in the %s" % hero['location'].capitalize())
  
  if len(hero['inventory']) > 0:
    printNow("\nYou have acquired some items:  " + ', '.join([i.upper() for i in hero['inventory']]))
    
  printNow("\nYou have %s moves left" % hero['moves'])

def examineRoom(room, items):
  """Action:
  Examine the hero, and print all relevant information.
  Args:
    room (dictionary): The room to examine.
    items (dictionary): The list of all items in the house.
  """
  roomDescription = room['examine']
  if room['items']:
    for item in room['items']:
      if 'location' in items[item]:
        roomDescription += items[item]['location'] + "\n"
  printNow(roomDescription)

def take(house, items, hero, object):
  """ Take an item from the current room.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
    object (string): The object the action is to be performed on, if it exists.
  """
  heroRoom = house[hero['location']]
  if object in heroRoom['items']:
    if 'take' in items[object]:
      hero['inventory'].append(object)
      heroRoom['items'].remove(object)
      printNow(items[object]['take'])
    else:
      printNow("You cannot take the %s from this room" % object)
  else:
    printNow("This room does not have a %s" % object)

def put(house, items, hero, object):
  """ Puts an item from the user inventory, in the current room.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
    object (string): The object the action is to be performed on, if it exists.
  """
  heroRoom = house[hero['location']]
  if object in hero['inventory']:
    if 'put' in items[object]:
      heroRoom['items'].append(object)
      hero['inventory'].remove(object)
      printNow(items[object]['put'])
    else:
      printNow("You cannot PUT the %s!" % object)
  else:
    printNow("You don't have a %s" % object)

def use(house, items, hero, object = False):
  """ Uses an item from the user inventory in the room.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
    object (string): The object the action is to be performed on, if it exists.
  """
  heroRoom = house[hero['location']]
  if object in hero['inventory']:
    if 'use' in items[object]:
      printNow(items[object]['use'])
      if object == 'key' and hero['location'] == 'foyer':
        heroRoom['events'].append('eventOpenExit')
    else:
      printNow("You cannot USE the %s!" % object)
  else:
    printNow("You don't have a %s" % object)

def eventLibrary(house, items, hero):
  """ Event
  Triggers the bookshelf opening into the laboratory if the user PUTs the BOOK.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
  """
  if 'book' in house['library']['items']:
    # Remove the event so it cannot be triggered again.
    house['library']['events'].remove('eventLibrary')

    # Update the house data.
    house['library']['move']['north'] = "laboratory"
    house['library']['examine'] = """=========== The Library ===========
This library could belong to a university! The old smell of ink, paper,
and wine overwhelmes your senses. A sofa and a low table
complete the room making it pleasant and warm.
The arch on the EAST side seem to open into a ballroom, and NORTH
the omnious precense of the laboratory.
"""
    items['bookshelf']['location'] = "The BOOKSHELF has moved, revealing the secret room."

    # Print the event.
    showInformation("\nThe Bookshelf shakes and trembles... Slowly, it moves revealing a passage NORTH.")

def eventOpenExit(house, items, hero):
  """ Event
  Triggers the exit door opening if the user USEs the KEY in the foyer.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
  """
  house['foyer']['events'].remove('eventOpenExit')
  house['foyer']['move']['south'] = "exit"
  house['foyer']['examine'] = """=========== The Foyer ===========
The entrance is a wide, long room with marble floors, and a large chandelier
lighting every corner. You can see the ballroom just NORTH and WEST
the famous courtyard.

The SOUTH door is now unlocked.

"""

  showInformation("SOUTH, you hear the sound of a door unlocking.")

def eventMakeKey(house, items, hero):
  """ Event
  Triggers when the user acquires all three pieces and makes the KEY.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
  """
  inventory = hero['inventory']
  if 'handle' in inventory and 'neck' in inventory and 'teeth' in inventory:
    inventory.remove('handle')
    inventory.remove('neck')
    inventory.remove('teeth')
    inventory.append('key')

    showInformation("You take all three pieces, and make a KEY out of them... You think you know where to USE it") 

####
# Utility Functions
####

def loadAsset(type, name):
  """ Load assets from the remote repo.
  Args:
    type (string): The type of asset to load (images, sounds).
    name (string): The name of the asset to load.
  """
  cwd = tempfile.gettempdir()
  url = "https://raw.githubusercontent.com/adiaw5/cst205Final/master/assests/" + type
  
  testfile = urllib.URLopener()
  testfile.retrieve(url + name, cwd + name)
  
  if type == 'sounds':
    return makeSound(cwd + name)
  elif type == 'images':
    return makeImage(cwd + name)
