import pygame
from utils import *
from debug import debug
import sys
from pathlib import Path
import time

class Editor:
    
    def __init__(self):

        self.screen_height = screen_height
        self.screen_width = screen_width

        
        self.textures = {}

        self.texturePointers = {}

        self.SetTextures()
        

        self.textureIndex = 0
        
        self.display_surface = pygame.display.get_surface()
        self.blocks = self.getBlocks()
        self.tileSize=20

        self.offset = pygame.math.Vector2()

        self.centralPosition = pygame.math.Vector2()
        self.centralPosition.x = 600
        self.centralPosition.y = 350

        self.cameraVector = pygame.math.Vector2()

        self.map = self.CreateMap()

        self.background = pygame.Rect(0,0,MAP_WIDTH*self.tileSize,MAP_HEIGHT*self.tileSize)
        
        
       

        
    def GetTextureNames(self):
        fileContents = os.listdir("{}textures".format(ROOT_DIR))

        
        

        def cutExtension(n: str):
            out = ""

            for i in n:
                if i == ".":
                    return out

                out += i
    
        fileContents = map(cutExtension, fileContents)
        return list(fileContents)


    def SetTextures(self):

        files = self.GetTextureNames()

        for file in files:
            self.textures[file] = pygame.image.load("{}textures/{}.png".format(ROOT_DIR,file)).convert_alpha()
        
        for index, file in enumerate(files):
            self.texturePointers[str(index)] = file



    def CreateMap(self):
        map = []
        for y in range(MAP_HEIGHT):
            map.append([])

        for yPos, y in enumerate(map):
            for x in range(MAP_WIDTH):
                map[yPos].append(0) 
        
        return map


    def run(self):
        while True:
            self.clearScreen()
            self.render()
            self.update()


    def changeOffset(self):

        key = pygame.key.get_pressed()

        self.cameraVector = pygame.math.Vector2(0,0)

        if key[pygame.K_w]:
            self.cameraVector.y = -2

        if key[pygame.K_s]:
            self.cameraVector.y = 2

        if key[pygame.K_a]:
            self.cameraVector.x = -2

        if key[pygame.K_d]:
            self.cameraVector.x = 2
        
        self.centralPosition += self.cameraVector

        self.offset.x = self.centralPosition.x - screen_width/2
        self.offset.y = self.centralPosition.y - screen_height/2


    def render(self):

        self.background = pygame.Rect((-self.offset.x, -self.offset.y),
                                      (MAP_WIDTH*self.tileSize,MAP_HEIGHT*self.tileSize))

        pygame.draw.rect(self.display_surface, (150,150,255), self.background)

        for y, row in enumerate(self.blocks):
            for x,column in enumerate(row):

                
                if column != "0":
                    self.display_surface.blit(self.textures[column],
                                            ((x*self.tileSize)-self.offset.x,
                                             (y*self.tileSize)-self.offset.y))
    

    def clearScreen(self):
        sqr=pygame.Rect((0,0),(self.screen_width,self.screen_height))
        pygame.draw.rect(self.display_surface,(0, 0, 0),sqr)


    def update(self):
        self.checkMouseEvents()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_e:
                    self.save()

                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

                elif event.key == pygame.K_q:
                    self.clear()

                elif event.key == pygame.K_c:
                    self.textureIndex += 1
                    self.textureIndex %= len(self.textures)

                elif event.key == pygame.K_x:
                    self.textureIndex -= 1
                    self.textureIndex %= len(self.textures)

        self.changeOffset()
        self.renderScripts()
        pygame.display.update()


    def getBlocks(self):
        out = []

        f = open("{}out.txt".format(ROOT_DIR),"r").read().splitlines()

        for l in f:
            n = l.split(",")
            n.pop(-1)
            out.append(n)
            
        return out

    def checkMouseEvents(self):
        key = pygame.mouse.get_pressed()

        if key[0]:
            x,y = pygame.mouse.get_pos()
           

            if int(y+self.offset.y)//20 >= len(self.map) or int(x+self.offset.x)//20 >= len(self.map[0]):
                return

            self.blocks[int(y+self.offset.y)//20][int(x+self.offset.x)//20] = self.texturePointers[str(self.textureIndex)]
            

    def save(self):
        f = open("{}out.txt".format(ROOT_DIR), "w")
        

        for row in self.blocks:
            for column in row:
                f.write(str(column))
                f.write(",")
            f.write("\n")

    def clear(self):
        print("a")
        

        for y in range(len(self.blocks)):
            for x in range(len(self.blocks[0])):
                self.blocks[y][x] = "0"

    def renderScripts(self):
        debug("press e to save", 10, 10)
        debug("press q to clear", 40, 10)
        debug("block: {}".format(self.texturePointers[str(self.textureIndex)]), 80, 10)
