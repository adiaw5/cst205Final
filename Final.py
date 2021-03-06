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

import copy
import java.awt.Font as Font
import os
import tempfile
import time
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

houseMaster = {
  "bedroom" : {
    'examine' : """A plain looking room with a messy bed, a night stand, a desk and a chair.
The light of the moon shines through the westside window.
A door to leading to a NORTH hallway is wide open. There
is also a door open in the EAST side leading to a courtyard.
""",
    'move' : {
      'north' : 'hallway',
      'east'  : 'courtyard',
    },
    'items' : ['handle','lever'],
    'events' : [],
    'assets': {
      'image' : 'bedroom.jpg'
    }
  },

  "courtyard" : {
    'examine' : """An wide square courtyard full of flowers and a bench. The center of the
courtyard leads splits into different paths: WEST is the
bedroom, EAST is the foyer
""",
    'move' : {
      'west' : 'bedroom',
      'east' : 'foyer'
    },
    'items' : ['stone'],
    'events' : [],
    'assets': {
      'image' : 'courtyard.jpg'
    }
  },

  'hallway' : {
    'examine' : """The long, narrow hallway. The wall paper decoration is clearly dated
and the boards creek as you walk. The light of a room
shines dimly at the NORTH end of the passageway. SOUTH is a
bedroom you're familiar with but can't remember how.
""",
    'move' : {
      'south' : 'bedroom',
      'north' : 'library',
    },
    'items' : [],
    'events' : [],
    'assets': {
      'image' : 'hallway.jpg'
    }
  },

  'library' : {
    'examine' : """This library could belong to a university! The old smell of ink, paper,
and wine overwhelmes your senses. A sofa and a low table.
The arch on the EAST side seem to open into a ballroom.
""",
    'move' : {
      'east'  : 'ballroom',
      'south' : 'hallway',
    },
    'items' : ['coffee', 'bookshelf'],
    'events' : ['eventLibrary'],
    'assets': {
      'image' : 'library.jpg',
      'sound' : '76175__mattpavone__planetary-flyby-faster.aiff'
    }
  },

  'ballroom' : {
    'examine': """The grand ballroom! It's already setup for the party, lined with tables,
decorations and soft music playing. You can see the wide
doors to the library WEST and the foyer SOUTH.
""",
    'move' : {
      'west' : 'library',
      'south' : 'foyer'
    },
    'items' : ['teeth','painting','cabinet'],
    'events' : [],
    'assets': {
      'image' : 'ballroom.jpg'
    }
  },

  'foyer' : {
    'examine' : """The entrance is a wide, long room with marble floors, and a large chandelier
lighting every corner. You can see the ballroom just
NORTH and WEST the famous courtyard. The main door is
locked by a skeleton key.
""",
    'move' : {
      'north' : 'ballroom',
      'west' : 'courtyard'
    },
    'items' : ['book'],
    'events' : [],
    'assets': {
      'image' : 'foyer.jpg',
      'sound' : 'creaky_door_4.wav'
    }
  },
  'laboratory' : {
    'examine' : """A laboratory fool of beakers, and burners. \nIt feels stuffy here!
The passageway SOUTH leads to the library.
""",
    'move' : {
      'south' : 'library'
    },
    'items' : ['neck'],
    'assets': {
      'image' : 'laboratory.jpg'
    }
  }
}

