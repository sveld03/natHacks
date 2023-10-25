# Experiment Parameters
subject = "Steven";
n_trials = 1;
n_images = 10;
down_time = 1500;
flash_time = 500;
    
if __name__ == "__main__": 
    
    # Get File Name
    file_name = "";
    import os.path;
    for experiment_number in range(100):
        file_name = "trial_data/" + subject + "_" + str(experiment_number) + "_faces(" + str(n_trials) + "_trials)(" + str(n_images) + "_images)(" + str(down_time) + "_downTime)(" + str(flash_time) + "_flashTime).csv";
        if(not os.path.isfile(file_name)):
            break;
            
    import pygame, random, time
    import numpy as np
    import winsound
    import csv
    
    frequency = 2500  # Set Starting Frequency To 2500 Hertz
    beep_duration = 150; # ms

    # Define color shorthands
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((1920, 1080), pygame.FULLSCREEN)
    screen.fill(BLACK)

    # Track number of flashes
    n_flashed = 0

    # Create pseudo-randomized vector of image choices
    image_labels = np.repeat(np.arange(n_images), n_trials)
    np.random.shuffle(image_labels);
    
    # Random position variables
    randx = 0
    randy = 0
    randomizer = False

    # Font for writing text to screen
    pygame.font.init()
    my_font = pygame.font.SysFont('Comic Sans MS', 200)

    # Print 10sec countdown to screen
    for countdown in range(10):
        screen.fill(BLACK)
        text_surface = my_font.render(str(10-countdown), False, (255, 255, 255))
        screen.blit(text_surface, (300,100))
        pygame.display.update()
        winsound.Beep(700, 150)
        time.sleep(.85)

    # Re-init black screen
    screen.fill(BLACK)
    text_surface = my_font.render("prog", False, (255, 255, 255))
    screen.blit(text_surface, (300,100))
    pygame.display.update()
    winsound.Beep(1300, 100)

    # Start timer
    init_time = time.time()
    
    # Loop through all trials
    while n_flashed < n_trials*n_images:
        
        # Check if it is time for next flash
        if (time.time() - init_time) >= down_time/1000.0:
            
            # Randomize a new position if one is needed
            if not randomizer:
                randx = np.random.randint(0, 750)
                randy = np.random.randint(0, 350)
                
            # Get image id for this trial
            image_id = image_labels[n_flashed]

            #TODO: flash the appropriate image
            pygame.draw.circle(screen, YELLOW, (250+randx,250+randy), 200)
                
            # Note that a new position has already been randomized for this flash
            if not randomizer:
                frequency = np.random.randint(440, 5000)
                winsound.Beep(frequency, beep_duration)
                randomizer = True

            pygame.display.update()
            if (time.time() - init_time) >= (down_time+flash_time)/1000.0:
                screen.fill(BLACK)
                pygame.display.update()
                init_time = time.time()
                n_flashed += 1
                randomizer = False
                                
    with open(file_name, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        # write the data
        writer.writerows([image_labels])