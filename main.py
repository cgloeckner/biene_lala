import pygame
import math
import random

class GameObject(object):
    def __init__(self, image, pos, speed):
        self.image = image
        self.position = pygame.math.Vector2(pos)
        self.move = pygame.math.Vector2()
        self.speed = speed

    def update(self, delta_time):
        self.position += self.move * self.speed * delta_time / 1000

        if self.position.y < 0:
            self.position.y = 0
        if self.position.y > 600:
            self.position.y = 600

    def draw(self, window):
        size = self.image.get_size()
        center_pos = self.position.x - size[0] // 2, self.position.y - size[1] // 2

        if self.move.x < 0:
            img = pygame.transform.flip(self.image, flip_x=True, flip_y=False)
        else:
            img = self.image

        window.blit(img, center_pos)


class FlyingObject(GameObject):
    def __init__(self, image, pos, speed):
        super().__init__(image, pos, speed)

        self.animation = random.randrange(1000)

    def update(self, delta_time):
        super().update(delta_time)

        self.animation += delta_time / 1000

        angle = 2 * math.pi * self.animation
        self.position.y += math.sin(angle)


def neue_wespe(wespe_img):
    pos_y = random.randrange(550) + 25
    speed = random.randrange(50) + 200

    obj = FlyingObject(wespe_img, (800 + wespe_img.get_size()[0] // 2, pos_y), speed)
    obj.move.x = -1

    return obj


def neues_gras(gras_img, speed):
    obj = GameObject(gras_img, (800 + gras_img.get_size()[0] // 2, 400), speed)
    obj.move.x = -1

    return obj

def neuer_felsen(felsen_img, speed):
    pos_y = random.randrange(50)+525
    obj = GameObject(felsen_img, (800 + felsen_img.get_size()[0] // 2, pos_y), speed)
    obj.move.x = -1

    return obj

def is_on_screen(obj):
    x = obj.position.x + obj.image.get_size()[0] // 2
    return x >= 0


def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()

    biene_img = pygame.transform.scale_by(pygame.image.load('biene.png'), 0.125)
    wespe_img = pygame.transform.scale_by(pygame.image.load('wespe.png'), 0.25)
    gras_img = pygame.image.load('gras.png')
    felsen_img = pygame.transform.scale_by(pygame.image.load('felsen.png'), 0.5)

    biene_obj = FlyingObject(biene_img, (biene_img.get_size()[0] // 2 + 50, 300), 250)

    alle_wespen = list()

    alles_gras = list()
    alles_gras.append(neues_gras(gras_img, biene_obj.speed))

    alle_felsen = list()
    alle_felsen.append(neuer_felsen(felsen_img, biene_obj.speed))

    running = True
    elapsed = 0
    timer = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False

        keys = pygame.key.get_pressed()
        biene_obj.move = pygame.math.Vector2()
        if keys[pygame.K_UP]:
            biene_obj.move.y = -1
        if keys[pygame.K_DOWN]:
            biene_obj.move.y = 1

        biene_obj.update(elapsed)

        for obj in alle_wespen:
            obj.update(elapsed)
            if not is_on_screen(obj):
                alle_wespen.remove(obj)

        for obj in alles_gras:
            obj.update(elapsed)
            if not is_on_screen(obj):
                alles_gras.remove(obj)

        for obj in alle_felsen:
            obj.update(elapsed)
            if not is_on_screen(obj):
                alle_felsen.remove(obj)

        if timer > 1000:
            alle_wespen.append(neue_wespe(wespe_img))
            alles_gras.append(neues_gras(gras_img, biene_obj.speed))
            alle_felsen.append(neuer_felsen(felsen_img, biene_obj.speed))
            timer -= 1000

        screen.fill('lightblue')

        for obj in alle_felsen:
            obj.draw(screen)

        for obj in alle_wespen:
            obj.draw(screen)

        biene_obj.draw(screen)

        for obj in alles_gras:
            obj.draw(screen)

        pygame.display.flip()

        elapsed = clock.tick(60)
        timer += elapsed

        pygame.display.set_caption(f'Biene Lala - FPS: {clock.get_fps():.1f}')

    pygame.quit()


if __name__ == '__main__':
    main()