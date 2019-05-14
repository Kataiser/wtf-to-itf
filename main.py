import copy
import os
import tkinter as tk
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()

    file_path = filedialog.askopenfilename(initialdir=os.getcwd(), title="Select Hourglass movie file", filetypes=[("Hourglass movies", ('*.wtf', '.hgm'))])

    try:
        with open(file_path, 'rb') as binary_file:
            data_raw = binary_file.read()
    except FileNotFoundError:
        raise SystemExit

    data = [d for d in bytearray(data_raw)][1024:]
    data_split = [data[i:i + 8] for i in range(0, len(data), 8)]
    out = []
    held_keys = []
    old_held_keys = []
    frames_unchanged = 0
    key_codes = {27: 'escape', 13: 'enter', 38: 'up', 40: 'down', 37: 'left', 39: 'right', 90: 'z', 88: 'x', 67: 'c', 65: 'a', 83: 's', 68: 'd', 81: 'q', 49: '1', 50: '2', 51: '3', 52: '4',
                 53: '5', 54: '6', 55: '7', 56: '8', 57: '9'}

    for frame in data_split:
        frames_unchanged += 1
        frame_keys = []

        for key_binary in frame:
            try:
                current_key = key_codes[key_binary]
                frame_keys.append(current_key)

                if current_key not in held_keys:
                    # key pressed this frame
                    held_keys.append(current_key)
            except KeyError:
                pass

        for old_held_key in old_held_keys:
            if old_held_key not in frame_keys:
                # key released this frame
                held_keys.remove(old_held_key)

        if old_held_keys != held_keys:
            # held keys have been changed
            out_line = ''

            for held_key in held_keys:
                out_line += f'{held_key} '

            out.append(out_line)

            try:
                out[-2] += str(frames_unchanged)
            except IndexError:
                # early in the file
                pass

            frames_unchanged = 0

        old_held_keys = copy.copy(held_keys)

    out_joined = '\n'.join(out)
    print(out_joined)

    with open(f'{os.path.split(file_path)[-1][:-4]}.itf', 'w') as out_file:
        out_file.write(out_joined)


if __name__ == '__main__':
    main()
