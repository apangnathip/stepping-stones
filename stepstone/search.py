def stepping_stones(n, ones):
    initial_board = [[0]*n for i in range(n)]
    for one in ones:
        initial_board[one[0]][one[1]] = 1

    # Process below is sort of redundant as it goes through EVERY cell 
    # and not just ones affected by change but its 1:43 AM right now and
    # I'm barely functioning.
    def neighbour_sum(board):
        """Checks each cell on the board for its sum by neighbours"""
        sums = {} # The sums here is a dictionary of keys according to the sum and the value being sets of positions
        for i in range(n): # Loop through every cell
            for j in range(n):
                if board[i][j]: continue
                sum = 0
                for k in range(-1, 2): # Loop through neighbours 
                    for l in range(-1, 2):
                        if k == 0 and l == 0 or i+k < 0 or j+l < 0: continue
                        try: # In the case where the index is out of range, just ignore
                            sum += board[i+k][j+l]
                        except: continue
                if sum > 1: 
                    if sum not in sums:
                        sums[sum] = set()
                    sums[sum].add((i, j))
        return sums

    highest = [] # List of highest number reached for each branch
    def recursive_placing(num, board): # The recursion here is travelling down a tree with several branches
        """Recursive function that goes through every possibility of stone placement"""
        sums = neighbour_sum(board)
        if num not in sums:
            highest.append(num - 1)
            return 
        for pos in sums[num]:
            copyboard = [row[:] for row in board] # Prevents a recursion's board from affecting another recursion's board
            copyboard[pos[0]][pos[1]] = num
            recursive_placing(num+1, copyboard)
    
    recursive_placing(2, initial_board)
    return max(highest)