itemsMaster = {
  'handle' : {
    'actions' : {
      'examine' : "The HANDLE of a key... It looks like \nit's missing the NECK and TEETH",
      'take' : "You gently place the HANDLE in your pocket.",
    },
    'location' : "You see a round loop like a HANDLE. Maybe you can TAKE it.",
    'assets' : {
      'image' : 'Inv_misc_key_04.jpg'
    }
  },
  'neck' : {
    'actions' : {
      'examine' : "The NECK of a key. A long and shiny \nbronze bar. Maybe you can TAKE it.",
      'take' : "You gently place the NECK in your pocket.",
    },
    'location' : "The NECK of a key seems to be resting at your reach.",
    'assets' : {
      'image' : 'Inv_misc_key_07.jpg'
    }
  },
  'teeth' : {
    'actions' : {
      'examine' : "The TEETH of a key. They seem to fit \nperfectly a skeleton lock.",
      'take' : "You gently place the TEETH in your pocket.",
    },
    'location' : "You can see the TEETH of a key shinning.",
    'assets' : {
      'image' : 'Inv_misc_key_13.jpg'
    }
  },
  'book' : {
    'actions' : {
      'examine' : "A heavy, wornout book. The title reads: \nExperiments.",
      'take': "You take the book...",
      'put': "You gently place the book...",
    },
    'location': "You notice a BOOK that reads 'Experiments'.",
    'assets' : {
      'image' : 'Inv_misc_book_11.jpg'
    }
  },
  'coffee' : {
    'actions' : {
      'examine' : "A cup of coffee. Steam indicates the cup still \nwarm. It looks like you can DRINK it",
      'drink' : "You take a sip. What a delicious cup of coffee!"
    },
    'location' : 'A still warm cup of COFFEE fills the room with a sweet scent.'
  },
  'stone' : {
    'actions' : {
      'examine' : "This colorful magic STONE will reset you move count.\nIt looks like you can USE it",
      'use' : "you USE the colorful magic STONE and reset your move count!"
    },
    'location' : 'A colorful STONE is in the courtyard.',
    'assets' : {      
      'sound' : 'zapsplat_fantasy_magic_twinkle_burst_002_25774.wav'
    }
  },
  'lever' : {
    'actions' : {
      'examine' : "This mysterious LEVER should open something.\nIt looks like you can USE it",
      'use' : "you USE the mysterious LEVER and open a window! Listen to the owls outside."
    },
    'location' : 'A mysterious LEVER is in the room.',
    'assets' : {      
      'sound' : 'owl-1.wav'
    }
  },
  'painting' : {
    'actions' : {
      'examine' : "You noticed that in the PAINTING the china CABINET\n is closed. EXAMIINE the CABINET"
    },
    'location' : 'A PAINTING of the ballroom which displays the china CABINET closed.'
  },
  'cabinet' : {
    'actions' : {
      'examine' : "This is the china CABINET in the PAINTING, which is open.\nYou should CLOSE the cabinet",
      'close' : "You have closed the china CABINET."
    },
    'assets' : {      
      'sound' : 'fox_audio_close_door_medicine_cabinet.wav'
    }    
  },
  'bookshelf' : {
    'actions' : {
      'examine' : "The bookshelf is full of books about science, \nbiology and physics... There is a gap. Something \ncan be PUT here."
    },
    'location' : "A BOOKSHELF lines the north wall from floor to celing."
  },
  'key' : {
    'actions' : {
      'examine' : "A shiny skeleton key. It would fit nicely in a \ndoor. But where can you USE it?",
      'use' : "you USE the key and jiggle it."
    },
    'assets' : {
      'image' : 'Inv_misc_key_15.jpg',
      'sound' : '109662__grunz__success.wav'
    }
  }
}

heroMaster = {
  'location' : 'bedroom',
  'inventory' : [],
  'moves' : 50,
  'name' : '',
  'textQueue' : [],
  'soundQueue' : None,
  'flags' : {
    'hud' : True,
    'map' : True
  }
}

configMaster = {
  'hud' : {
    'assets' : {
      'image' : 'hud.jpg',
      'sound' : 'bensound-ofeliasdream.wav'
    },
    'iconPos' : [173, 447],
    'textPos' : [26, 87],
  },
  'assets' : {
    'images' : [
      'Inv_misc_book_11.jpg',
      'Inv_misc_key_04.jpg',
      'Inv_misc_key_07.jpg',
      'Inv_misc_key_13.jpg',
      'Inv_misc_key_15.jpg',
      'ballroom.jpg',
      'bedroom.jpg',
      'courtyard.jpg',
      'foyer.jpg',
      'foyer_open.jpg',
      'hallway.jpg',
      'hud.jpg',
      'laboratory.jpg',
      'library.jpg',
      'library_open.JPG',
      'empty_slot.jpg'
    ],
    'sounds' : [
      '109662__grunz__success.wav',
      '325112__fisch12345__success.wav',
      '335751__j1987__put-item.wav',
      '359134__theminkman__metal-moving.wav',
      '410983__mihirfreesound__unlocking-door.wav',
      'creaky_door_4.wav',
      '76175__mattpavone__planetary-flyby-faster.aiff',
      'bensound-ofeliasdream.wav',
      'fox_audio_close_door_medicine_cabinet.wav',
      'zapsplat_fantasy_magic_twinkle_burst_002_25774.wav',
      'owl-1.wav',
    ]
  }
}

