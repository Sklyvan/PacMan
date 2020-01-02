import pygame
from PacMan_Exceptions import PacMan_Error
from Circular_Linked_List import Circular_LinkedList

class Labyrinth_Piece:
    def __init__(self, Type, x, y, Rotate=None, Horitzontal_Flip=None, Vertical_Flip=None, Auto_HitBox=True):
        self.x = x
        self.y = y
        self.Auto_HitBox = Auto_HitBox
        IMAGE_PATH = str("./Sprites/Labyrinth/Labyrinth-") + str(Type) + str(".png")
        if not Rotate:
            self.image = pygame.image.load(IMAGE_PATH).convert_alpha()
        elif Rotate:
            self.image = pygame.transform.rotate(pygame.image.load(IMAGE_PATH).convert_alpha(), Rotate)
        if Horitzontal_Flip:
            self.image = pygame.transform.flip(self.image, True, False)
        if Vertical_Flip:
            self.image = pygame.transform.flip(self.image, False, True)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.Size = self.rect.size
        self.Rect = pygame.Rect(self.x, self.y, self.Size[0], self.Size[1])

    def Get_Position(self):
        return self.x, self.y

class Labyrinth_Map:
    def __init__(self):
        self.image = pygame.image.load("./Sprites/Labyrinth/Labyrinth-Base.png").convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.Rect = pygame.Rect(0, 0, 816, 800)
        self.Outgoing_Objects_HitBox = [pygame.Rect(388, 0, 41, 120), pygame.Rect(0, 245, 162, 104), pygame.Rect(0, 400, 162, 104), pygame.Rect(654, 245, 162, 104),
                                        pygame.Rect(654, 400, 162, 104), pygame.Rect(0, 628, 75, 34), pygame.Rect(742, 628, 75, 34), pygame.Rect(16, 16, 785, 1), pygame.Rect(16, 785, 785, 1),
                                        pygame.Rect(16, 16, 1, 240), pygame.Rect(16, 504, 1, 300), pygame.Rect(800, 16, 1, 240), pygame.Rect(801, 504, 1, 300)]
        self.Pieces = []

    def Get_Rect_Coordinates(self):
        x = 816 - self.rect.center[0]
        y = 800 - self.rect.center[1]
        return x,y

class Portal:
    def __init__(self, Color):
        PATH = str("./Sprites/Portals/") + str(Color) + str("_Portal_")
        self.Portals = Circular_LinkedList()
        for i in range (1, 10):
            PORTAL_PATH = str(PATH) + str(i) + str(".png")
            self.Portals.Add(pygame.image.load(PORTAL_PATH).convert_alpha())

        self.Current_Frame = self.Portals.Initial
        self.Image = self.Current_Frame.Data

    def Get_Frame(self):
        Frame = self.Current_Frame.Data
        self.Image = Frame
        self.Current_Frame = self.Current_Frame.Next
        return Frame