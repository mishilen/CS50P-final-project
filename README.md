# PIXEL RUN
#### Video Demo:  <https://youtu.be/cEkcAvKYvqQ>
## **Description**:
This is an infinite runner game where the speed of enemies spawning increases after every 10 points scored.\
There are 3 types of enemies; fish, fly, and snail. With fly spawning the least, and snail spawning the most.\
Player can only jump over the fish and snail, and has to duck/slide to dodge the fly.\
The high score starts being displayed once the player has scored at least 1 point,\
and gets refreshed only when the game is closed.\
The game starts when the player presses any key on their keyboard.\
A point is scored every time the player successfully dodges the enemy.\
The player can use the following keys for movement:
```W, Up arrow, and Space to jump```,
```S and Down arrow to duck```

## **Installation Guide:**
1. Download the .zip file of the code
2. Extract the .zip file and open it in VS code
3. In the terminal, paste the following code:
```
pyinstaller project.py --onefile -w
```
4. Go in the extracted folder, two folders named **dist** and **build** would've been created.
5. ```CTRL + X``` on the **build** folder and paste it in the **dist** folder.
6. Go back in the extracted folder, copy **font**, **images**, and **sound** folder,\
then paste them in the **dist** folder.
7. Click on the .exe file to start playing.


## **Packages:**
**PYGAME:** Used for displaying actions in a separate window, specifically used for programming interactive games,\
and displaying graphics and sounds. The whole game is made using the pygame module, which is responsible for displaying images,\
fetching user input, making changes, displaying sound, and much more.

**RANDOM:** Used for generating a random enemy, with higher probability of the snail, and least probability of the fly.

## **Requirements:**
The requirements for this program have been included in "requirements.txt" which you can install using command:
```
pip install -r requirements.txt
```
## **Functionality:**
The program contains 2 classes, 8 methods, and 7 functions.

### **Player class:**
The player class creates a blueprint for our player, animating its steps, jumps, and ducks.\
It is responsible for all actions done by the player. It checks for what key the player has pressed, and performs actions as suitable.\
The player can only jump or duck when the player avatar is on the ground.

### **Obstacles class:**
Makes, animates, and deletes enemies. Gets a random enemy from the **main()** function and displays it on the screen.\
Deleting any enemy once it has passed a certain number of pixels out of screen.

### **main:**
Displays images on screen, gets user input, terminates the program on user input, and responsible for all execution.\
It's responsible for calling all other function, as well as keeping the game loop ongoing.

### **get_player():**
Loads all the images and sounds for the player, calls the Player class with all required parameter and returns it.

### **score_screen():**
Displays the ongoing score on the top left corner as the game progresses. The number is updated with every enemy successfully dodged.

### **game_screen():**
Checks for 2 conditions, whether the game has started or not. At start, it displays a start screen,\
and once the game has started after every game over, it displays the score of the last game,\
as well as the high score if the player has scored more than 0 points during the entire runtime.

### **get_high_score():**
Stores the highest points scored by player in a variable named "highscore"(if score is greater than 0),\
and returns its value.

### **collision():**
Takes in 2 parameters, the current position of the player and enemy, and checks for collision between the two.

### **background():**
Loops the background so that the sky and ground can look animated.

## **License:**
The images and audio files used within the game are from the following references:

[Designed by macrovector / Freepik](http://www.freepik.com/)\
[Platformer graphics (Deluxe) by Kenney Vleugels](www.kenney.nl)\
[SFX by Cleyton Kauffman](https://soundcloud.com/cleytonkauffman)
