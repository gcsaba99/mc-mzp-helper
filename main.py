import keyboard
import pygame
import sys
from PIL import Image, ImageChops
from pygame.locals import *
from pynput import keyboard

color_regions = []
color_image = pygame.image.load("colors.png")
color_image = pygame.transform.scale(color_image, (2560, 160))

colors = ['white', 'light gray', 'orange', 'cyan', 'magenta', 'purple', 'light blue', 'blue',
          'yellow', 'brown', 'lime', 'green', 'pink', 'red', 'gray', 'black']


def init_color_regions():
    image_colors = Image.open("colors.png")
    for i in range(len(colors)):
        color_region = image_colors.crop((i * 16, 0, 16 + i * 16, 16)).convert('RGB')
        color_regions.append(color_region)


def get_color(img_region):
    for i in range(len(colors)):
        color_region = color_regions[i]
        diff = ImageChops.difference(img_region, color_region)
        if not diff.getbbox():
            return colors[i]
    return 'empty'


def generate_data_file():
    image_array = open("data.txt", "w")

    image_mzp = Image.open("mzp_mc.png")

    init_color_regions()

    width, height = image_mzp.size

    for j in range(int(height / 16)):
        for i in range(int(width / 16)):
            left = i * 16
            top = 0 + j * 16
            right = i * 16 + 16
            bottom = 16 + j * 16
            mzp_region = image_mzp.crop((left, top, right, bottom)).convert('RGB')
            color = get_color(mzp_region)
            # print(f"{i}: mzp region's color: {color}")
            image_array.write(color)
            if not i == int(width / 16) - 1:
                image_array.write(',')

        if not j == int(height / 16) - 1:
            image_array.write('\n')

    print(f"Done. size: {image_mzp.size}")

    image_array.close()
    image_mzp.close()


# generate_data_file()

pos = {
    'sor': 199,
    'blokk': 0,
    'hanyasaval': 5
}


def get_row_and_blokk():
    """
    Lekéri konzolból hogy hanyadik sor és hanyadik blokktól nézze
    """
    block = 0
    sor = sorok_szama - int(input("add meg a sor számát: (a legalsó sor az 1.)"))
    pos['sor'] = sor
    lesz_e_blokk = input("hanyadik blokktól? (hanyd üresen ha az 1.től)")
    if not lesz_e_blokk == '':
        block = int(lesz_e_blokk)
    pos['blokk'] = block
    print(f"sor: {sorok_szama - sor} hanyadik blokktól: {block}")


def get_segment():
    """
    Megadja a következő 5 színt
    """
    row_length = len(image_data[pos['sor']].split(','))
    if pos['blokk'] + pos['hanyasaval'] > row_length:
        texts = image_data[pos['sor']].split(',')[pos['blokk']:row_length - 1]
    else:
        texts = image_data[pos['sor']].split(',')[pos['blokk']:pos['blokk'] + pos['hanyasaval']]
    print(f"{pos['blokk']} - {pos['blokk'] + pos['hanyasaval']}: {texts}")
    draw(texts)


def on_release(key):
    """
    OnKeyRelease event listener
    :param key: a lenyomott billentyű
    """
    if key == keyboard.Key.f6:
        pos['blokk'] += pos['hanyasaval']
        get_segment()
    if key == keyboard.Key.f7:
        pos['blokk'] = 0
        pos['sor'] -= 1
        get_segment()
    if key == keyboard.Key.f8:
        pos['blokk'] -= pos['hanyasaval']
        get_segment()


def draw(texts: []):
    """
    Kirajzolja a szövegeket, képeket a képernyőre
    :param texts: A színek tömbje
    """
    DISPLAYSURF.fill((255, 238, 161))
    for i in range(len(texts)):
        # draw text
        text = basicFont.render(texts[i], True, (0, 0, 0))
        textRect = text.get_rect()
        textRect.centerx = i * 160 + 80
        textRect.centery = 180
        DISPLAYSURF.blit(text, textRect)
        # draw image
        if not texts[i] == 'empty' and not texts[i] == '':
            color_index = colors.index(texts[i])
            DISPLAYSURF.blit(color_image, (i * 160, 0), (color_index * 160, 0, 160, 160))
    text = basicFont.render(f"{pos['blokk']} - {pos['blokk'] + pos['hanyasaval']}", True, (0, 0, 0))
    textRect = text.get_rect()
    textRect.centerx = DISPLAYSURF.get_rect().centerx
    textRect.centery = 225
    DISPLAYSURF.blit(text, textRect)


image_data = open("data.txt", "r").read().split('\n')
sorok_szama = len(image_data)
print(f"sorok száma: {sorok_szama}")

listener = keyboard.Listener(
    on_release=on_release).start()

get_row_and_blokk()

pygame.init()
basicFont = pygame.font.SysFont(None, 42)
DISPLAYSURF = pygame.display.set_mode((800, 250))
pygame.display.set_caption('Minecraft MZP build helper V2.0')

get_segment()
while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
    pygame.display.update()
