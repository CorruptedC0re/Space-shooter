import pygame
import pygame_menu
from random import randint, choice
distance_covered = 0
score = 0
shoot = 'LEFT'
IN_GAME = True
level = 1
time = 150
timer_mine_shot = pygame.time.set_timer(pygame.USEREVENT + 4, time)
get_sec = 0
def start_game():
    global shoot, score, distance_covered,IN_GAME, level, timer_mine_shot, time, get_sec
    ships = {'no_hero.jpg': [10, 5, 20, 25, 30, 10, 30, 10, 300, 50, 35, 10, 50, 50, (247, 5, 33)],
             'ship1.png': [0, 8, 10, 50, 50, 5, 10, 5, 600, 30, 75, 5, 50, 50, (255, 5, 230)],
             'ship2.png': [30, 4, 25, 15, 25, 10, 35, 15, 250, 60, 40, 10, 60, 60, (251, 255, 5)],
             'ship3.png': [10, 5, 20, 20, 30, 15, 40, 10, 350, 50, 40, 15, 60, 60, (255, 136, 0)],
             'ship4.png': [80, 2, 50, 10, 10, 20, 60, 30, 100, 250, 20, 40, 80, 80, (150, 255, 13)],
             'ship5.png': [40, 5, 40, 15, 25, 25, 50, 25, 300, 50, 35, 15, 80, 80, (0, 238, 255)],
             'ship6.png': [50, 4, 55, 15, 30, 20, 40, 30, 150, 200, 20, 30, 70, 70, (188, 196, 196)],
             'ship7.png': [100, 1, 100, 5, 5, 40, 100, 50, 50, 400, 10, 50, 90, 90, (0, 149, 255)]}
    levels = {1:[0,2], 2:[0,4], 3:[0,5], 4:[0,6], 5:[0,8], 6:[2,4], 7:[5,7],8:[7,8]}
    class Star(pygame.sprite.Sprite):
        def __init__(self, x, group):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('zvezda.bmp').convert()
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect(bottomleft=(x, -10))
            self.add(group)

        def update(self):
            if self.rect.topleft[1] > 800:
                self.kill()
            else:
                self.rect.y += 5

    class MyIstro(pygame.sprite.Sprite):
        def __init__(self):
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.image.load('hero.jpg').convert()
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (70, 70))
            self.rect = self.image.get_rect(center=(300, 700))
            self.xp = 100
            self.bron = 50
            self.lives = 0
            self.hidden = False
        def update(self, action):
            if action == 'LEFT':
                if self.rect.x > 0:
                    self.rect.x -= 5
            elif action == 'RIGHT':
                if self.rect.topright[0] < 600:
                    self.rect.x += 5
            elif action == 'DOWN':
                if self.rect.bottomleft[1] < 800:
                    self.rect.y += 5
            elif action == 'UP':
                if self.rect.y > 0:
                    self.rect.y -= 5

        def check_xp(self):
            global IN_GAME, get_sec
            if self.xp <= 0:
                self.lives -= 1
                if self.lives < 0:
                    self.kill()
                    IN_GAME = False
                else:
                    Explode(self.rect, explodes)
                    self.rect.x = 265
                    self.rect.y = 665
                    self.xp = 100
                    self.hidden = True
                    self.image.set_alpha(100)
                    get_sec = pygame.time.get_ticks()




    class Laser(pygame.sprite.Sprite):
        def __init__(self, group):
            global shoot
            pygame.sprite.Sprite.__init__(self)
            self.image = pygame.Surface((5, 40))
            self.image.fill((0, 255, 0))
            if shoot == 'LEFT':
                coord = (my_plane.rect.bottomleft[0], my_plane.rect.bottomleft[1] - 38)
            else:
                coord = (my_plane.rect.bottomright[0], my_plane.rect.bottomleft[1] - 35)
            self.rect = self.image.get_rect(bottomright=coord)
            self.add(group)
            shoot = shooting[shoot]

        def update(self):
            if self.rect.bottomleft[1] > 0:
                self.rect.y -= 5
            else:
                self.kill()

    class ELaser(pygame.sprite.Sprite):
        def __init__(self, group, ship):
            pygame.sprite.Sprite.__init__(self)
            self.enemy = ship.enemy
            self.image = pygame.Surface((5, 40))
            self.image.fill(ships[self.enemy][14])
            shoot = choice(['LEFT', 'RIGHT'])
            if shoot == 'LEFT':
                coord = (ship.rect.topleft[0] + 12, ship.rect.topleft[1] + 38)
            else:
                coord = (ship.rect.topright[0] - 12, ship.rect.topright[1] + 38)
            self.rect = self.image.get_rect(topleft=coord)
            self.add(group)

        def update(self):
            if self.rect.topleft[1] < 800:
                self.rect.y += 10
            else:
                self.kill()

    class Enemy(pygame.sprite.Sprite):
        def __init__(self, x, group):
            global level
            pygame.sprite.Sprite.__init__(self)
            if level > 8:
                if level % 8 == 0:
                    level_choose = 8
                else:
                    level_choose = 5
            else:
                level_choose = level
            self.enemy = ['no_hero.jpg', 'ship1.png', 'ship2.png', 'ship3.png', 'ship5.png', 'ship6.png', 'ship4.png', 'ship7.png']
            self.enemy = choice(self.enemy[levels[level_choose][0]:levels[level_choose][1]])
            if 'png' in self.enemy:
                self.image = pygame.image.load(self.enemy).convert_alpha()
            else:
                self.image = pygame.image.load(self.enemy).convert()
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (ships[self.enemy][12], ships[self.enemy][13]))
            self.image = pygame.transform.flip(self.image, 0, 1)
            self.rect = self.image.get_rect(center=(x, -25))
            self.add(group)
            self.xp = 100
            self.bron = ships[self.enemy][0]
        def update(self):
            if self.rect.topleft[1] < 800:
                self.rect.y += ships[self.enemy][1]
                for enemy in enemies:
                    if enemy == self:
                        continue
                    else:
                        if pygame.sprite.collide_circle_ratio(0.7)(enemy, self):
                            enemy.rect.y += 35
                            self.rect.x += 30
                            self.rect.y -= ships[self.enemy][1]
                if self.rect.bottomleft[1] < my_plane.rect.topleft[1] and my_plane.rect.topleft[1] - \
                        self.rect.bottomleft[1] <= 400:
                    if self.rect.center[0] < my_plane.rect.center[0] - 10:
                        self.rect.x += 2
                    elif self.rect.center[0] > my_plane.rect.center[0] + 10:
                        self.rect.x -= 2
            else:
                self.kill()

        def check_xp(self):
            global score
            if self.xp <= 0:
                self.kill()
                Explode(self.rect, explodes)
                score += ships[self.enemy][2]


    class Bonus(pygame.sprite.Sprite):
        def __init__(self, x, group):
            pygame.sprite.Sprite.__init__(self)
            self.icon = choice(['health.jpg', 'bronya.jpeg', 'heart.jpg'])
            self.image = pygame.image.load(self.icon).convert()
            self.image.set_colorkey((255, 255, 255))
            self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect(center=(x, -50))
            self.add(group)

        def update(self):
            if self.rect.topleft[1] < 800:
                self.rect.y += 4
            else:
                self.kill()


    class Explode(pygame.sprite.Sprite):
        def __init__(self, ship, group, full=True):
            pygame.sprite.Sprite.__init__(self)
            self.full = full
            self.ship_coords = ship.center
            self.number = 1
            self.image = pygame.image.load('fire{}.png'.format(self.number)).convert_alpha()
            self.image.set_colorkey((255,255,255))
            if self.full:
                self.image = pygame.transform.scale(self.image, (80,80))
            else:
                self.image = pygame.transform.scale(self.image, (30, 30))
            self.rect = self.image.get_rect(center=self.ship_coords)
            self.add(group)
        def if_over(self):
            if self.number == 16:
                for i in enemies:
                    if pygame.sprite.collide_circle_ratio(0.7)(self, i):
                        i.xp -= ships[i.enemy][3]
                        i.check_xp()
                if pygame.sprite.collide_circle_ratio(1)(self, my_plane):
                    if not my_plane.hidden:
                        my_plane.xp -= 10
                        my_plane.check_xp()
                self.kill()
        def if_over1(self):
            if self.number == 5:
                self.number = 12
            if self.number == 16:
                self.kill()


    def change_xp_and_bron(ship, com, changeship):
        tochange = ships[ship.enemy][com]
        if changeship.bron > 0:
            if changeship.bron - tochange < 0:
                changeship.bron = 0
                tochange -= changeship.bron
                changeship.xp -= tochange
            else:
                changeship.bron -= tochange
        else:
            changeship.xp -= tochange


    def check_level():
        global level, time, timer_mine_shot
        if level % 8 != 0:
            if score // 300 == level and score != 0:
                level += 1
                if level % 2 == 0 and time > 60:
                    time -= 15
                    timer_mine_shot = pygame.time.set_timer(pygame.USEREVENT + 4, time)
                for i in ships:
                    ships[i][3] += 2
                my_plane.xp = 100
                my_plane.bron = 100
        else:
            if score // 4000 != 0:
                for i in ships:
                    ships[i][3] += 2
                my_plane.xp = 100
                my_plane.bron = 100
                level += 1


    timer_star = pygame.time.set_timer(pygame.USEREVENT + 0, 500)
    timer_enemy = pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
    timer_shot_enemy = pygame.time.set_timer(pygame.USEREVENT + 2, 500)
    timer_bonus = pygame.time.set_timer(pygame.USEREVENT + 3, 8000)
    BACKGROUND = pygame.image.load('SPAACE.png')
    BACKGROUND = pygame.transform.scale(BACKGROUND, (600,800))
    clock = pygame.time.Clock()
    field.blit(BACKGROUND, (0,0))
    my_plane = MyIstro()
    information = pygame.Surface((200, 800))
    information.fill((33, 32, 32))
    font = pygame.font.SysFont('verdana', 24)
    font_health = font.render("Health/Armor:", 1, (255, 247, 0))
    font_distance = font.render("Distance:", 1, (255, 247, 0))
    font_distance_covered = font.render("{} km.".format(round(distance_covered / 1000, 3)), 1, (255, 255, 255))
    font_score = font.render("Score:", 1, (255, 247, 0))
    font_score_scored = font.render("{}".format(score), 1, (255, 255, 255))
    font_lives = font.render("Lives remain:",1,(255,247,0))
    font_lives_remain = font.render("{}".format(my_plane.lives),1,(255,255,255))
    font_level = font.render("Level:", 1, (255,247,0))
    font_level_now = font.render("{}".format(level), 1, (255,255,255))
    plane_image = pygame.image.load('hero.jpg').convert()
    plane_image.set_colorkey((255, 255, 255))
    plane_image = pygame.transform.scale(plane_image, (105, 105))
    rect_plane = plane_image.get_rect(topleft=(50, 690))
    information.blit(font_health, (20, 15))
    pygame.draw.rect(information, (255, 0, 0), (60, 60, 30, my_plane.xp * 2))
    pygame.draw.rect(information, (180, 180, 180), (110, 60, 30, my_plane.bron * 2))
    information.blit(font_distance, (45, 300))
    information.blit(font_distance_covered, (45, 340))
    information.blit(font_score, (65, 400))
    information.blit(font_score_scored, (75, 440))
    information.blit(font_lives, (25,500))
    information.blit(font_lives_remain, (95,540))
    information.blit(font_level, (70,600))
    information.blit(font_level_now, (95,640))
    information.blit(plane_image, rect_plane)
    field.blit(information, (600, 0))
    field.blit(my_plane.image, my_plane.rect)
    stars = pygame.sprite.Group()
    lasers = pygame.sprite.Group()
    enemies = pygame.sprite.Group()
    elasers = pygame.sprite.Group()
    bonuses = pygame.sprite.Group()
    explodes = pygame.sprite.Group()
    shooting = {'LEFT': 'RIGHT', 'RIGHT': 'LEFT'}
    for i in range(randint(1, 2)):
        Star(randint(0, 570), stars)
    pygame.display.update()
    pygame.mouse.set_visible(0)
    while 1:
        clock.tick(60)
        for i in pygame.event.get():
            if i.type == pygame.KEYUP and i.key == pygame.K_ESCAPE:
                exit()
            if i.type == pygame.USEREVENT + 0 and IN_GAME:
                for k in range(randint(1, 2)):
                    Star(randint(0, 570), stars)
            if i.type == pygame.USEREVENT + 1 and IN_GAME:
                center = randint(40, 560)
                Enemy(center, enemies)
            if i.type == pygame.USEREVENT + 3 and IN_GAME:
                Bonus(randint(30, 570), bonuses)
            if i.type == pygame.USEREVENT + 2 and IN_GAME:
                for m in enemies:
                    if m.rect.bottomleft[1] < my_plane.rect.topleft[1]:
                        if my_plane.rect.topleft[0] <= m.rect.center[0] <= my_plane.rect.topright[0] or \
                                my_plane.rect.topleft[0] <= m.rect.topleft[0] <= my_plane.rect.topright[0] or \
                                my_plane.rect.topleft[0] <= m.rect.topright[0] <= my_plane.rect.topright[0]:
                            ELaser(elasers, m)
            if i.type == pygame.KEYUP and i.key == pygame.K_RETURN and not IN_GAME:
                my_plane.rect.x = 265
                my_plane.rect.y = 665
                my_plane.xp = 100
                my_plane.bron = 50
                my_plane.lives = 0
                distance_covered = 0
                score = 0
                level = 1
                stars.empty()
                lasers.empty()
                enemies.empty()
                elasers.empty()
                bonuses.empty()
                explodes.empty()
                shoot = 'LEFT'
                IN_GAME = True
        if IN_GAME:
            distance_covered += 1
            keypressed = pygame.key.get_pressed()
            if keypressed[pygame.K_w] or keypressed[pygame.K_a] or keypressed[pygame.K_d] or keypressed[pygame.K_s]:
                if keypressed[pygame.K_s]:
                    my_plane.update('DOWN')
                elif keypressed[pygame.K_w]:
                    my_plane.update('UP')
                elif keypressed[pygame.K_a]:
                    my_plane.update('LEFT')
                else:
                    my_plane.update('RIGHT')
            if my_plane.hidden:
                sec = pygame.time.get_ticks()
                if (sec-get_sec)/1000 >= 3:
                    my_plane.hidden = False
                    my_plane.image.set_alpha(255)
            field.blit(BACKGROUND, (0, 0))
            information.fill((33, 32, 32))
            information.blit(font_health, (20, 15))
            pygame.draw.rect(information, (255, 0, 0), (60, 60, 30, my_plane.xp * 2))
            pygame.draw.rect(information, (180, 180, 180), (110, 60, 30, my_plane.bron * 2))
            information.blit(font_distance, (45, 300))
            font_distance_covered = font.render("{} km.".format(round(distance_covered / 1000, 3)), 1, (255, 255, 255))
            font_score_scored = font.render("{}".format(score), 1, (255, 255, 255))
            font_lives_remain = font.render("{}".format(my_plane.lives), 1, (255, 255, 255))
            font_level_now = font.render("{}".format(level), 1, (255, 255, 255))
            information.blit(font_distance_covered, (45, 340))
            information.blit(font_score, (65, 400))
            information.blit(font_score_scored, (75, 440))
            information.blit(plane_image, rect_plane)
            information.blit(font_lives, (25, 500))
            information.blit(font_lives_remain, (95, 540))
            information.blit(font_level, (70, 600))
            information.blit(font_level_now, (95, 640))
            field.blit(information, (600, 0))
            stars.draw(field)
            stars.update()
            mousepressed = pygame.mouse.get_pressed()
            if mousepressed[0] and IN_GAME:
                for event in pygame.event.get():
                    if event.type == pygame.USEREVENT + 4:
                        Laser(lasers)
            if lasers:
                lasers.draw(field)
                lasers.update()
                for i in lasers:
                    for k in enemies:
                        if pygame.sprite.collide_circle_ratio(0.7)(i, k):
                            Explode(k.rect,explodes,full=False)
                            score += 1
                            i.kill()
                            change_xp_and_bron(k, 3, k)
                            if k.rect.y - ships[k.enemy][4] < 0:
                                k.rect.y = 0
                            else:
                                k.rect.y -= ships[k.enemy][4]
                            k.check_xp()
            if bonuses:
                bonuses.draw(field)
                bonuses.update()
                for i in bonuses:
                    if pygame.sprite.collide_circle_ratio(0.7)(my_plane, i):
                        if 'health' in i.icon:
                            if my_plane.xp + 30 > 100:
                                my_plane.xp = 100
                            else:
                                my_plane.xp += 30
                        elif 'bronya' in i.icon:
                            if my_plane.bron + 30 > 100:
                                my_plane.bron = 100
                            else:
                                my_plane.bron += 30
                        elif 'heart' in i.icon:
                            my_plane.lives += 1
                        i.kill()
            field.blit(my_plane.image, my_plane.rect)
            if elasers:
                elasers.draw(field)
                elasers.update()
                if not my_plane.hidden:
                    for elaser in elasers:
                        if pygame.sprite.collide_circle_ratio(0.7)(my_plane, elaser):
                            Explode(my_plane.rect,explodes,full=False)
                            elaser.kill()
                            change_xp_and_bron(elaser, 5, my_plane)
                            my_plane.check_xp()
                            if my_plane.rect.y + 70 + ships[elaser.enemy][6] > 800:
                                my_plane.rect.y = 720
                            else:
                                my_plane.rect.y += ships[elaser.enemy][6]
            if enemies:
                enemies.draw(field)
                enemies.update()
                for i in enemies:
                    pygame.draw.rect(field, (255, 0, 0), (i.rect.topleft[0], i.rect.topleft[1] - 40, round(i.xp*(ships[i.enemy][12]/100)), 5))
                    pygame.draw.rect(field, (180, 180, 180),
                                     (i.rect.topleft[0], i.rect.topleft[1] - 20, round(i.bron*(ships[i.enemy][12]/100)), 5))
                    if not my_plane.hidden:
                        if pygame.sprite.collide_circle_ratio(0.7)(my_plane, i):
                            Explode(my_plane.rect,explodes)
                            score += ships[i.enemy][7]
                            change_xp_and_bron(i, 10, i)
                            change_xp_and_bron(i, 11, my_plane)
                            i.check_xp()
                            my_plane.check_xp()
                            if my_plane.rect.y > i.rect.topleft[1]:
                                if i.rect.y - ships[i.enemy][8] < 0:
                                    i.rect.y = 0
                                else:
                                    i.rect.y -= ships[i.enemy][8]
                                if my_plane.rect.y + 70 + ships[i.enemy][9] > 800:
                                    my_plane.rect.y = 720
                                else:
                                    my_plane.rect.y += ships[i.enemy][9]
                            else:
                                i.rect.y += ships[i.enemy][8]
                                if 0 > my_plane.rect.y - ships[i.enemy][9]:
                                    my_plane.rect.y = 0
                                else:
                                    my_plane.rect.y -= ships[i.enemy][9]
            if explodes:
                explodes.draw(field)
                for i in explodes:
                    i.number += 1
                    i.image = pygame.image.load('fire{}.png'.format(i.number)).convert_alpha()
                    i.image.set_colorkey((255, 255, 255))
                    if i.full:
                        i.image = pygame.transform.scale(i.image, (80, 80))
                    else:
                        i.image = pygame.transform.scale(i.image, (30,30))
                    i.rect = i.image.get_rect(center=i.ship_coords)
                    if i.full:
                        i.if_over()
                    else:
                        i.if_over1()
        else:
            ffont = pygame.font.SysFont('verdana', 40)
            ffontdesc = ffont.render('You were destroyed!', 1, (255, 0, 0))
            ffontdist = ffont.render('Distance covered: {} km.'.format(round(distance_covered / 1000, 3)), 1,
                                     (255, 0, 0))
            ffontscor = ffont.render('Scored: {} points.'.format(score), 1, (255, 0, 0))
            ffontone = ffont.render('Press ENTER to restart or ESC to exit!', 1, (255, 0, 0))
            field.fill((0, 0, 0))
            field.blit(ffontdesc, (200, 50))
            field.blit(ffontdist, (50, 200))
            field.blit(ffontscor, (50, 280))
            field.blit(ffontone, (30, 430))
            pygame.draw.line(field, (255, 0, 0), (30, 500), (785, 500), 5)
        check_level()
        pygame.display.update()


pygame.init()
field = pygame.display.set_mode((800,800), pygame.FULLSCREEN)
menu = pygame_menu.Menu(400,400, 'Shooter 2D', theme=pygame_menu.themes.THEME_ORANGE)
menu.add_button('Play', start_game)
menu.add_button('Quit', pygame_menu.events.EXIT)
menu.mainloop(field)
