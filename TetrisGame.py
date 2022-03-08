from shutil import move
import pygame
import TetrisEngine
import random
import math
import time

pygame.init()
WIDTH, HEIGHT = 900, 700
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("First Game!")
clock = pygame.time.Clock()
font = pygame.font.SysFont("Calibri", 11, bold=True)
available_pieces_list = ["I", "O", "L", "P", "S", "Z", "T"]
pieces_list = []
set_pieces_list = []
Grid_Width = 10
Grid_Height = 20
if (576 / Grid_Width) <= (480 / Grid_Height):
    Square_Size = 576 / Grid_Height
if (576 / Grid_Width) > (480 / Grid_Height):
    Square_Size = 480 / Grid_Height
Grid_rect_list = []
can_move_down = True

WHITE = (0, 0, 0)
BLACK = (255, 255 , 255)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)


def Create_Grid():

    for y in range(Grid_Height):
        for x in range(Grid_Width):
            eggs = x*(Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2))
            whys = y*(Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2))
            rect = pygame.Rect(eggs, whys, Square_Size, Square_Size)
            pygame.draw.rect(WIN, BLACK, rect)

    pygame.display.update()


def update_fps():
    coverrect = pygame.Rect(0, 0, 60, 40)
    pygame.draw.rect(WIN, WHITE, coverrect)
    fps = str(int(clock.get_fps()))
    fps_text = font.render(fps + " FPS", 1, pygame.Color("white"))
    WIN.blit(fps_text, (6,4))

def draw_window(gamestate, Tetromino):
    for r in range(Grid_Height):
        for c in range(Grid_Width):
            piece = gamestate.grid[r][c]
            garbage = gamestate.garbage[r][c]
            cols = c*(Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2))
            rols = r*(Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2))
            if piece != "--" or garbage != "--":
                if garbage != "--" and piece == "--":
                    tetrominodomino = pygame.Rect(cols, rols, Square_Size, Square_Size)
                    pygame.draw.rect(WIN, BLUE, tetrominodomino)
                elif garbage == "--" and piece != "--":
                    tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                    pygame.draw.rect(WIN, GREEN, tetrominodominay)
            elif piece == "--" and garbage == "--":
                tetrominodominay = pygame.Rect(cols, rols, Square_Size, Square_Size)
                pygame.draw.rect(WIN, BLACK, tetrominodominay)
    cursor = pygame.Rect(Tetromino.psuedorigin[0] * (Square_Size + 1) - 4 + ((WIDTH / 2) - (Square_Size * Grid_Width / 2)) +  + (Square_Size / 2), Tetromino.psuedorigin[1] * (Square_Size + 1) - 2 + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2)) +  + (Square_Size / 2), 4, 4)
    pygame.draw.rect(WIN, WHITE, cursor)
    pygame.draw.line(WIN, RED, ((Tetromino.psuedorigin[0] * (Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2)) +  + (Square_Size / 2)), (Tetromino.psuedorigin[1] * (Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2)) +  + (Square_Size / 2))), ((Tetromino.origin[0] * (Square_Size + 1) + ((WIDTH / 2) - (Square_Size * Grid_Width / 2)) + (Square_Size / 2)), (Tetromino.origin[1] * (Square_Size + 1) + ((HEIGHT / 2) - (Square_Size * Grid_Height / 2)) + (Square_Size / 2))))
    update_fps()
    pygame.display.update()

def snap_pieces(T):
    if (T.piecetype == "L" or 
        T.piecetype == "S" or 
        T.piecetype == "Z" or 
        T.piecetype == "T" or 
        T.piecetype == "P" or
        T.piecetype == "I" or
        T.piecetype == "O"):
        sample_origin = convert_to_reg_origin(T, T.psuedorigin)
        if (T.CheckPieceBounds(sample_origin))[0] == True:
            T.origin = sample_origin
    # elif (T.piecetype == "I" or 
    #     T.piecetype == "O"):
    #     origin1 = (round((T.origin[0]) * 2))/2
    #     origin2 = (round((T.origin[1]) * 2))/2
    #     T.origin = (origin1, origin2)

def convert_to_reg_origin(T, psuedorigin):

    if (T.piecetype == "L" or 
        T.piecetype == "S" or 
        T.piecetype == "Z" or 
        T.piecetype == "T" or 
        T.piecetype == "P"):
        x = round(psuedorigin[0])
        y = round(psuedorigin[1])
    elif (T.piecetype == "I" or 
        T.piecetype == "O"):
        lookableOriX, lookableOriY = str(psuedorigin[0]), str(psuedorigin[1])
        point_locx = 0
        point_locy = 0
        for i in range(len(lookableOriX)):
            if lookableOriX[i-1] == ".":
                point_locx = i
        for i in range(len(lookableOriY)):
            if lookableOriY[i-1] == ".":
                point_locy = i
        xrounder = lookableOriX[0:point_locx]
        yrounder = lookableOriY[0:point_locy]
        x = float(xrounder + "5")
        y = float(yrounder + "5")
    reg_origin = (x, y)
    return reg_origin

