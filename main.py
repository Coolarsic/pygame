import gc
import random
import time

import pygame
import sys
import asyncio
FPS = 30
clock = pygame.time.Clock()

can_spawn = True

player = None

tile_width = tile_height = 36

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
brokentiles_group = pygame.sprite.Group()
weapon = pygame.sprite.Group()
monsters = pygame.sprite.Group()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

effect_volume = 0.5
music_volume = 0.5

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)


pausebutton = pygame.transform.scale(pygame.image.load('pausebutton.png'), (40, 40))
colorkey = pausebutton.get_at((0, 0))
pausebutton.set_colorkey(colorkey)


def help_window():
    text = pygame.font.Font('pix.ttf', 25)
    text1 = pygame.font.Font('pix.ttf', 50)
    helpscreen = pygame.display.set_mode((1000, 600))
    pauseim = pygame.transform.scale(pygame.image.load('pausescreen.png'), (1000, 600))
    a = pygame.transform.scale(pygame.image.load('a.png'), (40, 40))
    e = pygame.transform.scale(pygame.image.load('e.png'), (40, 40))
    space = pygame.transform.scale(pygame.image.load('space.png'), (100, 100))
    d = pygame.transform.scale(pygame.image.load('d.png'), (40, 40))
    a.set_colorkey(a.get_at((0, 0)))
    d.set_colorkey(a.get_at((0, 0)))
    e.set_colorkey(a.get_at((0, 0)))
    space.set_colorkey(a.get_at((0, 0)))
    helpscreen.blit(pauseim, (0, 0))
    texttext = text.render('После последних событий, произошедших на планете "Спектр" прошло 2 года.', True, pygame.color.Color(100, 150, 255))
    texttext1 = text.render("И вот, на ней снова была замечена подозрительная активность. Как удалось ", True, pygame.color.Color(100, 150, 255))
    texttext2 = text.render("узнать, причиной всему этому стало огромное неопознанное существо. Ваша  ", True, pygame.color.Color(100, 150, 255))
    texttext3 = text.render('задача - разобраться, что происходит на планете "Спектр"', True, pygame.color.Color(100, 150, 255))
    control = text1.render('Управление', True, pygame.color.Color(255, 255, 255))
    home = pygame.transform.scale(pygame.image.load('mainmenu.png'), (50, 50))
    returning1 = text1.render('Чтобы вернуться в главное меню', True, pygame.color.Color(255, 255, 255))
    returning2 = text1.render('нажмите любую клавишу', True, pygame.color.Color(255, 255, 255))
    atext = text.render('-> Движение влево', True, pygame.color.Color(255, 255, 255))
    dtext = text.render('-> Движение вправо', True, pygame.color.Color(255, 255, 255))
    etext = text.render('-> Поднять оружие/выстрел', True, pygame.color.Color(255, 255, 255))
    spacetext = text.render('-> Прыжок', True, pygame.color.Color(255, 255, 255))
    while True:
        pygame.display.update()
        screen.blit(texttext, (20, 20))
        screen.blit(texttext1, (20, 50))
        screen.blit(texttext2, (20, 80))
        screen.blit(texttext3, (20, 110))
        screen.blit(control, (370, 150))
        screen.blit(returning1, (130, 480))
        screen.blit(returning2, (250, 530))
        screen.blit(a, (20, 220))
        screen.blit(d, (20, 280))
        screen.blit(e, (20, 340))
        screen.blit(space, (20, 370))
        screen.blit(atext, (70, 230))
        screen.blit(dtext, (70, 290))
        screen.blit(etext, (70, 350))
        screen.blit(spacetext, (130, 410))
        for i in pygame.event.get():
            if i.type == pygame.KEYDOWN or i.type == pygame.MOUSEBUTTONDOWN:
                return