def start():
  """This is the main loop that starts the game.
  First, it will print the instructions to the user and the introduction.
  Then, it will examine current room and ask for user input
  """

  # Print all initial information for the user.
  game = initialize()
  house = game['house']  
  items = game['items']
  hero = game['hero']

  # Start the main loop.
  hero['state'] = 'start'
  while(isPlaying(game)):
    # Prompt user for a name until one is provided.
    if hero['state'] == 'start':
      name = requestString("Please enter your name: ")
      if name == None:
        hero['name'] = 'quitter'
        hero['state'] = 'quit'
      elif name.strip() != '':
        name.strip().capitalize()
        hero['name'] = name
        hero['state'] = 'intro'
      continue

    elif hero['state'] == 'intro':
      showInformation(title + instructions)
      showInformation(introduction)
      examine(house, items, hero)
      hero['state'] = 'playing'

    elif hero['state'] == 'playing':
      playGame(game)

    printNow("\n".join(hero['textQueue']))
    renderScene(game)
    playSoundQueue(game)

  backgroundSound = game['config']['hud']['assets']['sound']
  sound = game['sounds'][backgroundSound]
  stopPlaying(sound)
  if  hero['state'] == "success":
    showInformation("%s! You have finally made out of the house! You have won the game, %s!" % (hero['name'], hero['name']))
  elif  hero['state'] == "quit":
    showInformation("Thank you for playing, %s. Please come again!" % hero['name'])
  else:
    showInformation("Sorry %s! You have run out of moves, please try again!" % hero['name'])

def playGame(game):
  hero = game['hero']
  house = game['house']
  items = game['items']

  # Process user inputs.
  user_response = requestString("What would like to do? ")
  if user_response == None:
    addToTextQueue(hero, "Please enter an action or QUIT to exit")
    return

  user_response = user_response.lower().strip()
  if len(user_response) == 0:
    addToTextQueue(hero, "Please enter an action or QUIT to exit")
    return

 # Empty the queue.
  hero['textQueue'] = []
  hero['soundQueue'] = None
  printNow("\n>>> You entered: " + user_response + "\n")
  args = user_response.split()

  # Game logic.
  if args[0] == "help": 
    showInformation(instructions)
  elif args[0] ==  "quit":
    hero['state'] = 'quit'
    return
  else:
    # Ensure there is a second argument.
    if len(args) < 2:
      args.append(False)
    
    # Count the moves.
    if args[0] == "move":
      hero['moves'] = hero['moves'] -1
      if hero['moves'] == 0:
        hero['state'] == "fail"
        return

    # Execute action.
    doAction(args[0], args[1], house, items, hero)
    checkEvents(house, items, hero)
      
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
    move(house, object, hero, items)
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
      addToTextQueue(hero, heroRoom[action])
    elif object in heroRoom['items'] and action in items[object]['actions']: 
      addToTextQueue(hero, items[object]['actions'][action])
      if object == 'cabinet' and hero['location'] == 'ballroom':
        hero['soundQueue'] = itemsMaster['cabinet']['assets']['sound']
    elif object in hero['inventory'] and action in items[object]['actions']: 
      addToTextQueue(hero, items[object]['actions'][action])
    else:
      # This action cannot be performed.
      addToTextQueue(hero, "%s, you don't know how to %s that object" % (hero['name'], action.upper()))

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

def move(house, direction, hero, items):
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
    examine(house, items, hero)
    hero['flags']['map'] = True
  else:
    #Invalid direction entered
    if direction:
      addToTextQueue(hero, "%s, you cannot move in the %s direction from this room." % (hero['name'], direction.upper()))
    printNavigation(hero, house[heroRoom])

