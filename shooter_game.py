from pygame import  *
from random import randint 
win_width = 700
win_height = 500


image_background = "galaxy.jpg"
image_rocket = "rocket.png"

font.init()
font1 = font.SysFont("Arial", 80)
font2 = font.SysFont("Arial", 40)
win = font1.render("You win!",True,(0,0,0))
lose = font1.render("You loser!", True,(0,0,0))

score = 0
dead = 10
lost = 0
max_lost = 3
life = 3

class GameSprite(sprite.Sprite):
    def __init__(self, player_image, player_x, player_y, size_x, size_y,  player_speed):
        super().__init__()
        self.image = transform.scale(image.load(player_image), (size_x, size_y))
        self.speed  = player_speed
        self.rect = self.image.get_rect()
        self.rect.x = player_x
        self.rect.y = player_y
    def reset(self):
        window.blit(self.image, (self.rect.x, self.rect.y))
class Player(GameSprite):
    def update(self):
       keys =  key.get_pressed()
       if keys[K_LEFT] and self.rect.x > 5:
           self.rect.x -= self.speed
       if keys[K_RIGHT] and self.rect.x < 620:
           self.rect.x += self.speed
    def fire (self):
        bullet = Bullet("bullet.png", self.rect.centerx, self.rect.top, 15, 20, -15)
        bullets.add(bullet)

class Enemy(GameSprite):
    def update(self):
        self.rect.y += self.speed
        global lost
        if self.rect.y > 500:
            self.rect.x = randint (80, 620)
            self.rect.y = 0
            lost += 1
class Bullet(GameSprite):
    def update(self):
        self.rect.y += self.speed
        if self.rect.y < 0:
            self.kill()

        


window = display.set_mode((win_width, win_height))
display.set_caption("Real Life")
background = transform.scale(image.load("galaxy.jpg"), (win_width, win_height))


mixer.init()
#mixer.music.load("space.ogg")
#mixer.music.play()

fire_sound = mixer.Sound("fire.ogg")

ship = Player(image_rocket, 5, 400, 80, 100, 10)
monsters = sprite.Group()
bullets = sprite.Group()
asteroids = sprite.Group()

for i in range(1, 3):
    asteroid = Enemy("asteroid.png", randint(80, 620), -40, 50, 50, randint(1, 3))
    asteroids.add(asteroid)
for i in range(1, 6):
    monster = Enemy("ufo.png", randint(80, 620),-40, 80, 50, randint(1, 5))
    monsters.add(monster)


game = True
clock = time.Clock()
finish = False
rel_time = False
num_fire = 0
from time import time as timer
while game:
    for e in event.get():
        if e.type == QUIT:
            game = False
        elif e.type == KEYDOWN:
            if e.key == K_SPACE:   
                if num_fire < 5 and rel_time == False:
                    num_fire += 1
                    fire_sound.play()
                    ship.fire()
                if num_fire >= 5 and rel_time == False:
                    rel_time = True 
                    last_time = timer() 
    if not finish:
        window.blit(background, (0, 0))
        ship.update()
        asteroids.update()
        bullets.update()
        monsters.update()
        ship.reset()
        monsters.draw(window)
        asteroids.draw(window)
        bullets.draw(window)

        if rel_time == True:
            now_time = timer()
            if now_time - last_time < 3:
                pass
            else:
                num_fire = 0 
                rel_time = False
        colides = sprite.groupcollide(monsters,bullets,True, True)
        for a in colides:
            score += 1
            monster = Enemy("ufo.png", randint(80, 620),-40, 80, 50, randint(1, 5))
            monsters.add(monster)
        if sprite.spritecollide(ship, monsters, False) or sprite.spritecollide(ship, asteroids, False):
            sprite.spritecollide(ship, monsters, True) 
            sprite.spritecollide(ship, asteroids, True)
            life = life -1 
        if life == 0 or lost >= max_lost:
            finish = True
            window.blit(lose, (200, 200))  
        if score >= dead:
            window.blit(win, (200, 200))
            finish = True
        if life == 3:
            color_life = (0, 150, 0)
        if life == 2:
            color_life = (100, 50, 0)
        if life == 1:
            color_life = (150, 0, 0)
        text_life = font1.render(str(life), 1, color_life )
        window.blit(text_life, (650, 10))
        display.update()
    time.delay(50)
