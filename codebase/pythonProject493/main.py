import pygame
import math
from pygame import mixer

pygame.init()

# setting up general
width, height = 1200, 800
wn = pygame.display.set_mode((width, height))
pygame.display.set_caption("Planet Simulation")
bg = pygame.image.load("space.gif")
mixer.init()
mixer.music.load("sky walker.mp3")
FONT = pygame.font.SysFont('consolas', 16)

# different planet color
Venus = (193, 143, 23)
Sun = (253, 184, 19)
Earth = (79, 76, 176)
Mars = (193, 68, 14)
Mercury = (173, 168, 165)


class Planet:
    AU = 149.6e6 * 1000
    G = 6.67428e-11
    scale = 200 / AU
    TIMESTEP = 3600 * 6  # half a day

    def __init__(self, name, x, y, radius, color, mass):
        self.x = x
        self.y = y
        self.radius = radius
        self.color = color
        self.mass = mass
        self.name = name

        self.orbit = []
        self.sun = False  # the Sun will not move
        self.distance_to_sun = 0

        self.x_vel = 0
        self.y_vel = 0

    def attraction(self, other):
        other_x, other_y = other.x, other.y
        distance_x = other_x - self.x
        distance_y = other_y - self.y
        distance = math.sqrt(distance_x ** 2 + distance_y ** 2)

        if other.sun:
            self.distance_to_sun = distance

        force = self.G * self.mass * other.mass / distance ** 2
        theta = math.atan2(distance_y, distance_x)
        force_x = math.cos(theta) * force
        force_y = math.sin(theta) * force
        return force_x, force_y

    def update_position(self, planets):
        total_fx = total_fy = 0
        for planet in planets:
            if self == planet:
                continue

            fx, fy = self.attraction(planet)
            total_fx += fx
            total_fy += fy

        self.x_vel += total_fx / self.mass * self.TIMESTEP
        self.y_vel += total_fy / self.mass * self.TIMESTEP

        self.x += self.x_vel * self.TIMESTEP
        self.y += self.y_vel * self.TIMESTEP
        self.orbit.append((self.x, self.y))

    def draw(self, wn):
        x = self.x * self.scale + width / 2
        y = self.y * self.scale + height / 2

        if len(self.orbit) > 2:
            updated_points = []
            for point in self.orbit:
                x, y = point
                x = x * self.scale + width / 2
                y = y * self.scale + height / 2
                updated_points.append((x, y))

            pygame.draw.lines(wn, self.color, False, updated_points, 2)

        pygame.draw.circle(wn, self.color, (x, y), self.radius)

        planet_name = FONT.render(self.name, 1, "white")

        if not self.sun:
            wn.blit(planet_name, (x - planet_name.get_width() / 2, (y - 20) - planet_name.get_height() / 2))
        elif self.sun:
            wn.blit(planet_name, (x - planet_name.get_width() / 2, y - planet_name.get_height() / 2))


def main():
    run = True
    clock = pygame.time.Clock()

    sun = Planet("Sun", 0, 0, 30, Sun, 1.98892 * 10 ** 30)
    sun.sun = True

    earth = Planet("Earth", -1 * Planet.AU, 0, 16, Earth, 5.9742 * 10 ** 24)
    earth.y_vel = 29.783 * 1000

    mercury = Planet("Mercury", 0.387 * Planet.AU, 0, 8, Mercury, 3.30 * 10 ** 23)
    mercury.y_vel = -47.4 * 1000

    venus = Planet("Venus", 0.723 * Planet.AU, 0, 14, Venus, 4.8685 * 10 ** 24)
    venus.y_vel = -35.02 * 1000

    mars = Planet("Mars", -1.524 * Planet.AU, 0, 12, Mars, 6.39 * 10 ** 23)
    mars.y_vel = 24.077 * 1000

    planets = [sun, earth, mars, mercury, venus]

    mixer.music.play(loops=10000000)
    while run:
        clock.tick(60)
        wn.fill((0, 0, 0))
        wn.blit(bg, (0, 0))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        for planet in planets:
            planet.update_position(planets)
            planet.draw(wn)

        pygame.display.update()

    pygame.quit()


main()
