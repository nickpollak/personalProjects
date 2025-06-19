#place 8 queens without them being able to take eachother
def checkBoard(board):
    d = checkDiagonals(board)
    if d:
        return True
    return False


#I wrote the following functions but I don't need due to permutations I am giving it have no conflicts
#if there are no 1's in the row it will return true
# def checkHorizontals(arr):
#     count = 0
#     for r in range(len(arr)):
#         for c in range(len(arr)):
#             if arr[r][c] == 1:
#                 count += 1
#         if count > 1:
#             return False
#         count = 0
#     return True

# #if there are no 1's in the column it will return true
# def checkVerticals(arr):
#     count = 0
#     for c in range(len(arr)):
#         for r in range(len(arr)):
#             if arr[r][c] == 1:
#                 count += 1
#         if count > 1:
#             return False
#         count = 0
#     return True

#if there are no 1's in the diagonals it will return true
def checkDiagonals(board):
    seenLR = set()
    seenRL = set()
    for row in range(len(board)):
        for col in range(len(board[row])):
            if board[row][col] == 1:
                if (row - col) in seenLR or (row + col) in seenRL:
                    return False
                seenLR.add(row - col)
                seenRL.add(row + col)
    return True

#helper function
def printBoard(b):
    for i in range(len(b)):
        print(b[i], "\n")

#manual testing if you want to test the individual board it gives you and
#replace the existing board

# rows = 8
# cols = 8
# board = [[0 for x in range(cols)] for y in range(rows)]
#known good set up for all true:
# board[0][3] = 1
# board[1][5] = 1
# board[2][7] = 1
# board[3][2] = 1
# board[4][0] = 1
# board[5][6] = 1
# board[6][4] = 1
# board[7][1] = 1
# print(checkBoard(board))


#make the permutation in 1's and 0's for any permutation
def generateCombination(perm):
    board = [[0 for x in range(8)] for y in range(8)]
    for r, c in enumerate(perm):
        board[r][c] = 1
    return board

#Got this helper function to make permutations of 0 to 7
def genPerms(a, size):
    if size == 1:
        makePerm(a[:])
        return
    for i in range(size):
        genPerms(a, size - 1)
        if size % 2 == 1:
            a[0], a[size-1] = a[size-1], a[0]
        else:
            a[i], a[size-1] = a[size-1], a[i]

#calling function to integrate the two previous functions
def makePerm(perm):
    b = generateCombination(perm)
    if checkBoard(b):
        solutions.append(b)

#empty list to hold solutions
solutions = []
#make a list of 0 to 7
initialList = list(range(8))
#call function to generate everything and test them
genPerms(initialList, len(initialList))


#you can only see 60 solutions so I made it so you can specify which solutions you want to see
# just edit the numbers in the range(0, 50) to see different solutions
for b in range(0, 50):
    printBoard(solutions[b])
    print("-----------------------")

print("Total possible solutions: ", len(solutions))