def settings_window():
    global effect_volume, music_volume
    text = pygame.font.Font('pix.ttf', 25)
    text1 = pygame.font.Font('pix.ttf', 50)
    pause = text1.render("Настройки", True, pygame.color.Color(100, 150, 255))
    pausescr = pygame.display.set_mode((1000, 600))
    pauseim = pygame.transform.scale(pygame.image.load('pausescreen.png'), (1000, 600))
    contimage = pygame.transform.scale(pygame.image.load('continue.png'), (50, 50))
    mainmenu = pygame.transform.scale(pygame.image.load('mainmenu.png'), (50, 50))
    volume = pygame.transform.scale(pygame.image.load('volume.png'), (50, 50))
    contimage.set_colorkey(contimage.get_at((0, 0)))
    volume.set_colorkey(volume.get_at((0, 0)))
    mainmen = text.render("Вернуться в главное меню", True, pygame.color.Color(255, 255, 255))
    while True:
        effvol = text.render(f"Громкость эффектов (↑, ↓ на клавиатуре): {round(effect_volume * 100)}%", True,
                             pygame.color.Color(255, 255, 255))
        musvol = text.render(f"Громкость музыки (←, → на клавиатуре): {round(music_volume * 100)}%", True,
                             pygame.color.Color(255, 255, 255))
        for i in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_LEFT] and round(music_volume, 3) > 0:
                music_volume -= 0.05
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and round(music_volume, 3) < 1:
                music_volume += 0.05
            elif pygame.key.get_pressed()[pygame.K_UP] and round(effect_volume, 3) < 1:
                effect_volume += 0.05
                snd = pygame.mixer.Sound('buttonhover.mp3')
                snd.set_volume(effect_volume)
                snd.play()
            elif pygame.key.get_pressed()[pygame.K_DOWN] and round(effect_volume, 3) > 0:
                effect_volume -= 0.05
                snd = pygame.mixer.Sound('buttonhover.mp3')
                snd.set_volume(effect_volume)
                snd.play()
            elif i.type == pygame.MOUSEBUTTONDOWN and pausescr.blit(mainmenu, (470, 100)).collidepoint(
                    pygame.mouse.get_pos()):
                return
        pausescr.blit(pauseim, (0, 0))
        pausescr.blit(pause, (390, 20))
        pausescr.blit(mainmen, (340, 170))
        pausescr.blit(effvol, (210, 370))
        pausescr.blit(musvol, (220, 320))
        pausescr.blit(mainmenu, (470, 100))
        pygame.display.update()
        clock.tick(30)


