import pygame
from pygame.locals import *
from random import choice
import sqlite3
import subprocess


def run_second_file():
    subprocess.run(["new_backpack.exe"])
    return False


class Bacppack:
    def __init__(self):
        self.con = sqlite3.connect("Sql/data.sqlite")
        self.cur = self.con.cursor()
        self.result = self.cur.execute("""SELECT * FROM equipped_items""").fetchall()

    def Xp_b(self):
        if 'Ласточка' in self.result[0]:
            return 200
        else:
            return 100

    def hil_b(self):
        if 'Полнолуние' in self.result[0]:
            return 100
        else:
            return 50

    def speed(self):
        if 'Филин' in self.result[0]:
            return 10
        else:
            return 5

    def ult(self):
        if 'Черная дурь' in self.result[0]:
            return 150
        else:
            return 0

    def stam(self):
        if 'Бякко' in self.result[0]:
            return 100
        else:
            return 0


class enemys:
    def __init__(self):
        self.chance_cpavna = [1, 1, 1, 1, 1, 1, 1, 1, 1]
        self.mobs = []
        self.count_mob = 0
        self.enemy_levo = [pygame.image.load('enemy_lev/1.png'), pygame.image.load('enemy_lev/2.png'),
                           pygame.image.load('enemy_lev/3.png'), pygame.image.load('enemy_lev/4.png'),
                           pygame.image.load('enemy_lev/5.png'), pygame.image.load('enemy_lev/6.png')]

        self.enemy_prav = [pygame.image.load('enemy/1.png'), pygame.image.load('enemy/2.png'),
                           pygame.image.load('enemy/3.png'), pygame.image.load('enemy/4.png'),
                           pygame.image.load('enemy/5.png'), pygame.image.load('enemy/6.png')]
        self.atack_prav = [pygame.image.load('enemy_atack_prav/1.png'), pygame.image.load('enemy_atack_prav/2.png'),
                           pygame.image.load('enemy_atack_prav/3.png'), pygame.image.load('enemy_atack_prav/4.png'),
                           pygame.image.load('enemy_atack_prav/5.png'), pygame.image.load('enemy_atack_prav/6.png')]

        self.atack_lev = [pygame.image.load('enemy_atack_lev/1.png'), pygame.image.load('enemy_atack_lev/2.png'),
                          pygame.image.load('enemy_atack_lev/3.png'), pygame.image.load('enemy_atack_lev/4.png'),
                          pygame.image.load('enemy_atack_lev/5.png'), pygame.image.load('enemy_atack_lev/6.png')]

        self.Right_enemy = True

        self.atack_count = -1
        self.atack_true = False
        self.count_enemy = 30
        self.gdu = 0
        self.uron = 1

    def spavner_mobov(self):
        if self.count_mob < self.count_enemy:
            x_spawn = choice([(i - 200) for i in range(1401)])
            y_spawn = choice([i for i in range(-200, 1001) if i < 0 or i > 800])
            mob = choice(self.chance_cpavna)
            if mob == 1:
                self.mobs.append([1, 100, x_spawn, y_spawn, 1, self.uron, 0, 0, True, False])
            elif mob == 2:
                self.mobs.append([1, 200, x_spawn, y_spawn, 0.5, 3, 0, 0, True, False])
            self.count_mob += 1
        c = 0
        for i in self.mobs:
            if len(i) == 10:
                c += 1
        if c == 0:
            self.count_mob = 0
            self.uron += 2

    def peredvigenye(self, x_player, y_player):
        for i in self.mobs:
            if len(i) == 10:
                if x_player > i[2] and y_player > i[3]:
                    i[8] = True
                    i[2] += i[4]
                    i[3] += i[4]
                elif x_player < i[2] and y_player < i[3]:
                    i[8] = False
                    i[2] -= i[4]
                    i[3] -= i[4]
                elif x_player < i[2]:
                    i[8] = False
                    i[2] -= i[4]
                elif y_player < i[3]:
                    i[3] -= i[4]
                elif x_player > i[2]:
                    i[8] = True
                    i[2] += i[4]
                elif y_player > i[3]:
                    i[3] += i[4]

    def otrisovka(self):
        for i in self.mobs:
            if len(i) == 10:
                if i[0] == 1:
                    if 0 < i[1]:
                        i[7] += 1
                        if i[8] is True:
                            if i[9] is True:
                                if i[6] >= 59:
                                    i[6] = 1
                                    i[9] = False
                                screen.blit(self.atack_prav[i[6] // 10], (i[2], i[3]))
                            else:
                                if i[7] >= 59:
                                    i[7] = 1
                                screen.blit(self.enemy_prav[i[7] // 10], (i[2], i[3]))
                        else:
                            if i[9] is True:
                                if i[6] >= 59:
                                    i[6] = 1
                                    i[9] = False
                                screen.blit(self.atack_lev[i[6] // 10], (i[2], i[3]))
                            else:
                                if i[7] >= 59:
                                    i[7] = 1
                                screen.blit(self.enemy_levo[i[7] // 10], (i[2], i[3]))
                        pygame.draw.rect(screen, (0, 0, 0), (i[2], i[3], 50, 5))
                        pygame.draw.rect(screen, (155, 0, 0), (i[2], i[3], i[1] // 2, 5))
                elif i[0] == 2:
                    if 0 < i[1]:
                        pass
            if len(i) == 3:
                screen.blit(pygame.image.load('Death/death_enemy.png'), (i[1], i[2]))

    def udar_enemy(self, x_player, y_player):
        uron = 0
        for i in self.mobs:
            if len(i) == 10:
                if i[0] == 1:
                    enemy_rect = Rect((i[2] - 20, i[3] - 20, 100, 140))
                    if enemy_rect.collidepoint(x_player + 10, y_player + 10):
                        if i[6] == 0 or i[6] % 5 == 0:
                            i[6] += 1
                            uron = + i[5]
                            i[9] = True
                        else:
                            i[6] += 1
                elif i[0] == 2:
                    enemy_rect = Rect((i[2] - 50, i[3] - 50, 175, 175))
                    if enemy_rect.collidepoint(x_player + 10, y_player + 10):
                        if i[6] == 0 or i[6] % 5 == 0:
                            i[6] += 1
                            uron = + i[5]
                        else:
                            i[6] += 1
        return uron

    def poluchenie_urona(self, x_player, y_player):
        Exp = 0
        rect_atack = Rect((x_player - 50, y_player - 50, 100, 100))
        for i in self.mobs:
            if len(i) == 10:
                if rect_atack.collidepoint(i[2], i[3]):
                    i[1] -= 50
                    if i[1] <= 0:
                        del self.mobs[self.mobs.index(i)]
                        self.mobs.append([i[0], i[2], i[3]])
                        Exp += 100
        return Exp

    def poluchenie_urona_x(self):
        for i in self.mobs:
            if len(i) == 10:
                del self.mobs[self.mobs.index(i)]
                self.mobs.append([i[0], i[2], i[3]])

    def otodvig(self, x, y):
        for i in self.mobs:
            if len(i) == 3:
                i[1] += x
                i[2] += y
            else:
                i[2] += x
                i[3] += y


class person:
    def __init__(self):
        self.Go_lev = [pygame.image.load('levo/1.png'), pygame.image.load('levo/2.png'),
                       pygame.image.load('levo/3.png'), pygame.image.load('levo/4.png'),
                       pygame.image.load('levo/5.png'), pygame.image.load('levo/6.png'),
                       pygame.image.load('levo/7.png'), pygame.image.load('levo/8.png'),
                       pygame.image.load('levo/9.png'), pygame.image.load('levo/10.png'),
                       pygame.image.load('levo/11.png'), pygame.image.load('levo/12.png')]

        self.Go_prav = [pygame.image.load('pravo/1.png'), pygame.image.load('pravo/2.png'),
                        pygame.image.load('pravo/3.png'), pygame.image.load('pravo/4.png'),
                        pygame.image.load('pravo/5.png'), pygame.image.load('pravo/6.png'),
                        pygame.image.load('pravo/7.png'), pygame.image.load('pravo/8.png'),
                        pygame.image.load('pravo/9.png'), pygame.image.load('pravo/10.png'),
                        pygame.image.load('pravo/11.png'), pygame.image.load('pravo/12.png')]

        self.heal_lev = [pygame.image.load('Heal_Lev/1.png'), pygame.image.load('Heal_Lev/2.png'),
                         pygame.image.load('Heal_Lev/3.png'), pygame.image.load('Heal_Lev/4.png')]

        self.heal_prav = [pygame.image.load('Heal/1.png'), pygame.image.load('Heal/2.png'),
                          pygame.image.load('Heal/3.png'), pygame.image.load('Heal/4.png')]

        self.Atack_prav = [pygame.image.load('Atack_prav/1.png'), pygame.image.load('Atack_prav/2.png'),
                           pygame.image.load('Atack_prav/3.png'), pygame.image.load('Atack_prav/4.png'),
                           pygame.image.load('Atack_prav/5.png'), pygame.image.load('Atack_prav/6.png'),
                           pygame.image.load('Atack_prav/7.png'), pygame.image.load('Atack_prav/8.png'),
                           pygame.image.load('Atack_prav/9.png')]

        self.Atack_lev = [pygame.image.load('Atack_lev/1.png'), pygame.image.load('Atack_lev/2.png'),
                          pygame.image.load('Atack_lev/3.png'), pygame.image.load('Atack_lev/4.png'),
                          pygame.image.load('Atack_lev/5.png'), pygame.image.load('Atack_lev/6.png'),
                          pygame.image.load('Atack_lev/7.png'), pygame.image.load('Atack_lev/8.png'),
                          pygame.image.load('Atack_lev/9.png')]

        self.die = pygame.image.load('Death/Death.png')

    def Heal(self, x_per, y_per, Pravo, heal_count):
        if Pravo is True:
            screen.blit(self.heal_prav[heal_count], (x_per, y_per))
        else:
            screen.blit(self.heal_lev[heal_count], (x_per, y_per))

    def atack(self, x_per, y_per, Pravo, atack_count):
        if Pravo is True:
            screen.blit(self.Atack_prav[atack_count], (x_per, y_per))
        else:
            screen.blit(self.Atack_lev[atack_count], (x_per, y_per))

    def GO_GO(self, x_per, y_per, Pravo, c):
        if Pravo is True:
            screen.blit(self.Go_prav[c], (x_per, y_per))
        else:
            screen.blit(self.Go_lev[c], (x_per, y_per))

    def die_per(self, x, y):
        screen.blit(self.die, (x, y))


if __name__ == '__main__':
    pygame.init()
    count = 0
    pygame.display.set_caption('Движущийся круг 2')
    size = width, height = 1000, 800
    screen = pygame.display.set_mode(size)
    mapp = pygame.image.load(' Background/map.png').convert()
    print(mapp.get_rect())
    # _________________________________
    clock = pygame.time.Clock()
    running = True
    screen.fill((0, 0, 0))
    pygame.mouse.set_visible(False)
    x, y = width // 2 - 50, height // 2 - 30
    x_map, y_map = -1966, -1935
    # _____________________________________
    back = Bacppack()
    spped = back.speed()
    Go = 0
    heal = back.hil_b()
    atack_count = 0
    atack_True = False
    heal_true = False
    Right = True
    XP = back.Xp_b()
    stamina = back.stam()
    hilka = 100
    ulta = back.ult()
    Go_boot = False
    # _________________________________________
    rect_top_left = Rect((0, 0, 250, 200))
    rect_top_center = Rect((250, 0, 500, 200))
    rect_top_right = Rect((750, 0, 250, 200))
    rect_left = Rect((0, 200, 250, 400))
    rect_right = Rect((750, 200, 250, 400))
    rect_bottom_left = Rect((0, 600, 250, 200))
    rect_bottom_center = Rect((250, 600, 500, 200))
    rect_bottom_right = Rect((750, 600, 250, 200))
    V_enemy = 0.5
    # _________________________________
    enemyk = enemys()
    per = person()
    # ________________________________
    pygame.mixer.music.load('Sound/Sound.mp3')
    pygame.mixer.music.play()
    while running:
        keys = pygame.key.get_pressed()
        enemyk.spavner_mobov()
        screen.fill((0, 0, 0))
        screen.blit(mapp, (x_map, y_map))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                print("Нажата кнопка: ", event.button, x, y)  # atack.zaderjka()
                if stamina > 0:
                    if stamina == 100:
                        stamina -= 100
                        ulta += enemyk.poluchenie_urona(x, y)
                        atack_True = True
                        if ulta > 250:
                            ulta = 250
                        rect_atack = Rect((x - 15, y - 15, 100, 100))
                        print(rect_atack)
                else:
                    running = False
            elif keys[K_e]:
                if hilka == 100:
                    hilka -= 100
                    XP += 50
                    heal_true = True
                    if XP > 200:
                        XP = 200
            elif keys[K_x]:
                if ulta == 250:
                    ulta -= 250
                    enemyk.poluchenie_urona_x()
        if keys[K_b]:
            run_second_file()
        # ---------------------------------------------------
        if enemyk.udar_enemy(x, y) > 0:
            XP -= enemyk.udar_enemy(x, y)
        if keys[K_ESCAPE]:
            running = False
        if XP <= 0:
            per.die_per(x, y)
            screen.blit(pygame.image.load('Death/Death.png'), (x, y))
            running = False
        # _________________________________________________________________
        if keys[K_a] or keys[K_LEFT]:
            if Right is True:
                Right = False
                Go = 0
            else:
                if Go_boot is False:
                    Go += 1
                    if Go > 55:
                        Go = 0
            if x != 0:
                x -= spped
        elif keys[K_d] or keys[K_RIGHT]:
            if Right is False:
                Right = True
                Go = 0
            else:
                if Go_boot is False:
                    Go += 1
                    if Go > 55:
                        Go = 0
            if x != 900:
                x += spped
        elif keys[K_w] or keys[K_UP]:
            if Go_boot is False:
                Go += 1
                if Go > 55:
                    Go = 0
            if y != 0:
                y -= spped
        elif keys[K_s] or keys[K_DOWN]:
            if Go_boot is False:
                Go += 1
                if Go > 55:
                    Go = 0
            if y != 740:
                y += spped
        # ___________________________________________________________
        enemyk.peredvigenye(x, y)
        if rect_top_left.collidepoint(x, y):
            if x_map <= 0:
                x_map += 2
            if y_map <= 0:
                y_map += 2
            enemyk.otodvig(2, 2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_top_center.collidepoint(x, y):
            if y_map <= 0:
                y_map += 2
            enemyk.otodvig(0, 2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_top_right.collidepoint(x, y):
            if x_map >= -2932:
                x_map -= 2
            if y_map <= 0:
                y_map += 2
            enemyk.otodvig(-2, 2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_left.collidepoint(x, y):
            if x_map <= 0:
                x_map += 2
            enemyk.otodvig(2, 0)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_right.collidepoint(x, y):
            if x_map >= -2932:
                x_map -= 2
            enemyk.otodvig(-2, 0)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_bottom_left.collidepoint(x, y):
            if x_map <= 0:
                x_map += 2
            if y_map >= -3070:
                y_map -= 2
            enemyk.otodvig(2, -2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_bottom_center.collidepoint(x, y):
            if y_map >= -3070:
                y_map -= 2
            enemyk.otodvig(0, -2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        elif rect_bottom_right.collidepoint(x, y):
            if x_map >= -2932:
                x_map -= 2
            if y_map >= -3070:
                y_map -= 2
            enemyk.otodvig(-2, -2)
            Go_boot = True
            if Go_boot is True:
                Go += 1
                if Go > 55:
                    Go = 0
        else:
            Go_boot = False
        # -------------------------------------------------------------------------
        if stamina < 100:
            stamina += 5
        if hilka < 101:
            hilka += 0.1
            if hilka > 100:
                hilka = 100
        if ulta < 251:
            ulta += 0.1
            if ulta > 250:
                ulta = 250
        # ----------------------------------------------------------------------
        enemyk.otrisovka()
        if heal < 39 and heal_true:
            heal += 1
            per.Heal(x, y, Right, heal // 10)
            if heal == 39:
                heal = 0
                heal_true = False
        elif atack_count < 34 and atack_True:
            atack_count += 1
            per.atack(x, y, Right, atack_count // 5)
            if atack_count == 34:
                atack_count = 0
                atack_True = False
        else:
            per.GO_GO(x, y, Right, Go // 5)
        # __________________________________________________
        screen.blit(pygame.image.load('Interface/scale_hp.png'), (0, 0))
        color_xp = (136, 0, 21)
        pygame.draw.rect(screen, color_xp, (90, 29, XP * 1.2, 42))
        # __________________________________________________________
        stamina_color = (0, 0, 255)
        screen.blit(pygame.image.load('Interface/stroke_panel.png'), (850, 650))
        pygame.draw.rect(screen, stamina_color, (875, 675, stamina // 2, 50))
        screen.blit(pygame.image.load('Interface/mous.png'), (882, 600))
        # _____________________________________________________________
        hilka_color = (0, 255, 0)
        screen.blit(pygame.image.load('Interface/stroke_panel.png'), (700, 550))
        pygame.draw.rect(screen, hilka_color, (725, 575, hilka // 2, 50))
        screen.blit(pygame.image.load('Interface/e.png'), (732, 500))
        # _____________________________________________________________
        ulta_color = (255, 255, 255)
        screen.blit(pygame.image.load('Interface/stroke_panel.png'), (550, 650))
        pygame.draw.rect(screen, ulta_color, (575, 675, ulta // 5, 50))
        screen.blit(pygame.image.load('Interface/x.png'), (582, 600))
        screen.blit(pygame.image.load('Interface/Backpack_png.png'), (920, 5))
        screen.blit(pygame.image.load('Interface/b.png'), (940, 90))
        # ___________________________________________________________
        pygame.display.update()
        clock.tick(60)
    pygame.quit()
