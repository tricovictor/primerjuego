import pygame, random

#defino ancho
WIDTH = 800
#defino alto
HEIGHT = 600
BLACK = (0, 0, 0)
x = 0
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
background = pygame.image.load("assets/background.png").convert()

def uploadBackground():
    # Fondo en movimiento
    global x
    x_relativa = x % background.get_rect().width
    screen.blit(background, (x_relativa - background.get_rect().width, 0))
    if x_relativa < WIDTH:
        screen.blit(background, (x_relativa, 0))
    x += 5

def draw_text(surface, text, size, x,y):
    font = pygame.font.SysFont("serif", size)
    text_surface = font.render(text,True,(255,255,255))
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x,y)
    surface.blit(text_surface, text_rect)

#Función para mostrar Game Over
def show_go_screen():
    screen.blit(background, [0, 0])                                      #dejo la pantalla con el fondo
    draw_text(screen, "DISPAROS", 65, WIDTH // 2, HEIGHT / 4)
    draw_text(screen, "(Gracias por jugar)", 27, WIDTH // 2, HEIGHT // 2)
    draw_text(screen, "Presione tecla para salir", 17, WIDTH // 2, HEIGHT * 2/3)
    draw_text(screen, "Puntaje total", 22, WIDTH // 2,  450)
    draw_text(screen, str(score), 30, WIDTH // 2, 500)

    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.KEYUP:         #pregunto si una tecla se ha soltado
                waiting = False


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

class Explosion(pygame.sprite.Sprite):
    def __init__(self, center):
        super().__init__()
        self.image = explosion_anim[0]
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.frame = 0
        self.last_update = pygame.time.get_ticks()
        self.frame_rate = 50
    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update > self.frame_rate:
            self.last_update = now
            self.frame += 1
            if self.frame == len(explosion_anim):
                self.kill()
            else:
                center = self.rect.center
                self.image = explosion_anim[self.frame]
                self.rect = self.image.get_rect()
                self.rect.center = center

explosion_anim = []
for i in range(9):
    file = "assets/regularExplosion0{}.png".format(i)
    img = pygame.image.load(file).convert()
    img.set_colorkey(BLACK)
    img_scale = pygame.transform.scale(img,(70,70))
    explosion_anim.append(img_scale)

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

game_over = False
running = True
score = 0
while running:
    if game_over:  # mover la logica del juego para dentro de game over
        running = False
        show_go_screen()  # creo esta pantalla

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

        explosion = Explosion(hit.rect.center)
        all_sprites.add(explosion)
        meteor = Meteor()
        all_sprites.add(meteor)
        meteor_list.add(meteor)

    hits = pygame.sprite.spritecollide(player, meteor_list,False)
    if hits:
        #Si el running esta en False cuando chocan se termina el juego
        #running = True
        game_over = True

    #screen.fill(BLACK)
    screen.blit(background, [0,0])
    draw_text(screen,str(score),25, WIDTH // 2,10)
    uploadBackground()
    all_sprites.draw(screen)
    pygame.display.flip()
pygame.quit()