def printNavigation(hero, room):
  """Utility Function
  Prints the different directions and destinations for a room.
  Args:
    room (dictionary): The room to print directions of.
  """
  navigation = room['move']
  if len(navigation) > 1:
    addToTextQueue(hero, "You can see a few places you can MOVE to:")
  elif len(navigation) == 1:
    addToTextQueue(hero, "You can only MOVE")
  else:
    addToTextQueue(hero, "What? How is it possible?! You're trapped... No place to MOVE!")

  for direction, room in navigation.items():
    addToTextQueue(hero, "  %s to the %s" % (direction.upper(), room.capitalize()))

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
    examineRoom(heroRoom, items, hero)
    return

  # Examine the hero.
  if object == 'me':
    examineMe(hero)
    return

  # Check if the room or user have the object.
  
  if object in hero['inventory'] or object in heroRoom['items']:
    if 'examine' in items[object]['actions']:
      addToTextQueue(hero, items[object]['actions']['examine'])
      return

  addToTextQueue(hero, "Strange... you cannot examine that.")

def examineMe(hero):
  """Action:
  Examine the hero, and print all relevant information.
  Args:
    hero (dictionary): The hero to examine..
  """
  addToTextQueue(hero, "\nYou're in the %s" % hero['location'].capitalize())
  
  if len(hero['inventory']) > 0:
    addToTextQueue(hero, "\nYou have acquired some items:  " + ', '.join([i.upper() for i in hero['inventory']]))
    
  addToTextQueue(hero, "\nYou have %s moves left" % hero['moves'])

def examineRoom(room, items, hero):
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
  addToTextQueue(hero, roomDescription)

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
    if 'take' in items[object]['actions']:
      hero['inventory'].append(object)
      heroRoom['items'].remove(object)
      addToTextQueue(hero, items[object]['actions']['take'])
      hero['flags']['hud'] = True
    else:
      addToTextQueue(hero, "You cannot take the %s from this room" % object)
  else:
    addToTextQueue(hero, "This room does not have a %s" % object)

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
    if 'put' in items[object]['actions']:
      heroRoom['items'].append(object)
      hero['inventory'].remove(object)
      addToTextQueue(hero, items[object]['actions']['put'])
      hero['flags']['hud'] = True
    else:
      addToTextQueue(hero, "You cannot PUT the %s!" % object)
  else:
    addToTextQueue(hero, "You don't have a %s" % object)

def use(house, items, hero, object = False):
  """ Uses an item from the user inventory in the room.
  Args:
    house (dictionary): The house layout.
    items (dictionary): The list of all items in the house.
    hero (dictionary): The hero performing the action.
    object (string): The object the action is to be performed on, if it exists.
  """
  heroRoom = house[hero['location']]
  if object in hero['inventory'] or object in heroRoom['items']:
    if 'use' in items[object]['actions']:
      addToTextQueue(hero, items[object]['actions']['use'])
      if object == 'key' and hero['location'] == 'foyer':
        heroRoom['events'].append('eventOpenExit')
      elif object == 'stone' and hero['location'] == 'courtyard':
        #player uses the magic stone reset move count
        heroRoom['items'].remove(object)
        hero['moves'] = 50
        hero['soundQueue'] = itemsMaster['stone']['assets']['sound']
        addToTextQueue(hero, "%s, you have 50 moves again!" % hero['name'])
      elif object == 'lever' and hero['location'] == 'bedroom':
        hero['soundQueue'] = itemsMaster['lever']['assets']['sound']
    else:
      addToTextQueue(hero, "You cannot USE the %s!" % object)
  else:
    addToTextQueue(hero, "You don't have a %s" % object)

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
    hero['soundQueue'] = house['library']['assets']['sound']
    # Update the house data.
    house['library']['move']['north'] = "laboratory"
    house['library']['assets']['image'] = "library_open.JPG"
    house['library']['examine'] = """This library could belong to a university! The old smell of ink, paper,
and wine overwhelmes your senses. A sofa and a low table
complete the room making it pleasant and warm.
The arch on the EAST side seem to open into a ballroom, and NORTH
the omnious precense of the laboratory.
"""
    items['bookshelf']['location'] = "The BOOKSHELF has moved, revealing the secret room."
    hero['flags']['map'] = True

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
  house['foyer']['assets']['image'] = "foyer_open.jpg"
  house['foyer']['examine'] = """
The entrance is a wide, long room with marble floors, and a large chandelier
lighting every corner. You can see the ballroom just NORTH and WEST
the famous courtyard.

The SOUTH door is now unlocked.

"""
  hero['soundQueue'] = house['foyer']['assets']['sound']
  hero['flags']['map'] = True
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
    hero['soundQueue'] = itemsMaster['key']['assets']['sound']
    hero['flags']['hud'] = True

    showInformation("You take all three pieces, and make a KEY out of them... You think you know where to USE it") 

