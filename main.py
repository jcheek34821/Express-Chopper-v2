# Importing all necessary libraries from multiprocessing.connection import Listener
import cv2
import os
from pynput.keyboard import Key, Listener
import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd


wait_key = 10
current_frame_array = []
is_beginning = True
frame_range = [0, 0, -1]
video_string = ""
data_string = ""
destination_string = ""
img_array = []
is_paused = False
current_frame = 0
end_program = False
one_pressed = False
num = 0
jump = False
jump_end = False
reference_select = False
super_speed = False


def run_main():
    global jump
    global num
    if destination_label["text"] != "mp4 file" and video_label["text"] != "select destination":
        global current_frame
        root.destroy()
        # Collect events until released
        with Listener(on_press=on_press, on_release=on_release) as listener:
            video_window = tk.Tk("Express Video Chopper")
            vid = cv2.VideoCapture(video_string)
            if not vid.isOpened():
                print("error...")

            while vid.isOpened():
                if jump:
                    vid.set(1, num)
                    jump = False
                elif jump_end:
                    break
                    # vid.set(1, vid.get(cv2.CAP_PROP_FRAME_COUNT) + 1)
                ute, pic_fra = vid.read()
                num = num + 1
                if ute and not end_program:
                    im = cv2.resize(pic_fra, (960, 540))
                    cv2.imshow("Express Video Chopper", im)
                    current_frame = int(vid.get(cv2.CAP_PROP_POS_FRAMES))
                    if cv2.waitKey(wait_key) & 0xFF == ord('u'):
                        break
                else:
                    cv2.waitKey(0)
                    cv2.destroyAllWindows()
                    break

            vid.release()

            # run the application
            listener.join()

            cv2.destroyAllWindows()


def check_frame(frame):
    for x in current_frame_array:
        if x[0] <= frame <= x[1]:
            return True
    return False


def get_next_frame(frame):
    for x in current_frame_array:
        if frame < x[0] and frame < x[1]:
            return x[0]
    return frame


def on_press(key):
    global super_speed
    global wait_key
    global is_paused
    global is_beginning
    global frame_range
    global current_frame
    global end_program
    global one_pressed
    global jump
    global num
    global reference_select
    if reference_select:
        if format(key) == '\'0\'':
            frame_range[2] = 0
        elif format(key) == '\'1\'':
            frame_range[2] = 1
        elif format(key) == '\'2\'':
            frame_range[2] = 2
        elif format(key) == '\'3\'':
            frame_range[2] = 3
        elif format(key) == '\'4\'':
            frame_range[2] = 4
        elif format(key) == '\'5\'':
            frame_range[2] = 5
        elif format(key) == '\'6\'':
            frame_range[2] = 6
        elif format(key) == '\'7\'':
            frame_range[2] = 7
        elif format(key) == '\'8\'':
            frame_range[2] = 8
        elif format(key) == '\'9\'':
            frame_range[2] = 9
        elif format(key) == '\'r\'':
            frame_range[1] = 0
            print("Removed " + str(frame_range[1]))
            print("Still recording...")
            reference_select = False
            wait_key = 10
        if frame_range[2] != -1:
            print("Reference set as " + str(frame_range[2]))
            current_frame_array.append(frame_range)
            frame_range = [0, 0, -1]
            is_beginning = True
            reference_select = False
            wait_key = 10
    else:
        if key == Key.space and not is_paused:
            if is_beginning:
                frame_range[0] = current_frame
                print("Recording from " + str(frame_range[0]))
                is_beginning = False
            else:
                frame_range[1] = current_frame
                print("Stopped Recording at " + str(frame_range[1]))
                print("Select a reference number:")
                wait_key = 0
                reference_select = True
        if format(key) == '\'s\'' and not is_paused:
            save_video()
        if format(key) == '\'r\'' and not is_paused:
            current_frame_array.pop()
            print("Deleted last frames...")
        if key == Key.ctrl_l or key == Key.ctrl_r and not is_paused:
            if super_speed:
                wait_key = 10
                super_speed = False
            else:
                wait_key = 1
                super_speed = True
        if format(key) == '\'p\'':
            if is_paused and one_pressed:
                wait_key = 10
                is_paused = False
                print("Video resume...")
            elif not is_paused:
                wait_key = 0
                is_paused = True
                print("Video paused...")
        if format(key) == '\'q\'' and not is_paused:
            print("Exiting program...press q again")
            end_program = True
        if format(key) == '\'1\'':
            one_pressed = True
        if key == Key.left and not is_paused:
            jump = True
            num = num - 30


def on_release(key):
    global jump
    global num
    global one_pressed
    global wait_key
    global frame_range
    global is_beginning
    global reference_select
    if not reference_select:
        if key == Key.right and not is_paused:
            wait_key = 10
        if format(key) == '\'1\'':
            one_pressed = False
        if key == Key.right and not is_paused:
            jump = True
            num = num + 900


def num_exists(n):
    for x in current_frame_array:
        if x[2] == n:
            return True
    return False


def save_video():
    global end_program
    global is_paused
    is_paused = True
    print("Video paused...")
    print("Saving video...")
    # Read the video from specified path
    cam = cv2.VideoCapture(video_string)

    # frame
    width = 1920
    height = 1080

    for x in range(0, 9):
        if num_exists(x):
            mp4string = str(x) + ".mp4"
            path_count = 1

            while os.path.exists(destination_string + "/" + mp4string):
                mp4string = mp4string + "(" + str(path_count) + ").mp4"
                path_count += 1

            # choose codec according to format needed
            fourcc = cv2.VideoWriter_fourcc(*'mp4v')
            video = cv2.VideoWriter(destination_string + "/" + mp4string, fourcc, 30, (width, height))
            for y in current_frame_array:
                if y[2] == x:
                    cam.set(1, y[0])
                    currentframe = y[0]
                    while currentframe <= y[1]:
                        # reading from frame
                        ret, frame = cam.read()
                        if ret:
                            video.write(frame)

                            # increasing counter so that it will
                            # show how many frames are created
                            currentframe += 1
                        else:
                            break
            print("Video " + str(x) + " saved")
            video.release()
    cam.release()
    end_program = True


def select_media_file():
    global video_string
    media_filetypes = (
        ('MP4', '*.mp4'),
        ('MOV', '*.mov'),
        ('All files', '*.*')
    )

    video_string = fd.askopenfilename(
        title='Import Video',
        initialdir='/',
        filetypes=media_filetypes)
    if video_string != "":
        video_label["text"] = video_string


def choose_directory():
    global destination_string
    destination_string = fd.askdirectory(
        title='Select Destination')
    if destination_string != "":
        destination_label["text"] = destination_string


# create the root window
root = tk.Tk()
root.title('Express Video Trimmer Setup')
root.resizable(False, False)
root.geometry('1000x300')

# video file label
video_label = ttk.Label(
    root,
    text="mp4 file")
video_label.pack()

# import video button
import_video_button = ttk.Button(
    root,
    text='Import Video',
    command=select_media_file
)
import_video_button.pack(expand=True)

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# select destination label
destination_label = ttk.Label(
    root,
    text="select destination")
destination_label.pack()

# choose directory button
choose_directory_button = ttk.Button(
    root,
    text='Choose Directory',
    command=choose_directory
)
choose_directory_button.pack(expand=True)

# space label
space_label = ttk.Label(
    root,
    text="")
space_label.pack()

# go button
go_button = ttk.Button(
    root,
    text='Go',
    command=run_main
)
go_button.pack(expand=True)

# run the application
root.mainloop()

# Release all space and windows once done
cv2.destroyAllWindows()
