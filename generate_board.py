import cv2
import numpy as np

square_px = 100
rows      = 10
cols      = 7

h = rows * square_px
w = cols * square_px
board = np.zeros((h, w), dtype=np.uint8)

for r in range(rows):
    for c in range(cols):
        if (r + c) % 2 == 0:
            board[r*square_px:(r+1)*square_px,
                  c*square_px:(c+1)*square_px] = 255

cv2.imwrite("checkerboard_PRINT_ME.png", board)
print("Done — print at 100% scale, no fit-to-page")