import time

import pygame
import sys
import random
import os
FPS = 30
clock = pygame.time.Clock()


player = None

tile_width = tile_height = 24

all_sprites = pygame.sprite.Group()
tiles_group = pygame.sprite.Group()
player_group = pygame.sprite.Group()
brokentiles_group = pygame.sprite.Group()
empty_group = pygame.sprite.Group()

SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

effect_volume = 0.5
music_volume = 0.5

size = [SCREEN_WIDTH, SCREEN_HEIGHT]
screen = pygame.display.set_mode(size)

bg = pygame.transform.scale(pygame.image.load('bg.jpg'), [1000, 600])

pausebutton = pygame.transform.scale(pygame.image.load('pausebutton.png'), (40, 40))
colorkey = pausebutton.get_at((0, 0))
pausebutton.set_colorkey(colorkey)
pausebutton.convert_alpha()


def level_1():
    global player
    pygame.display.set_mode([1000, 600])
    zast = pygame.image.load('zastavka1.jpg')
    screen.blit(pygame.transform.scale(zast, [1000, 600]), (0, 0))
    pygame.display.update()
    time.sleep(4)
    screen.blit(bg, (0, 0))
    player, level_x, level_y, portal = generate_level(load_level('level_1.txt'))
    pygame.display.flip()

    while True:
        screen.blit(bg, (0, 0))
        screen.blit(pausebutton, (0, 0))
        all_sprites.draw(screen)
        all_sprites.update()
        for i in pygame.event.get():
            if i.type == pygame.MOUSEBUTTONDOWN and screen.blit(pygame.transform.scale(pausebutton, [40, 40]), (0, 0)).collidepoint(pygame.mouse.get_pos()):
                # pausescreen()
                pass
            elif i.type == pygame.KEYDOWN:
                player.update()
        camera = Camera()
        camera.update(player)
        portal.update()

        for sprite in all_sprites:
            camera.apply(sprite)
        pygame.display.flip()
        clock.tick(30)


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
                        pass
                        #settings_window()
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
                        #help_window()
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


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet, columns, rows, x, y):
        super().__init__(all_sprites)
        self.frames = []
        self.cut_sheet(sheet, columns, rows)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)

    def cut_sheet(self, sheet, columns, rows):
        self.rect = pygame.Rect(0, 0, sheet.get_width() // columns,
                                sheet.get_height() // rows)
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

    def update(self):
        self.cur_frame = (self.cur_frame + 1) % len(self.frames)
        self.image = self.frames[self.cur_frame]


class Player(pygame.sprite.Sprite):
    right = True

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('right.png'), (48, 48))
        colorkeypl = self.image.get_at((0, 0))
        self.image.set_colorkey(colorkeypl)
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x + 9
        self.y = pos_y + 22
        self.velx = 0
        self.vely = 0
        self.add(all_sprites)
        self.can_jump = True
        self.is_dead = False
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.vely < 10:
            self.vely += 2
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.vely = 0
            self.can_jump = True
        if pygame.key.get_pressed()[pygame.K_d] and self.velx < 4:
            self.velx += 2
        elif pygame.key.get_pressed()[pygame.K_a] and self.velx > -4:
            self.velx -= 2
        if not pygame.key.get_pressed()[pygame.K_a] and not pygame.key.get_pressed()[pygame.K_d]:
            self.velx = 0
        if pygame.key.get_pressed()[pygame.K_SPACE] and self.can_jump is True:
            self.can_jump = False
            self.vely -= 16
        self.rect = self.rect.move(self.velx, self.vely)


class Spider(pygame.sprite.Sprite):
    right = True

    def __init__(self, pos_x, pos_y):
        super().__init__()
        self.image = pygame.transform.scale(pygame.image.load('spider.jpg'), (128, 128))
        self.image.set_colorkey(self.image.get_at((0, 0)))
        self.rect = self.image.get_rect().move(tile_width * pos_x + 15, tile_height * pos_y + 5)
        self.x = pos_x + 9
        self.y = pos_y + 22
        self.velx = 0
        self.vely = 0
        self.add(all_sprites)
        self.can_jump = True
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        if not pygame.sprite.spritecollideany(self, tiles_group) and self.vely < 10:
            self.vely += 2
        if pygame.sprite.spritecollideany(self, tiles_group):
            self.vely = 0
            self.can_jump = True
        if player.x > self.x and self.velx < 4:
            self.velx += 2
        elif player.x < self.x and self.velx > -4:
            self.velx -= 2
        if player.is_dead is True:
            self.velx = 0
        if player.y < self.y and self.can_jump is True:
            self.can_jump = False
            self.vely -= 16
        self.rect = self.rect.move(self.velx, self.vely)



class Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(tiles_group, all_sprites)
        self.add(all_sprites)
        self.add(tiles_group)
        self.image = pygame.transform.scale(pygame.image.load('wall.png'), (24, 24))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.mask = pygame.mask.from_surface(self.image)


class Broken_Tile(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(brokentiles_group, all_sprites)
        self.add(all_sprites)
        self.add(brokentiles_group)
        self.image = pygame.transform.scale(pygame.image.load('broken_wall.png'), (24, 24))
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)


    def update(self):
        if pygame.sprite.collide_mask(self, player):
            self.image = pygame.transform.scale(pygame.image.load('empty.png'), (24, 24))
            self.image.set_colorkey(self.image.get_at((0, 0)))


'''class Empty(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y):
        super().__init__(empty_group, all_sprites)
        self.add(all_sprites)
        self.add(empty_group)
        self.image = pygame.transform.scale(pygame.image.load('empty.png'), (24, 24))
        colorkeyemp = pygame.image.load('empty.png').get_at((0, 0))
        self.image.set_colorkey(colorkeyemp)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x, tile_height * pos_y)
        self.x = tile_width * pos_x
        self.y = tile_height * pos_y

    def draw(self, scr):
        scr.blit(self.image, (self.x, self.y))

'''
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
        self.image = pygame.transform.scale(pygame.image.load('teleport.png'), (250, 250))
        alphachannel = self.image.get_at((0, 0))
        self.image.set_colorkey(alphachannel)
        self.rect = self.image.get_rect().move(
            tile_width * pos_x - 87, tile_height * pos_y - 155)



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

