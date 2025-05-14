import cv2
import numpy as np
import json
import os

class InvisibilityCloak:
    def __init__(self):
        # Initialize video capture with error handling
        self.cap = cv2.VideoCapture(1)
        if not self.cap.isOpened():
            raise RuntimeError("Error: Could not open camera. Please check if it's connected properly.")
        
        self.background = None
        self.color_presets = {
            'black': {'lower': [0, 0, 0], 'upper': [180, 255, 50]},
            'green': {'lower': [35, 100, 100], 'upper': [85, 255, 255]},
            'yellow': {'lower': [20, 100, 100], 'upper': [30, 255, 255]},
            'blue': {'lower': [100, 100, 100], 'upper': [130, 255, 255]},
            'red': {'lower': [0, 100, 100], 'upper': [10, 255, 255]}
        }
        self.current_preset = 'black'
        self.load_presets()
        
        # Create trackbars for HSV adjustment
        cv2.namedWindow('HSV Controls')
        cv2.createTrackbar('H Lower', 'HSV Controls', self.color_presets[self.current_preset]['lower'][0], 180, lambda x: None)
        cv2.createTrackbar('S Lower', 'HSV Controls', self.color_presets[self.current_preset]['lower'][1], 255, lambda x: None)
        cv2.createTrackbar('V Lower', 'HSV Controls', self.color_presets[self.current_preset]['lower'][2], 255, lambda x: None)
        cv2.createTrackbar('H Upper', 'HSV Controls', self.color_presets[self.current_preset]['upper'][0], 180, lambda x: None)
        cv2.createTrackbar('S Upper', 'HSV Controls', self.color_presets[self.current_preset]['upper'][1], 255, lambda x: None)
        cv2.createTrackbar('V Upper', 'HSV Controls', self.color_presets[self.current_preset]['upper'][2], 255, lambda x: None)

    def load_presets(self):
        try:
            if os.path.exists('color_presets.json'):
                with open('color_presets.json', 'r') as f:
                    saved_presets = json.load(f)
                    self.color_presets.update(saved_presets)
        except Exception as e:
            print(f"Error loading presets: {e}")

    def save_presets(self):
        try:
            with open('color_presets.json', 'w') as f:
                json.dump(self.color_presets, f)
        except Exception as e:
            print(f"Error saving presets: {e}")

    def capture_background(self):
        ret, bg_frame = self.cap.read()
        if ret:
            self.background = cv2.flip(bg_frame, 1)
            print("Background captured!")
        else:
            print("Error: Failed to capture background")

    def get_current_hsv_values(self):
        return {
            'lower': [
                cv2.getTrackbarPos('H Lower', 'HSV Controls'),
                cv2.getTrackbarPos('S Lower', 'HSV Controls'),
                cv2.getTrackbarPos('V Lower', 'HSV Controls')
            ],
            'upper': [
                cv2.getTrackbarPos('H Upper', 'HSV Controls'),
                cv2.getTrackbarPos('S Upper', 'HSV Controls'),
                cv2.getTrackbarPos('V Upper', 'HSV Controls')
            ]
        }

    def set_hsv_values(self, preset_name):
        if preset_name in self.color_presets:
            preset = self.color_presets[preset_name]
            cv2.setTrackbarPos('H Lower', 'HSV Controls', preset['lower'][0])
            cv2.setTrackbarPos('S Lower', 'HSV Controls', preset['lower'][1])
            cv2.setTrackbarPos('V Lower', 'HSV Controls', preset['lower'][2])
            cv2.setTrackbarPos('H Upper', 'HSV Controls', preset['upper'][0])
            cv2.setTrackbarPos('S Upper', 'HSV Controls', preset['upper'][1])
            cv2.setTrackbarPos('V Upper', 'HSV Controls', preset['upper'][2])
            self.current_preset = preset_name

    def save_current_preset(self, preset_name):
        self.color_presets[preset_name] = self.get_current_hsv_values()
        self.save_presets()
        print(f"Saved current settings as preset: {preset_name}")

    def run(self):
        print("Controls:")
        print("'a' - Capture background")
        print("'r' - Recalibrate background")
        print("'s' - Save current HSV values as preset")
        print("'1-5' - Switch between presets (1:black, 2:green, 3:yellow, 4:blue, 5:red)")
        print("'q' - Quit")

        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Error: Failed to capture frame")
                break

            frame = cv2.flip(frame, 1)

            if self.background is None:
                cv2.imshow("Press 'a' to capture the background", frame)
                key = cv2.waitKey(1) & 0xFF
                if key == ord('a'):
                    self.capture_background()
                continue

            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
            current_hsv = self.get_current_hsv_values()
            
            lower = np.array(current_hsv['lower'])
            upper = np.array(current_hsv['upper'])
            
            mask = cv2.inRange(hsv, lower, upper)
            mask_inv = cv2.bitwise_not(mask)

            background_part = cv2.bitwise_and(self.background, self.background, mask=mask)
            visible_part = cv2.bitwise_and(frame, frame, mask=mask_inv)
            final_output = cv2.add(background_part, visible_part)

            # Display the output
            cv2.imshow('Invisible Cloak', final_output)
            cv2.imshow('Mask', mask)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                break
            elif key == ord('a'):
                self.capture_background()
            elif key == ord('r'):
                self.background = None
            elif key == ord('s'):
                preset_name = input("Enter preset name: ")
                self.save_current_preset(preset_name)
            elif key in [ord('1'), ord('2'), ord('3'), ord('4'), ord('5')]:
                preset_map = {'1': 'black', '2': 'green', '3': 'yellow', '4': 'blue', '5': 'red'}
                self.set_hsv_values(preset_map[chr(key)])

        self.cap.release()
        cv2.destroyAllWindows()

if __name__ == "__main__":
    try:
        cloak = InvisibilityCloak()
        cloak.run()
    except Exception as e:
        print(f"Error: {e}")
