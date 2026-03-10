# generate_board.py
import cv2
import numpy as np

square_px = 100       # size of each square in pixels
rows      = 10        # total rows of squares
cols      = 7         # total columns of squares

h = rows * square_px
w = cols * square_px
board = np.zeros((h, w), dtype=np.uint8)

for r in range(rows):
    for c in range(cols):
        if (r + c) % 2 == 0:
            board[r*square_px : (r+1)*square_px,
                  c*square_px : (c+1)*square_px] = 255

cv2.imwrite("checkerboard_PRINT_ME.png", board)
print("File saved: checkerboard_PRINT_ME.png")  # disable fit to page!

# lsusb | grep Intel