def pausescreen():
    global effect_volume, music_volume
    text = pygame.font.Font('pix.ttf', 25)
    text1 = pygame.font.Font('pix.ttf', 50)
    pause = text1.render("Пауза", True, pygame.color.Color(100, 150, 255))
    pausescr = pygame.display.set_mode((1000, 600))
    pauseim = pygame.transform.scale(pygame.image.load('pausescreen.png'), (1000, 600))
    contimage = pygame.transform.scale(pygame.image.load('continue.png'), (50, 50))
    mainmenu = pygame.transform.scale(pygame.image.load('mainmenu.png'), (50, 50))
    volume = pygame.transform.scale(pygame.image.load('volume.png'), (50, 50))
    contimage.set_colorkey(contimage.get_at((0, 0)))
    volume.set_colorkey(volume.get_at((0, 0)))
    mainmen = text.render("Вернуться в главное меню", True, pygame.color.Color(255, 255, 255))
    ret = text.render("Вернуться в игру", True, pygame.color.Color(255, 255, 255))
    while True:
        effvol = text.render(f"Громкость эффектов (↑, ↓ на клавиатуре): {round(effect_volume * 100)}%", True,
                             pygame.color.Color(255, 255, 255))
        musvol = text.render(f"Громкость музыки (←, → на клавиатуре): {round(music_volume * 100)}%", True,
                             pygame.color.Color(255, 255, 255))
        for i in pygame.event.get():
            if pygame.key.get_pressed()[pygame.K_LEFT] and round(music_volume, 3) > 0:
                music_volume -= 0.05
            elif pygame.key.get_pressed()[pygame.K_RIGHT] and round(music_volume, 3) < 1:
                music_volume += 0.05
            elif pygame.key.get_pressed()[pygame.K_UP] and round(effect_volume, 3) < 1:
                effect_volume += 0.05
                snd = pygame.mixer.Sound('buttonhover.mp3')
                snd.set_volume(effect_volume)
                snd.play()
            elif pygame.key.get_pressed()[pygame.K_DOWN] and round(effect_volume, 3) > 0:
                effect_volume -= 0.05
                snd = pygame.mixer.Sound('buttonhover.mp3')
                snd.set_volume(effect_volume)
                snd.play()
            elif i.type == pygame.MOUSEBUTTONDOWN and pausescr.blit(contimage, (250, 100)).collidepoint(pygame.mouse.get_pos()):
                return
            elif i.type == pygame.MOUSEBUTTONDOWN and pausescr.blit(mainmenu, (650, 100)).collidepoint(pygame.mouse.get_pos()):
                [a.kill() for a in all_sprites]
                [a.kill() for a in player_group]
                [a.kill() for a in tiles_group]
                [a.kill() for a in brokentiles_group]
                [a.kill() for a in weapon]
                [a.kill() for a in monsters]
                draw_intro()
        pausescr.blit(pauseim, (0, 0))
        pausescr.blit(pause, (430, 20))
        pausescr.blit(mainmen, (530, 170))
        pausescr.blit(effvol, (210, 370))
        pausescr.blit(musvol, (220, 320))
        pausescr.blit(ret, (170, 170))
        pausescr.blit(contimage, (250, 100))
        pausescr.blit(mainmenu, (650, 100))
        pygame.display.update()
        clock.tick(30)


