from pygame import *
from random import choice, randint

window = display.set_mode((700,500))
display.set_caption('Snake')

class Game_sprite(sprite.Sprite):
    def __init__(self, img, x,y, w,h):
        super().__init__()
        self.image = transform.scale(image.load(img),(w,h))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
    def reset(self):
        window.blit(self.image,(self.rect.x, self.rect.y))

class Snake(Game_sprite):
    def __init__(self, img, x,y, w,h,t):
        super().__init__( img, x,y, w,h)
        # 0-голова 1 - тело 2-попа 
        self.type = t
        self.speed = 25
        self.direction = "0"
        self.cur_image = self.image
        self.wait = 15 
    def update(self):
        if self.direction == 'l':
            self.rect.x-=self.speed
        elif self.direction == 'r':
            self.rect.x+=self.speed
        elif self.direction == 'u':
            self.rect.y-=self.speed
        elif self.direction == 'd':
            self.rect.y+=self.speed
            
    def get_direction(self): 
        keys = key.get_pressed()
        if keys[K_UP] and self.direction != 'd':
            self.direction = 'u'
            self.image = transform.rotate(self.cur_image,0)
        elif keys[K_DOWN] and self.direction != 'u':
            self.direction = 'd'
            self.image = transform.rotate(self.cur_image, 180)
        elif keys[K_LEFT] and self.direction != 'r':
            self.direction = 'l'
            self.image = transform.rotate(self.cur_image, 90)
        elif keys[K_RIGHT] and self.direction != 'l':
            self.direction = 'r'
            self.image = transform.rotate(self.cur_image, -90)
    def set_direct(self):
        if self.direction == 'd':
            self.image = transform.rotate(self.cur_image,180)
        elif self.direction == 'u':
            self.image = transform.rotate(self.cur_image, 0)
        elif self.direction == 'r':
            self.image = transform.rotate(self.cur_image, -90)
        elif self.direction == 'l':
            self.image = transform.rotate(self.cur_image, 90)


    def eat(self,food):
        global speed
        speed+=1
        food.position()

class Food(Game_sprite):
    def __init__(self,imgs,x,y,w,h):
        super().__init__(imgs[0],x,y,w,h)
        self.costumes = []
        self.costumes.append(self.image)
        for i in range(len(imgs)-1):
            self.image=transform.scale(image.load(imgs[i+1]),(w,h))
            self.costumes.append(self.image)
    def set_costume(self,n):
        self.image = self.costumes[n]
    def rand_costume(self):
        self.image =  choice(self.costumes)
    def position(self):
        self.rect.x = int(randint(0,700-self.rect.width)/25)*25
        self.rect.y = int(randint(0,500-self.rect.height)/25)*25
        self.rand_costume()



head = Snake('snake.png',350,250,25,25,0)
hvost = Snake('popa.png',350,275,25,25,0)
snake = [head,hvost]
food = Food(['apple.png','vishna.png','ogurchik.png'],-100,-100,25,25)
food.position()

font.init()
font1=font.SysFont('Arial',30,15)

speed = 1



clock = time.Clock()

fps = 60
wait = 0
score=font1.render('Счет:'+str(speed-1),1,(0,0,0))
game = True
while game:
    for e in event.get():
        if  e.type == QUIT:
            game = False

    window.fill((0,250,90))
    window.blit(score,(10,60))
    head.get_direction()
    if wait == 0:
        wait = head.wait*(speed//5/2)
        for e in range(len(snake)-1,0,-1):
            snake[e].direction = snake[e-1].direction
            snake[e].rect.x = snake[e-1].rect.x
            snake[e].rect.y = snake[e-1].rect.y
            snake[e].set_direct()
        head.update()
    else:
        wait-=1
    food.reset()
    if head.rect.colliderect(food):
        head.eat(food)
        telo = Snake('hvost.png',head.rect.x,head.rect.y,25,25,0)
        snake.insert(1,telo)
        if speed%5==0:
            head.wait-=5
        if head.wait<15:
            head.wait=2
    for s in snake:
        head.reset()
        s.reset()

    


    display.update()
    clock.tick(fps)