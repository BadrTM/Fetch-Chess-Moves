#Importing Libraries

from chessdotcom import get_player_game_archives
import requests
import re

##########################
#####<--Code Below-->#####
##########################


def get_player_moves(username, color, NumOfMonths = 1, NumOfGames = 20):

    #Initiating Variables
    BlackGames = 0
    WhiteGames = 0
    GWon = 0
    GLost = 0
    GDrawn = 0
    GameNum = 0

    #Fetching the URLs of the matches in the months that the player played in
    data = get_player_game_archives(username).json

    #Fetching the latest month
    url = data['archives'][-1]

    #Accessing the URL and getting the games
    global playerGames
    playerGames = requests.get(url).json()

    #Adding games from previous 2-3 months to the ['games'] Value list if NumOfMonths > 1
    if NumOfMonths > 1:
        Add_To_Games(NumOfMonths, username)
    else:
        pass

    #Setting playerGames['games'][-NumOfGames:] to a variable to make the code look cleaner
    RangedNumOfGames = playerGames['games'][-NumOfGames:]

    #print() to seperate the output from the terminal header
    print()

    #Loop throught each game in ['games']
    for i in range(NumOfGames):
        try:
            try:
                #Makes sure that the games analyzed are either RAPID or BLITZ
                if (RangedNumOfGames[i]['time_class'] == 'rapid') or (RangedNumOfGames[i]['time_class'] == 'blitz'):

                    #Filters the list of games to only analyze games in which opponent is BLACK
                    if color == 'BLACK':
                        
                        if RangedNumOfGames[i]['black']['username'].upper() == username:

                            GameNum += 1
                            print(GameNum)
                            print(f"[{RangedNumOfGames[i]['time_class'].upper()}]")

                            BlackGames += 1
                
                            pgnList = RangedNumOfGames[i]['pgn'].split('\n')
                
                            #stripping {[%clk 0:09:55.3]} from the moves
                            stripped = re.sub(r"\{\[.*?\}", "", pgnList[-2]).split("  ")

                            if (RangedNumOfGames[i]['black']['result'] == 'win'):
                                print("[Opponent Won]")
                                GWon += 1
                            elif (RangedNumOfGames[i]['black']['result'] != 'win') and (RangedNumOfGames[i]['black']['result'] != 'stalemate') and (RangedNumOfGames[i]['black']['result'] != 'repetition') and (RangedNumOfGames[i]['black']['result'] != 'agreed'):
                                print(f"[Opponent Lost by {RangedNumOfGames[i]['black']['result']}]")
                                GLost += 1
                            else:
                                if RangedNumOfGames[i]['black']['result'] == 'stalemate':
                                    print(f"[The game was drawn by Stalemate]")
                                    GDrawn += 1
                                elif RangedNumOfGames[i]['black']['result'] == 'repetition':
                                    print(f"[The game was drawn by Repetition]")
                                    GDrawn += 1
                                elif RangedNumOfGames[i]['black']['result'] == 'agreed':
                                    print(f"[The game was drawn by Agreement]")
                                    GDrawn += 1
                                else:
                                    print("[The game was probably drawn due to Insufficient Materials]")
                                    GDrawn += 1

                            print(f"As Black, your opponent replies with {stripped[1]} against {stripped[0]}\n")
                            print(f"Then this is played {stripped[0:20]}\n\n")

                        else:
                            pass
                    
                    #Filters the list of games to only analyze games in which opponent is BLACK
                    elif color == 'WHITE':
                                      
                        if RangedNumOfGames[i]['black']['username'].upper() != username:
                            
                            GameNum += 1
                            print(GameNum)
                            print(f"[{RangedNumOfGames[i]['time_class'].upper()}]")

                            WhiteGames += 1
                
                            pgnList = RangedNumOfGames[i]['pgn'].split('\n')
                
                            #stripping {[%clk 0:09:55.3]} from the moves
                            stripped = re.sub(r"\{\[.*?\}", "", pgnList[-2]).split("  ")

                            FirstMove = stripped[0]

                            if (RangedNumOfGames[i]['white']['result'] == 'win'):
                                print("[Opponent Won]")
                                GWon += 1
                            elif (RangedNumOfGames[i]['white']['result'] != 'win') and (RangedNumOfGames[i]['white']['result'] != 'stalemate') and (RangedNumOfGames[i]['white']['result'] != 'repetition') and (RangedNumOfGames[i]['white']['result'] != 'agreed'):
                                print(f"[Opponent Lost by {RangedNumOfGames[i]['white']['result']}]")
                                GLost += 1
                            else:
                                if RangedNumOfGames[i]['white']['result'] == 'stalemate':
                                    print(f"[The game was drawn by Stalemate]")
                                    GDrawn += 1
                                elif RangedNumOfGames[i]['white']['result'] == 'repetition':
                                    print(f"[The game was drawn by Repetition]")
                                    GDrawn += 1
                                elif RangedNumOfGames[i]['white']['result'] == 'agreed':
                                    print(f"[The game was drawn by Agreement]")
                                    GDrawn += 1
                                else:
                                    print("[The game was probably drawn due to Insufficient Materials]")
                                    GDrawn += 1
                                

                            print(f"As White, your opponent usually starts with ({FirstMove})\n")
                            print(f"Then their opponents played {stripped[1:20]}")
                            print()

                        else:
                            pass  

                    else:
                        return print(f"{color} is not an option! Please choose either white or black for the color.")
                        
                else:
                    continue

            except IndexError:
                print(f"\nERRRRROOOOOORRRRR: Game {i} has no moves or is [BULLET]\n")
                continue
    
        except IndexError:
            print(f"\nOpponent has only played {i} games this month")
            break

    #Separator
    print("\n","-"*60, sep="")
                                      
    #Prints the total number of games opponent played as the specified color (Black/White)
    if color == "BLACK":
        print(f"Games as Black in the past {NumOfGames} games: {BlackGames}\n")
    elif color == "WHITE":
        print(f"Games as White in the past {NumOfGames} games: {WhiteGames}\n")
    
    #Function returns the total games won, lost, and drawn for the opponent when playing as specificed color
    return print(f"Games Won: {GWon}\nGames Lost: {GLost}\nGames Drawn: {GDrawn}\n")


