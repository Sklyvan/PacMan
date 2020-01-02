import pygame
import time
from pygame.locals import *
from Characters import PacMan_Player, Ghost_Enemy
from Game_Map import Labyrinth_Map, Portal, Labyrinth_Piece
from PacMan_Exceptions import PacMan_Error
import sys
import os

def INIT_GAME_VALUES():
    global WIN_SIZE, WIN_NAME, WIN_BG, WIN, GAME_SPEED, ANIMATION_FRAME_RATE, PacMan, Ghosts, Labyrinth, GAME_OVER_FONT, DEV_MODE, DEV_FONT, PacMan_Direction, \
        AnimationChecker, Special_Phase_Timer, AutoMove_Timer, Ghost_Directions, GAME_LOOP, Labyrinth_Pieces
    os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (550, 150) # Starting the game screen on the center.
    pygame.init()
    GAME_LOOP = True
    WIN_SIZE = (816, 800)
    WIN_NAME = "Python Pac-Man"
    WIN_BG = (0, 0, 0)
    WIN = pygame.display.set_mode(WIN_SIZE)
    pygame.display.set_caption(WIN_NAME)
    GAME_SPEED = 0.50
    ANIMATION_FRAME_RATE = 30
    PacMan = PacMan_Player(385, 725, GAME_SPEED, 35)
    Ghosts = [Ghost_Enemy(410, 355, GAME_SPEED, "Red", 35, "DOWN", 15), Ghost_Enemy(360, 355, GAME_SPEED, "Blue", 35, "UP", 15), Ghost_Enemy(310, 355, GAME_SPEED, "Pink", 35, "LEFT", 15), Ghost_Enemy(460, 355, GAME_SPEED, "Orange", 35, "RIGHT", 15)]
    Labyrinth = Labyrinth_Map()
    Labyrinth_Pieces = []
    Labyrinth_Pieces.append(Labyrinth_Piece(1, 65, 64))
    Labyrinth_Pieces.append(Labyrinth_Piece(2, 213, 66))
    Labyrinth_Pieces.append(Labyrinth_Piece(2, 478, 66))
    Labyrinth_Pieces.append(Labyrinth_Piece(1, 653, 64))
    Labyrinth_Pieces.append(Labyrinth_Piece(3, 165, 169))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 213, 169, Auto_HitBox=False))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 318, 159, -90, Auto_HitBox=False))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 478, 169, 180, Auto_HitBox=False))
    Labyrinth_Pieces.append(Labyrinth_Piece(3, 554, 169))
    Labyrinth_Pieces.append(Labyrinth_Piece(2, 215, 500, 90))
    Labyrinth_Pieces.append(Labyrinth_Piece(2, 551, 500, 90))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 318, 480, -90, Auto_HitBox=False))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 125, 600, 90, Auto_HitBox=False))
    # Labyrinth_Pieces.append(Labyrinth_Piece(5, 515, 600, 90, Auto_HitBox=False))
    # Labyrinth_Pieces.append(Labyrinth_Piece(6, 301, 329))
    Labyrinth.Pieces = Labyrinth_Pieces
    GAME_OVER_FONT = pygame.font.Font('./Sprites/Fonts/Game_Over.ttf', 100)
    DEV_FONT = pygame.font.SysFont('Consolas', 15)
    DEV_MODE = False
    PacMan_Direction = [None, None]
    AnimationChecker = 0  # To slow down the Pac-Man animation.
    Special_Phase_Timer = None  # Counting 10 seconds of Blue & White Pac-Man.
    AutoMove_Timer = None  # To keep moving on the selected direction. (For example: keep moving left 5 seconds)
    Ghost_Directions = [None, None, None, None]
    GAME_LOOP = True
    return True

def isTouching_NormalEdges(Labyrinth, Object): # Using png to check collision on the flat edges of the map.
    Offset = (round(Object.x), round(Object.y))
    return Labyrinth.mask.overlap(Object.mask, Offset)

def isTouchingEdges(Labyrinth, Object):
    try: # Getting the hitbox on a different way depending on if the Object is PacMan or Ghost.
        if type(Object) == Ghost_Enemy:
            Object_HitBox = Object.Big_HitBox
        else:
            Object_HitBox = Object.Rect
    except AttributeError:
        raise PacMan_Error(f"Object of {type(Object)} class doesn't have Rect or Big_HitBox attribute.")
    else:
        for Labyrinth_Edge in Labyrinth.Outgoing_Objects_HitBox: # Checking if the object is touching any of the parts of the labyrinth.
            if Object_HitBox.colliderect(Labyrinth_Edge):
                return True
            else:
                pass
        for Labyrinth_Piece in Labyrinth.Pieces: # Checking if the object is touching any of the parts of the labyrinth.
            if Object_HitBox.colliderect(Labyrinth_Piece.Rect):
                return True
            else:
                pass

