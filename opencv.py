import cv2 as cv
import numpy as np
import pandas as pd
import sys
import os
import glob
import time

# from PIL import Image

HEIGHT, WIDTH = 720, 720
UHEIGHT = int(HEIGHT/12)
UWIDTH = int(WIDTH/12)

MAZE_FILE = "Open_Maze.csv"

main_dir = os.path.split(os.path.abspath(__file__))[0]

def overlay_image(img, img_overlay, x, y):
    """Overlay `img_overlay` onto `img` at (x, y) and blend using `alpha_mask`.

    `alpha_mask` must have same HxW as `img_overlay` and values in range [0, 1].
    """
    # Image ranges
    y1, y2 = max(0, y), min(img.shape[0], y + img_overlay.shape[0])
    x1, x2 = max(0, x), min(img.shape[1], x + img_overlay.shape[1])

    # Overlay ranges
    y1o, y2o = max(0, -y), min(img_overlay.shape[0], img.shape[0] - y)
    x1o, x2o = max(0, -x), min(img_overlay.shape[1], img.shape[1] - x)

    # Exit if nothing to do
    if y1 >= y2 or x1 >= x2 or y1o >= y2o or x1o >= x2o:
        return

    # Blend overlay within the determined ranges
    img_crop = img[y1:y2, x1:x2]
    img_overlay_crop = img_overlay[y1o:y2o, x1o:x2o]

    alphaoverlay = img_overlay[y1o:y2o, x1o:x2o, 3]/255.0
    alphaunderlay = 1 - alphaoverlay

    for color in range(3):
        img_crop[:,:,color] = (alphaoverlay*img_overlay_crop[:,:,color] +
                                alphaunderlay*img_crop[:,:,color])

def rotate_image(image, angle):
    image_center = tuple(np.array(image.shape[1::-1]) / 2)
    rot_mat = cv.getRotationMatrix2D(image_center, angle, 1.0)
    result = cv.warpAffine(image, rot_mat, image.shape[1::-1], flags=cv.INTER_LINEAR)
    return result


pathimages = os.path.join(main_dir, "src", "gym_rat_runner", "images")

dict = {}
for file in glob.glob(pathimages + "/*.png"):
    figname = os.path.split(file)[1][:-4]
    dict[figname] = cv.imread(file, cv.IMREAD_UNCHANGED)
    dict[figname] = cv.resize(dict[figname], (UHEIGHT, UWIDTH), interpolation = cv.INTER_AREA)

maze_file = os.path.join(main_dir, "src", "gym_rat_runner", "envs", "maze", MAZE_FILE)
maze = pd.read_csv(maze_file, header= None)

# Write some Text

font                   = cv.FONT_HERSHEY_SIMPLEX
bottomLeftCornerOfText = (10,HEIGHT-UHEIGHT//2)
fontScale              = 0.5
fontColor              = (255,255,255)
thickness              = 2
lineType               = 2

frames = []
for step in range(2*9):

    frame = np.zeros((HEIGHT,WIDTH,4), np.uint8)
    frame[:] = (21, 89, 33, 255)

    for i in range(maze.shape[0]):
        for j in range(maze.shape[1]):
            if maze.iloc[i,j] == 1:
                overlay_image(frame, dict['wall'], i*UWIDTH, j*UHEIGHT)


    test = rotate_image(dict['rat'], step*45)
    overlay_image(frame, test, UWIDTH, 10*UHEIGHT)
    overlay_image(frame, dict['cat'], 5*UWIDTH, 5*UHEIGHT)
    overlay_image(frame, dict['cheese'], 10*UWIDTH, 1*UHEIGHT)

    cv.putText(frame,'Frame: ' + str(step) , bottomLeftCornerOfText,
                font, fontScale, fontColor, thickness, lineType)

    frames.append(frame)

out = cv.VideoWriter('sample.mov',cv.VideoWriter_fourcc(*"avc1"), 20, (WIDTH, HEIGHT), True)

for i in range(len(frames)):
    out.write(frames[i][:,:,:3])
    cv.imshow("Preview",frames[i])
    cv.waitKey(50)


out.release()
cv.destroyAllWindows()
