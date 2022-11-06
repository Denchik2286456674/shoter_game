
# підключення бібліотек
from pygame import *

# клас-батько
class GameSprite(sprite.Sprite):
    def __init__(self, player_image, p_x, p_y, p_speed,width,height):
        super().__init__()
        self.image = transform.scale(image.load(player_image),(width,height))
        self.speed = p_speed
        self.rect = self.image.get_rect()
        self.rect.x = p_x
        self.rect.y = p_y
    def reset(self):
        window.blit(self.image, (self.rect.x , self.rect.y))
# клас для ракеток
class Player(GameSprite):
    def update_right(self):
        keys = key.get_pressed()
        if [K_UP] and self.rect.y > 5:
            self.rect.y -= self.speed
        if [K_DOWN] and self.rect.y < 420:
            self.rect.y += self.speed
    def update_left(self):
        keys = key.get_pressed()
        if [K_w] and self.rect.y > 5:
            self.rect.y -= self.speed
        if [K_s] and self.rect.y < 420:
            self.rect.y += self.speed
racket_right = Player("racket_r.png", 520, 200, 4, 50, 150)
racket_left = Player("racket_l.png", 30, 200, 4, 50, 150)
ball = GameSprite("ball.png", 200, 200, 4, 50, 50)
win_width = 600  # window width
win_height = 500 # window height

window = display.set_mode((win_width, win_height)) # встановити ширину і висоту вікна
fon = (200, 255, 255) # колір для фону гри
window.fill(fon)      # залити фон певним кольором

# прапорці, які відповідають за стан гри
game = True
finish = False

clock = time.Clock() # годинник 
FPS = 60 #кількість кадрів в секунду
speed_x = 3
speed_y = 3
# ігровий цикл
while game:
    for e in event.get():  # перевірка всіх подій
        if e.type == QUIT: # тип подій - закрити вікно
            game = False   # закінчуємо цикл while
    if finish != True:
        window.fill(fon)
        racket_right.update_right()
        racket_left.update_left()
        ball.rect.x += speed_x
        ball.rect.y += speed_y
        if ball.rect.y > win_height-50 or ball.rect.y < 0:
            speed_y *= -1
        
        racket_right.reset()
        racket_left.reset()
        ball.reset()
    display.update()
    clock.tick(FPS)
