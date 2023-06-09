"""
@author: Quynh Le (Hana)
@date: May 11, 2023
@note: Redo using penality (-1) and reward (+1) method to update Q-Values 
"""

INITIAL_NUM_STICKS = 10
MAX_PLAYER_STICKS = 3

def displayRules():
  print("Welcome to NIM!")
  print("Rule: You and the computer will take turns to take sticks from the pile. The computer will go first, then it's your turn. Whoever takes the last stick wins.")
  print("\nThe number of sticks: ", INITIAL_NUM_STICKS)

def humanTurn(remainSticks):
  while True:
    humanChoice = int(input("How many sticks do you want to take? "))
    if 1 <= humanChoice <= min(MAX_PLAYER_STICKS, remainSticks):
      return humanChoice
    else:
      print("Invalid value. Enter a number from 1 to", min(MAX_PLAYER_STICKS, remainSticks), "sticks.")

#Offset value for row and col in Q-Value table. Row and col start with 0 but minimum number of sticks is 1
OFFSET = 1

#Computer's turn to choose based on the largest Q-Value learned for each number of remaining sticks
#If tie, choose the highest number of sticks
def compTurn(remainSticks, qValues):
  compChoice = 1
  #Initialize max Q-Value to the Q-value of the first choice for the number of remaining sticks
  maxQValue = qValues[0][remainSticks]
  for option in range(MAX_PLAYER_STICKS):
    if (maxQValue < qValues[option][remainSticks]):
      maxQValue = qValues[option][remainSticks]
      compChoice = option + OFFSET
  return compChoice

def main():
  remainSticks = INITIAL_NUM_STICKS
  qValues = []
  compMoves = []
  humanMoves = []
  play = True
  isCompTurn = True

  #Load Q-Values table if it exists, or initialize it if it doesn't
  try:
    file = open("q_table.txt", "r")
    for line in file:
      valueArray = line.split(" ")
      row = []
      for value in valueArray:
        row.append(int(value))
      qValues.append(row)
    file.close()

  except IOError:
    file = open("q_table.txt", "x")
    #Initialize table with 0s
    for i in range(MAX_PLAYER_STICKS):
      row = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      qValues.append(row)

    #Assign 1 or -1 to the first 3 rows and 3 cols
    for row in range(MAX_PLAYER_STICKS):
      for col in range(MAX_PLAYER_STICKS):
        if (row == col):
          qValues[row][col] = 1
        else:
          qValues[row][col] = -1

  while (play):
    print("---------------------------------")
    print("Remaining sticks: " + str(remainSticks))

    if (isCompTurn):
      print("Computer's turn:")
      compChoice = compTurn(remainSticks=remainSticks - OFFSET,
                            qValues=qValues)
      print("Computer takes " + str(compChoice) + " sticks")
      remainSticks -= compChoice

      #Save computer's moves
      compMoves.append([compChoice, remainSticks])

    else:
      print("Your turn:")
      humanChoice = humanTurn(remainSticks=remainSticks)
      print("You take " + str(humanChoice) + " sticks")
      remainSticks -= humanChoice

      #Save human's moves
      humanMoves.append([humanChoice, remainSticks])

    if (remainSticks == 0):
      print("---------------------------------")
      print("There are no sticks left.")

      #Reward rules: 1 is Reward; -1 is Penalty
      compReward = 0
      humanReward = 0

      if (isCompTurn):
        compReward = 1
        humanReward = -1
        print("Computer wins!")
      else:
        compReward = -1
        humanReward = 1
        print("You win!")

      #Update Q-Values
      for move in compMoves:
        numSticksChosen = move[0] - OFFSET
        numSticksRemain = move[1] + move[0] - OFFSET
        qValues[numSticksChosen][numSticksRemain] += compReward

      #Update Q-Values to 'q_table.txt'
      try:
        file = open("q_table.txt", "w")
        file.truncate()  #Remove existing Q-Values content
        content = ""
        for row in qValues:
          line = " ".join(str(qValue) for qValue in row)
          line += "\n"
          content += line
        file.write(content)  #Update file with new Q-Values
      except IOError:
        print("Error updating q_table.txt")

      break

    #Take turn
    isCompTurn = not isCompTurn


displayRules()
main()
