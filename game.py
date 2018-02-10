import sys
import sdl2
import sdl2.ext
import ctypes
from random import randint

WHITE=sdl2.ext.Color(255,255,255)
BLACK=sdl2.ext.Color(0,0,0)
RED=sdl2.ext.Color(255,0,0)
BLUE=sdl2.ext.Color(0,0,255)
LIGHT_RED=sdl2.ext.Color(255,128,128)
LIGHT_BLUE=sdl2.ext.Color(128,128,255)

class SoftwareRenderer(sdl2.ext.SoftwareSpriteRenderSystem):
    def __init__(self, window):
        super(SoftwareRenderer, self).__init__(window)

    def render(self, components):
        sdl2.ext.fill(self.surface, BLACK)
        super(SoftwareRenderer, self).render(components)

class Square(sdl2.ext.Entity):

    def __init__(self, world, sprite, posx=0, posy=0):
        self.sprite = sprite
        self.sprite.position = posx, posy

    def update(self, sprite):
        posx, posy = self.sprite.position
        self.sprite = sprite
        self.sprite.position = posx, posy

    def get_area(self):
        posx, posy = self.sprite.position
        return posx, posx+100, posy, posy+100

class SpriteFactory(sdl2.ext.SpriteFactory):
    def __init__(self):
        super(SpriteFactory,self).__init__(sdl2.ext.SOFTWARE)

    def get_sprite(self, color=WHITE, size=(100,100)):
        return self.from_color(color, size)

def run():
    sdl2.ext.init()
    window=sdl2.ext.Window("Pong", size=(320,320))
    window.show()

    world=sdl2.ext.World()
    spriterenderer=SoftwareRenderer(window)
    world.add_system(spriterenderer)

    factory=SpriteFactory()

    square_pos = [(5,5),(110,5),(215,5),(5,110),(110,110),(215,110),
            (5,215),(110,215),(215,215)]

    squares = []

    for (x,y) in square_pos:
        squares.append(Square(world,factory.get_sprite(),x,y))

    mouse_x = ctypes.c_int(0)
    mouse_y = ctypes.c_int(0)

    marks=[[None,None,None],
           [None,None,None],
           [None,None,None]]
    turn=randint(0,10)
    win=False
            
    running=True
    while running:
        events=sdl2.ext.get_events()
        for event in events:
            if event.type==sdl2.SDL_QUIT:
                running=False
                break
            if event.type==sdl2.SDL_MOUSEMOTION or event.type==sdl2.SDL_MOUSEBUTTONDOWN:
                sdl2.SDL_GetMouseState(ctypes.byref(mouse_x), ctypes.byref(mouse_y))
                #print(mouse_x, mouse_y)
                
                for idx, square in enumerate(squares):
                    x1, x2, y1, y2 = square.get_area()
                    if x1<=mouse_x.value<=x2 and y1<=mouse_y.value<=y2:
                        if not marks[idx/3][idx%3] and event.type==sdl2.SDL_MOUSEMOTION:
                            if turn%2==0:
                                square.update(factory.get_sprite(LIGHT_RED))
                            if turn%2==1:
                                square.update(factory.get_sprite(LIGHT_BLUE))
                        elif not marks[idx/3][idx%3] and event.type==sdl2.SDL_MOUSEBUTTONDOWN:
                            if turn%2==0:
                                square.update(factory.get_sprite(RED))
                                marks[idx/3][idx%3]=0
                                turn+=1
                                continue
                            if turn%2==1:
                                square.update(factory.get_sprite(BLUE))
                                marks[idx/3][idx%3]=1
                                turn+=1
                                continue
                    elif marks[idx/3][idx%3]==0:
                        square.update(factory.get_sprite(RED))
                    elif marks[idx/3][idx%3]==1:
                        square.update(factory.get_sprite(BLUE))
                    else:
                        square.update(factory.get_sprite(WHITE))
            for row in marks:
                if row.count(0)==3:
                    print "RED"
                    win=True
                if row.count(1)==3:
                    print "BLUE"
                    win=True
            for col in range(len(marks[0])):
                if [row[col] for row in marks].count(0)==3:
                    print "RED"
                    win=True
                if [row[col] for row in marks].count(1)==3:
                    print "BLUE"
                    win=True
            if [marks[i][i] for i in range(3)].count(0)==3:
                print "RED"
                win=True
            if [marks[i][i] for i in range(3)].count(1)==3:
                print "BLUE"
                win=True
            if [marks[i][abs(i-2)] for i in range(3)].count(0)==3:
                print "RED"
                win=True
            if [marks[i][abs(i-2)] for i in range(3)].count(1)==3:
                print "BLUE"
                win=True
            if sum(x is not None for x in [row[i] for row in marks for i in range(3)])==9 and not win:
                print "TIE"
                marks=[[None,None,None],
                       [None,None,None],
                       [None,None,None]]
                for square in squares:
                    square.update(factory.get_sprite(WHITE))
            if win:
                marks=[[None,None,None],
                       [None,None,None],
                       [None,None,None]]
                for square in squares:
                    square.update(factory.get_sprite(WHITE))
                win=False
        world.process()
    return 0

if __name__=="__main__":
    sys.exit(run())
