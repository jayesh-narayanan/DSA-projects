class Maze:
    def __init__(self, m: int, n : int) -> None:
        ## DO NOT MODIFY THIS
        ## We initialise the list with all 0s, as initially all cells are vacant
        self.grid_representation = []
        for row in range(m):
            grid_row = []
            for column in range(n):
                grid_row.append(0)
            self.grid_representation.append(grid_row)
    
    def add_ghost(self, x : int, y: int) -> None:
        # IMPLEMENT YOUR FUNCTION HERE
        self.grid_representation[x][y]=1
    def remove_ghost(self, x : int, y: int) -> None:
        # IMPLEMENT YOUR FUNCTION HERE
        self.grid_representation[x][y]=0
    def is_ghost(self, x : int, y: int) -> bool:
        # IMPLEMENT YOUR FUNCTION HERE
        return self.grid_representation[x][y]==1
    def print_grid(self) -> None:
        # IMPLEMENT YOUR FUNCTION HERE
        for i in range(self.rows()):
            for j in range(self.cols()):
                print(self.grid_representation[i][j],end='')
                print(" ",end='')
            print('')
    def rows(self) -> int:
        return len(self.grid_representation)
    def cols(self) -> int:
        return len((self.grid_representation[0]))