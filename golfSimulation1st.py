# -*- coding: utf-8 -*-
"""
Created on April 2 19:34:24 2014

@author: Griffin Tschurwald
"""

import pygame
from pygame.locals import *
import random
import math
import time

#in pygame, positive is right and down cuz apparently why not

#constants for the simulation
InitialBallSpeed = 120 #m/s
InitialBallAngle = 14 #degrees from horizontal
InitialBallSpeedx = math.cos(math.radians(InitialBallAngle))*InitialBallSpeed
InitialBallSpeedy = -math.sin(math.radians(InitialBallAngle))*InitialBallSpeed
wx = 0 #x wind velocity in m/s
wy = 0#-1 is needed because of directional switching
p = 1.2047 #kg/m^3
m = .0455 #kg
radius = .021 #meters
Cd = .4 #drag coefficient, should be about .4
Cl = .16 # lift coefficient should be around .17
g = 9.8 #m/s^2
Area = 3.1415*radius*radius
#This timestep will be the one to make calculations
timeStep = .01 #seconds
trailx = []
traily = []
#dragx = (-(Cd*.5*p*(self.vx-wx)**2*Area)/m)
#dragy = ((-self.vy/((vy**2)**.5))(Cd*.5*p*(self.vy-wy)**2*Area)/m)

#The model will calculate using the predefined timestep due to inconsistincies
#with pygame's timing features.' The actual simulation may not quite be real 
#time but it will be quite close

class GolfModel:
    """ Encodes the simulation state, determines what happens to  """
    def __init__(self):
        self.Ball = Ball((255,255,255),5,100,500,InitialBallSpeedx,\
        InitialBallSpeedy,0,0,0,0,0)

    def update(self):
        self.Ball.update()
        if -.01<model.Ball.timeCounter%.2<.01:#this appends x position every .2 seconds
            trailx.append(model.Ball.px)#the *2 is to make the path bigger on screen
            traily.append(model.Ball.py)
        
        if model.Ball.timeCounter>1 and model.Ball.py >= 500:#basically when ball reaches start height again
            model.Ball.grounded = 1#sets grounded to true

class Ball:
    """ Encodes the state of a ball in the simulation
    Units are seconds, meters, Newtons, and Kilograms
    """
    def __init__(self,color,radius,px,py,vx,vy,ax,ay,timeCounter,spin,grounded):
        self.color = color
        self.radius = radius
        self.px = px
        self.py = py
        self.vx = vx
        self.vy = vy
        self.ax = ax
        self.ay = ay
        self.timeCounter = timeCounter
        self.spin = spin
        self.grounded = grounded

    def update(self):
        if self.grounded == 0:
            self.px += self.vx*timeStep 
            self.py += self.vy*timeStep
            self.vx += self.ax*timeStep
            self.vy += self.ay*timeStep
            self.ax = (-(Cd*.5*p*(self.vx-wx)**2*Area)/m)#+\
            #(((self.vy)/math.fabs(self.vy))*(Cl*.5*p*(self.vy-wy)**2*Area)/m)
            self.ay = g + ((-(self.vy)/math.fabs(self.vy))*(Cd*.5*p*(self.vy-wy)**2*Area)/m)\
            +(-(Cl*.5*p*(self.vx-wx)**2*Area)/m)
            self.timeCounter += timeStep
        
        
        
        
          
class PyGameWindowView:
    """ A view of my model rendered in a Pygame window """
    def __init__(self,model,screen):
        self.model = model
        self.screen = screen
        self.font = pygame.font.SysFont('Arial', 15)
        
    def draw(self):
        self.screen.fill(pygame.Color(0,100,255))
        pygame.draw.circle(self.screen, self.model.Ball.color, (int(self.model.Ball.px), int(self.model.Ball.py)), self.model.Ball.radius)
        counter = 0
        while counter<len(trailx):
            pygame.draw.circle(self.screen, (0,255,0), (int(trailx[counter]), int(traily[counter])), 3)
            counter +=1
        #if model.Ball.grounded = 
        #this will draw the ground
        pygame.draw.rect(self.screen, (0,0,0), (20,500,760,10))
        #these will be text boxes drawn to measure key parameters
        self.screen.blit(self.font.render('Velocity (m/s)= ' + str(((self.model.Ball.vx)**2 + (self.model.Ball.vy)**2)**.5), True, (0,0,0)), (10, 100))
        self.screen.blit(self.font.render('Time Passed (s) = ' + str(self.model.Ball.timeCounter), True, (0,0,0)), (10, 120))
        self.screen.blit(self.font.render('Distance Traveled (m) = ' + str(self.model.Ball.px-100), True, (0,0,0)), (10, 140))
        self.screen.blit(self.font.render('Height (m) = ' + str(500-self.model.Ball.py), True, (0,0,0)), (10, 160))
        self.screen.blit(self.font.render('press space to send the ball flying!', True, (0,0,0)), (10, 180))
        pygame.display.update()

#class PyGameMouseController:
#    def __init__(self,model):
#        self.model = model
#    
#    def handle_mouse_event(self,event):
#        if event.type == MOUSEMOTION:
#            self.model.paddle.x = event.pos[0] - self.model.paddle.width/2.0

class PyGameKeyboardController:
    """ Handles keyboard input for brick breaker """
    def __init__(self,model):
        self.model = model
    
   
        

if __name__ == '__main__':
    pygame.init()
    
    size = (800,600)
    screen = pygame.display.set_mode(size)

    model = GolfModel()
    view = PyGameWindowView(model,screen)
    controller = PyGameKeyboardController(model)

  #  controller = PyGameKeyboardController(model)

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            #if event.type == KEYDOWN:
             #   controller.handle_keyboard_event(event)
            
           
        model.update()
        view.draw()
        pygame.time.delay(20)
        current_time = pygame.time.get_ticks()
  
       
        
    pygame.quit()