def level_1():
    global player, can_spawn
    shotgun = Weapon(28, 5, 'shotgun')
    pygame.display.set_mode([1000, 600])
    zast = pygame.image.load('zastavka1.jpg')
    screen.blit(pygame.transform.scale(zast, [1000, 600]), (0, 0))
    pygame.display.flip()
    time.sleep(4)
    player, level_x, level_y, portal = generate_level(load_level('level_1.txt'))
    pygame.display.flip()
    camera = Camera()
    itr = 0
    while True:
        bg = pygame.transform.scale(pygame.image.load(f'space-pixel-art-{itr}.png'), [1000, 1000])
        screen.blit(bg, (0, 0))
        screen.blit(pausebutton, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()

        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN and screen.blit(pygame.transform.scale(pausebutton, [40, 40]), (0, 0)).collidepoint(pygame.mouse.get_pos()):
                pausescreen()
            elif i.type == pygame.KEYDOWN:
                player.update()
        camera.update(player)

        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(30)
        itr += 1
        if itr == 35:
            itr = 0
        if shotgun.equip is True and can_spawn is True:
            spider1 = Enemy(30, 3)
            spider2 = Enemy(31, 3)
            spider3 = Enemy(34, 3)
            can_spawn = False


def ShadowText(screen, text, size, x, y, color=(150,150,255), drop_color=(100,100,200), font=None, offset=5):
    text_bitmap = font.render(text, True, drop_color)
    screen.blit(text_bitmap, (x+offset, y+offset))
    text_bitmap = font.render(text, True, color)
    screen.blit(text_bitmap, (x, y))


def draw_intro():
    pygame.init()

    pygame.display.set_caption('Space expedition')
    img = pygame.image.load('main.png')

    prevfont = pygame.font.Font('Tr2n.ttf', 60)
    buttonfont = pygame.font.Font('rus.ttf', 40)

    newgame = buttonfont.render("Новая игра", True, pygame.color.Color(255, 255, 255))
    cont = buttonfont.render("Продолжить", True, pygame.color.Color(255, 255, 255))
    settings = buttonfont.render("Настройки", True, pygame.color.Color(255, 255, 255))
    help = buttonfont.render("Помощь", True, pygame.color.Color(255, 255, 255))
    ex = buttonfont.render("Выйти", True, pygame.color.Color(255, 255, 255))

    hoversound = pygame.mixer.Sound('buttonhover.mp3')
    sounds = True

    while True:
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == pygame.QUIT:
                sys.exit(0)
            if screen.blit(ex, (373, 400)).collidepoint(pos) or screen.blit(help, (350, 350)).collidepoint(pos) or screen.blit(newgame, (320, 200)).collidepoint(pos) or screen.blit(settings, (323, 300)).collidepoint(pos) or screen.blit(cont, (300, 250)).collidepoint(pos):
                if screen.blit(ex, (373, 400)).collidepoint(pos):
                    ex = buttonfont.render("Выйти", True, pygame.color.Color(155, 155, 255))
                    if sounds is True:
                        hoversound.set_volume(effect_volume)
                        hoversound.play()
                        sounds = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        sys.exit()
                else:
                    ex = buttonfont.render("Выйти", True, pygame.color.Color(255, 255, 255))

                if screen.blit(settings, (323, 300)).collidepoint(pos):
                    settings = buttonfont.render("Настройки", True, pygame.color.Color(155, 155, 255))
                    if sounds is True:
                        hoversound.set_volume(effect_volume)
                        hoversound.play()
                        sounds = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        settings_window()
                else:
                    settings = buttonfont.render("Настройки", True, pygame.color.Color(255, 255, 255))

                if screen.blit(newgame, (320, 200)).collidepoint(pos):
                    newgame = buttonfont.render("Новая игра", True, pygame.color.Color(155, 155, 255))
                    if sounds is True:
                        hoversound.set_volume(effect_volume)
                        hoversound.play()
                        sounds = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pygame.display.flip()
                        level_1()
                else:
                    newgame = buttonfont.render("Новая игра", True, pygame.color.Color(255, 255, 255))

                if screen.blit(help, (350, 350)).collidepoint(pos):
                    help = buttonfont.render("Помощь", True, pygame.color.Color(155, 155, 255))
                    if sounds is True:
                        hoversound.set_volume(effect_volume)
                        hoversound.play()
                        sounds = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        pass
                        help_window()
                else:
                    help = buttonfont.render("Помощь", True, pygame.color.Color(255, 255, 255))
                if screen.blit(cont, (300, 250)).collidepoint(pos):
                    cont = buttonfont.render("Продолжить", True, pygame.color.Color(155, 155, 255))
                    if sounds is True:
                        hoversound.set_volume(effect_volume)
                        hoversound.play()
                        sounds = False
                else:
                    cont = buttonfont.render("Продолжить", True, pygame.color.Color(255, 255, 255))
            else:
                sounds = True
        screen.blit(pygame.transform.scale(img, size), (0, 0))
        screen.blit(ex, (373, 400))
        screen.blit(cont, (300, 250))
        screen.blit(help, (350, 350))
        screen.blit(settings, (323, 300))
        screen.blit(newgame, (320, 200))
        ShadowText(screen, "Space expedition", 60, 160, 10, font=prevfont)
        pygame.display.update()


class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, typ, velx, vely=0):
        super().__init__(all_sprites)
        self.add(all_sprites)
        if typ == 'pistol':
            self.image = pygame.transform.scale(pygame.image.load('pistol_bullet.png'), (20, 20))
        elif typ == 'rifle':
            self.image = pygame.transform.scale(pygame.image.load('rifle_bullet.png'), (20, 20))
        elif typ == 'shotgun':
            self.image = pygame.transform.scale(pygame.image.load('pistol_bullet.png'), (20, 20))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect().move(x, y)
        self.vely = vely
        self.velx = velx
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.image = pygame.image.load('empty.png')
            self.image.set_colorkey(self.image.get_at((0, 0)))
            self.kill()
            gc.collect()
        elif pygame.sprite.spritecollideany(self, monsters):
            a = pygame.sprite.spritecollideany(self, monsters)
            if a.is_dead is False:
                a.is_dead = True
                a = range(-5, 6)
                for _ in range(20):
                    part = OnKillParticle((self.rect.x, self.rect.y), random.choice(a), random.choice(a))
                self.image = pygame.image.load('empty.png')
                self.image.set_colorkey(self.image.get_at((0, 0)))
                self.kill()
                gc.collect()
        self.rect.move_ip(self.velx, self.vely)


