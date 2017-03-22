"""
This module contains the Wumpus Agent
        Made for UCI CS 171
Created by: Ryan Atkins | ratkins@uci.edu
"""

import WumpusWorldGameState as wumpus

class Agent(object):
    """docstring for Agent"""
    def __init__(self):
        self.current_location   = [0,0]
        self.visited            = [(0,0)]
        self.safe               = []
        self.possible_wumpus    = []
        self.plan           = []
        self.num_moves      = 0
        self.direction      = 'right'
        self.return_goal    = ''
        self.exiting        = False
        self.return_route   = []
        self.backtrack_route = []
        self.move           = ''
        self.has_gold       = False
        self.has_arrow      = True
        self.shot_arrow     = 0
        self.Wumpus_alive   = True
        self.Wumpus_loc     = []
        self.added_move     = False
        self.col_limit      = 100
        self.row_limit      = 100
        self.inner_row      = 1
        self.inner_col      = 100
        self.c              = 0
        self.r              = 1
        self.snake_end      = [100,100]
        self.backtracking   = False
        self.restart        = 0


    def _update_visited(self):
        if self.direction == 'right':
            self.current_location[0] += 1
        elif self.direction == 'down':
            self.current_location[1] += 1
        elif self.direction == 'left':
            self.current_location[0] -= 1
        elif self.direction == 'up':
            self.current_location[1] -= 1
        
        self.visited.append((self.current_location[0], self.current_location[1]))


    def _update_direction(self,current,next_move):
        if next_move not in ['left','right']:
            pass
        else:
            if next_move == 'right':
                if current == 'right':
                    self.direction = 'down'
                elif current == 'down':
                    self.direction = 'left'
                elif current == 'left':
                    self.direction = 'up'
                elif current == 'up':
                    self.direction = 'right'
            else:
                if current == 'right':
                    self.direction = 'up'
                elif current == 'down':
                    self.direction = 'right'
                elif current == 'left':
                    self.direction = 'down'
                elif current == 'up':
                    self.direction = 'left'


    def calculate_turn(self, return_direction):
        if return_direction == 'left':
            if self.direction == 'left':
                self.plan.append('forward')
                self.added_move     = True
                self.move = 'forward'
                # self.return_route.pop()
            elif self.direction == 'up':
                self.plan.append('left')
                self.added_move     = True
                self.move = 'left'
            elif self.direction == 'down':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'
            elif self.direction == 'right':
                self.plan.append('left')
                self.added_move     = True
                self.move = 'left'

        elif return_direction == 'right':
            if self.direction == 'right':
                self.plan.append('forward')
                self.added_move     = True
                self.move = 'forward'
                # self.return_route.pop()
            elif self.direction == 'up':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'
            elif self.direction == 'down':
                self.plan.append('left')
                self.added_move     = True
                self.move = 'left'
            elif self.direction == 'left':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'

        elif return_direction == 'up':
            if self.direction == 'up':
                self.plan.append('forward')
                self.added_move     = True
                self.move = 'forward'
            elif self.direction == 'right':
                self.plan.append('left')
                self.added_move     = True
                self.move = 'left'
            elif self.direction == 'left':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'
            elif self.direction == 'down':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'

        elif return_direction == 'down':
            if self.direction == 'down':
                self.plan.append('forward')
                self.added_move     = True
                self.move = 'forward'
            elif self.direction == 'left':
                self.plan.append('left')
                self.added_move     = True
                self.move = 'left'
            elif self.direction == 'right':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'
            elif self.direction == 'up':
                self.plan.append('right')
                self.added_move     = True
                self.move = 'right'

        # self._update_direction(self.direction,self.move)
        # if self.move == 'forward':
        #     self._update_visited()


    def backtrack(self):

        if len(self.return_route) == 0:
            self.return_route = self.visited[:-1]

        # print('return_route: ', self.return_route)   ## This Print Statement
        previous   = self.return_route[-1]
        difference = [previous[0] - self.current_location[0],previous[1] - self.current_location[1]]

        # print('difference -> ', difference)

        if difference[0] == -1:
            self.return_goal = 'left'
        elif difference[0] == 1:
            self.return_goal = 'right'
        elif difference[1] == -1:
            self.return_goal = 'up'
        elif difference[1] == 1:
            self.return_goal = 'down'

        # print('facing:', self.direction)   ## This Print Statement
        # print('return_goal:', self.return_goal)
        # print('current_location:', self.current_location)

        self.calculate_turn(self.return_goal)


    def gen_wumpus_list(self,location):
        # Left
        self.possible_wumpus.append((location[0]-1,location[1]))
        # Right
        self.possible_wumpus.append((location[0]+1,location[1]))
        # Up 
        self.possible_wumpus.append((location[0],location[1]-1))
        # Down
        self.possible_wumpus.append((location[0],location[1]+1))

        # Clean up list to valid locaitons.
        # print('possible_wumpus:', self.possible_wumpus)
        i = 0
        for x,y in self.possible_wumpus:
            # print('(',x,',',y,') [',i,']')
            if (x,y) == (0,0):
                self.possible_wumpus.pop(i)
            if x < 0 or x > self.col_limit-1:
                self.possible_wumpus.pop(i)
            if y < 0 or y > self.col_limit-1:
                self.possible_wumpus.pop(i)
            i += 1

        for x,y in self.visited:
            if (x,y) in self.possible_wumpus:
                self.possible_wumpus.remove((x,y))

        # print('possible_wumpus:',self.possible_wumpus)

        if len(self.possible_wumpus) == 1:
            self.Wumpus_loc = self.possible_wumpus[0]


    def shot_at(self):
        if self.direction == 'right':
            self.shot_at = (self.current_location[0]+1,self.current_location[1])
        elif self.direction == 'left':
            self.shot_at = (self.current_location[0]-1,self.current_location[1])
        elif self.direction == 'down':
            self.shot_at = (self.current_location[0],self.current_location[1]+1)
        else:
            self.shot_at = (self.current_location[0],self.current_location[1]-1)


    def orientate_to_shoot(self):
        if (self.Wumpus_loc[0], self.Wumpus_loc[1]) == (self.current_location[0],self.current_location[1]+1):
            return 'down'
        elif (self.Wumpus_loc[0], self.Wumpus_loc[1]) == (self.current_location[0],self.current_location[1]-1):
            return 'up'
        elif (self.Wumpus_loc[0], self.Wumpus_loc[1]) == (self.current_location[0]-1,self.current_location[1]):
            return 'left'
        elif (self.Wumpus_loc[0], self.Wumpus_loc[1]) == (self.current_location[0]+1,self.current_location[1]):
            return 'right'


    def will_hit_wumpus(self):
        if self.direction == 'right':
            if (self.current_location[0]+1,self.current_location[1]) == self.Wumpus_loc:
                return True
        elif self.direction == 'left':
            if (self.current_location[0]-1,self.current_location[1]) == self.Wumpus_loc:
                return True
        elif self.direction == 'up':
            if (self.current_location[0],self.current_location[1]-1) == self.Wumpus_loc:
                return True
        elif self.direction == 'down':
            if (self.current_location[0],self.current_location[1]+1) == self.Wumpus_loc:
                return True
        else:
            return False


    def calculate_snake_end(self):
        # Even Number columns
        if self.col_limit % 2 == 0:
            self.snake_end[0] = (self.col_limit/2) - 1
            self.snake_end[1] = (self.col_limit/2)
        # Odd Number columns
        else:
            self.snake_end[0] = ((self.col_limit-1)/2)
            self.snake_end[1] = ((self.col_limit-1)/2)

        # print('Snake_End:',self.snake_end)


    def add_adjacent(self):
        lx,ly = self.current_location

        # Left
        l = (lx-1,ly)
        r = (lx+1,ly)
        u = (lx,ly-1)
        d = (lx,ly+1)

        # Left
        if self.direction != 'left':
            if l not in self.safe:
                if l[0] >= 0 and l[0] <= self.col_limit-1 and l[1] >= 0 and l[1] <= self.row_limit-1:
                    self.safe.append(l)
        # Right
        if self.direction != 'right':
            if r not in self.safe:
                if r[0] >= 0 and r[0] <= self.col_limit-1 and r[1] >= 0 and r[1] <= self.row_limit-1:
                    self.safe.append(r)
        # Up 
        if self.direction != 'up':
            if u not in self.safe:
                if u[0] >= 0 and u[0] <= self.col_limit-1 and u[1] >= 0 and u[1] <= self.row_limit-1:
                    self.safe.append(u)
        # Down
        if self.direction != 'down':
            if d not in self.safe:
                if d[0] >= 0 and d[0] <= self.col_limit-1 and d[1] >= 0 and d[1] <= self.row_limit-1:
                    self.safe.append(d)


        for x,y in self.visited:
            if (x,y) in self.safe:
                self.safe.remove((x,y))


    def return_to_safe(self):
        if self.current_location != [0,0]:
            self.backtrack()


    def get_move(self, percepts):
        "Take in a set of strings and return a string"
        """
        Inputs to this function is a set containing possible strings:
            Stench
            Breeze
            Bump
            Scream
            Glitter
        Outputs of the function:
            Left
            Right
            Forward
            Grab
            Shoot
            Climb
        Note: Capitalization does not matter.
        """

        # If Agent has the Gold, set flag to exit the cave.
        if self.has_gold:
            if not self.exiting:
                self.exiting = True

        # If the Agent is exiting, no need to check precepts.
        #  Backtrack path to  exit. 
        #  Just retraces previous steps taken.
        #  Future implementation could implement search algorithm to exit in fewer moves. 
        if self.exiting:
            if self.current_location == [0,0]:
                self.plan.append('climb')
                self.added_move = True
            else:
                self.backtrack()

        # If the Agent is backtracking, handle logic here until Agent reaches a
        #  previously known safe square to explore another path.
        elif self.backtracking:
            if self.current_location != [0,0] and self.restart in [0,1]:
                self.backtrack()
            else:
                if self.will_hit_wumpus() or ((0,1) not in self.safe and self.current_location == [0,0]):
                    self.plan.append('climb')
                    self.added_move = True
                else:
                    if self.restart > 5:
                        self.plan.append('climb')
                        self.added_move = True
                    else:
                        if self.restart == 0:
                            self.plan.append('left')
                        elif self.restart == 1:
                            self.visited = [(0,0)]
                            self.plan.append('forward')
                        elif self.restart == 2:
                            # First check for Gold.
                            if not self.has_gold and 'Glitter' in percepts:
                                self.plan.append('grab')
                                self.has_gold   = True
                            else:
                                self.plan.append('left')
                            
                            self.restart = 0
                            self.backtracking = False

                        self.added_move = True
                        self.restart += 1
                    

        # Main logic to handle exploration of cave. 
        # Will pass to another section if the Agent needs to backtrack or exit.
        else:
            # If at least 1 percept sensed, evaluate percepts to decide move.
            if len(percepts) > 0:

                # First check for Gold.
                if not self.has_gold and 'Glitter' in percepts:
                    if not self.added_move:
                        self.plan.append('grab')
                        self.added_move = True
                        self.has_gold   = True

                # Next check to see if Agent hit a wall.
                if 'Bump' in percepts:
                    if not self.added_move:
                        if self.direction == 'right':
                            self.col_limit = self.current_location[0]
                            self.inner_col = self.col_limit - 2
                            self.current_location[0] -= 1
                            self.visited.pop()
                        elif self.direction == 'down':
                            self.row_limit = self.current_location[1]
                            if self.snake_end == [100,100]:
                                self.calculate_snake_end()
                            self.current_location[1] -= 1
                            self.visited.pop()
                        elif self.direction == 'left':
                            self.current_location[0] += 1
                            self.visited.pop()
                        elif self.direction == 'up':
                            self.current_location[1] += 1
                            self.visited.pop()

                        self.plan.append('right')
                        self.added_move     = True

                # If Breeze in (0,0) -> pit possible in either direction.
                #   safest to just exit cave. 
                if 'Breeze' in percepts:
                    if self.current_location == [0,0]:
                        if not self.added_move:
                            self.plan.append('climb')
                            self.added_move = True
                    else:
                        if not self.added_move:
                            if len(self.safe) > 0:
                                self.backtracking = True
                                self.return_to_safe()
                            else:
                                self.exiting = True
                                self.backtrack()

                # Check to see if the Wumpus has been killed.
                if 'Scream' in percepts:
                    # Wumpus has been shot
                    self.Wumpus_alive   = False
                    self.Wumpus_loc     = self.shot_at
                    # print('Killed Wumpus! @',self.Wumpus_loc)

                # When sensing Stench, shoot and see if you hear Wumpus die.
                #  If so, continue ignoring all Stench.
                #  If not, backtrack to exit.
                if self.Wumpus_alive:
                    if 'Stench' in percepts:
                        if not self.added_move:
                            # Initial Stench, generate Possible Wumpus location list.
                            if len(self.possible_wumpus) == 0:
                                self.gen_wumpus_list(self.current_location)

                            if self.has_arrow:
                                # Check if you already found the Wumpus
                                if len(self.Wumpus_loc) > 0:
                                    wumpus_dir = self.orientate_to_shoot()
                                else:
                                    wumpus_dir = self.direction

                                if self.direction == wumpus_dir:
                                    self.plan.append('shoot')
                                    self.added_move = True
                                    self.has_arrow  = False
                                    self.shot_arrow = self.num_moves
                                    self.shot_at()
                                    self.possible_wumpus.remove(self.shot_at)
                                else:
                                    self.calculate_turn(wumpus_dir)
                            
                            else:
                                if len(self.Wumpus_loc) == 0:
                                    if len(self.possible_wumpus) == 1:
                                        self.Wumpus_loc = self.possible_wumpus[0]
                                
                                # check for first move after shooting arrow
                                if self.num_moves - self.shot_arrow == 1:
                                    if not self.added_move:
                                        self.plan.append('forward')
                                        self.added_move = True
                                
                                else:
                                    if self.will_hit_wumpus():
                                        # self.backtrack()
                                        self.backtracking = True
                                        self.return_to_safe()
                                    else:
                                        self.plan.append('forward')
                                        self.added_move = True
                
                else:
                    # Here the Wumpus is no longer Alive
                    # Behave just like no percepts.
                    if self.current_location == self.snake_end:
                        self.exiting = True
                        self.backtrack()
                    elif self.current_location == [self.c,self.r]:
                        if not self.added_move:
                            self.plan.append('right')
                            self.added_move = True
                            self.c  += 1
                            self.r  += 1
                    elif self.current_location == [self.inner_col,self.inner_row]:
                        if not self.added_move:
                            self.plan.append('right')
                            self.added_move = True
                            if self.direction == 'down':
                                self.inner_col -= 1
                            if self.direction == 'right':
                                self.inner_row += 1
                    elif not self.added_move:
                        self.plan.append('forward')
                        self.added_move     = True

            # Otherwise, no percepts, save adjacent 'safe' squares and move forward.
            else:
                self.add_adjacent()

                # Agent will prefer to snake through cave around the border before moving inwards.
                if self.current_location == self.snake_end:
                    self.exiting = True
                    self.backtrack()
                elif self.current_location == [self.c,self.r]:
                    if not self.added_move:
                        self.plan.append('right')
                        self.added_move = True
                        self.c  += 1
                        self.r  += 1
                elif self.current_location == [self.inner_col,self.inner_row]:
                    if not self.added_move:
                        self.plan.append('right')
                        self.added_move = True
                        if self.direction == 'down':
                            self.inner_col -= 1
                        if self.direction == 'right':
                            self.inner_row += 1
                elif not self.added_move:
                    self.plan.append('forward')
                    self.added_move     = True

        
        # print('Agent facing:',self.direction)
        # print('Agent plan:', self.plan)
        self.move = self.plan.pop(0)
        # print('Agent remaining plan:', self.plan)

        self._update_direction(self.direction,self.move)
        # print('Agent next facing:',self.direction)

        if self.move == 'forward':
            self._update_visited()

            for x,y in self.visited:
                if (x,y) in self.safe:
                    self.safe.remove((x,y))

            if self.exiting or self.backtracking:
                if len(self.return_route) > 0:
                    self.return_route.pop()


        # print('\n')
        self.num_moves += 1
        self.added_move = False
        return self.move
        
