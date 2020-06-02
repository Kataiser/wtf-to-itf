import os
import time
import tkinter as tk
from tkinter import filedialog


def reverse():
    root = tk.Tk()
    root.withdraw()
    file_paths = filedialog.askopenfilenames(initialdir=os.getcwd(), title="Select the Iji TAS file", filetypes=[("Iji TAS files", '*.itf')])

    for file_path in root.tk.splitlist(file_paths):
        start_time = time.perf_counter()
        file_name = os.path.splitext(file_path)[0]

        try:
            with open(file_path, 'r') as itf_file:
                itf_data = itf_file.readlines()
        except FileNotFoundError:
            raise SystemExit

        header_path = 'header.bin' if os.path.exists('header.bin') else 'resources\\header.bin'

        with open(header_path, 'rb') as header_file:
            header_data = header_file.read()

        output = bytearray(header_data)
        held_keys = []
        frames_total = 0
        steps_total = 0
        key_codes = {'escape': 27, 'enter': 13, 'u': 38, 'd': 40, 'l': 37, 'r': 39, 'z': 90, 'x': 88, 'c': 67, 's': 83, 'one': 49, 'two': 50, 'three': 51, 'four': 52, 'five': 53, 'six': 54,
                     'seven': 55, 'eight': 56, 'nine': 57}

        for line in itf_data:
            if line.startswith('//') or line == '\n':
                continue

            frame_data = bytearray(b'\0' * 8)
            line_split = line.split(' ')

            for key_change in line_split[:-1]:
                if key_change[-1] == '-':
                    held_keys.append(key_change[:-1])
                elif key_change[-1] == '+':
                    held_keys.remove(key_change[:-1])

            try:
                line_frames = int(line_split[-1])
            except ValueError:
                line_frames = 1

            for key_held in enumerate(held_keys):
                frame_data[key_held[0]] = key_codes[key_held[1]]

            print("{}: {}".format(steps_total, line.rstrip('\n')))
            output.extend(frame_data * line_frames)
            frames_total += line_frames
            steps_total += 1

        with open(f'{file_name}.wtf', 'wb') as out_file:
            out_file.write(output)
            out_file.seek(4)
            out_file.write(frames_total.to_bytes(4, byteorder='little'))
            out_file.write(int(0).to_bytes(4, byteorder='little'))
            out_file.seek(84)
            out_file.write(int(0).to_bytes(64, byteorder='little'))

        print(f"\n\"{file_path}\": Took {round(time.perf_counter() - start_time, 3)} seconds for {frames_total} frames and {len(itf_data)} steps")


if __name__ == '__main__':
    reverse()
