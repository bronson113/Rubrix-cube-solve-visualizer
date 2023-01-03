import copy
import re
import os
import time

COLOR = "wgrbcy"  # up: white, left: red, front: blue, right: orange, back: green, down: yellow
FACE = "ulfrbd"
OPPOSITE = "drblfu"
COLORED = {' ':'   ','   ':'   ','w':'\x1b[47m w \x1b[m','g':'\x1b[42m g \x1b[m','r':'\x1b[41m r \x1b[m','b':'\x1b[44m b \x1b[m','c':'\x1b[46m o \x1b[m','y':'\x1b[43m y \x1b[m'}
class Rubix_solver():
    def __init__(self, order):
        self.order = order
        global COLOR
        self.face = [[j for i in range(order**2)]for j in range(6)]
        #s = "abcdefghijklmnopqrstuvwx"
        #self.face = [[j for j in s[i:i+4]] for i in range(0,24,4)]
        self.tmp = [[' ' for i in range(order*4+3)]for j in range(order*3)]
        self.updated = False

    def map_face_to_tmp(self):
        for i in range(self.order**2):
            self.tmp[i//self.order][self.order+(i%self.order)+1]=self.face[0][i]                       #up
            self.tmp[self.order + i//self.order][i%self.order]=self.face[1][i]                         #left
            self.tmp[self.order + i//self.order][self.order+(i%self.order)+1]=self.face[2][i]          #front
            self.tmp[self.order + i//self.order][2 * self.order+(i%self.order)+2]=self.face[3][i]      #right
            self.tmp[self.order + i//self.order][3 * self.order+(i%self.order)+3]=self.face[4][i]      #back
            self.tmp[self.order*2 + i//self.order][self.order+(i%self.order)+1]=self.face[5][i]        #down
        for i,k in enumerate(self.tmp):
            for j,c in enumerate(k):
                self.tmp[i][j] = COLORED[c]

    def turn(self, side='u', layer=1, count=1):
        self.updated = True
        #print(side,layer,count)
        faces = []
        orient = []
        rev = False
        if side == 'u' or side == 'd':
            if side == 'd':
                k = self.order - layer
                count = 4-count
                rev = True
            else:
                k = layer-1
            faces = [1,2,3,4]
            orient = [2,2,2,2]
        elif side =='r' or side =='l':
            if side == 'r':
                k = self.order - layer
            else:
                k = layer-1
                count = 4-count
                rev = True
            faces = [0,2,5,4]
            orient = [1,1,1,-3]
        elif side =='f' or side =='b':
            if side == 'b':
                k = self.order - layer
                count = 4-count
            else: k = layer-1
            faces = [0,1,5,3]
            orient = [-4,-1,2,-5]
        origin = copy.deepcopy(self.face)
        for i in range(self.order):
            indexs = [0,0,0,0]
            for j in range(4):
                if orient[j]==2:  indexs[j] = i + k*self.order                                          #horizontal top-down
                if orient[j]==1:  indexs[j] = i*self.order + k                                          #vertical left-right
                if orient[j]==-1: indexs[j] = i*self.order + (self.order - (k+1) )                      #vertical right-left
                if orient[j]==-2: indexs[j] = i + (self.order - (k+1))*self.order                       #horizontal down-top
                if orient[j]==-3: indexs[j] = (self.order - (i+1))*self.order + (self.order - (k+1) )   #vertical right-left rev
                if orient[j]==-4: indexs[j] = (self.order - (i+1)) + (self.order - (k+1))*self.order    #horizontal down-top rev
                if orient[j]==-5: indexs[j] = (self.order - (i+1))*self.order + k                       #vertical left-right
            #print(indexs,k,faces)
            for j in range(4):
                #print(self.face[ faces[j] ][ indexs[j] ] , origin[ faces[(j+count)%4] ][ indexs[(j+count)%4] ])
                self.face[ faces[j] ][ indexs[j] ] = origin[ faces[(j+count)%4] ][ indexs[(j+count)%4] ]
        if rev: count = 4-count
        if layer == 1:
            for times in range(count):
                tozip = [self.face[ FACE.index(side) ][i:i+self.order] for i in range(0,self.order**2,self.order)][::-1]
                self.face[ FACE.index(side) ] = list(zip(*tozip))
                tmp=[]
                for i in self.face[ FACE.index(side) ]: tmp+=i
                self.face[ FACE.index(side) ] = tmp

        if layer == self.order:
            for times in range(count):
                tozip = [self.face[ OPPOSITE.index(side) ][i:i+self.order] for i in range(0,self.order**2,self.order)][::-1]
                self.face[ OPPOSITE.index(side) ] = list(zip(*tozip))
                tmp=[]
                for i in self.face[ OPPOSITE.index(side) ]: tmp+=i
                self.face[ OPPOSITE.index(side) ] = tmp

        #self.map_face_to_tmp()
        return True

    def alg_parser(self, alg):
        alg = ''.join([c for c in alg if c not in "()"])
        for step in alg.lower().split(' '):
            print(self)
            #print(step)
            try:    t = re.search('[uflrbdm]',step).group(0)
            except: continue
            mod = step.split(t)
            if mod[0]=='':mod[0]=1
            if mod[1]=='\'':mod[1]=3
            if mod[1]=='':mod[1]=1
            if t=='m':
                t = 'r'
                mod[0]+=1
            self.turn(t,int(mod[0]),int(mod[1]))
            print(self)
            clear = lambda : os.system('clear')
            pause = input()
            clear()


    def __str__(self):
        if self.updated:
            self.updated = False
            self.map_face_to_tmp()

        return '\n'.join([''.join(list(self.tmp[i])) for i in range(self.order*3)])+'\n'+'-'*30


def main():
    alg = input('your alg:')
    my_rubix = Rubix_solver(3)
    my_rubix.map_face_to_tmp()
    my_rubix.alg_parser(alg)
    print(my_rubix)
    print("[+] simulation finished")
if __name__=='__main__':
    main()
