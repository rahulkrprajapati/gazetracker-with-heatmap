import cv2
import autopy
from matplotlib import pyplot as plt
import seaborn as sns
import pyscreenshot
import PIL
from PIL import Image
from seaborn.matrix import heatmap
import pyautogui
import numpy as np

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
            cv2.circle(
                img=roi_color2,
                center=circle_center,
                radius=2,
                color=WHITE,
                thickness=3
            )

            x_pos = int(eye_x_pos)
            y_pos = int(eye_y_pos)
            (x_pos, y_pos) = transform_video_coordinates_to_screen(eye_x_pos, eye_y_pos)
            autopy.mouse.move(x_pos, y_pos)
    except Exception as e:
        print('Exception:', e)
face_cascade = cv2.CascadeClassifier(
    'haarcascades/haarcascade_frontalface_default.xml'
)

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
    print("frame per second of camera")
    print(video_capture.get(cv2.CAP_PROP_FPS))
else:
    video_resolution = None
screen_size = autopy.screen.size()
fourcc = cv2.VideoWriter_fourcc(*"XVID")
out = cv2.VideoWriter("output.avi", fourcc, 30.0, (1366, 768))
while 1:
    success, image = video_capture.read()
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
    
    background_screenshot = pyautogui.screenshot()
    frame = np.array(background_screenshot)
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    my_dpi = 118
    width = int(screen_size[0])
    height = int(screen_size[1])
    plt.scatter(eye_x_positions, eye_y_positions, alpha=0.8)
    plt.tight_layout(pad=1)
    plt.axis('off')
    plt.savefig('scatter.png', dpi=my_dpi*2)
    scatter = PIL.Image.open("scatter.png")
    new_size = (width, height)
    scatter = scatter.resize(new_size)
    scatter = scatter.save("new_scatter.png")
    img2 = cv2.imread('new_scatter.png')
    final_frame = cv2.addWeighted(frame,0.7,img2,0.3,0)
    plt.clf()
    # eye_x_positions = list()
    # eye_y_positions = list()
    # eye_x_positions.clear()
    # eye_y_positions.clear()
    #cv2.imshow('img', image)
    cv2.imshow('img', final_frame)
    #todo write output
    out.write(final_frame)
    key_pressed = cv2.waitKey(30) & 0xff
    if key_pressed == ESCAPE_KEY:
        break
video_capture.release()
out.release()
cv2.destroyAllWindows()