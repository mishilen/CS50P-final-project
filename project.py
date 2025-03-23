import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import pygame
from random import randint, choice
import os


class Player(pygame.sprite.Sprite):
    def __init__(self, player_images:list, player_jump, duck_image, duck_rect, jump_sound, slide_sound):
        super().__init__()
        self.walk = player_images
        self.jump = player_jump
        self.duck = duck_image
        self.duck_rect = duck_rect
        self.index = 0
        self.image = self.walk[self.index]
        self.rect = self.image.get_rect(midbottom=(200, 405))
        self.gravity = 0
        self.is_duck = False
        self.jump_sound = jump_sound
        self.jump_channel = pygame.mixer.Channel(1)
        self.jump_sound.set_volume(0.7)
        self.slide_sound = slide_sound
        self.slide = pygame.mixer.Channel(2)

    def actions(self) -> None:
        key = pygame.key.get_pressed()
        if ACTIVE:
            if (
                key[pygame.K_SPACE] or key[pygame.K_w] or key[pygame.K_UP]
            ) and self.rect.bottom == 405:
                self.gravity = -16
                self.jump_channel.play(self.jump_sound)

            if (key[pygame.K_s] or key[pygame.K_DOWN]) and self.rect.bottom == 405:
                self.is_duck = True
                self.animate(self.is_duck)
            else:
                self.is_duck = False
                self.animate(self.is_duck)

    def player_gravity(self) -> None:
        self.gravity += 0.9
        self.rect.y += self.gravity
        if self.rect.bottom >= 405:
            self.rect.bottom = 405

    def animate(self, bool:bool) -> None:
        if self.rect.bottom < 405:
            self.image = self.jump
        elif bool:
            self.slide.play(self.slide_sound, loops=0)
            self.image = self.duck
            self.rect = self.duck_rect
        else:
            self.index += 0.3
            if int(self.index) >= len(self.walk):
                self.index = 0
            self.image = self.walk[int(self.index)]
            self.rect = self.image.get_rect(midbottom=(200, 405))

    def update(self):
        self.actions()
        self.player_gravity()
        self.animate(self.is_duck)


class Obstacles(pygame.sprite.Sprite):
    def __init__(self, enemy):
        super().__init__()
        self.score = 0
        if enemy == "fly":
            fly1 = pygame.image.load(os.path.join("images","enemies/flyFly1.png")).convert_alpha()
            fly2 = pygame.image.load(os.path.join("images","enemies/flyFly2.png")).convert_alpha()
            self.enemy = [fly1, fly2]
            y = 320
        elif enemy == "snail":
            snail1 = pygame.image.load(os.path.join("images","enemies/snailWalk1.png")).convert_alpha()
            snail2 = pygame.image.load(os.path.join("images","enemies/snailWalk2.png")).convert_alpha()
            self.enemy = [snail1, snail2]
            y = 403
        else:
            fish1 = pygame.image.load(os.path.join("images","enemies/fishSwim1.png" )).convert_alpha()
            fish2 = pygame.image.load(os.path.join("images","enemies/fishSwim2.png")).convert_alpha()
            self.enemy = [fish1, fish2]
            y = 385

        self.index = 0
        self.image = self.enemy[self.index]
        self.rect = self.image.get_rect(midbottom=(randint(900, 1100), y))

    def animate(self):
        self.index += 0.1
        if int(self.index) >= len(self.enemy):
            self.index = 0
        self.image = self.enemy[int(self.index)]

    def update(self):
        self.animate()
        self.rect.x -= 8
        if self.rect.x <= -10:
            self.kill()
            global score
            score += 1


pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((800, 500))
clock = pygame.time.Clock()
pygame.display.set_caption("Pixel Run")
icon_surf = pygame.image.load(os.path.join("images","player/p3_icon.png"))
pygame.display.set_icon(icon_surf)
ACTIVE: bool = False
start: bool = True
score: int = 0
high_score :int = 0
new_high_score: bool = False
# backgrounds
sky_surf = pygame.image.load(os.path.join("images","bg/bg_grasslands.png")).convert()
sky = pygame.transform.scale(sky_surf, (1000, 500))
ground_surf = pygame.image.load(os.path.join("images","bg/Ground.png")).convert()
pygame.mixer.music.load(os.path.join("sound","Level_1.wav"))
pygame.mixer.music.set_volume(0.2)
width: int = 0


