from wand.image import Image, Color
from wand.display import display
import os
import sys

def uminekofy(path):
    # resize and crop to 640x480, preserving pixel aspect ratio
    img = Image(filename=path)
    img.transform(resize='640x480^')
    img.transform(crop='640x480')
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
    # blur effect
    if True:
        blur = posterized.clone()
        #blur.motion_blur(sigma=5, angle=-60)
        blur.blur(sigma=2)
        blur.alpha_channel = 'activate'
        blur.evaluate(operator='set', value=img.quantum_range * 0.66, channel='alpha')
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
    final_image = posterized.clone()
    final_image.composite(blur)
    final_image.composite(edge, operator='multiply')
    return final_image

def main():
    #for image_path in os.scandir('images'):
    #    print(image_path)
    #    img = uminekofy(image_path)
    #    display(img)
    if len(sys.argv) != 3:
        print("USAGE: uminekofy <src> <dest>")
        sys.exit(1)
    img = uminekofy(sys.argv[1])
    img.save(filename=sys.argv[2])

if __name__ == "__main__":
    main()
