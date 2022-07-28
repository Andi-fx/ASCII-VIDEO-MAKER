from cgitb import small
import cv2 as cv
import numpy as np
import os 

cap = cv.VideoCapture(0, cv.CAP_DSHOW)

# Define cell & screen size 
cell_width, cell_height = 10, 15
width, height = 800, 600

cap.set(cv.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv.CAP_PROP_FRAME_HEIGHT, height)

# For file name writting purposes
cam_pics = os.getcwd() + "/Camera-Pictures"
cam_vids = os.getcwd() + "/Camera-Videos"

if not os.path.exists(cam_pics):
    os.makedirs("Camera-Pictures")
if not os.path.exists(cam_vids):
    os.makedirs("Camera-Videos")

starting_pictures = os.listdir(cam_pics)
starting_videos = os.listdir(cam_vids)

picture_counter = len(starting_pictures)
video_counter = len(starting_videos)
recording = False


# Calculate the smaller frame (where the ascii-related operations are made)
new_width, new_height = (width // cell_width, height // cell_height)
new_dimensions = (new_width, new_height)

chars = " .,-~:;=!*#$@"
colors_reduced = (255 / len(chars))

font = cv.FONT_HERSHEY_SIMPLEX
font_size = 0.5

amountof = (os.listdir(os.getcwd() + "/Camera-Pictures"))

def add_gui(window:np.mat):
    if recording:
        recording_text = "R = Stop Recording"
        recording_color = (0, 0, 200)
    else:
        recording_text = "R = Record"
        recording_color = (75, 250, 96)
        
    text_box = cv.rectangle(window, (15, 20), (190, 70), (30, 30, 30), -1)
    cv.rectangle(window, (15, 20), (190, 70), (0, 0, 0), 2)
    cv.putText(window, "Q = Take A Photo", (20, 40), font, 0.5, (75, 250, 96), 1, cv.LINE_8)
    cv.putText(window, recording_text, (20, 60), font, 0.5, recording_color, 1, cv.LINE_8)


def handle_input(key):

    global recording
    global video_counter
    global picture_counter
    global video

    if key == ord("q") or key == ord("Q"):
        picture_counter += 1
        cv.imwrite(cam_pics + "/PICTURE-" + str(picture_counter) + ".jpg", ascii_image_no_gui)

    if key == ord("r"):
        recording = not recording
        if recording:
            video_counter += 1
            video = cv.VideoWriter((cam_vids + "/VIDEO-" + str(video_counter) + ".avi"), cv.VideoWriter_fourcc(*"MP42"), 24.0, (width, height))
            print("RECORDING: " + str(recording) + " ", video_counter)      
        else:
            print("END OF RECORDING: " + str(video_counter))
            video.release()      
        
    if recording:
        video.write(generate_ascii(frame, False))
    

def generate_ascii(image:np.mat, gui:bool):
    ascii_window = np.zeros((height, width, 3), np.uint8)
    small_image = cv.resize(image, new_dimensions, interpolation=cv.INTER_NEAREST)
    gray_image = cv.cvtColor(small_image, cv.COLOR_BGR2GRAY)
    for i in range(new_height):
        for j in range(new_width):
            intensity = gray_image[i, j]
            char_index = int(intensity / colors_reduced)
            char = chars[char_index]
            cv.putText(ascii_window, char, (j * cell_width, i * cell_height), font, font_size, (255, 255, 255), 1)

    if (gui):
        add_gui(ascii_window)
        
    return ascii_window


while True:
    ret, frame = cap.read()
    frame = cv.flip(frame, 1)    

    ascii_image = generate_ascii(frame, True)
    ascii_image_no_gui = generate_ascii(frame, False)

    cv.imshow("ASCII-VIDEO-MAKER", ascii_image)

    # Handle input
    key = cv.waitKey(1)
    handle_input(key)

   # When pressing ESC
    if key == 27:
        break         
    # When clicking the "X"
    if cv.getWindowProperty("ASCII-VIDEO-MAKER", cv.WND_PROP_VISIBLE) < 1:        
        break 
    
cap.release()
cv.destroyAllWindows()