class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self, x, y):
        y = y - 1
        x = x - 0.5
        super().__init__(all_sprites)
        self.frames = []
        self.add(all_sprites)
        self.cut_sheet(pygame.transform.scale(pygame.image.load('animate_player_right.png'), (tile_width * 4, tile_height * 2)), 4, 1)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 2, tile_height * 2))
        self.rect = self.rect.move(x * tile_width, y * tile_height)
        self.vely = 0
        self.velx = 0
        self.x = x
        self.y = y
        self.can_jump = True
        self.is_dead = False
        self.iter = 0
        self.mask = pygame.mask.from_surface(self.image)
        self.inventory = []

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.iter += 1
        if self.right is True and (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]) and self.iter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 2, tile_height * 2))
        elif self.right is False and (pygame.key.get_pressed()[pygame.K_d] or pygame.key.get_pressed()[pygame.K_a]) and self.iter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 2, tile_height * 2))
            self.image = pygame.transform.flip(self.image, True, False)
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.vely < 12:
            self.vely += 6
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.vely = 0
            self.can_jump = True
        if pygame.key.get_pressed()[pygame.K_d]:
            self.right = True
            if self.velx < 10:
                self.velx += 5
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.right = False
            if self.velx > -10:
                self.velx -= 5
        if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
            self.velx = 0
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.can_jump is True:
            self.can_jump = False
            self.vely = self.vely - tile_height
        for t in tiles_group:
            if self.rect.move(self.velx, 0).colliderect(t):
                self.velx = 0
            elif self.rect.move(0, self.vely).colliderect(t):
                self.vely = 0
                self.can_jump = True
        self.rect = self.rect.move(self.velx, self.vely)
        for w in weapon:
            if pygame.key.get_pressed()[pygame.K_e] and pygame.sprite.collide_mask(self, w) and w.equip is False:
                w.equip = True
                w.rect.update(self.rect[0] + 27, self.rect[1] + 15, tile_width, tile_height)
            elif w.equip is True:
                w.rect[0] = self.rect[0] + tile_width
                w.rect[1] = self.rect[1] + tile_height // 2 - 12
                if not self.right:
                    w.image = w.img
                    w.rect[0] -= tile_width * 2
                else:
                    w.image = pygame.transform.flip(w.img, True, False)


