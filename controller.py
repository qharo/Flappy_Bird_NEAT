#imports
import neat
from neat import genome
import pygame
import UI
import time
import ENV
import os
import math

def main():
    pygame.init()
    screen = pygame.display.set_mode((800,600))
    pygame.display.set_caption("Tetris!")
    ui = UI.UI(screen)
    env = ENV.ENV(ui)
    pausedScore = 0

    running = True
    clock = pygame.time.Clock()

    while running:
        clock.tick(30)

        eventList = pygame.event.get()


        for event in eventList:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if ui.playButton.rect.collidepoint(event.pos):
                    ui.play = True
                    ui.pause = False
                    ui.ai = False
                if ui.pauseButton.rect.collidepoint(event.pos):
                    ui.play = False
                    ui.pause = True
                    ui.ai = False
                if ui.aiButton.rect.collidepoint(event.pos):
                    ui.play = False
                    ui.pause = False
                    ui.ai = True
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and ui.play:
                    ui.bird.jump()
                elif event.key == pygame.K_c:
                    ui.play = True
                    ui.pause = False
                    ui.ai = False
                elif event.key == pygame.K_v:
                    ui.play = False
                    ui.pause = True
                    ui.ai = False
                elif event.key == pygame.K_b:
                    ui.play = False
                    ui.pause = False
                    ui.ai = True
        pipe_ind = 0
        if len(ui.pipes) > 1 and ui.bird.x > ui.pipes[0].x + ui.pipes[0].topImg.get_width():
            pipe_ind = 1

        if ui.ai: 
            topDist = math.sqrt((ui.bird.y - ui.pipes[pipe_ind].height)**2 + (ui.bird.x - ui.pipes[pipe_ind].x)**2)
            botDist = math.sqrt((ui.bird.y - ui.pipes[pipe_ind].bottom)**2 + (ui.bird.x - ui.pipes[pipe_ind].x)**2)
            node1 = math.tanh(botDist*-9.749626181433037 + topDist*7.421829737099346 + -1.5124999690945855)  
            node2 = math.tanh(-0.32225091056986166*ui.bird.y + -1.5139683158120754)
            #node3 = math.tanh(node1*0.9461879016848148 + -2.053755308044066)  
            node4 = math.tanh(node1*1.7817381083953472 + 0.825235157745086)
            value = math.tanh(node1 + node2 + node4)
            if value > 0.5:
                ui.bird.jump()             
            # if pygame.time.get_ticks() % 2 == 0:
            #         #     print('jumping')
            #     ui.bird.jump()
            # print("asdfasdfasdfas")
            #ui.bird.jump()
 

        if ui.collided:
            running = False

        pausedScore = ui.fscore
        if not ui.pause:
            ui.fscore = pausedScore
            ui.move()
        ui.update()
        pygame.display.update()

main()
# def run(conPath):
#     config = neat.config.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, conPath)
#     pop = neat.Population(config)
#     pop.add_reporter(neat.StdOutReporter(True))
#     pop.add_reporter(neat.StatisticsReporter())

#     winner = pop.run(main, 10)


# if __name__ == "__main__":
#     local_dir = os.path.dirname(__file__)
#     conPath = os.path.join(local_dir, "config-feedforward.txt")
    #run(conPath)