import copy
import os
import time
import tkinter as tk
from tkinter import filedialog


def main():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select Hourglass movie file", filetypes=[("Hourglass movies", ('*.wtf', '.hgm'))])

    for file_path in root.tk.splitlist(file_paths):
        file_name = os.path.split(file_path)[-1]
        start_time = time.perf_counter()

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
        frames_not_marked = 0
        frames_total = 0
        key_codes = {27: 'escape', 13: 'enter', 38: 'up', 40: 'down', 37: 'left', 39: 'right', 90: 'z', 88: 'x', 67: 'c', 65: 'a', 83: 's', 68: 'd', 81: 'q', 49: 'one', 50: 'two', 51: 'three',
                     52: 'four', 53: 'five', 54: 'six', 55: 'seven', 56: 'eight', 57: 'nine'}

        for frame in data_split:
            frames_unchanged += 1
            frames_not_marked += 1
            frames_total += 1
            frame_keys = []

            pressed_keys = []
            for key_binary in frame:
                try:
                    current_key = key_codes[key_binary]
                    frame_keys.append(current_key)

                    if current_key not in held_keys:
                        # key pressed this frame
                        held_keys.append(current_key)
                        pressed_keys.append(current_key)
                except KeyError:
                    pass

            released_keys = []
            for old_held_key in old_held_keys:
                if old_held_key not in frame_keys:
                    # key released this frame
                    held_keys.remove(old_held_key)
                    released_keys.append(old_held_key)

            if old_held_keys != held_keys:
                # held keys have been changed
                out_line = ''

                for pressed_key in pressed_keys:
                    out_line += f'{pressed_key}- '
                for released_key in released_keys:
                    out_line += f'{released_key}+ '

                out.append(out_line)

                try:
                    out[-2] += str(frames_unchanged)
                except IndexError:
                    # early in the file
                    out.insert(0, str(frames_unchanged))

                frames_unchanged = 0

                if frames_not_marked >= 900:  # 30 seconds
                    len_of_out = len(out)
                    out.insert(len_of_out - 1, f"// Frame {frames_total}, step {len_of_out - 1}")
                    frames_not_marked = 0

            old_held_keys = copy.copy(held_keys)

        out_joined = "// Generated from {}\n// by https://github.com/Kataiser/wtf-to-itf\n\n{}".format(file_name, '\n'.join(out))
        print(out_joined)

        with open(f'{file_name[:-4]}.itf', 'w') as out_file:
            out_file.write(out_joined)

        print(f"\n\"{file_path}\": Took {round(time.perf_counter() - start_time, 3)} seconds for {frames_total} frames and {len(out)} steps")


if __name__ == '__main__':
    main()