def main():
    global original_origin
    global can_move_down
    FPS = 60
    TARGET_FPS = 80
    int = random.randint(0, 6)
    T = TetrisEngine.Tetromino(available_pieces_list[int])
    pieces_list.append(T)
    print(available_pieces_list[int])
    print(T.Box_Coords)
    print(T.origin)
    gs = TetrisEngine.GameState()
    velocity = 0.03
    prev_time = time.time()
    dt = 0
    run = True
    WIN.fill(WHITE)
    Create_Grid()
    create_new_piece = False
    moveOn = True
    isdone = False
    while run:
        isdone = T.isdone
        if moveOn == False:
            isdone = True
        if isdone == True:
            create_new_piece = True
            moveOn = True
            isdone = False
        
        if create_new_piece == True:
            while (len(pieces_list)) > 0:
                set_pieces_list.append(pieces_list[0])
                pieces_list.pop(0)
            int = random.randint(0, 6)
            T = TetrisEngine.Tetromino(available_pieces_list[int])
            pieces_list.append(T)
            create_new_piece = False

        clock.tick(FPS)

        now = time.time()
        dt = now - prev_time
        prev_time = now

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    snap_pieces(T)
                    T.Box_Coords = T.RotatePiece(90)
                if event.key == pygame.K_SPACE:
                    T.Box_Coords = T.harddrop(gs)
                    T.isdone = True
            if event.type == pygame.KEYUP:
                snap_pieces(T)

        keys_pressed = pygame.key.get_pressed()
        if keys_pressed[pygame.K_RIGHT]:
            original_origin = T.psuedorigin
            sample_origin = convert_to_reg_origin(T, (T.psuedorigin[0] + velocity * dt * TARGET_FPS, T.psuedorigin[1]))
            if (T.CheckPieceBounds(sample_origin))[0] == True:
                T.psuedorigin = (T.psuedorigin[0] + velocity * dt * TARGET_FPS, T.psuedorigin[1])
            else:
                T.psuedorigin = original_origin
        if keys_pressed[pygame.K_LEFT]:
            original_origin = T.psuedorigin
            sample_origin = convert_to_reg_origin(T, (T.psuedorigin[0] - velocity * dt * TARGET_FPS, T.psuedorigin[1]))
            if (T.CheckPieceBounds(sample_origin))[0] == True:
                T.psuedorigin = (T.psuedorigin[0] - velocity * dt * TARGET_FPS, T.psuedorigin[1])
            else:
                T.psuedorigin = original_origin
        if keys_pressed[pygame.K_DOWN]:
            original_origin = T.psuedorigin
            sample_origin = convert_to_reg_origin(T, (T.psuedorigin[0], T.psuedorigin[1] + velocity * dt * TARGET_FPS))
            if (T.CheckPieceBounds(sample_origin))[0] == True:
                if T.CheckIfDone(sample_origin) == False:
                    T.psuedorigin = (T.psuedorigin[0], T.psuedorigin[1] + velocity * dt * TARGET_FPS)
                elif T.CheckIfDone(sample_origin) == True:
                    can_move_down = False
                    T.isdone = True
                    T.psuedorigin = original_origin
            else:
                T.psuedorigin = original_origin
        if keys_pressed[pygame.K_UP]:
            original_origin = T.psuedorigin
            sample_origin = convert_to_reg_origin(T, (T.psuedorigin[0], T.psuedorigin[1] - velocity * dt * TARGET_FPS))
            if (T.CheckPieceBounds(sample_origin))[0] == True:
                T.psuedorigin = (T.psuedorigin[0], T.psuedorigin[1] - velocity * dt * TARGET_FPS)
            else:
                T.psuedorigin = original_origin 

        gs.clear(pieces_list)    

        # for piece in pieces_list:
        #     if piece.isdone == False:
        #         original_origin = T.psuedorigin
        #         sample_origin = convert_to_reg_origin(piece, (piece.psuedorigin[0], piece.psuedorigin[1] + 0.08))
        #         if (piece.CheckPieceBounds(sample_origin))[0] == True:
        #             if piece.CheckIfDone(sample_origin) == False:
        #                 piece.psuedorigin = (piece.psuedorigin[0], piece.psuedorigin[1] + 0.08)
        #             elif piece.CheckIfDone(sample_origin) == True:
        #                 piece.isdone = True
        #                 piece.psuedorigin = original_origin
        #         else:
        #             piece.psuedorigin = original_origin
        
        if T.HDS == False:
            T.origin = convert_to_reg_origin(T, T.psuedorigin)

        gs.update(pieces_list)
        if gs.successful_update == False:
            moveOn = False
            T.harddrop(gs)
            gs.origin_of_death.clear()
            gs.coord_of_death.clear()
            T.isdone = True
            can_move_down = True
            gs.update(pieces_list)
            gs.successful_update = True

        print(" ")
        print(" ")

        # for i in range (0, 24):    
        #     print(gs.garbage[i])
        print(gs.highest_garbage_x)

        draw_window(gs, T)

    pygame.quit()

if __name__ == "__main__":
    main()