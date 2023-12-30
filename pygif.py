#!/usr/bin/env python3

from importlib import import_module, reload
from PIL import Image, ImageDraw, ImageTk
from tkinter import Tk, Label
import os
import argparse

class Scene:
    def __init__(self):
        self.particles = []
        # 2
        self.add(Rocket(60, 240, (100,100,200),  9, 15))
        self.add(Rocket(70, 240, (100,150,150), 10, 15))
        self.add(Rocket(80, 240, (100,200,100), 10, 15))
        self.add(Rocket(90, 240, ( 75,250, 75),  9, 15))
        self.add(Rocket(90, 240, ( 75,250, 75),  8, 15))
        self.add(Rocket(80, 240, (100,200,100),  7, 15))
        self.add(Rocket(70, 240, (100,150,150),  6, 15))
        self.add(Rocket(60, 240, (100,100,200),  5, 15))
        self.add(Rocket(70, 240, (100,150,150),  5, 15))
        self.add(Rocket(80, 240, (100,200,100),  5, 15))
        self.add(Rocket(90, 240, ( 75,250, 75),  5, 15))
        # 0
        self.add(Rocket(110, 240, (250,250,  0),  9, 15))
        self.add(Rocket(120, 240, (250,200,  0), 10, 15))
        self.add(Rocket(130, 240, (250,150,  0), 10, 15))
        self.add(Rocket(140, 240, (259,100,  0),  9, 15))
        self.add(Rocket(110, 240, (250,250,  0),  8, 15))
        self.add(Rocket(110, 240, (250,255,  0),  7, 15))
        self.add(Rocket(140, 240, (255,100,  0),  8, 15))
        self.add(Rocket(140, 240, (255,100,  0),  7, 15))
        self.add(Rocket(110, 240, (250,250,  0),  6, 15))
        self.add(Rocket(120, 240, (250,200,  0),  5, 15))
        self.add(Rocket(130, 240, (250,150,  0),  5, 15))
        self.add(Rocket(140, 240, (250,100,  0),  6, 15))
        # 2
        self.add(Rocket(160, 240, (250,100,100),  9, 15))
        self.add(Rocket(170, 240, (250,  0,150), 10, 15))
        self.add(Rocket(180, 240, (250,  0,200), 10, 15))
        self.add(Rocket(190, 240, (250,  0,250),  9, 15))
        self.add(Rocket(190, 240, (250,  0,250),  8, 15))
        self.add(Rocket(180, 240, (250,  0,200),  7, 15))
        self.add(Rocket(170, 240, (250,  0,150),  6, 15))
        self.add(Rocket(160, 240, (250,100,100),  5, 15))
        self.add(Rocket(170, 240, (250,  0,150),  5, 15))
        self.add(Rocket(180, 240, (250,  0,200),  5, 15))
        self.add(Rocket(190, 240, (250,  0,250),  5, 15))
        # 4
        self.add(Rocket(210, 240, (200,  0,250), 10, 15))
        self.add(Rocket(210, 240, (200,  0,250),  9, 15))
        self.add(Rocket(210, 240, (200,  0,250),  8, 15))
        self.add(Rocket(220, 240, (150,  0,250),  7, 15))
        self.add(Rocket(230, 240, (100,  0,250),  7, 15))
        self.add(Rocket(240, 240, ( 50,  0,250), 10, 15))
        self.add(Rocket(240, 240, ( 50,  0,250),  9, 15))
        self.add(Rocket(240, 240, ( 50,  0,250),  8, 15))
        self.add(Rocket(240, 240, ( 50,  0,250),  7, 15))
        self.add(Rocket(240, 240, ( 50,  0,250),  6, 15))
        self.add(Rocket(240, 240, ( 50,  0,250),  5, 15))

    def update(self):
        for particle in self.particles:
            particle.update(self)
                
        image = Image.new("RGB", (320, 240), (0,0,32))
        canvas = ImageDraw.Draw(image)
        for particle in self.particles:
            particle.draw(canvas)
        return image
    
    def add(self, particle):
        self.particles.append(particle)

    def remove(self, particle):
        self.particles.remove(particle)


class BaseParticle:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color

    def draw(self, canvas):
        canvas.ellipse((self.x, self.y, self.x + 5, self.y + 5), fill=self.color)

    def update(self, scene):
        pass

class Particle(BaseParticle):
    def __init__(self, x, y, color, speed_x, speed_y):
        BaseParticle.__init__(self, x, y, color)
        self.speed_x = speed_x
        self.speed_y = speed_y
        self.gravity = 1

    def fade(self):
        self.color = (
            self.color[0] - 10 if self.color[0] > 10 else 0,
            self.color[1] - 10 if self.color[1] > 10 else 0,
            self.color[2] - 10 if self.color[2] > 10 else 0)
    
    def update(self, scene):
        self.x += self.speed_x
        self.y -= self.speed_y
        self.speed_y -= self.gravity
        self.fade()
        if 0 == self.color[0] and 0 == self.color[1] and 0 == self.color[2]:
            scene.remove(self)

class Rocket(BaseParticle):
    def __init__(self, x, y, color, speed, count):
        BaseParticle.__init__(self, x, y, color)
        self.speed = speed
        self.count = count
        self.initial_y = y
        self.initial_count = count

    def reset(self):
        self.y = self.initial_y
        self.count = self.initial_count

    def update(self, scene):
        if self.count > 0:
            self.count -= 1
            self.y -= self.speed
        else:
            scene.add(Particle(self.x, self.y, self.color, 5, 10))
            scene.add(Particle(self.x, self.y, self.color, -5, 10))
            scene.add(Particle(self.x, self.y, self.color, 5, 0))
            scene.add(Particle(self.x, self.y, self.color, -5, 0))
            self.reset()

def create_image():
    image = Image.new("RGB", (320, 240), (0,0,32))
    return image

def update(root, label, scene):
    global pygif, mtime
    time = os.path.getmtime(__file__)
    if time != mtime:
        print("reload")
        mtime = time
        pygif = reload(pygif)
        scene = pygif.Scene()
    image = scene.update()
    img = ImageTk.PhotoImage(image)
    label.configure(image = img)
    label.image = img
    label.pack()
    root.after(100, lambda: update(root, label, scene))

def visu():
    root = Tk()
    root.title("PyGif")

    image = create_image()
    test = ImageTk.PhotoImage(image)
    label = Label(root, image=test)
    label.pack()
    root.after(100, lambda: update(root, label, Scene()))

    root.resizable(False,False)
    root.mainloop()

def write_gif(filename):
    scene = Scene()
    frames = []
    for n in range(56):
        frames.append(scene.update())
    
    image = frames[14]
    image.save(filename, format="GIF", append_images=frames,
               save_all=True, duration=0, loop=0)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--filename', '-f', type=str, required=False, default=None)
    args = parser.parse_args()
    if args.filename == None:
        visu()
    else:
        write_gif(args.filename)

if __name__ == "__main__":
    pygif = import_module("pygif")
    mtime = os.path.getmtime(__file__)
    main()
