import pygame, random

#defino ancho
WIDTH = 800
#defino alto
HEIGHT = 600
BLACK = (0, 0, 0)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/background.png").convert()

def draw_text(surface, text, size, x,y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load("assets/player.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 10
        self.speed_x = 0

    def update(self):
        self.speed_x = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT]:
            self.speed_x = -5
        if keystate[pygame.K_RIGHT]:
            self.speed_x = 5
        self.rect.x += self.speed_x
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
        if self.rect.left < 0:
            self.rect.left = 0

    def shoot(self):
        bullet = Bullet(self.rect.centerx, self.rect.top)
        all_sprites.add(bullet)
        bullets.add(bullet)


class Meteor(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(meteor_images)
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(WIDTH -self.rect.width)
        self.rect.y = random.randrange(-100, -40)
        self.speedy = random.randrange(1,10)
        self.speedx = random.randrange(-5, 5)

    def update(self):
        self.rect.x += self.speedx
        self.rect.y += self.speedy
        if self.rect.top > HEIGHT + 10 or self.rect.left < -25 or self.rect.right > WIDTH +22:
            self.rect.x = random.randrange(WIDTH - self.rect.width)
            self.rect.y = random.randrange(-100,-40)
            self.speedy = random.randrange(1,8)

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.image.load("assets/laser1.png").convert()
        self.image.set_colorkey(BLACK)
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.centerx = x
        self.speedy = -10

    def update(self):
        self.rect.y += self.speedy
        if self.rect.bottom < 0:
            self.kill()

meteor_images = []
meteor_list = ["assets/meteorGrey_big1.png",
               "assets/meteorGrey_big2.png",
               "assets/meteorGrey_big3.png",
               "assets/meteorGrey_big4.png",
               "assets/meteorGrey_med1.png",
               "assets/meteorGrey_med2.png",
               "assets/meteorGrey_small1.png",
               "assets/meteorGrey_small2.png",
               "assets/meteorGrey_tiny1.png",
               "assets/meteorGrey_tiny2.png"]

for img in meteor_list:
    meteor_images.append(pygame.image.load(img).convert())

all_sprites = pygame.sprite.Group()
meteor_list = pygame.sprite.Group()
bullets = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

for i in range(8):
    meteor = Meteor()
    all_sprites.add(meteor)
    meteor_list.add(meteor)

running = True
score = 0
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.shoot()

    all_sprites.update()

    hits = pygame.sprite.groupcollide(meteor_list, bullets,True,True)
    for hit in hits:
        score += 1
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteor_list,False)
    if hits:
        #Si el running esta en False cuando chocan se termina el juego
        running = True

    #screen.fill(BLACK)
    screen.blit(background, [0,0])
    draw_text(screen,str(score),25, WIDTH // 2,10)
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()