####
# Utility Functions
####

def initialize():
  """ Utility Function
  Initialize the game data.
  Load the assets for the game, and setup the
  game scene.
  Returns:
    The game hash with the game instance.
  """
  game = {}
  game['house'] = copy.deepcopy(houseMaster)
  game['hero'] = copy.deepcopy(heroMaster)
  game['items'] = copy.deepcopy(itemsMaster)
  game['config'] = copy.deepcopy(configMaster)
  game['images'] = {}
  game['sounds'] = {}
  loadAssets(game)

  # Initialize the scene with dynamic sizes.
  heroLoc = game['hero']['location']
  heroRoom = game['house'][heroLoc]['assets']['image']
  heroImage = game['images'][heroRoom]
  hudImage = game['images']['hud.jpg']
  game['scene'] = makeEmptyPicture(getWidth(hudImage), getHeight(hudImage) + getHeight(heroImage))
  hudHeight = getHeight(heroImage)
  copyImage(game['images']['hud.jpg'], game['scene'], 0, hudHeight)

  # Setup the necessary variables to track the duration of
  # background sound.
  backgroundSound = game['config']['hud']['assets']['sound']
  sound = game['sounds'][backgroundSound]
  game['config']['sound_duration'] = getDuration(sound)

  return game

def loadAssets(game):
  """ Utility Function
  iterate over all the game assets and load them by type.
  Args:
    game (dictionary): The game instance with all the data.
  """
  allAssets = game['config']['assets']
  for type, assets in allAssets.items():
    for asset in assets:
      loadAsset(asset, type, game)

def loadAsset(name, type, game):
  """ Utility Function
  Loads the asset file to the game hash.
  Args:
    name (string):     The name of the file to load
    type (string):     The type of the asset to load.
    game (dictionary): The game instance with all the data.
  """
  if not name in game[type]:
    game[type][name] = downloadAsset(type, name)
  
def downloadAsset(type, name):
  """ Load assets from the remote repo.
  Args:
    type (string): The type of asset to load (images, sounds).
    name (string): The name of the asset to load.
  """
  cwd = ''
  try:
    cwd = tempfile.gettempdir()
  except:
    cwd = os.getcwd() + '/VASC9tmp'
    if not os.path.isdir(cwd):
      os.mkdir(cwd)
      printNow("Saving files to the local directory: %s" % cwd)
  url = "https://raw.githubusercontent.com/adiaw5/cst205Final/master/assets/%s/" % type

  testfile = urllib.URLopener()
  printNow("Loading now: %s" % (url + name))
  testfile.retrieve(url + name, cwd + name)

  if type == 'sounds':
    return makeSound(cwd + name)
  elif type == 'images':
    return makePicture(cwd + name)

def addToTextQueue(hero, string):
  """ Utility Function
  The hero game state, and the string to add.
  Breakline delimeters are split to produce the array of text.
  Args:
    hero (dictionary): The hero instance with all the data.
    string (string):   The string to add to the queue.
  """
  parts = string.split('\n')
  for part in parts:
    hero['textQueue'].append(part)

def printTextQueue(game):
  """ Utility Function
  Print the all the text that has been queued into a black
  image with white text.
  Args:
    game (dictionary): The game instance with all the data.
  Returns:
    The image is with the game text.
  """
  strings = game['hero']['textQueue']
  textImage = makeEmptyPicture(500, 172, black)
  scene = game['scene']
  origX = 15
  origY = 15
  for string in strings:
    addText(textImage, origX, origY, string, white)
    origY += 15
  return textImage

def printStatus(game):
  """ Utility Function
  Create an image with the name and status.
  Args:
    game (dictionary): The game instance with all the data.
  Returns:
    The image is with the game status.
  """
  textImage = makeEmptyPicture(163, 62, black)
  myFont = makeStyle("Helvetica", Font.BOLD, 12)
  text = "%s (%s/%s)" % (game['hero']['name'], game['hero']['moves'], 50)
  addTextWithStyle(textImage, 15, 40, text, myFont, white)
  return textImage