def Objects_Collision(Object_1, Object_2): # Getting Object_1 HitBox and Object_2 HitBox.
    try:
        if type(Object_1) == PacMan_Player or type(Object_1) == Labyrinth_Map or type(Object_1) == Labyrinth_Piece: # Depending on the type of object, we use the normal Rect or a bigger hitbox.
            Object_1_Rect = Object_1.Rect
        else:
            Object_1_Rect = Object_1.Big_HitBox
    except AttributeError:
        raise PacMan_Error(f"Object 1 of {type(Object_1)} class doesn't have Rect or Big_HitBox attribute.")
    else:
        try:
            if type(Object_2) == PacMan_Player or type(Object_2) == Labyrinth_Map or type(Object_1) == Labyrinth_Piece:
                Object_2_Rect = Object_2.Rect
            else:
                Object_2_Rect = Object_2.Big_HitBox
        except AttributeError:
            raise PacMan_Error(f"Object 2 of {type(Object_2)} class doesn't have Rect or Big_HitBox attribute.")
        else:
            return Object_1_Rect.colliderect(Object_2_Rect) # Returns True if one HitBox is inside the other.

def Update_Screen(Win, PacMan, Ghosts, AllowAnimation, PacMan_Direction, Ghosts_Directions, Labyrinth):
    Win.fill(WIN_BG) # Turning black the screen.
    Win.blit(Labyrinth.image, (0,0))
    for Piece in Labyrinth_Pieces:
        Win.blit(Piece.image, Piece.Get_Position())
    if DEV_MODE:
        """Text_Surface = DEV_FONT.render(f"Player Position: {PacMan.x},{PacMan.y} {PacMan_Direction[0],PacMan.Current_Direction}", True, (255, 255, 255), (134, 128, 128)) # PacMan coordinates and direction.
        Win.blit(Text_Surface, (0, 0))"""
        PacMan_Counter = 1
        for Ghost in Ghosts:
            if PacMan_Counter == 1:
                Colour = "Red"
            if PacMan_Counter == 2:
                Colour = "Blue"
            if PacMan_Counter == 3:
                Colour = "Pink"
            if PacMan_Counter == 4:
                Colour = "Orange"
            """Text = DEV_FONT.render(f"{Colour} Ghost: {Ghost.x},{Ghost.y} {Ghost.Current_Direction}", True, (255, 255, 255), (134, 128, 128)) # Ghost coordinates and direction.
            PacMan_Counter += 1
            Win.blit(Text, (0, 25*PacMan_Counter))"""
            pygame.draw.rect(Win, (229, 19, 19), Ghost.Rect, 2) # Drawing HitBoxes
            pygame.draw.rect(Win, (229, 19, 19), Ghost.Big_HitBox, 2) # Drawing Big HitBoxes
        pygame.draw.rect(Win, (229, 19, 19), PacMan.Rect, 2)
        pygame.draw.rect(Win, (34, 255, 0), Labyrinth.Rect, 2)
        for Outgoing_Object in Labyrinth.Outgoing_Objects_HitBox:
            pygame.draw.rect(Win, (229, 19, 19), Outgoing_Object, 2)
        for Piece in Labyrinth_Pieces:
            if Piece.Auto_HitBox:
                pygame.draw.rect(Win, (229, 19, 19), Piece.Rect, 2)

    if AllowAnimation: # Since we want a retro animation, we don't want to update animation at 60 FPS.
        PacMan_Phase = PacMan.Next_Phase() # Getting the next phase.
        Ghosts_Phases = []
        for Ghost in Ghosts:
            Ghosts_Phases.append(Ghost.Next_Phase()) # Getting the next phase.
    elif not AllowAnimation:
        PacMan_Phase = PacMan.Current_Phase # Not changing phase.
        Ghosts_Phases = []
        for Ghost in Ghosts:
            Ghosts_Phases.append(Ghost.Current_Phase) # Not changing phase.

    if not PacMan.isDead:
        if PacMan_Direction[0]: # If there's a direction we have to move the player.
            # Getting the corresponding surface depending on direction and last phase, and going to the new position.
            PacMan.Move(PacMan_Direction[1])
            Win.blit(PacMan.Get_Surface(PacMan_Phase, PacMan_Direction[1]), PacMan.Get_Position())

            for i in range(len(Ghosts_Directions)):
                Ghost = Ghosts[i]
                if Ghost.HoldDirection_Counter > 0:
                    Ghost_Direction = Ghost.Current_Direction
                    Ghost.HoldDirection_Counter -= 1
                else:
                    Ghost_Direction = Ghosts_Directions[i]

                Ghost_Phase = Ghosts_Phases[i]
                if Ghost_Direction:
                    Ghost.Move(Ghost_Direction)
                    if Ghost.isSpecial: # If Ghost is special, we show it with Special Skin. (Blue or White)
                        if Ghost.SpecialMode == 0:
                            Win.blit(Ghost.Get_Surface(Ghost_Phase, "SPECIAL_BLUE"), Ghost.Get_Position())
                        elif Ghost.SpecialMode == 1:
                            Win.blit(Ghost.Get_Surface(Ghost_Phase, "SPECIAL_WHITE"), Ghost.Get_Position())
                    else:
                        Win.blit(Ghost.Get_Surface(Ghost_Phase, Ghost_Direction), Ghost.Get_Position()) # Showing normal ghost.

        if PacMan_Direction[0] is None and PacMan_Direction[1] is None: # If there's no direction, we just draw Pac-Man and Ghost at phase 0. (It means the game didn't start)
            Win.blit(PacMan.Phases["UP"][0], PacMan.Get_Position())
            for Ghost in Ghosts:
                Win.blit(Ghost.Phases["UP"][0], Ghost.Get_Position())
        elif PacMan_Direction[0] is False: # If direction[0] is False, it means the Pac-Man is stopped by a wall.
            Win.blit(PacMan.Get_Surface(PacMan_Phase, PacMan_Direction[1]), PacMan.Get_Position())
            for i in range(len(Ghosts)):
                Ghost = Ghosts[i]
                if Ghost.HoldDirection_Counter > 0:
                    Ghost_Direction = Ghost.Current_Direction
                    Ghost.HoldDirection_Counter -= 1
                else:
                    Ghost_Direction = Ghosts_Directions[i]
                Ghost.Move(Ghost_Direction)
                Win.blit(Ghost.Get_Surface(Ghost.Current_Phase, Ghost_Direction), Ghost.Get_Position())
    elif PacMan.isDead:
        Text = GAME_OVER_FONT.render(f"Game Over", False, (186, 0, 0), (0, 0, 0))
        Win.blit(Text, (35, 300))
        pygame.display.update()
        time.sleep(3)

        INIT_GAME_VALUES()

