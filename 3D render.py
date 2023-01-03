#! /usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, math, itertools, re
import pygame as pg
from random import randint
from rubix_solver import Rubix_solver


W, BLACK, R, BLUE, G = (255,255,255), (0,0,0), (255,0,0), (0,0,255), (0,255,0)
CLEAR = (255,255,255,0)
Y, C, M, O, LB = (255,255,0), (0,255,255), (255,0,255), (255,128,0), (135,206,250)
Color_list = [W, BLACK, R, BLUE, G, Y, C, M, O, LB]
Face_color = [W, G, R, BLUE, O, Y]


def to2D(p, rz=False):
    ox,oy,oz = p

    oz+=0

    ox-=camx; oy-=camy; oz-=camz

    x, oz = ox*math.cos(roth) - oz*math.sin(roth), ox*math.sin(roth) + oz*math.cos(roth)
    y, z = oy*math.cos(rotv) - oz*math.sin(rotv), oy*math.sin(rotv) + oz*math.cos(rotv)

    if z<0: return None

    if abs(z)<=min_z: z = min_z

    f=(min(_W,_H)*(_fov/2*math.pi))/z
    if rz: return (int(cx + x*f),int(cy + y*f),x**2+y**2+z**2)
    else: return (int(cx + x*f),int(cy + y*f))

class cube():

    def __init__(self, rel):
        self.struct = [(1,1,1),(1,1,-1),(1,-1,-1),(1,-1,1),(-1,1,1),(-1,1,-1),(-1,-1,-1),(-1,-1,1)]
        self.points = self.calc_ps(rel)
        self.vert = [(0,1),(1,2),(2,3),(0,3),(4,5),(5,6),(6,7),(4,7),(0,4),(1,5),(2,6),(3,7)]
        self.face = [(0,1,2,3),(4,5,6,7),(0,1,5,4),(2,3,7,6),(0,4,7,3),(1,5,6,2)] #R, L, D, U, B, F
        self.colors = [C]*6 #[G, BLUE, W, Y, O, R]

    def calc_ps(self, rel):
        return [(i+rel[0],j+rel[1],k+rel[2]) for (i,j,k) in self.struct]

    def draw(self, screen):
        todraw = []
        for c,p in zip(self.colors, self.face):
            ps = [i for i in [to2D(self.points[_],True) for _ in p] if i!=None ]
            _ =sum([i[2] for i in ps])
            dots = [i[:2] for i in ps]
            if len(ps)>2:
                todraw.append((_,c,dots))

        return todraw

    def change_color(self, face, c):
        self.colors[face] = c

class Rubix(Rubix_solver):

    def __init__(self):
        super().__init__(3)
        self.cubes = [cube((i,j,k)) for i,j,k in itertools.product(range(-2,4,2),range(-2,4,2),range(-2,4,2))]
        self.map_face_to_cube()
        self.updated = False

    def map_face_to_cube(self):
        for i in range(3):
            for j in range(3):
                #map bottom/top:
                self.cubes[(2-j)+i*9].change_color(3,Face_color[self.face[0][i+j*3]])
                self.cubes[6+(j)+(i)*9].change_color(2,Face_color[self.face[5][i+j*3]]) #top
                #map left/right:
                self.cubes[(2-i)+(j)*3].change_color(1,Face_color[self.face[1][i+j*3]]) #left
                self.cubes[18+i+(j)*3].change_color(0,Face_color[self.face[3][i+j*3]])

                #map front/back:
                self.cubes[(j)*3+i*9].change_color(5,Face_color[self.face[2][i+j*3]])
                self.cubes[(j)*3+(2-i)*9+2].change_color(4,Face_color[self.face[4][i+j*3]]) #back
                #self.cubes[]

    def draw(self, screen):
        if self.updated:
            self.updated=False
            self.map_face_to_cube()

        todraw=[]
        for i in self.cubes:
            todraw+= i.draw(screen)
        return todraw

def alg_parser(rubix, alg):
    alg = ''.join([c for c in alg if c not in "()"])
    for step in alg.lower().split(' '):
        #print(self)
        print(step)
        try:    t = re.search('[uflrbdm]',step).group(0)
        except: continue
        mod = step.split(t)
        if mod[0]=='':mod[0]=1
        if mod[1]=='\'':mod[1]=3
        if mod[1]=='':mod[1]=1
        if t=='m':
            t = 'r'
            mod[0]+=1
        yield rubix.turn(t,mod[0],int(mod[1]))

def main():


    global _W,_H,cx,cy,camx,camy,camz,rotv,roth,_fov,min_z
    _W, _H = 800,600
    cx, cy = _W//2, _H//2
    camx, camy, camz = -20,0,0
    min_z = 0.1
    _fov = 0.25*math.pi
    rotv, roth = 0,0 # math.PI ~ -math.PI

    pg.init()
    pg.event.get(); pg.mouse.get_rel(); pg.event.set_grab(1); pg.mouse.set_visible(0);
    screen  = pg.display.set_mode((_W, _H))
    fpslock = pg.time.Clock()

    pg.font.init()
    myfont = pg.font.SysFont('Times',20)

    #cubes = [cube((i,j,k)) for i,j,k in itertools.product(range(-2,4,2),range(-2,4,2),range(-2,4,2))]
    rubix = Rubix()
    algo_to_do = iter(alg_parser(rubix, "B D F' B' D L2 U L U' B D' R B R D' R L' F U2 D"))

    while True:
        dt = fpslock.tick()/100.0
        pg.display.set_caption("Rubix Solver - FPS: {}".format(fpslock.get_fps()))
        for event in pg.event.get():
            if event.type == pg.QUIT: pg.quit();sys.exit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_ESCAPE: pg.quit();sys.exit()
                if event.key == pg.K_RETURN:
                    try: next(algo_to_do)
                    except: pass
            if event.type == pg.MOUSEMOTION:
                x,y = event.rel;
                x/=200; y/=200
                rotv+=y; roth+=x
                rotv%=2*math.pi
                roth%=2*math.pi

        keys = pg.key.get_pressed()
        if keys[pg.K_w]: camx += dt*math.sin(roth); camz += dt*math.cos(roth)
        if keys[pg.K_s]: camx -= dt*math.sin(roth); camz -= dt*math.cos(roth)
        if keys[pg.K_a]: camx -= dt*math.cos(roth); camz += dt*math.sin(roth)
        if keys[pg.K_d]: camx += dt*math.cos(roth); camz -= dt*math.sin(roth)
        if keys[pg.K_SPACE]:  camy -= dt*1
        if keys[pg.K_LSHIFT]: camy += dt*1

        #cubes[randint(0,len(cubes)-1)].change_color(randint(0,5),Color_list[randint(2,len(Color_list)-1)])


        screen.fill(LB)

        faces = []
        #for i in cubes: faces+=i.draw(screen)
        faces+=rubix.draw(screen)
#        for a,b in vert:
#            pg.draw.line(screen, R, to2D(points[a]), to2D(points[b]))
#
#        for _ in points:
#            pg.draw.circle(screen, W, to2D(_) , 1, 0)

        #print(faces)

        todraw = sorted(faces,reverse=1)

        for _,c,ps in todraw:
            pg.draw.polygon(screen, c, ps)
            pg.draw.polygon(screen, BLACK, ps, 3)


        text_drawn = myfont.render('{}, {}, {}'.format(*list(map(int,(camx,camy, camz)))), False, BLACK)
        screen.blit(text_drawn,(0,0))

        pg.display.flip()



if __name__ == '__main__':
    main()
