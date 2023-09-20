from random import randrange, choice, random

class Maze:
    def __init__(self, rows, columns, length=10, launchpads=False):
        self.rows = rows
        self.columns = columns
        self.start = (randrange(rows), randrange(columns))
        self.visited = []
        self.maze = [[0 for j in range(columns)] for i in range(rows)]
        self.gen_maze(length)
        if launchpads:
            self.gen_launchpads()

    def has_been_visited(self, row, col):
        if (row, col) in self.visited:
            return True
        return False

    def count_paths(self):
        paths = 0
        for row in self.maze:
            for i in row:
                if i == 1:
                    paths += 1
        return paths

    def gen_maze(
            self,
            length,
            ):
        cur_pos = (self.start[0], self.start[1])
        self.visited.append(cur_pos)
        while self.count_paths() < length:
            self.maze[cur_pos[0]][cur_pos[1]] = 1
            choices = []
            if cur_pos[0] < self.rows - 1 and not self.has_been_visited(cur_pos[0]+1, cur_pos[1]):
                choices.append((cur_pos[0]+1, cur_pos[1]))
            if cur_pos[0] > 0 and not self.has_been_visited(cur_pos[0]-1, cur_pos[1]):
                choices.append((cur_pos[0]-1, cur_pos[1]))
            if cur_pos[1] < self.columns - 1 and not self.has_been_visited(cur_pos[0], cur_pos[1]+1):
                choices.append((cur_pos[0], cur_pos[1]+1))
            if cur_pos[1] > 0 and not self.has_been_visited(cur_pos[0], cur_pos[1]-1):
                choices.append((cur_pos[0], cur_pos[1]-1))
            
            if not choices:
                i -= 2
                self.maze[cur_pos[0]][cur_pos[1]] = 0
                cur_pos = self.visited.pop()
            else:
                cur_pos = choice(choices) 
        
        #Generate launchpads
    def gen_launchpads(self):
        for i in range(10, len(self.maze)):
            for j in range(0, len(self.maze[i])):
                if(
                    random() >= .99
                    and self.maze[i-1][j] == 0
                    and self.maze[i][j] == 1
                ):
                    self.maze[i][j] = 2

        


#----------------TESTING---------------------#
if __name__ == "__main__":
    for i in range(50):
        print(f"iteration {i}:")
        m = Maze(10, 10)
        m.gen_maze(length=20)
        for row in m.maze:
            for j in row:
                print(j, end=' ')
            print()

        print('\n\n')
            
             


        
        
