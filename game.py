import pygame
import math
import sqlite3
global W
global H
pygame.init()
db = sqlite3.connect('local.db')
cur = db.cursor()
cur.execute('''CREATE TABLE IF NOT EXISTS Media(
                title TEXT,cor1 INT,cor2 INT)''')

def run():
    class Button():
        def __init__(self, text, x, y):
            self.text = text
            self.x = x
            self.y = y
            self.font = pygame.font.SysFont('Arial', 30, 1, 0)
            colour = pygame.color.Color('#FFFFFF')
            self.text = self.font.render("RESTART", True, colour)
            self.rect = self.text.get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

        def show(self):
            screen.blit(self.text,(self.x,self.y))

        def click(self):
            while 1:
                clic=pygame.mouse.get_pressed()
                x, y = pygame.mouse.get_pos()
                even=pygame.event.wait()
                if clic[0]:
                    is_inside = self.rect.collidepoint(x, y)
                    if is_inside:
                        start()
                        break

            values = {
                'title': ' АВАРИЯ! '
            }
            cur.execute("insert into Media values(?,?,?)", [values['title'],mainx,mainy])
            a = cur.execute("SELECT* from Media")
            db.commit()
            for el in cur:
                if a.lastrowid>10:
                    cur.execute("DROP TABLE Media")
                    cur.execute('''CREATE TABLE IF NOT EXISTS Media(
                                    title TEXT,cor1 INT,cor2 INT)''')
                print(el)

    def control_main_car():
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            main_car[1] -= speed
        elif keys[pygame.K_DOWN]:
            main_car[1] += speed
        elif keys[pygame.K_RIGHT]:
            main_car[0] += speed
        elif keys[pygame.K_LEFT]:
            main_car[0] -= speed

        if main_car[0] > W - carwidth:
            main_car[0] = W - carwidth
        elif main_car[0] < 0:
            main_car[0] = 0
        elif main_car[1] < 0:
            main_car[1] = 0
        elif main_car[1] > H - carheight:
            main_car[1] = H - carheight

    def move_enemy():

        speed_enemy=7
        car1[1]+=speed_enemy
        car2[1]-=speed_enemy
        if car1[1]>H:
            car1[1]=0
        elif car2[1]<0:
            car2[1]=H

    def check_game_over(main_car, carx):
        distance= math.sqrt(math.pow(main_car[0] - carx[0], 2) + math.pow(carx[1] - main_car[1], 2))
        if distance<carwidth: return True
        else: return False
    def start():
        screen.fill((0, 0, 0))
        nonlocal x0
        if x0 >-50:
            x0 = -100
        for i in range(20):
            if x0<H:
                screen.blit(road,(0,road_increm*i+x0),road_crop)
            elif x0>H:
                x0=-100
        x0 += 7
        screen.blit(car_main, main_car)
        screen.blit(car_enemy, car1)
        screen.blit(car_enemy, car2)


    W = 800
    H = 750
    screen = pygame.display.set_mode((W, H))
    car_main = pygame.image.load('D:/Scripts/car2.png')# нужно ввести свой путь до изображения
    car_main = pygame.transform.scale(car_main, (W // 10, H // 12))
    carwidth = car_main.get_rect().width
    carheight = car_main.get_rect().height
    main_car = [W // 2, H // 2]
    speed = 15
    car_enemy= pygame.image.load('D:/Scripts/car2.png')# нужно ввести свой путь до изображения
    car_enemy = pygame.transform.scale(car_main, (W // 10, H // 12))
    car1=[W//8,0]
    car2 = [W//1.2,H-carheight]
    pygame.display.flip()
    road=pygame.image.load('D:/Scripts/fon.jpg')# нужно ввести свой путь до изображения
    road_crop=(325,0,W,50)
    road_increm=road_crop[3]
    x0 = -100
    mainx = 0
    mainy = 0
    clock=pygame.time.Clock()
    button=Button("RESTART",350,350)
    while 1:
        for event in pygame.event.get():
            if event.type==pygame.QUIT:
                exit()
                cur.close()

        start()
        control_main_car()
        move_enemy()

        if check_game_over(main_car,car1) or check_game_over(main_car,car2):
            mainx = main_car[0]
            mainy = main_car[1]
            main_car = [W // 2, H // 2]
            screen.fill((255, 0, 0))
            button.show()
            pygame.time.delay(200)
            pygame.display.flip()
            button.click()

        clock.tick(60)
        pygame.display.update()

if __name__=="__main__":
    run()
