# required py libraries
import cv2

# open coloured image
img_original = cv2.imread("127.jpg", 1)

# change to grayscale image
img_greyscale = cv2.imread("127.jpg", 0)

# image size
print(img_original.shape)
print(img_greyscale.shape)

# resize image
img_original_resize = cv2.resize(img_original, (int(img_original.shape[1]/2), int(img_original.shape[0]/2)))
img_greyscale_resize = cv2.resize(img_greyscale, (int(img_greyscale.shape[1]/2), int(img_greyscale.shape[0]/2)))

# show image
cv2.imshow("Landscape", img_original_resize)
cv2.imshow("Landscape in grayscale", img_greyscale_resize)

# close window only after key press
cv2.waitKey(0)
cv2.destroyAllWindows()