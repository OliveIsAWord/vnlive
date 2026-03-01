from wand.image import Image, Color
from wand.display import display
import os
import sys
import time as time_lib

do_timing = False
current_time = None

def time(msg, restart=False):
    global current_time
    if not do_timing:
        return
    if current_time == None or restart:
        current_time = time_lib.time()
        #print("Timing ...")
        return
    now = time_lib.time()
    print(msg, "...\t", now - current_time)
    current_time = now

def uminekofy(path, time_of_day = 'day'):
    time("start", restart=True)
    # resize and crop to 640x480, preserving pixel aspect ratio
    img = Image(filename=path)
    img.transform(resize='640x480^')
    img.transform(crop='640x480')
    time("resize")
    if time_of_day == 'night' or time_of_day == 'storm':
        darkness = img.clone()
        darkness.transform_colorspace('gray')
        hi = 220 / 255
        lo = 170 / 255
        darkness = darkness.fx(f'clamp(({hi} - u)/({hi - lo}))')
        darkness.negate()
        color = '#777' if time_of_day == 'storm' else '#000'
        darkness_color = Image(width=darkness.width, height=darkness.height, background=color)
        darkness_color.alpha_channel = 'activate'
        darkness_color.composite_channel('alpha', darkness, operator='copy_alpha')
        img.composite(darkness_color)
    time("night")
    # posterization
    if True:
        posterized = img.clone()
        #posterized.level(black=0.4, white=0.6)
        posterized.transform_colorspace('hsv')
        low_threshold = 0.1
        high_threshold = 1.0 - low_threshold
        ops = [
            ('subtract', img.quantum_range * low_threshold),
            ('divide', high_threshold - low_threshold),
        ]
        for o, v in ops:
            posterized.evaluate(operator=o, value=v, channel='blue')
        posterized.transform_colorspace('rgb')
        posterized.posterize(levels=11)
    time("posterize")
    # blur effect
    if True:
        blur = posterized.clone()
        blur.motion_blur(sigma=10, angle=-45)
        blur.blur(sigma=2)
        blur.alpha_channel = 'activate'
        blur.evaluate(operator='set', value=img.quantum_range * 0.66, channel='alpha')
    time("blur")
    # edge effect
    if True:
        edge = img.clone()
        edge.transform_colorspace('gray')
        awa = Image(width=640, height=480, background=Color('white'))
        for angle in [0,90,180,270]:
            edge2 = edge.clone()
            edge2.rotate(angle)
            edge2.morphology(method='correlate', kernel='sobel')
            edge2.rotate(360-angle)
            edge2.negate()
            awa.composite(edge2, operator='multiply')
        edge = awa
        #edge.edge(radius=1)
        edge.color_threshold(start='#777', stop='#fff')
        edge.alpha_channel = 'activate'
        edge.evaluate(operator='set', value=img.quantum_range * 0.5, channel='alpha')
    time("edge")
    final_image = posterized.clone()
    final_image.composite(blur)
    final_image.composite(edge, operator='multiply')
    time("composite")
    return final_image

def main():
    #for image_path in os.scandir('images'):
    #    print(image_path)
    #    for tod in ['day', 'night', 'storm']:
    #        img = uminekofy(image_path, tod)
    #        display(img)
    if len(sys.argv) != 3:
        print("USAGE: uminekofy <src> <dest>")
        sys.exit(1)
    img = uminekofy(sys.argv[1], time_of_day='day')
    #display(img)
    img.save(filename=sys.argv[2])

if __name__ == "__main__":
    main()