def printLocation(game):
  """ Utility Function
  Create an image with the name and status.
  Args:
    game (dictionary): The game instance with all the data.
  Returns:
    The image is with the game status.
  """
  textImage = makeEmptyPicture(163, 62, black)
  myFont = makeStyle("Helvetica", Font.BOLD, 20)
  text = "The %s" % game['hero']['location'].capitalize()
  addTextWithStyle(textImage, 5, 40, text, myFont, white)
  return textImage

def isPlaying(game):
  """ Utility Function
  Check the state of the hero and return a boolean if true.

  Args:
    game (dictionary): The game instance with all the data.
  Returns:
    boolean, True if the game is active. Otherwise false.
  """
  state = game['hero']['state']
  return state != 'quit' and state != 'fail' and state != 'success'

def copyImage(image,interface, targetX =0, targetY = 0):
  """
  This function copies the different pictures to create the game interface.

  Args:
    image: This is the various image that constitute the interface
    interface: This the empty picuture frame on which to copy the picture to
    targetX: this is the x coordonate where to copy the picture to
    targetY: This is the y coordonate where to copy the picture to
  """
  # Get the width and Height 
  targetW = getWidth(interface)
  targetH = getHeight(interface)
  sourceW = getWidth(image)
  sourceH = getHeight(image)

  if(targetX > targetW or targetY > targetH):
    return interface
  xMax = min(targetX + sourceW, targetW)
  yMax = min(targetY + sourceH, targetH)
  x = 0
  for destX in range(targetX, xMax):
    y = 0
    for destY in range(targetY, yMax):
      p = getPixel(image, x, y)
      destPixel = getPixel(interface, destX, destY)
      setColor(destPixel, getColor(p))
      y += 1
    x += 1
  return interface

def renderScene(game):
  """ Utility Function
  Renders the scene as the use moves through various 
  parts of the house
  Args:
    game (dictionary): Current instance of the game.
  """
  #Get the game references
  house = game['house']
  hero = game['hero']
  items = game['items']
  heroRoom = house[hero['location']]
  imageName = heroRoom['assets']['image']
  heroImage = game['images'][imageName]

  if hero['flags']['map']:
    #Gets the current hero room image
    roomImage = heroRoom['assets']['image']
    gameImages = game['images'][roomImage]
    copyImage(gameImages, game['scene'])
    
    statusImage = printStatus(game)
    locationImage = printLocation(game)
    copyImage(statusImage, game['scene'], 0, getHeight(gameImages))
    copyImage(locationImage, game['scene'], 400, getHeight(gameImages))

  if hero['flags']['hud']:
    #Gets the current hero inventory
    inventory = hero['inventory']
    itemPosX = game['config']['hud']['iconPos'][0]
    itemPosY = game['config']['hud']['iconPos'][1]

    #Loops through the item list and copy the existing items to the hud
    for i in range(0, 6):
      image = game['images']['empty_slot.jpg']
      if i < len(inventory):
        item = inventory[i]
        itemImage = items[item]['assets']['image']
        image =  game['images'][itemImage]
      copyImage(image, game['scene'], itemPosX, itemPosY)
      itemPosX += getWidth(image)

  textImage = printTextQueue(game)
  x = (getWidth(game['scene']) - getWidth(textImage)) / 2
  y = getHeight(game['scene']) - getHeight(textImage) - 38
  copyImage(textImage, game['scene'], x, y)

  #Repaints the scene on the current hero location
  hero['flags']['hud'] = False
  hero['flags']['map'] = False
  repaint(game['scene'])

def playSoundQueue(game):
  """ Utility Function
  Play the sound queued in the game.
  Args:
    game (dictionary): The game instance with all the data.
  """
  if (not ('sound_start_ts' in game['config']) or time.time() - game['config']['sound_start_ts'] > game['config']['sound_duration']):
    backgroundSound = game['config']['hud']['assets']['sound']
    sound = game['sounds'][backgroundSound]
    play(sound)
    game['config']['sound_start_ts'] = time.time()

  if game['hero']['soundQueue']:
    sound = game['sounds'][game['hero']['soundQueue']]
    play(sound)
