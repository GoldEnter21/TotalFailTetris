from difflib import HtmlDiff
import math
from operator import truediv
from pickle import TRUE
import TetrisGame
import time

class GameState():
    def __init__(self):
        self.grid = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.garbage = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
        self.successful_update = True
        self.clearing_allowed = True
        self.garbage_poslist = [[], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
        self.highest_garbage = 20
        self.highest_garbage_x = [20, 20, 20, 20, 20, 20, 20, 20, 20, 20]
        self.origin_of_death = []
        self.coord_of_death = []
    
    def clear(self, piece_list):
        if self.clearing_allowed == True:
            self.grid.clear()
            self.grid = [
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"]
        ]
    
    def update(self, piece_list):
        
        for piece in piece_list:
            # print(piece.piecetype)
            if (piece.piecetype == "L" or 
                piece.piecetype == "S" or 
                piece.piecetype == "Z" or 
                piece.piecetype == "T" or 
                piece.piecetype == "P" or
                piece.piecetype == "I" or
                piece.piecetype == "O"):
                if piece.isdone == False:
                    for coord in piece.Box_Coords:
                        if self.grid[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] == "--":
                            self.grid[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] = "P" + "-"
                        if self.garbage[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] == "D-":
                            self.successful_update = False
                            self.origin_of_death.append((piece.origin[0], piece.origin[1]))
                            self.coord_of_death.append((int(piece.origin[0] + coord[0]), int(piece.origin[1] + coord[1])))
                            # piece.isdone = True
                if piece.isdone == True:
                    for coord in piece.Box_Coords:
                        if self.grid[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] == "--":
                            self.grid[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] = "P" + "-"
                        self.garbage[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] = "D" + "-"
                            # if int(piece.origin[1] + coord[1]) > self.highest_garbage:
                            #     self.highest_garbage = int(piece.origin[1] + coord[1])
                            #     self.highest_garbage_x[int(piece.origin[0] + coord[0])] = int(piece.origin[1] + coord[1])
                            # elif int(piece.origin[1] + coord[1]) < self.highest_garbage or int(piece.origin[1] + coord[1]) == self.highest_garbage:
                            #     self.highest_garbage_x[int(piece.origin[0] + coord[0])] = int(piece.origin[1] + coord[1])
                        # piece.set == True
            # elif (piece.piecetype == "I" or piece.piecetype == "O"):
            #     for coord in piece.Box_Coords:
            #         self.grid[int(piece.origin[1] + coord[1])][int(piece.origin[0] + coord[0])] = "P" + "-"
        self.clearing_allowed = False
        for row in range(len(self.garbage)):
            if self.garbage[row] == ["D-", "D-", "D-", "D-", "D-", "D-", "D-", "D-", "D-", "D-"]:
                self.garbage.pop(row)
                self.garbage.insert(0, ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"])
                self.highest_garbage = self.highest_garbage + 1
                for i in range(len(self.highest_garbage_x)):
                    self.highest_garbage_x[i] = self.highest_garbage_x[i] + 1
                    if self.highest_garbage_x[i] > 20:
                        self.highest_garbage_x[i] = 20
                    # garbage_found = False
                    # z = 0
                    # for n in range(len(self.garbage)):
                    #     if self.garbage[n][i] == "D-":
                    #         garbage_found = True
                    #         z = n
                    # if garbage_found == False:
                    #     z = 20
                    # elif garbage_found == True:
                    #     self.highest_garbage_x[i] = z
                self.grid.pop(row)
                self.grid.insert(0, ["--", "--", "--", "--", "--", "--", "--", "--", "--", "--"])
                print (len(self.garbage))
        for i in range(len(self.garbage_poslist)):
            self.garbage_poslist[i] = []
        for row in range(len(self.garbage)):
            D_pos_list = []
            for i in range(len(self.garbage[row])):
                if self.garbage[row][i] == "D-":
                    D_pos_list.append(i)
            self.garbage_poslist[row] = D_pos_list
        current_highest_garbgarb = 20
        for i in range(len(self.garbage_poslist)):
            if len(self.garbage_poslist[i]) > 0:
                if current_highest_garbgarb > i:
                    current_highest_garbgarb = i
            for n in range(len(self.garbage_poslist[i])):
                if self.highest_garbage_x[self.garbage_poslist[i][n]] > i:
                    self.highest_garbage_x[self.garbage_poslist[i][n]] = i
        self.highest_garbage = current_highest_garbgarb
        self.clearing_allowed = True
        return [self.successful_update, self.origin_of_death, self.coord_of_death]

class Tetromino():
    def __init__(self, type):
        if (type == "I" or 
            type == "L" or 
            type == "P" or 
            type == "O" or 
            type == "S" or 
            type == "Z" or 
            type == "T"): 
            self.piecetype = type
            if type == "T":
                self.Box_Coords = [(-1,0), (0,1), (1,0), (0,0)]
                self.origin = (4,1)
                self.psuedorigin = (4,1)
            if type == "Z":
                self.Box_Coords = [(0,1), (-1,1), (1,0), (0,0)]
                self.origin = (4,1)
                self.psuedorigin = (4,1)
            if type == "S":
                self.Box_Coords = [(-1,0), (0,1), (1,1), (0,0)]
                self.origin = (4,1)
                self.psuedorigin = (4,1)
            if type == "O":
                self.Box_Coords = [(-0.5, 0.5), (0.5, 0.5), (-0.5, -0.5), (0.5, -0.5)]
                self.origin = (4.5, 0.5)
                self.psuedorigin = (4.5, 0.5)
            if type == "P":
                self.Box_Coords = [(-1,0), (-1,1), (1,0), (0,0)]
                self.origin = (4,1)
                self.psuedorigin = (4,1)
            if type == "L":
                self.Box_Coords = [(-1,0), (1,0), (1,1), (0,0)]
                self.origin = (4,1)
                self.psuedorigin = (4, 1)
            if type == "I":
                self.Box_Coords = [(-1.5,0.5), (-0.5,0.5), (0.5,0.5), (1.5,0.5)]
                self.origin = (4.5, 0.5)
                self.psuedorigin = (4.5, 0.5)
        self.isdone = False
        self.set = False
        self.hardropcoordsy = []
        self.hardropcoordsx = []
        self.HDS = False

    def RotatePiece(self, angle):
        newcoordslist = []
        ox, oy = self.origin[0], self.origin[1]
        # print("origin:", ox, oy)
        for i in self.Box_Coords:
            px1, py1 = i[0] + self.origin[0], i[1] + self.origin[1]
            # print("coord:", px1, py1)

            qx = int(round((ox + math.cos(math.radians(angle)) * (px1 - ox) - math.sin(math.radians(angle)) * (py1 - oy))))
            qy = int(round((oy + math.sin(math.radians(angle)) * (px1 - ox) + math.cos(math.radians(angle)) * (py1 - oy))))
            aqx = qx - ox
            aqy = qy - oy
            newcoordslist.append((aqx, aqy))
        return newcoordslist
    
    def CheckPieceBounds(self, test_origin):
        cani = True
        problem = 0
        piece_movable = [cani, problem]
        for i in self.Box_Coords:
            px2, py2 = i[0] + test_origin[0], i[1] + test_origin[1]
            if px2 < 0: 
                problem = 1
                cani = False
            if py2 < 0: 
                problem = 2
                cani = False
            if px2 >= 10: 
                problem = 3
                cani = False
            if py2 >= 21: 
                problem = 4
                cani = False
        piece_movable = [cani, problem]
        return piece_movable

    def CheckIfDone(self, test_origin):
        done = False
        if self.isdone != True:
            done = False
            for i in range(len(self.Box_Coords)):
                py2 = test_origin[1] + self.Box_Coords[i][1]
                if py2 >= 20:
                    done = True
        elif self.isdone == False:
            done = False
        return done

    def harddrop(self, gamestate):
        def odd_occurring_num(arr):
            return [i for i in arr if arr.count(i) < 2]
        newcoordslist1 = []
        newcoordslist =[]
        for i in self.Box_Coords:
            px3, py3 = int(i[0] + self.origin[0]), int(i[1] + self.origin[1])
            if self.hardropcoordsx.count(px3) > 0:
                if self.hardropcoordsy[self.hardropcoordsx.index(px3)] < py3:
                    self.hardropcoordsy.pop(self.hardropcoordsx.index(px3))
                    self.hardropcoordsx.pop(self.hardropcoordsx.index(px3))
                    self.hardropcoordsy.append(py3)
                    self.hardropcoordsx.append(px3)
            else:
                self.hardropcoordsy.append(py3)
                self.hardropcoordsx.append(px3)

        bottomy = max(self.hardropcoordsy)
        bottomx = []
        for i in range(len(self.hardropcoordsy)):
            if self.hardropcoordsy[i] == bottomy or self.hardropcoordsx.count(self.hardropcoordsx[i]) < 2:
                bottomx.append(self.hardropcoordsx[i])
        possible_HDFS = []
        for i in bottomx:
            possible_HDFS.append(gamestate.highest_garbage_x[i] - self.hardropcoordsy[self.hardropcoordsx.index(i)] - 1)
        HARD_DF = min(possible_HDFS)
        for i in range(4):
            newcoordslist1.append(((self.Box_Coords[i][0] + self.origin[0]), (self.Box_Coords[i][1] + self.origin[1] + HARD_DF)))
        self.origin = ((self.origin[0]), (self.origin[1] + HARD_DF))
        for i in range(4):
            newcoordslist.append(((newcoordslist1[i][0] - self.origin[0]), (newcoordslist1[i][1] - self.origin[1])))
        self.HDS = True
        return newcoordslist
