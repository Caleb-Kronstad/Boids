#imports
import pygame as py

class Cache:
    def __init__(this):
        this.text_cache = {}
        this.image_cache = {}

    def LoadImage(this, path, convert_alpha=True):
        if path not in this.image_cache:
            if convert_alpha == True:
                this.image_cache[path] = py.image.load(path).convert_alpha()
            else:
                this.image_cache[path] = py.image.load(path)
        return this.image_cache[path]

    def RenderText(this, font, text, color, antialiasing=True):
        key = (font, text, color)
        if key not in this.text_cache:
            text_surface = font.render(text, antialiasing, color)
            this.text_cache[key] = text_surface
        return this.text_cache[key]