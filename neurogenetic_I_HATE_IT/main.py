import pygame
import random
import time
import config
import simulation
import json
pygame.init()

WHITE = (255, 255, 255)
screen_x = 800
screen_y = 300
groundSpeed = 15
cloadSpeed = 5
rex_a = 3  # 引力加速度
rex_v = 20  # 跳跃初速度
myfontScore = pygame.font.Font(None, 20)
flySpeed = 15


class ground:
    def __init__(self, screen, x):
        self.groundPath = "neurogenetic_I_HATE_IT\\imgs\\ground.png"
        self.groundFile = pygame.image.load(self.groundPath)
        self.x = x
        self.imgwidth = self.groundFile.get_width()
        self.screen = screen

    def groundMove(self):
        self.x -= groundSpeed

    def groundDisplay(self):
        self.screen.blit(self.groundFile, (self.x, screen_y -
                                           self.groundFile.get_height()))


class cload:
    def __init__(self, screen):
        self.cloadPath = "neurogenetic_I_HATE_IT\\imgs\\cload.png"
        self.cloadFile = pygame.image.load(self.cloadPath)
        self.imgwidth = self.cloadFile.get_width()
        self.y = random.randint(0, 7)*screen_y/10
        self.x = screen_x
        self.screen = screen

    def cloadMove(self):
        self.x -= cloadSpeed

    def cloadDisplay(self):
        self.screen.blit(self.cloadFile, (self.x, self.y))


class rex:
    def __init__(self):
        self.rexWalk1path = "neurogenetic_I_HATE_IT\\imgs\\rexWalk1.png"
        self.rexWalk2path = "neurogenetic_I_HATE_IT\\imgs\\rexWalk2.png"
        self.rexJumppath = "neurogenetic_I_HATE_IT\\imgs\\rexJump.png"
        self.rexHide1path = "neurogenetic_I_HATE_IT\\imgs\\rexHide1.png"
        self.rexHide2path = "neurogenetic_I_HATE_IT\\imgs\\rexHide2.png"
        self.rexFile = pygame.image.load(self.rexWalk1path)
        self.x = int(screen_x/10)
        self.y = screen_y-self.rexFile.get_height()
        self.ySpeed = 0  # 0：uping 1:falling
        self.index = 1
        self.screen = screen
        self.status = 0  # 0:walk 1:jump 2:hide
        self.score = 0
        self.live = 1

    def rexWalk(self):
        if self.status == 1:
            self.rexJump()
            return
        if self.status == 2:
            self.rexHide()
            return
        if self.index:
            self.rexFile = pygame.image.load(self.rexWalk1path)
            self.y = screen_y-self.rexFile.get_height()
            self.index -= 1
        else:
            self.rexFile = pygame.image.load(self.rexWalk2path)
            self.y = screen_y-self.rexFile.get_height()
            self.index += 1

    def rexJump(self):
        self.rexFile = pygame.image.load(self.rexJumppath)
        if self.status == 1:
            self.y -= self.ySpeed
            self.ySpeed -= rex_a
            if self.y >= screen_y-self.rexFile.get_height():  # 到达地面
                self.y = screen_y-self.rexFile.get_height()
                self.status = 0
                self.ySpeed = 0
        else:
            self.status = 1
            self.ySpeed = rex_v

    def rexHide(self):
        self.y = screen_y-self.rexFile.get_height()
        if self.index:
            self.rexFile = pygame.image.load(self.rexHide1path)
            self.index -= 1
        else:
            self.rexFile = pygame.image.load(self.rexHide2path)
            self.index += 1

    def rexDisplay(self):
        self.screen.blit(self.rexFile, (self.x, self.y))


class cactus:
    def __init__(self, screen):
        self.cactusBigpath1 = "neurogenetic_I_HATE_IT\\imgs\\cacyusBig1.png"
        self.cactusBigpath2 = "neurogenetic_I_HATE_IT\\imgs\\cacyusBig2.png"
        self.cactusSmallpath = "neurogenetic_I_HATE_IT\\imgs\\cacyusSmall.png"
        index = random.randint(0, 2)
        if index == 0:
            self.cactusFile = pygame.image.load(self.cactusBigpath1)
        elif index == 1:
            self.cactusFile = pygame.image.load(self.cactusBigpath2)
        elif index == 2:
            self.cactusFile = pygame.image.load(self.cactusSmallpath)
        self.y = screen_y-self.cactusFile.get_height()
        self.x = screen_x
        self.screen = screen

    def cactusMove(self):
        self.x -= groundSpeed

    def cactusDisplay(self):
        self.screen.blit(self.cactusFile, (self.x, self.y))


class fly:
    def __init__(self, screen):
        self.fly1Path = "neurogenetic_I_HATE_IT\\imgs\\fly1.png"
        self.fly2Path = "neurogenetic_I_HATE_IT\\imgs\\fly2.png"
        self.flyFile = pygame.image.load(self.fly1Path)
        self.index = 0
        self.x = screen_x
        self.screen = screen
        self.y = screen_y-70

    def flyMove(self):
        if self.index <= 3:
            self.flyFile = pygame.image.load(self.fly1Path)
            self.index += 1
        elif self.index > 3:
            self.flyFile = pygame.image.load(self.fly2Path)
            self.index += 1
            if self.index == 6:
                self.index = 1
        self.x -= flySpeed

    def flyDisplay(self):
        self.screen.blit(self.flyFile, (self.x, self.y))