def main() -> None:
    global ACTIVE, score, start, high_score, new_high_score
    player = pygame.sprite.GroupSingle()
    player.add(get_player())
    enemy = pygame.sprite.Group()
    spawn_time: int = 1600
    timer = pygame.USEREVENT + 1
    pygame.time.set_timer(timer, spawn_time)

    run: bool = True
    pygame.mixer.music.play(-1)

    while run:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                run = False
                break

            if ACTIVE:
                if score > 0 and score % 10 == 0 and spawn_time > 700:
                    spawn_time -= 30
                    pygame.time.set_timer(timer, spawn_time)
                if event.type == timer:
                    enemy.add(Obstacles(choice(["fly", "snail", "snail", "snail", "fish", "fish"])))

            else:
                if event.type == pygame.KEYDOWN:
                    ACTIVE = True
                    score = 0
                    spawn_time = 1400
                    start = False

        if ACTIVE:
            pygame.mixer.music.set_volume(0.2)
            screen.fill((0, 0, 0))
            background()
            player.draw(screen)
            player.update()
            enemy.draw(screen)
            enemy.update()
            ACTIVE = collide(player.sprite, enemy)
            score_screen()
        else:
            if score > high_score:
                new_high_score = True
                high_score = get_high_score(score)
            elif high_score > score:
                new_high_score = False

            pygame.mixer.music.set_volume(0)
            game_screen()
        pygame.display.update()
        clock.tick(60)
    pygame.quit()


def get_player() -> any:
    player_images = [pygame.image.load(os.path.join("images", f"player/p3_walk0{i}.png")).convert_alpha() for i in [3, 4, 5, 7, 5, 4]]
    player_jump = pygame.image.load(os.path.join("images", "player/p3_jump.png"))
    duck_image = pygame.image.load(os.path.join("images", "player/p3_duck.png")).convert_alpha()
    duck_rect = duck_image.get_rect(midbottom = (200, 403))
    jump_sound = pygame.mixer.Sound(os.path.join("sound", "audio_jump.mp3"))
    slide_sound = pygame.mixer.Sound(os.path.join("sound", "plip_ducking.wav"))
    return (Player(player_images, player_jump, duck_image, duck_rect, jump_sound, slide_sound))


def score_screen() -> None:
    font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 60)
    bar = font.render(f"Score: {score}", None, ("#675668"))
    screen.blit(bar, bar.get_rect(topleft=(30, 40)))


def game_screen() -> None:
    global my_font
    screen.fill("pink")
    if start:
        stand = pygame.image.load(os.path.join("images","player/p3_front.png")).convert_alpha()
        my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 80)
        display_text = my_font.render(f"Pixel Run", False, ("#675668"))
        my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 70)
        instruction = my_font.render(f"Press any key to run", False, ("#675668"))
        screen.blit(instruction, instruction.get_rect(center=(405, 400)))
    else:
        stand = pygame.image.load(os.path.join("images","player/p3_front_sad.png")).convert_alpha()
        my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 77)
        display_text_bg = my_font.render(f"Game Over", False, ("#BB6ADF"))
        display_text_bg.set_alpha(50)
        my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 75)
        display_text = my_font.render(f"Game Over", False, ("#675668"))
        my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 70)
        score_display = my_font.render(f"Score: {score} ", False, ("#675668"))
        if new_high_score == True and high_score > 0:
            my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 71)
            high_score_bg = my_font.render(f"New high score: {high_score}", False, ("#BB6ADF"))
            high_score_bg.set_alpha(50)
            my_font = pygame.font.Font(os.path.join("font","Pixeltype.ttf"), 70)
            high_score_display = my_font.render(f"New high score: {high_score}", False, ("#675668"))
            screen.blit(high_score_bg, high_score_display.get_rect(center = (395, 430)))
            screen.blit(high_score_display, high_score_display.get_rect(center = (400, 430)))
            screen.blit(score_display, score_display.get_rect(center=(405, 370)))
        elif high_score > 0 and not new_high_score:
            high_score_display = my_font.render(f"High score: {high_score}", False, ("#675668"))
            screen.blit(high_score_display, high_score_display.get_rect(center = (400, 430)))
            screen.blit(score_display, score_display.get_rect(center=(405, 370)))
        else:
            screen.blit(score_display, score_display.get_rect(center=(405, 390)))
        screen.blit(display_text_bg, display_text_bg.get_rect(center=(410, 100)))

    screen.blit(display_text, display_text.get_rect(center=(410, 100)))
    stand = pygame.transform.scale2x(stand)
    screen.blit(stand, stand.get_rect(center=(400, 240)))


def get_high_score(num) -> int:
    highscore = 0
    if num > highscore:
        highscore = num
    return highscore


def collide(player, enemy) -> bool:
    global ACTIVE
    if pygame.sprite.spritecollide(player, enemy, False):
        bump_sound = pygame.mixer.Sound(os.path.join("sound", "gameover.wav"))
        bump_sound.play()
        enemy.empty()
        return False
    return True


def background() -> None:
    global width
    screen.blit(sky, (width, 0))
    screen.blit(sky, (1000 + width, 0))
    screen.blit(ground_surf, (width, 400))
    screen.blit(ground_surf, (1000 + width, 400))

    if width == -1000:
        screen.blit(sky, (1000 + width, 0))
        screen.blit(ground_surf, (1000 + width, 400))
        width = 0
    width -= 2


if __name__ == "__main__":
    main()
