# Invisibility Cloak

A Python-based implementation of the "Invisibility Cloak" effect using OpenCV. This project allows you to create a Harry Potter-style invisibility effect by replacing a specific color in your webcam feed with a previously captured background.

## Features

- Real-time color detection and replacement
- Multiple color presets (black, green, yellow, blue, red)
- Custom color calibration with HSV controls
- Background recalibration
- Save and load custom color presets
- Error handling and user feedback
- Mask preview for better calibration

## Requirements

- Python 3.x
- OpenCV (cv2)
- NumPy

## Installation

1. Clone this repository:
```bash
git clone https://github.com/Assem-ElQersh/Invisibility-Cloak.git
cd Invisibility-Cloak
```

2. Install the required packages:
```bash
pip install opencv-python numpy
```

## Usage

1. Run the program:
```bash
python "Invisiblity Cloak.py"
```

2. Controls:
- `a` - Capture background
- `r` - Recalibrate background
- `s` - Save current HSV values as preset
- `1-5` - Switch between presets:
  - `1` - Black
  - `2` - Green
  - `3` - Yellow
  - `4` - Blue
  - `5` - Red
- `q` - Quit

3. HSV Controls:
- Use the trackbars in the 'HSV Controls' window to fine-tune the color detection
- The 'Mask' window shows the detected color in real-time
- Adjust the values until you get the best invisibility effect

## How It Works

1. The program captures a background image when you press 'a'
2. It then detects a specific color in the webcam feed
3. The detected color is replaced with the corresponding part of the background image
4. The result creates an illusion of invisibility

## Tips for Best Results

1. Use a solid-colored cloth (preferably black or green)
2. Ensure good lighting conditions
3. Keep the background static
4. Adjust HSV values if the color detection isn't perfect
5. Recalibrate the background if it changes

## Customization

You can create and save your own color presets:
1. Adjust the HSV values using the trackbars
2. Press 's' to save the current settings
3. Enter a name for your preset
4. Your preset will be saved in `color_presets.json`

## Error Handling

The program includes error handling for:
- Camera initialization
- Frame capture
- Background capture
- File operations

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to submit issues and enhancement requests! 
