from maze import *
from exception import *
from stack import *
class PacMan:
    navigator_maze = []
    def __init__(self, grid : Maze) -> None:
        self.navigator_maze = grid.grid_representation
        self.rows=grid.rows()
        self.cols=grid.cols()
        self.visited=[]
        for row in range(self.rows):
            grid_row = []
            for column in range(self.cols):
                grid_row.append(0)
            self.visited.append(grid_row)
    def find_path(self, start : tuple[int, int], end : tuple[int, int]) -> list[tuple[int, int]]:
        # IMPLEMENT FUNCTION HERE
        ans=[]
        if self.navigator_maze[start[0]][start[1]]==1 or self.navigator_maze[end[0]][end[1]]==1:
            raise PathNotFoundException
        stk=Stack()
        stk.push(start)
        while(stk.is_empty() is not True):
            pointer=stk.top()
            if self.check_end(pointer,end):
                ans.insert(0,stk.pop())
                pointer=end
                while(stk.size()>=1):
                    cell=stk.pop()
                    if self.is_neighbour(cell,pointer):
                        ans.insert(0,cell)
                        pointer=cell
                return ans
            if self.deadend(pointer,stk):
                stk.pop()

        raise PathNotFoundException

    def deadend(self,cell:tuple[int,int],stk:Stack) -> bool:
        flag=True
        if (cell[0]>0 and self.navigator_maze[cell[0]-1][cell[1]]==0 and self.visited[cell[0]-1][cell[1]]==0):
            stk.push((cell[0]-1,cell[1]))
            self.visited[cell[0]-1][cell[1]]=1
            flag=False
        if (cell[1]>0 and self.navigator_maze[cell[0]][cell[1]-1]==0 and self.visited[cell[0]][cell[1]-1]==0):
            stk.push((cell[0],cell[1]-1))
            self.visited[cell[0]][cell[1]-1]=1
            flag=False
        if (cell[0]<self.rows-1 and self.navigator_maze[cell[0]+1][cell[1]]==0 and self.visited[cell[0]+1][cell[1]]==0):
            stk.push((cell[0]+1,cell[1]))
            self.visited[cell[0]+1][cell[1]]=1
            flag=False
        if (cell[1]<self.cols-1 and self.navigator_maze[cell[0]][cell[1]+1]==0 and self.visited[cell[0]][cell[1]+1]==0):
            stk.push((cell[0],cell[1]+1))
            self.visited[cell[0]][cell[1]+1]=1
            flag=False
        return flag

    def check_end(self,cell:tuple[int,int],end:tuple[int,int]) -> bool:
        return cell==end

    def is_neighbour(self,cell1:tuple[int,int], cell2:tuple[int,int]) -> bool:
        return abs(cell1[0]-cell2[0]) + abs(cell1[1]-cell2[1]) == 1