class Weapon(pygame.sprite.Sprite):
    right = True

    def __init__(self, pos_x, pos_y, typ):
        super().__init__(all_sprites, weapon)
        self.add(all_sprites)
        self.add(weapon)
        self.can_shoot = True
        self.equip = False

        if typ == 'pistol':
            self.typ = 'pistol'
            self.image = pygame.transform.scale(pygame.image.load('pistol.png'), (tile_width, tile_height))
            self.shootsound = pygame.mixer.Sound('pistol_sound.mp3')
            self.cooldown = 1.5
            self.img = pygame.transform.scale(pygame.image.load('pistol.png'), (tile_width, tile_height))
        elif typ == 'rifle':
            self.typ = 'rifle'
            self.image = pygame.transform.scale(pygame.image.load('rifle.png'), (tile_width * 2, tile_height * 2))
            self.shootsound = pygame.mixer.Sound('rifle_sound.mp3')
            self.cooldown = 1
            self.img = pygame.transform.scale(pygame.image.load('rifle.png'), (tile_width * 2, tile_height * 2))
        elif typ == 'shotgun':
            self.typ = 'shotgun'
            self.shootsound = pygame.mixer.Sound('shotgun_sound.mp3')
            self.image = pygame.transform.scale(pygame.image.load('shotgun.png'), (tile_width * 2, tile_height * 2))
            self.cooldown = 0.5
            self.img = pygame.transform.scale(pygame.image.load('shotgun.png'), (tile_width * 2, tile_height * 2))
            self.rect = self.image.get_rect().move(tile_width * (pos_x - 1), tile_height * (pos_y - 1) - 15)
        self.shootsound.set_volume(effect_volume)
        self.image.set_colorkey(self.image.get_at((1, 1)))

        self.mask = pygame.mask.from_surface(self.image)


    def update(self):
        global player
        self.shootsound.set_volume(effect_volume)
        if pygame.key.get_pressed()[pygame.K_e] and self.equip and self.can_shoot:
            self.shoot(player.right)


    def shoot(self, right=True):
        self.shootsound.play()
        velx = 0
        if right is True:
            velx = 60
        else:
            velx = -60
        if self.typ == 'pistol':
            bullet = Bullet(self.rect[0], self.rect[1], 'pistol', velx)
        elif self.typ == 'rifle':
            bullet = Bullet(self.rect[0], self.rect[1], 'rifle', velx)
        elif self.typ == 'shotgun':
            bullet1 = Bullet(self.rect[0], self.rect[1], 'shotgun', velx, random.randint(-20, 20))
            bullet2 = Bullet(self.rect[0], self.rect[1], 'shotgun', velx, random.randint(-20, 20))
            bullet3 = Bullet(self.rect[0], self.rect[1], 'shotgun', velx, random.randint(-20, 20))
            bullet4 = Bullet(self.rect[0], self.rect[1], 'shotgun', velx, random.randint(-20, 20))
            bullet5 = Bullet(self.rect[0], self.rect[1], 'shotgun', velx, random.randint(-20, 20))


    
    async def make_cooldown(self, sec):
        await asyncio.sleep(sec)
        self.can_shoot = True


class Enemy(pygame.sprite.Sprite):
    right = True

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.add(all_sprites)
        self.add(monsters)
        self.cut_sheet(pygame.transform.scale(pygame.image.load('animated_spider.png'), (240, 60)), 4, 1)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
        self.rect = self.rect.move(x * tile_width, y * tile_height)
        self.vely = 0
        self.velx = 6
        self.x = x
        self.y = y
        self.can_jump = True
        self.is_dead = False
        self.iter = 0
        self.mask = pygame.mask.from_surface(self.image)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.iter += 1
        if self.right is True and self.rect[0] < player.rect[0] and self.iter % 5 == 0 and self.is_dead is False:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
        elif self.right is False and self.rect[0] > player.rect[0] and self.iter % 5 == 0 and self.is_dead is False:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
            self.image = pygame.transform.flip(self.image, True, False)
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.vely < 10:
            self.vely += 5
        for i in tiles_group:
            if pygame.sprite.collide_mask(self, i):
                self.vely = 0
                self.can_jump = True
        if player.rect[0] > self.rect[0]:
            self.right = True
            if self.velx < 6:
                self.velx += 3
        elif player.rect[0] < self.rect[0]:
            self.right = False
            if self.velx > -6:
                self.velx -= 3
        if pygame.sprite.collide_mask(self, player) and self.is_dead is False:
            player.is_dead = True
        if self.is_dead is True:
            self.velx = 0
            if self.image.get_alpha() > 0:
                self.image.set_alpha(self.image.get_alpha() - 1)
        self.rect = self.rect.move(self.velx, self.vely)


