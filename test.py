import requests
import random

base_url = "http://light-bikes.inseng.net"

def create_game(addServerBot, boardSize, numPlayers, serverBotDifficulty):
    endpoint = f"{base_url}/games/"
    data = {
        "addServerBot": addServerBot,
        "boardSize": boardSize,
        "numPlayers": numPlayers,
        "serverBotDifficulty": serverBotDifficulty
    }
    response = requests.post(endpoint, data=data)
    return response.json()

def show_game(gameId):
    endpoint = f"{base_url}/games/{gameId}"
    response = requests.get(endpoint)
    return response.json()

def join_game(gameId, name):
    endpoint = f"{base_url}/games/{gameId}/join"
    data = {
        "name": name
    }
    response = requests.post(endpoint, data = data)
    return response.json()

def move(gameId, playerId, x, y):
    endpoint = f"{base_url}/games/{gameId}/move"
    data = {
        "playerId": playerId,
        "x": x,
        "y": y
    }
    response = requests.post(endpoint, data = data)
    if response.status_code != 200:
        print(response.json())
    return response.json()

def get_curr_from_show(showRes):
    curr_id = show_res['games'][0]['current_player'] 
    return curr_id

def is_valid_move(showRes, new_x, new_y):
    curr_info = get_curr_from_show(showRes)
    curr_x = curr_info['x']
    curr_y = curr_info['y']
    length = len(show_res['games'][0]['board'])

    board = show_res['games'][0]['board']
    

    if(new_x) < 0 or (new_x) >= length:
            return False
    elif(new_y) < 0 or (new_y) >= length:
            return False
    elif board[new_x][new_y] != None:
            return False

    return True

def make_move(curr_x, curr_y, opp_x, opp_y, length):
    range = length / 5
    distance = ((curr_x - opp_x)**2 + (curr_y - opp_y)**2)**0.5

    
    # Calculate the vector to the opponent
    dx, dy = opp_x - curr_x, opp_y - curr_y

    # Normalize the vector to get the direction -- accounts for the negative case
    direction = dx / abs(dx) if dx != 0 else 0, dy / abs(dy) if dy != 0 else 0

    if distance > range:

        # Move in the direction that is closest to the true path to the opponent
        if abs(direction[0]) > abs(direction[1]):
            return curr_x + direction[0], curr_y
        else:
            return curr_x, curr_y + direction[1]
    else:
        if abs(direction[0]) > abs(direction[1]):
            return curr_x, curr_y + direction[1]
        else:
            return curr_x + direction[0], curr_y
            
  
game_info = create_game(True, 25, 2, 2)
print(game_info)
gameId = game_info["id"]



# gameId = 734


r = join_game(gameId, "Sid")

# show_res = show_game(gameId)
# curr_id = show_res['games'][0]['current_player']['id']
# length = len(show_res['games'][0]['board'])
# print(length)

# #print(r[0]['players'])

# #print("Current Player Info:")

# curr_info = get_curr_from_show(show_res)
# print(curr_info)



# curr_id = curr_info['id']
# curr_x = curr_info['x']
# curr_y = curr_info['y']

# if(curr_x < 13):
#     dir = 1
# else:
#     dir = -1

print("\n Starting Loop... \n")

show_res = show_game(gameId)
curr_info = get_curr_from_show(show_res)
curr_id = curr_info['id']

length = len(show_res['games'][0]['board'])

moves = [(1, 0), (-1, 0), (0, 1), (0, -1)]
prev_move = (0, 0)

while(True):
    show_res = show_game(gameId)
    curr_info = get_curr_from_show(show_res)
    if show_res['games'][0]['winner'] != None:
        print("Game Over")
        break
    if curr_info['name'] == 'Sid':

        print(curr_info['x'], ", ", curr_info['y'])

        curr_x = curr_info['x']
        curr_y = curr_info['y']

        #print("Here: ")
        #print(show_res['games'][0]['players'])

        opp_x = show_res['games'][0]['players'][0]['x']
        opp_y = show_res['games'][0]['players'][0]['y']

        turn_x, turn_y = make_move(curr_x, curr_y, opp_x, opp_y, length)
        print(turn_x, ", ", turn_y)
        if(is_valid_move(show_res, int(turn_x), int(turn_y))):
            move(gameId, curr_id, int(turn_x), int(turn_y))
            continue
        

        repeat_x = curr_x + prev_move[0]
        repeat_y = curr_y + prev_move[1]

        if prev_move != (0, 0) and is_valid_move(show_res, repeat_x, repeat_y):
            move(gameId, curr_id, repeat_x, repeat_y)
            continue

        random.shuffle(moves)
        for mv in moves:
            dx, dy = mv
            new_x, new_y = curr_x + dx, curr_y + dy
            if is_valid_move(show_res, new_x, new_y):
                move(gameId, curr_id, new_x, new_y)
                prev_move = mv
                break
        
        # if(is_valid_move(show_res, curr_x + 1, curr_y)):
        #     move(gameId, curr_id, curr_x + 1, curr_y)
        # elif(is_valid_move(show_res, curr_x - 1, curr_y)):
        #     move(gameId, curr_id, curr_x - 1, curr_y)
        # elif(is_valid_move(show_res, curr_x, curr_y + 1)):
        #     move(gameId, curr_id, curr_x, curr_y + 1)
        # elif(is_valid_move(show_res, curr_x, curr_y - 1)):
        #     move(gameId, curr_id, curr_x, curr_y - 1)

        