from class_file import *
from numbers import Number
from re import S
from time import sleep
from turtle import position
import pygame
import random
import winsound
import math
from pygame import font, mixer
import sys
import time
import threading
from queue import PriorityQueue
from random import choice
from pygame.locals import *
from class_file import*
def DFS_findPath(grid_cells, start, end, cols, rows):
    stack = [(start, [start])]
    path = []
    while stack:
        (vertex, trace) = stack.pop()
        if vertex == end:
            path = trace
            break  
        if vertex.passed == False:
            vertex.passed = True
            neighbors = vertex.check_neighbors_pass(grid_cells, cols, rows) #check the available directions (wall or not)
            for neighbor in neighbors:
                if not neighbor.passed:
                    stack.append((neighbor, trace + [neighbor]))
    for i in range (len(grid_cells)):
        grid_cells[i].passed = False
    return path

def BFS_findPath(grid_cells, start, end, cols, rows):
    queue = [start]
    start.passed = True
    trace = {start: -1}
    while queue: 
        vertex = queue[0]
        queue.pop(0)
        if vertex == end:
            break
        neighbors = vertex.check_neighbors_pass(grid_cells, cols, rows)
        for neighbor in neighbors:
            if not neighbor.passed:
                queue.append(neighbor)
                trace[neighbor] = vertex
                neighbor.passed = True
    for i in range(len(grid_cells)):
        grid_cells[i].passed = False
    u = end
    path = []
    path.append(u)
    u = trace[u]
    while u != -1:
        path.append(u)
        u = trace[u]
    return path[::-1]
def dis_to_goal(cell1, cell2):
    x1,y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)


def AStar_findPath(grid_cells, start, end, cols, rows):
    cor_start = (start.x, start.y)
    cor_end = (end.x, end.y)
    g_score = {cell: float('inf') for cell in grid_cells}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in grid_cells}
    f_score[start] = dis_to_goal(cor_start, cor_end)

    
    trace = {start: -1}

    find_index = lambda x, y: x + y * cols
    res = PriorityQueue()
    res.put((dis_to_goal(cor_start, cor_end), dis_to_goal(cor_start, cor_end), (start.x, start.y)))
    while not res.empty():
        vertex_cor = res.get()[2]
        vertex = grid_cells[find_index(vertex_cor[0], vertex_cor[1])]
        if vertex == cor_end:
            break
        neighbors = vertex.check_neighbors_pass(grid_cells, cols, rows)
        for neighbor in neighbors:
            cor_neighbor = (neighbor.x, neighbor.y)
            temp_g_score = g_score[vertex] + 1
            temp_f_score = temp_g_score + dis_to_goal(cor_neighbor, cor_end)
            if temp_f_score < f_score[neighbor]:
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = temp_f_score
                res.put((f_score[neighbor], dis_to_goal(cor_neighbor,cor_end), cor_neighbor))
                trace[neighbor] = vertex

    u = end
    path = []
    path.append(u)
    u = trace[u]
    while u != -1:
        path.append(u)
        u = trace[u]
    return path[::-1]
def DFS_spread(grid_cells, start, cols, rows):
    stack = [start]
    path = []
    while stack:
        vertex = stack.pop()
        if not vertex.passed:
            path.append(vertex)
            vertex.passed = True
            neighbors = vertex.check_neighbors_pass(grid_cells, cols, rows)
            for neighbor in neighbors:
                if not neighbor.passed:
                    stack.append(neighbor)
    for i in range (len(grid_cells)):
        grid_cells[i].passed = False
    return path     






def euclid_distance(cell1, cell2):
    return (cell1.x - cell2.x)**2 + (cell1.y - cell2.y)**2

def select_start_end(grid_cells, cols, rows):
    random_start = random.choice(grid_cells)
    path = DFS_spread(grid_cells, random_start, cols, rows)
    rad = (cols**2 + rows**2)/ 4
    list_end = [vertex for vertex in path if euclid_distance(vertex, random_start) >= rad]
    random_end = random.choice(list_end)
    return (random_start, random_end)