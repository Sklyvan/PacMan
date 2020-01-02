import pygame
from PacMan_Exceptions import PacMan_Error
import random
import time

class PacMan_Player:
    def __init__(self, Initial_X, Initial_Y, Speed, Size):
        """
        Loading the images files, and creating one array for every possible direction, with the 3 phases.
        """
        # Initial x,y position and speed.
        self.x = Initial_X
        self.y = Initial_Y
        self.Speed = Speed
        self.Size = Size
        self.isDead = False
        self.Current_Phase = 0 # Using that to know the current phase, so we can know what's the next phase.
        self.Current_Direction = None
        self.Phases = {"RIGHT": None, "LEFT": None, "UP": None, "DOWN": None}
        self.Locations = [] # Array to save all the x,y coordinates of the player.
        PATH = "./Sprites/Characters/PacMan-"
        for Phase in self.Phases:
            # Going to every direction, and depending on the direction, rotating the image the needed degrees.
            Current_Phases = [] # For every direction, that contains the 3 phases.
            if Phase == "RIGHT":
                for i in range (3):
                    Current_Path = str(PATH) + str(i) + str(".png") # Getting the image path.
                    Current_Phases.append(pygame.transform.scale(pygame.image.load(Current_Path), (Size, Size)))
                self.Phases[Phase] = Current_Phases
            if Phase == "LEFT":
                for i in range(3):
                    Current_Path = str(PATH) + str(i) + str(".png")
                    toRotate = (pygame.transform.scale(pygame.image.load(Current_Path), (Size, Size)))
                    Current_Phases.append(pygame.transform.rotate(toRotate, 180))
                self.Phases[Phase] = Current_Phases
            if Phase == "UP":
                for i in range(3):
                    Current_Path = str(PATH) + str(i) + str(".png")
                    toRotate = (pygame.transform.scale(pygame.image.load(Current_Path), (Size, Size)))
                    Current_Phases.append(pygame.transform.rotate(toRotate, 90))
                self.Phases[Phase] = Current_Phases
            if Phase == "DOWN":
                for i in range(3):
                    Current_Path = str(PATH) + str(i) + str(".png")
                    toRotate = (pygame.transform.scale(pygame.image.load(Current_Path), (Size, Size)))
                    Current_Phases.append(pygame.transform.rotate(toRotate, -90))
                self.Phases[Phase] = Current_Phases
        self.image = self.Phases["UP"][0].convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)

    def Move(self, Direction, ExtraSpeed=0):
        """Changing the position on screen of the object."""
        self.Current_Direction = Direction
        if Direction == "LEFT":
            self.x -= (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new pacman location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
        elif Direction == "RIGHT":
            self.x += (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new pacman location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
        elif Direction == "UP":
            self.y -= (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new pacman location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
        elif Direction == "DOWN":
            self.y += (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new pacman location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
        else:
            raise PacMan_Error(f"{Direction} isn't an avalaible Pac-Man direction.")

    def Next_Phase(self):
        # Going to the next phase.
        if self.Current_Phase == 0:
            self.Current_Phase = 1
            return 1
        elif self.Current_Phase == 1:
            self.Current_Phase = 2
            return 2
        elif self.Current_Phase == 2:
            self.Current_Phase = 0
            return 0
        else:
            raise PacMan_Error(f"Phase should be 0, 1 or 2, not {self.Current_Phase}")

    def Get_Position(self):
        return self.x, self.y

    def Teleport(self):
        if self.x >= 785: # If is on the right, go to left.
            self.x = 0
            self.Current_Direction = "LEFT"
        elif self.x <= 0: # If is on the letf, go to right.
            self.x = 785
            self.Current_Direction  = "RIGHT"

        return self.x, self.Current_Direction

    def Get_Surface(self, Type, Direction):
        # Knowing the phase number and out direction, returning the corresponding image as a surface.
        self.image = self.Phases[Direction][Type].convert_alpha() # Saving the current surface for collide effects.
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        return self.image

class Ghost_Enemy:
    def __init__(self, Initial_X, Initial_Y, Speed, Colour, Size, Start_Direction, Big_HitBox_Size):
        PATH = "./Sprites/Characters/" + str(Colour) + str("-Ghost-") # Creating image path, depending on the colour.
        EYES_PATH = "./Sprites/Characters/Eyes-"
        SPECIAL_PATH = "./Sprites/Characters/Special-Ghost-"
        self.Big_HitBox_Size = Big_HitBox_Size
        self.Forbidden_Direction = None # When the Ghost touches an edge, we avoid to go to that direction again.
        self.HoldDirection_Counter = 0 # Using that to continue going to the same direction when touching an edge.
        self.Current_Phase = 0
        self.Current_Direction = Start_Direction
        self.Phases = {"RIGHT": None, "LEFT": None, "UP": None, "DOWN": None}
        self.Eyes = {"RIGHT": None, "LEFT": None, "UP": None, "DOWN": None} # Just eyes images, using it when the ghost is killed.
        self.Locations = []  # Array to save all the x,y coordinates of the player.
        self.isSpecial = False # Using that to know when we have to change the image to blue/white.
        self.SpecialMode = 0
        self.Time = None
        for Eye in self.Eyes: # Adding the eyes images to the dictionary.
            Current_Path = str(EYES_PATH) + str(Eye) + str(".png")
            Eye_Image = pygame.transform.scale(pygame.image.load(Current_Path), (Size, Size))
            self.Eyes[Eye] = Eye_Image
        for Phase in self.Phases:
            Current_Path = PATH + str(Phase)
            Current_Phases = []
            for i in range(1, 2+1):
                try:
                    Current_Phases.append(pygame.transform.scale(pygame.image.load(Current_Path+str("-")+str(i)+str(".png")), (Size, Size)))
                except pygame.error:
                    raise PacMan_Error(f"Can't open image file, {Colour} not avaliable.")
            self.Phases[Phase] = Current_Phases
        self.Phases["SPECIAL_BLUE"] = [pygame.transform.scale(pygame.image.load(str(SPECIAL_PATH) + str("Blue-1.png")), (Size, Size)), pygame.transform.scale(pygame.image.load(str(SPECIAL_PATH) + str("Blue-2.png")), (Size, Size))]
        self.Phases["SPECIAL_WHITE"] = [pygame.transform.scale(pygame.image.load(str(SPECIAL_PATH) + str("White-1.png")), (Size, Size)), pygame.transform.scale(pygame.image.load(str(SPECIAL_PATH) + str("White-2.png")), (Size, Size))]
        self.x = Initial_X
        self.y = Initial_Y
        self.Initial_X = Initial_X
        self.Initial_Y = Initial_Y
        self.Speed = Speed
        self.Colour = Colour
        self.Size = Size
        self.isDead = False
        self.image = self.Phases["UP"][0].convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
        self.Big_HitBox = pygame.Rect(self.x - self.Big_HitBox_Size/2, self.y - self.Big_HitBox_Size/2, self.Size + self.Big_HitBox_Size, self.Size + self.Big_HitBox_Size)

    def Move(self, Direction, ExtraSpeed=0):
        """Changing the position on screen of the object."""
        self.Current_Direction = Direction
        if Direction == "LEFT":
            self.x -= (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new ghost location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
            self.Big_HitBox = pygame.Rect(self.x - self.Big_HitBox_Size/2, self.y - self.Big_HitBox_Size/2, self.Size + self.Big_HitBox_Size, self.Size + self.Big_HitBox_Size)
        elif Direction == "RIGHT":
            self.x += (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new ghost location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
            self.Big_HitBox = pygame.Rect(self.x - self.Big_HitBox_Size/2, self.y - self.Big_HitBox_Size/2, self.Size + self.Big_HitBox_Size, self.Size + self.Big_HitBox_Size)
        elif Direction == "UP":
            self.y -= (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new ghost location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
            self.Big_HitBox = pygame.Rect(self.x - self.Big_HitBox_Size/2, self.y - self.Big_HitBox_Size/2, self.Size + self.Big_HitBox_Size, self.Size + self.Big_HitBox_Size)
        elif Direction == "DOWN":
            self.y += (self.Speed + ExtraSpeed)
            self.Locations.append((self.x, self.y)) # Adding the new ghost location to the Locations Array.
            self.Rect = pygame.Rect(self.x, self.y, self.Size, self.Size)
            self.Big_HitBox = pygame.Rect(self.x - self.Big_HitBox_Size/2, self.y - self.Big_HitBox_Size/2, self.Size + self.Big_HitBox_Size, self.Size + self.Big_HitBox_Size)
        else:
            raise PacMan_Error(f"{Direction} isn't an avalaible Ghost direction.")

    def Get_Oposite_Direction(self, Direction):
        if Direction == "LEFT":
            return "RIGHT"
        if Direction == "RIGHT":
            return "LEFT"
        if Direction == "UP":
            return "DOWN"
        if Direction == "DOWN":
            return "UP"
        else:
            raise PacMan_Error(f"{Direction} isn't an avaliable direction.")

    def Auto_Move(self):
        Directions = ["LEFT", "RIGHT", "UP", "DOWN"]
        if self.Forbidden_Direction is not None:
            Directions.remove(self.Forbidden_Direction)
        Direction = random.choice(Directions)
        return Direction

    def Next_Phase(self):
        if self.Current_Phase == 0:
            self.Current_Phase = 1
            return 1
        elif self.Current_Phase == 1:
            self.Current_Phase = 0
            return 0
        else:
            raise PacMan_Error(f"Ghost phase should be 0 or 1, not {self.Current_Phase}")

    def Next_Special(self):
        if self.SpecialMode == 0:
            self.SpecialMode = 1
            return 1
        elif self.SpecialMode == 1:
            self.SpecialMode = 0
            return 0

    def Get_Position(self):
        return self.x, self.y

    def Teleport(self):
        if self.x >= 785:
            self.x = 0
            Direction = "LEFT"
        elif self.x <= 0:
            self.x = 785
            Direction = "RIGHT"

    def Get_Surface(self, Type, Direction):
        self.image = self.Phases[Direction][Type].convert_alpha() # Saving the current surface for collide effects.
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        return self.image

    def Start_Timer(self):
        self.Time = time.time()