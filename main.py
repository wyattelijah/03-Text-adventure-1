import sys, logging, os, json

version = (3,7)
assert sys.version_info >= version, "This script requires at least Python {0}.{1}".format(version[0],version[1])

logging.basicConfig(format='[%(filename)s:%(lineno)d] %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)




# Game loop functions
def render(room,moves,points):
    ''' Displays the current room, moves, and points '''

    print('\n\nMoves: {moves}, Points: {points}'.format(moves=moves, points=points))
    print('\n\nYou are in the {name}'.format(name=room['name']))
    print(room['desc'])
    if len(room['inventory']):
        print('You see the following items:')
        for i in room['inventory']:
            print('\t{i}'.format(i=i))

def getInput(verbs):
    ''' Asks the user for input and normalizes the inputted value. Returns a list of commands '''

    response = input('\nWhat would you like to do? ').strip().upper().split()
    if (len(response)):
        #assume the first word is the verb
        response[0] = normalizeVerb(response[0],verbs)
    return response


def update(response,room,current,inventory):
    ''' Process the input and update the state of the world '''
    s = list(response)[0]  #We assume the verb is the first thing typed
    if s == "":
        print("\nSorry, I don't understand.")
        return current
    elif s == 'EXITS':
        printExits(room)
        return current
    else:
        for e in room['exits']:
            if s == e['verb'] and e['target'] != 'NoExit':
                return e['target']
    print("\nYou can't go that way!")
    return current


# Helper functions

def printExits(room):
    e = ", ".join(str(x['verb']) for x in room['exits'])
    print('\nYou can go the following directions: {directions}'.format(directions = e))

def normalizeVerb(selection,verbs):
    for v in verbs:
        if selection == v['v']:
            return v['map']
    return ""

def end_game(winning,points,moves):
    if winning:
        print('\n\nYou have won! Congratulations')
        print('\nYou scored {points} points in {moves} moves! Nicely done!'.format(moves=moves, points=points))
    else:
        print('\n\nThanks for playing!')
        print('\nYou scored {points} points in {moves} moves. See you next time!'.format(moves=moves, points=points))





def main():

    # Game name, game file, starting location, winning location(s), losing location(s)
    games = [
        (   'My Game',          'game.json',    'START',    ['END'],    [])
        ,(  'Zork I',           'zork.json',    'WHOUS',    ['NIRVA'],  [])
        ,(  'A Nightmare',      'dream.json',    'START',   ['AWAKE'],  ['END'])
    ]

    # Ask the player to choose a game
    game = {}
    while not game:
        print('\n\nWhich game would you like to play?\n')
        for i,g in enumerate(games):
            print("{i}. {name}".format(i=i+1, name=g[0]))
        try:
            choice = int(input("\nPlease select an option: "))
            game = games[choice-1]
        except:
            continue
            
    name,gameFile,current,win,lose = game





    with open(gameFile) as json_file:
        game = json.load(json_file)

    moves = 0
    points = 0
    inventory = []

    print("\n\n\n\nWelcome to {name}!\n\n".format(name=name))
    while True:

        render(game['rooms'][current],moves,points)

        response = getInput(game['verbs'])

        if response[0] == 'QUIT':
            end_game(False,points,moves)
            break

        current = update(response,game['rooms'][current],current,inventory)

        moves += 1

        if current in win:
            end_game(True,points,moves)
            break
        if current in lose:
            end_game(False,points,moves)
            break






if __name__ == '__main__':
	main()