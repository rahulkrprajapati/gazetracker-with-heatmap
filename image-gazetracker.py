import cv2
import autopy
from matplotlib import pyplot as plt
import seaborn as sns
import pyscreenshot
import PIL
from PIL import Image
from seaborn.matrix import heatmap

ESCAPE_KEY = 27

WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

def transform_video_coordinates_to_screen(eye_x_pos, eye_y_pos):
    if not video_resolution:
        return (eye_x_pos, eye_y_pos)

    return (
        eye_x_pos / video_resolution[0] * screen_resolution[0],
        eye_y_pos / video_resolution[1] * screen_resolution[1],
    )


def update_mouse_position(hough_circles, eye_x_pos, eye_y_pos, roi_color2):
    try:
        for circle in hough_circles[0, :]:

            circle_center = (circle[0], circle[1])

            cv2.circle(
                img=roi_color2,
                center=circle_center,
                radius=circle[2],
                color=WHITE,
                thickness=2
            )
            # print("drawing circle")
            # draw the center of the circle
            cv2.circle(
                img=roi_color2,
                center=circle_center,
                radius=2,
                color=WHITE,
                thickness=3
            )

            # print(i[0],i[1])

            x_pos = int(eye_x_pos)
            y_pos = int(eye_y_pos)
            (x_pos, y_pos) = transform_video_coordinates_to_screen(eye_x_pos, eye_y_pos)
            autopy.mouse.move(x_pos, y_pos)
    except Exception as e:

        print('Exception:', e)

face_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_default.xml'
)
# eye_cascade = cv2.CascadeClassifier(
#     'haarcascades/haarcascade_eye.xml'
# )

#testing right eye tracking
eye_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_righteye_2splits.xml'
)

#number signifies camera
video_capture = cv2.VideoCapture(0)
eye_x_positions = list()
eye_y_positions = list()

screen_resolution = autopy.screen.size()
print("screen resolution is")
print(screen_resolution)
if video_capture.isOpened():
    video_resolution = (
        video_capture.get(cv2.CAP_PROP_FRAME_WIDTH),
        video_capture.get(cv2.CAP_PROP_FRAME_HEIGHT),
    )
else:
    video_resolution = None

while 1:
    success, image = video_capture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    #faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    eyes = eye_cascade.detectMultiScale(gray)

    for (eye_x, eye_y, eye_width, eye_height) in eyes:

        cv2.rectangle(
            img=image, 
            pt1=(eye_x, eye_y), 
            pt2=(eye_x + eye_width, eye_y + eye_height), 
            color=GREEN, 
            thickness=2
        )
        roi_gray2 = gray[eye_y: eye_y + eye_height, eye_x: eye_x + eye_width]
        roi_color2 = image[eye_y: eye_y + eye_height, eye_x: eye_x + eye_width]

        hough_circles = cv2.HoughCircles(
            roi_gray2,
            cv2.HOUGH_GRADIENT,
            1,
            200,
            param1=200,
            param2=1,
            minRadius=0,
            maxRadius=0
        )

        eye_x_pos = (eye_x + eye_width) / 2
        eye_y_pos = (eye_y + eye_height) / 2
        print(eye_x_pos, eye_y_pos)
        eye_x_positions.append(eye_x_pos)
        eye_y_positions.append(eye_y_pos)
        

        update_mouse_position(hough_circles, eye_x_pos, eye_y_pos, roi_color2)

    cv2.imshow('img', image)

    key_pressed = cv2.waitKey(30) & 0xff
    if key_pressed == ESCAPE_KEY:
        break


video_capture.release()
cv2.destroyAllWindows()
data = list(zip(eye_x_positions, eye_y_positions))

print("Printing x positions")
print(eye_x_positions)
print("Printing y positions")
print(eye_y_positions)
print("Printing compacted dict of coordinates")
print(data)

screenshot = pyscreenshot.grab()
screenshot.save("screenshot.png")
background_image = PIL.Image.open("screenshot.png")
width, height = background_image.size

print(width, height)
my_dpi = 118
#trying contour heatmap
# x = sns.kdeplot(eye_x_positions, eye_y_positions, shade=True, cmap='Reds', shade_lowest=False)
#trying scatter plot
plt.scatter(eye_x_positions, eye_y_positions)

#Comment starts
plt.tight_layout(pad=1)
plt.axis('off')
#plt.figure(figsize=(width/my_dpi, height/my_dpi), dpi=my_dpi)
#plt.figure(figsize=(width, height))
plt.savefig('scatter.png', dpi=my_dpi*2)
scatter = PIL.Image.open("scatter.png")

new_size = (width, height)
scatter = scatter.resize(new_size)
scatter = scatter.save("new_scatter.png")

img1 = cv2.imread('screenshot.png')
img2 = cv2.imread('new_scatter.png')
dst = cv2.addWeighted(img1,0.7,img2,0.3,0)
cv2.imshow('scatter plot',dst)
cv2.imwrite('Output_Scatter.png', dst) 

cv2.waitKey(0)
cv2.destroyAllWindows()
plt.clf()
#comment ends

"""Adding code for heatmap"""
x = sns.kdeplot(eye_x_positions, eye_y_positions, shade=True, cmap='rocket_r', shade_lowest=False)
plt.tight_layout(pad=1)
plt.axis('off')
plt.savefig('heatmap.png', dpi=my_dpi*2)
heatmap = PIL.Image.open("heatmap.png")

new_size = (width, height)
heatmap = heatmap.resize(new_size)
heatmap = heatmap.save("new_heatmap.png")

img1 = cv2.imread('screenshot.png')
img2 = cv2.imread('new_heatmap.png')
dst = cv2.addWeighted(img1,0.6,img2,0.4,0)
cv2.imshow('heatmap plot',dst)
cv2.imwrite('Output_heatmap.png', dst) 

cv2.waitKey(0)
cv2.destroyAllWindows()