INIT_GAME_VALUES()

while GAME_LOOP:
    if AutoMove_Timer is None or time.time() - AutoMove_Timer >= 1:
        for Ghost in Ghosts:
            i = Ghosts.index(Ghost) # Getting the ghost position.
            Ghost_Directions[i] = Ghost.Auto_Move() # Adding the current move direction to the old position.
        AutoMove_Timer = time.time()
    if Special_Phase_Timer:
        if time.time() - Special_Phase_Timer >= 10 and Ghosts[0].isSpecial: # If the special time ends, stop being special and turn time to 0 for the next use.
            for Ghost in Ghosts:
                Ghost.SpecialMode = 0
                Ghost.isSpecial = False
            Special_Phase_Timer = time.time()
        elif time.time() - Special_Phase_Timer >= 7 and AnimationChecker == ANIMATION_FRAME_RATE: # If we're reaching the last seconds of time, and its the frame to animate.
            for Ghost in Ghosts:
                Ghost.Next_Special() # Alternating the white and blue skin.

    if AnimationChecker == 0: # We are going to next frame every 150 iterations, more info at the end of the loop.
        Update_Screen(WIN, PacMan, Ghosts, True, PacMan_Direction, Ghost_Directions, Labyrinth)
    else:
        Update_Screen(WIN, PacMan, Ghosts, False, PacMan_Direction, Ghost_Directions, Labyrinth)

    for Event in pygame.event.get():
        if Event.type == pygame.KEYDOWN:
            if Event.key == K_ESCAPE:
                GAME_LOOP = False
                pygame.quit()
                sys.exit()
        if Event.type == pygame.QUIT:
            GAME_LOOP = False
            pygame.quit()
            sys.exit()
        elif Event.type == pygame.KEYDOWN: # Depending on the key pressed, we go to the direction.
            if Event.key == K_LEFT or Event.key == K_a:
                PacMan_Direction = (True, "LEFT")
            elif Event.key == K_RIGHT or Event.key == K_d:
                PacMan_Direction = (True, "RIGHT")
            elif Event.key == K_DOWN or Event.key == K_s:
                PacMan_Direction = (True, "DOWN")
            elif Event.key == K_UP or Event.key == K_w:
                PacMan_Direction = (True, "UP")
            elif Event.key == K_SPACE:
                for Ghost in Ghosts:
                    Ghost.isSpecial = True
                Special_Phase_Timer = time.time()
            elif Event.key == K_TAB:
                if DEV_MODE is True:
                    DEV_MODE = False
                elif DEV_MODE is False:
                    DEV_MODE = True

    if isTouchingEdges(Labyrinth, PacMan) or isTouching_NormalEdges(Labyrinth, PacMan):
        PacMan_Direction = (False, PacMan_Direction[1]) # Saving the last direction before the collision with the map edge, and adding False to the Tuple, to know that there's a collision.
        if PacMan_Direction[1] == "LEFT": # If the direction of the edge is Left, rotate 180 degrees and get a little bit away from wall (To avoid a touching wall loop).
            PacMan.Move("RIGHT", ExtraSpeed=3)
        elif PacMan_Direction[1] == "RIGHT":
            PacMan.Move("LEFT", ExtraSpeed=3)
        elif PacMan_Direction[1] == "UP":
            PacMan.Move("DOWN", ExtraSpeed=3)
        elif PacMan_Direction[1] == "DOWN":
            PacMan.Move("UP", ExtraSpeed=3)

    for i in range(len(Ghosts)):
        Ghost = Ghosts[i]
        if Objects_Collision(Ghost, PacMan):
            if not Ghost.isSpecial: # If the ghost is in normal mode, so it can kill player.
                PacMan.isDead = True
            elif Ghost.isSpecial: # If the ghost is special, is the PacMan who kills Ghost, so Ghost disapears.
                Ghost.x, Ghost.y = Ghost.Initial_X, Ghost.Initial_Y # Going back to initial position
                Ghost.isSpecial = False # Since the ghost has been killed, the ghost is in normal mode again.
                Ghost.isDead = True
        for Test_Collision_Ghost in Ghosts:
            if Ghost != Test_Collision_Ghost: # Avoiding to check collision with himself.
                if Objects_Collision(Ghost, Test_Collision_Ghost): # If there's a collision.
                    Oposite_Direction_1 = Test_Collision_Ghost.Get_Oposite_Direction(Test_Collision_Ghost.Current_Direction) # Getting the oposite direction of the 2 ghosts.
                    Oposite_Direction_2 = Ghost.Get_Oposite_Direction(Ghost.Current_Direction)
                    Test_Collision_Ghost.Forbidden_Direction = Oposite_Direction_1 # Adding the oposite as a forbidden direction for a time.
                    Ghost.Forbidden_Direction = Oposite_Direction_2
                    Test_Collision_Ghost.Move(Oposite_Direction_1, ExtraSpeed=5) # Moving on the oposite direction.
                    Test_Collision_Ghost.HoldDirection_Counter = 150  # Bounce with other ghost.
                    Ghost.Move(Oposite_Direction_2, ExtraSpeed=5) # Moving on the oposite direction.
                    Ghost.HoldDirection_Counter = 150 # Bounce with other ghost effect.
        Ghost_Direction = Ghost_Directions[i]
        Ghost.Forbidden_Direction = Ghost_Direction
        if isTouchingEdges(Labyrinth, Ghost) or isTouching_NormalEdges(Labyrinth, Ghost):
            if Ghost_Direction == "LEFT":
                Ghost.Move("RIGHT", ExtraSpeed=10)
                Ghost.HoldDirection_Counter = 100 # Bounce with wall effect.
            elif Ghost_Direction == "RIGHT":
                Ghost.Move("LEFT", ExtraSpeed=10)
                Ghost.HoldDirection_Counter = 100 # Bounce with wall effect.
            elif Ghost_Direction == "UP":
                Ghost.Move("DOWN", ExtraSpeed=10)
                Ghost.HoldDirection_Counter = 100 # Bounce with wall effect.
            elif Ghost_Direction == "DOWN":
                Ghost.Move("UP", ExtraSpeed=10)
                Ghost.HoldDirection_Counter = 100 # Bounce with wall effect.
            else:
                raise PacMan_Error(f"Ghost {Ghost.Colour} recieved an auto movement wrong direction, {Ghost_Direction}")

    if Objects_Collision(Labyrinth, PacMan): # Checking if the PacMan is on the teleport zone.
        PacMan.Teleport()

    for Ghost in Ghosts:
        if Objects_Collision(Labyrinth, Ghost): # Checking if the Ghost is on the teleport zone.
            Ghost.Teleport()

    if AnimationChecker == ANIMATION_FRAME_RATE:
        # If our variable is 150 we are going to restart it to 0, since at 150 we go to the next frame.
        AnimationChecker = 0
    else:
        AnimationChecker += 1

    pygame.display.update()