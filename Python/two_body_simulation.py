import math
import time

import matplotlib.pyplot as plt
import numpy as np
from tkinter import *

# initialConditions
initial_eccentricity = 0.7
initial_q = 0.2


class BodyModel(object):
    def __init__(self, x, y, m):
        self.x = x
        self.y = y
        self.m = m

    def __str__(self):
        return "x: " + str(self.x) + " y: " + str(self.y) + " mass: " + str(self.m)
    
    def writeDataToTxtFile(self, Controller):
        with open('results.txt','a') as filehandle:
            
            filehandle.write('%s,' %Controller.body_one.x)
            filehandle.write('%s,' %Controller.body_one.y)
            filehandle.write('%s,' %Controller.body_two.x)
            filehandle.write('%s,' %Controller.body_two.y)
            filehandle.write('\n')
            
            filehandle.close()


class TwoBodyController(object):
    def __init__(self, eccentricity):
        self.eccentricity = eccentricity
        self.body_one = BodyModel(x=0, y=0, m=1)
        self.body_two = BodyModel(x=0, y=0, m=0)
        self.u = [0, 0, 0, 0]
        self.m1 = self.body_one.m
        self.m2 = self.body_two.m  # will be set to q
        self.q = 0  # current mass ratio m2/m1
        self.m12 = 0  # will be set to m1+m2

    def derivative(self):
        du = [None] * len(self.u)

        # x and y coordinates
        r = [self.u[0], self.u[1]]

        # distance between bodies
        rr = math.sqrt(math.pow(r[0], 2) + math.pow(r[1], 2))

        for i in range(2):
            du[i] = self.u[i + 2]
            du[i + 2] = -(1 + self.q) * r[i] / (math.pow(rr, 3))

        return du

    def runge_kutta_calculate(self, h):  # h: timestep u:variable
        a = [h / 2, h / 2, h, 0]
        b = [h / 6, h / 3, h / 3, h / 6]
        u0 = []
        ut = []
        dimension = len(self.u)

        for i in range(dimension):
            u0.append(self.u[i])
            ut.append(0)

        for j in range(4):
            du = self.derivative()

            for i in range(dimension):
                self.u[i] = u0[i] + a[j] * du[i]
                ut[i] = ut[i] + b[j] * du[i]

        for i in range(dimension):
            self.u[i] = u0[i] + ut[i]

    def update_position(self):
        timestep = 0.15
        self.runge_kutta_calculate(timestep)
        self.calculate_new_position()

    def calculate_new_position(self):
        r = 1
        a1 = (self.m2 / self.m12) * r
        a2 = (self.m1 / self.m12) * r

        self.body_one.x = -a2 * self.u[0]
        self.body_one.y = -a2 * self.u[1]

        self.body_two.x = a1 * self.u[0]
        self.body_two.y = a1 * self.u[1]

    def reset_state_to_initial_conditions(self):
        self.q = initial_q
        self.eccentricity = initial_eccentricity

        self.u[0] = 1
        self.u[1] = 0
        self.u[2] = 0
        self.u[3] = self.initial_velocity(self.q, self.eccentricity)

        self.m2 = self.q
        self.m12 = self.m1 + self.m2

    def initial_velocity(self, q, eccentricity):
        return math.sqrt((1 + q) * (1 + eccentricity))

controller = TwoBodyController(0.2)
controller.reset_state_to_initial_conditions()

bodyModel=BodyModel(0, 2, 1)

body_one_x = list()
body_one_y = list()
body_two_x = list()
body_two_y = list()

t = 0
T = 10000

for i in range(t, T):
    controller.update_position()
    bodyModel.writeDataToTxtFile(controller)
    body_one_x.append(controller.body_one.x)
    body_one_y.append(controller.body_one.y)
    body_two_x.append(controller.body_two.x)
    body_two_y.append(controller.body_two.y)