#Function to add games from the previous 2-3 months to the ['games'] Value list
def Add_To_Games(NumOfMonths, username):
    data = get_player_game_archives(username).json

    if NumOfMonths == 2:
        url = data['archives'][-NumOfMonths]
        GameMonth = requests.get(url).json()

        playerGames['games'][0:0] = GameMonth['games']

    elif NumOfMonths == 3:
        url = data['archives'][-NumOfMonths + 1]
        GameMonth = requests.get(url).json()
        playerGames['games'][0:0] = GameMonth['games']

        url = data['archives'][-NumOfMonths]
        GameMonth = requests.get(url).json()
        playerGames['games'][0:0] = GameMonth['games']

    else:
        pass

    return


#Taking the users input
User = input('Enter the username of your opponent: ').upper()
Color = input('Enter the color your opponent is playing with: ').upper()
NumOfMonths = input('You want to analyze the games for the past how many calendar months? Range (1-3 months) (default: 1) ')
NumOfGames = input('Enter the number of games you would like to analyze (default: 20): ')

#I think that's inefficient and I'm pretty sure there is a better way to do it, but this piece of code avoids errors when user leaves input as blank
if (type(NumOfGames) == type("")) and (NumOfGames != "") and (type(NumOfMonths) == type("")) and (NumOfMonths != ""):
    get_player_moves(User, Color, int(NumOfMonths), int(NumOfGames))
elif (type(NumOfGames) == type("")) and (NumOfGames != "") and (NumOfMonths == ""):
    get_player_moves(User, Color, 1, int(NumOfGames))
elif (type(NumOfMonths) == type("")) and (NumOfMonths != "") and (NumOfGames == ""):
    get_player_moves(User, Color, int(NumOfMonths))
else:
    get_player_moves(User, Color)
                                      