class Boss(pygame.sprite.Sprite):
    right = True

    def __init__(self, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.add(all_sprites)
        self.add(monsters)
        self.cut_sheet(pygame.transform.scale(pygame.image.load('animated_spider.png'), (tile_width * 10, tile_height * 10)), 4, 1)
        self.cur_frame = 0
        self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
        self.rect = self.rect.move(x * tile_width, y * tile_height)
        self.vely = 0
        self.velx = 6
        self.x = x
        self.y = y
        self.can_jump = True
        self.is_dead = False
        self.iter = 0

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.iter += 1
        if self.right is True and self.x < player.x and self.iter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
        elif self.right is False and self.x > player.x and self.iter % 5 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = pygame.transform.scale(self.frames[self.cur_frame], (tile_width * 3, tile_height * 3))
            self.image = pygame.transform.flip(self.image, True, False)
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.vely < 10:
            self.vely += 5
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.vely = 0
            self.can_jump = True
        if player.x > self.x:
            self.right = True
            if self.velx < 10:
                self.velx += 5
        elif player.x < self.x:
            self.right = False
            if self.velx > -10:
                self.velx -= 5
        if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
            self.velx = 0
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.can_jump is True:
            self.can_jump = False
            self.vely -= 16
        self.rect = self.rect.move(self.velx, self.vely)


class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(all_sprites)
        self.add(tiles_group)
        self.image = pygame.transform.scale(pygame.image.load('broken_wall.png'), (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Broken_Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(brokentiles_group, all_sprites)
        self.add(all_sprites)
        self.add(brokentiles_group)
        self.image = pygame.transform.scale(pygame.image.load('broken_wall.png'), (tile_width, tile_height))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)




    def update(self):
        if pygame.sprite.collide_mask(self, player):
            self.image = pygame.transform.scale(pygame.image.load('empty.png'), (tile_width, tile_height))
            self.image.set_colorkey(self.image.get_at((0, 0)))
            a = range(-5, 6)
            for _ in range(20):
                part = Particle((self.rect.x, self.rect.y), random.choice(a), random.choice(a))


class Camera:
    def __init__(self):
        self.dx = 0
        self.dy = 0

    def apply(self, obj):
        obj.rect.x += self.dx
        obj.rect.y += self.dy

    def update(self, target):
        self.dx = -(target.rect.x + target.rect.w // 2 - SCREEN_WIDTH // 2)
        self.dy = -(target.rect.y + target.rect.h // 2 - SCREEN_HEIGHT // 2)


class Portal(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(all_sprites)
        self.add(all_sprites)
        self.image = pygame.transform.scale(pygame.image.load('teleport.png'), (tile_width * 10, tile_height * 10))
        alphachannel = self.image.get_at((0, 0))
        self.image.set_colorkey(alphachannel)
        self.rect = self.image.get_rect().move(
            tile_width * (pos_x - 5), tile_height * (pos_y - 6))


class Particle(pygame.sprite.Sprite):
    images = [pygame.transform.scale(pygame.image.load("broken_wall.png"), (3, 3))]
    for scale in (3, 5, 7):
        images.append(pygame.transform.scale(images[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 5

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


class OnKillParticle(pygame.sprite.Sprite):
    images = [pygame.transform.scale(pygame.image.load('onkillparticle.png'), (3, 3))]
    for scale in (3, 5, 7):
        images.append(pygame.transform.scale(images[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(all_sprites)
        self.image = random.choice(self.images)
        self.rect = self.image.get_rect()

        self.velocity = [dx, dy]
        self.rect.x, self.rect.y = pos

        self.gravity = 5

    def update(self):
        self.velocity[1] += self.gravity
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        if not self.rect.colliderect(screen.get_rect()):
            self.kill()


def main():
    draw_intro()

def load_level(filename):
    filename = "data/" + filename
    with open(filename, 'r') as mapFile:
        level_map = [line.strip() for line in mapFile]
    max_width = max(map(len, level_map))
    return list(map(lambda x: x.ljust(max_width, '.'), level_map))


def generate_level(level):
    new_player, x, y, portal = None, None, None, None
    for y in range(len(level)):
        for x in range(len(level[y])):
            if level[y][x] == '.':
                pass
            elif level[y][x] == '7':
                new_player = Player(x, y)
            elif level[y][x] == '#':
                Tile(x, y)
            elif level[y][x] == '@':
                Broken_Tile(x, y)
            elif level[y][x] == '0':
                portal = Portal(x, y)
    return new_player, x, y, portal


if __name__ == '__main__':
    main()

