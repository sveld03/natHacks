# -*- coding: utf-8 -*-
"""
Created on Sat Nov 18 23:49:32 2023

@author: sandr
"""

import time
from PIL import Image
import pygame
import sys
import os


pygame.init()

# Set up the display
info = pygame.display.Info()
width, height = info.current_w, info.current_h # display dimensions info
screen = pygame.display.set_mode((width, height)) # creates screen variable
pygame.display.set_caption("Clue: The BCI Expansion")

# Set up fonts and text
font = pygame.font.SysFont("Arial", 50)

fps_cap = 30;


pygame.init()
screen = pygame.display.set_mode((1920, 1080)) # change to the real resolution
pygame.display.set_caption("Clue: The BCI Expansion")

target = pygame.image.load("images\image_target_sm.png")
title_image= pygame.image.load("images/title_card.png")

        
num_key_frames_murder = 30
murder_frames = [None]*num_key_frames_murder;
murder_frame_ind = 0;
with Image.open('images/murder.gif') as im:
    for i in range(num_key_frames_murder):
        im.seek(im.n_frames // num_key_frames_murder * i)
        murder_frames[i] = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert()
        
num_key_frames_envelope = 66
envelope_frames = [None]*num_key_frames_envelope;
envelope_frame_ind = 0;
with Image.open('images/envelope.gif') as im:
    for i in range(num_key_frames_envelope):
        im.seek(im.n_frames // num_key_frames_envelope * i)
        envelope_frames[i] = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert()
        
num_key_frames_maid = 84
maid_frames = [None]*num_key_frames_maid;
maid_frame_ind = 0;
with Image.open('images/maid.gif') as im:
    for i in range(num_key_frames_maid):
        im.seek(im.n_frames // num_key_frames_maid * i)
        maid_frames[i] = pygame.image.fromstring(im.tobytes(), im.size, im.mode).convert()


# Main game loop

running = True;
last_frame_time = time.time();
screen_index = 0

while running:
    
    while(time.time()-last_frame_time < 1/fps_cap):
        continue;
    
    for event in pygame.event.get(): # iterates over all events in event queue
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            screen_index += 1
            if(screen_index==7):
                running = False

    screen.fill((255, 255, 255))

    if screen_index == 0:
        screen.blit(title_image, (660,240))

        # Draw text
        text = font.render("Click to continue", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height *0.95-100 ))
        screen.blit(text, text_rect)

    elif screen_index == 1:

        # draw maid gif
        screen.blit(maid_frames[maid_frame_ind], (660,240))
        maid_frame_ind += 1;
        if(maid_frame_ind>=num_key_frames_maid):
            maid_frame_ind=0;

        # Draw text
        a=200;
        text = font.render("You are a lowly maid serving Lord Dawson in his manor.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+a))
        screen.blit(text, text_rect)
        text = font.render("And you are ready to move on up in the world.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+55+a))
        screen.blit(text, text_rect)
        
    elif screen_index == 2:

        # Draw text
        text = font.render("You and an accomplice decide to murder", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        text = font.render("him at an upcoming dinner party.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2+55))
        screen.blit(text, text_rect)
        text = font.render("You will open the gun safe and your accomplice will shoot him.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2+150))
        screen.blit(text, text_rect)

    elif screen_index == 3:

        # draw letter gif
        screen.blit(envelope_frames[envelope_frame_ind], (660,240))
        envelope_frame_ind += 1;
        if(envelope_frame_ind>=num_key_frames_envelope):
            envelope_frame_ind=0;
        
        # Draw text
        a=180
        text = font.render("Choose ONE of the provided images.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+a))
        screen.blit(text, text_rect)
        text = font.render("This is your accomplice.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+55+a))
        screen.blit(text, text_rect)
        text = font.render("Study their face for the next few minutes.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+110+a))
        screen.blit(text, text_rect)
        
    elif screen_index == 4:

        # draw death gif
        screen.blit(murder_frames[murder_frame_ind], (660,240))
        murder_frame_ind += 1;
        if(murder_frame_ind>=num_key_frames_murder):
            murder_frame_ind=0;
        
        # Draw text
        a=180;
        text = font.render("Your accomplice manages to fatally shoot Lord Dawson.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+a))
        screen.blit(text, text_rect)
        text=font.render("However, you are immediately implicated as you were the only", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+55+a))
        screen.blit(text, text_rect)
        text=font.render("person that night who knew the code to the gun safe.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+110+a))
        screen.blit(text, text_rect)

    elif screen_index == 5:
        
        a=20;
        text = font.render("You are now in police custody.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)
        text = font.render("A new BCI interrogation technique will determine", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 + 55+a))
        screen.blit(text, text_rect)
        text = font.render("which of the dinner guests you recognize, ", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 +110+a))
        screen.blit(text, text_rect)
        text = font.render("thus implicating your accomplice", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 2 +165+a))
        screen.blit(text, text_rect)
       
       
    elif screen_index == 6:

        target_rect = (660,240)
        screen.blit(target, target_rect)

        a=180;
        text = font.render("The calibration phase is about to begin.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+a))
        screen.blit(text, text_rect)
        text = font.render("Study this face and press ENTER when you see it during calibration.", True, (0, 0, 0))
        text_rect = text.get_rect(center=(width // 2, height // 1.5+55+a))
        screen.blit(text, text_rect)
      


    # Update the display
    pygame.display.flip()
    last_frame_time = time.time()

# Quit Pygame
pygame.quit()




from P3TE_GUI_suspect_irrelevant import Begin_Experiment
Begin_Experiment();