def BadRoll():
    flag = 0
    global Cactus
    global Flies
    global screen
    for i in Cactus:
        if i.x <= 0:
            Cactus.remove(i)
        if i.x > 2*screen_x/3:
            flag = 1
    for i in Flies:
        if i.x <= 0:
            Flies.remove(i)
        if i.x > 2*screen_x/3:
            flag = 1
    if flag == 0:
        if random.randint(0, 20) == 0:
            if random.randint(0, 1) == 0:
                aCactus = cactus(screen)
                Cactus.append(aCactus)
            else:
                aFly = fly(screen)
                Flies.append(aFly)
    for i in Cactus:
        i.cactusMove()
        i.cactusDisplay()
    for i in Flies:
        i.flyMove()
        i.flyDisplay()


def backgroundRoll():
    # for ground
    flag = 0
    index = 0
    global Grounds
    global screen
    while flag == 0:
        for i in Grounds:
            if i.x <= -i.imgwidth:
                Grounds.remove(i)
            if i.x+i.imgwidth > screen_x:
                flag = 1
            if i.x + i.imgwidth > index:
                index = i.x+i.imgwidth
        if flag == 0:
            aGround = ground(screen, index)
            Grounds.append(aGround)
    for i in Grounds:
        i.groundMove()
        i.groundDisplay()
    # for cloads
    global Cloads
    flag = 0
    for i in Cloads:
        if i.x >= 3*screen_x/5:
            flag = 1
        if i.x <= -i.imgwidth:
            Cloads.remove(i)
    if flag == 0:
        aCload = cload(screen)
        Cloads.append(aCload)
    for i in Cloads:
        i.cloadMove()
        i.cloadDisplay()


def gameRestart():
    global Rexs
    for Arex in Rexs:
        Arex.__init__()
    global Grounds, Cloads, Cactus, Flies
    Grounds = []
    Cloads = []
    Cactus = []
    Flies = []

    simulation.Clearing()
    simulation.Generate()


def get_inputs(Rex):
    global Cactus, Flies
    inputs = [3, 3, 0]
    # inputs[2]=Rex.status-1
    flydis = 100
    cactusdis = 100
    for fly in Flies:
        if fly.x + fly.flyFile.get_width() + Rex.rexFile.get_width() < Rex.x:
            pass
        else:
            flydis = fly.x/Rex.x
            break
    for cactu in Cactus:
        if cactu.x + cactu.cactusFile.get_width() < Rex.x:
            pass
        else:
            cactusdis = cactu.x/Rex.x
            break
    if flydis < cactusdis:
        inputs[0] = flydis
    elif flydis > cactusdis:
        inputs[1] = cactusdis
    return inputs


def get_feed_forward():
    global Rexs
    index = 0
    isallDead = 1
    for Rex in Rexs:
        if Rex.live == 1:
            isallDead = 0
            inputs = get_inputs(Rex)
            outputs = simulation.players[index].neuronetwork.feed_forward(
                inputs)
            if(index == 0):
                print(outputs)
            if outputs[0] <= 0.5 and outputs[1] <= 0.5:
                Rex.rexJump()
            if outputs[1] >= 0.5 and outputs[1] >= 0.5:
                if Rex.status == 0 or Rex.status == 2:
                    Rex.status = 2
            Rex.rexWalk()
            Rex.rexDisplay()
            Rex.score += 0.1
            simulation.players[index].score = Rex.score
            index += 1
            ifIsdead(Rex)
    if isallDead:
        time.sleep(1)
        gameRestart()


def ifIsdead(Rex):
    for i in Cactus:
        if Rex.x + Rex.rexFile.get_width() > i.x and Rex.x < i.x+i.cactusFile.get_width() and Rex.y+Rex.rexFile.get_height() >= i.y:
            Rex.live = 0
    for i in Flies:
        if Rex.x + Rex.rexFile.get_width() > i.x and Rex.x < i.x+i.flyFile.get_width() and Rex.y-Rex.rexFile.get_height() < i.y:
            Rex.live = 0


def suspend():
    while 1:
        time.sleep(2)
        if pygame.key.get_pressed()[pygame.K_SPACE]:
            return


def save():
    index = 0
    for genome in simulation.generation.genomes:
        dic = genome.data
        js = json.dumps(dic)
        name = str(index)+'th'+'genome'
        file = open('./neurogenetic_I_HATE_IT/ai/'+name, 'w')
        file.write(js)
        file.close()
        index += 1


def read():
    index = 0
    for player in simulation.players:
        try:
            name = str(index)+'th'+'genome'
            file = open('./neurogenetic_I_HATE_IT/ai/'+name, 'r')
            js = file.read()
            dic = json.loads(js)
            player.neuronetwork.set_weights(dic)
        except:
            pass
        index += 1


simulation = simulation.Simulation()

pygame.display.set_caption('a game')
screen = pygame.display.set_mode((screen_x, screen_y))
Grounds = []
Cloads = []
Cactus = []
Flies = []
Rexs = []

for i in range(config.Population):
    Arex = rex()
    Rexs.append(Arex)
read()
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit(0)
    if pygame.key.get_pressed()[pygame.K_SPACE]:
        suspend()
    if pygame.key.get_pressed()[pygame.K_s]:
        save()
    time.sleep(0.01)
    screen.fill(WHITE)
    backgroundRoll()
    BadRoll()
    get_feed_forward()
    pygame.display.update()
    # 刷新画面
