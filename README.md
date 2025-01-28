# Pulse Streamer Control Suite

## Overview

The **Pulse Streamer Control Suite** includes two Python scripts designed to facilitate the testing and control of Pulse Streamer devices. These scripts can be used to generate custom signal patterns visible with an oscilloscope. The suite contains:

- `pulse_streamer_test.py`: A simple script for testing the Pulse Streamer without a GUI.
- `pulse_streamer_test_with_interface.py`: An advanced script featuring a professional GUI interface for detailed control and visualization of the signal patterns.

## Prerequisites

Ensure you have the following installed on your system:

- **Python 3.6 or higher**: Required to run the scripts.
- **Tkinter**: For the GUI (usually comes pre-installed with Python).

## Installation

### 1. Clone the Repository
Clone the repository to your local machine:
```bash
git clone https://github.com/Aman-Sunesh/PulseStreamer-Control-Panel.git
cd PulseStreamer-Control-Panel
```

## 2. Run the Script
Execute the script using Python:

For the non-GUI version:

```bash
python pulse_streamer_test.py
```

For the GUI version:

```bash
python pulse_streamer_test_with_interface.py
```

## Usage

 **NOTE:** To ensure a successful connection to the Pulse Streamer, both the device and your computer must be on the same network. It is recommended to run the code using a development environment like **Visual Studio Code** or a similar IDE that runs directly on your machine, rather than a browser-based environment.


### Non-GUI Script
1. Run `pulse_streamer_test.py`.
2. Follow the on-screen prompts to connect to the Pulse Streamer and test different patterns.

### GUI Script
1. Run `pulse_streamer_test_with_interface.py`.
2. Use the GUI to:
   - Connect to the Pulse Streamer using the provided IP address field.
   - Select the channel type (Digital or Analog).
   - Enter the channel number and pattern for signal generation.
   - Define the number of runs for the pattern.
   - Start and stop the pattern streaming with the interface controls.

### Viewing Results
Connect an oscilloscope to the Pulse Streamer to view the output of the signal patterns defined in either script.

## Features and Functionalities

1. **Simple Test Script**:
   - Basic connectivity and functionality tests without the need for a GUI.

2. **GUI-Based Control Script**:
   - Comprehensive control over signal pattern creation.
   - Dynamic user interface for intuitive operation.

3. **Custom Signal Pattern Creation**:
   - Easily define and visualize complex signal patterns.

4. **Extensive Hardware Control**:
   - Detailed command over digital and analog outputs.

5. **Cross-Platform Compatibility**:
   - Works on Windows, macOS, and Linux.

## Customization

Modify the signal patterns directly in the GUI or edit the script to preset patterns or automate specific tests.

## Troubleshooting

### Connection Issues
- **Issue**: Unable to connect to the Pulse Streamer.
- **Solution**: Ensure the correct IP address is entered and that the device is properly connected to the network.

### GUI Issues
- **Issue**: The GUI does not start or displays errors.
- **Solution**: Verify that Tkinter is installed and functioning. On Linux, you might need to install it separately via your package manager.

## Acknowledgments

- [Swabian Instruments Documentation](https://www.swabianinstruments.com/pulse-streamer-8-2/doc/)
- Python Community: For providing extensive libraries and tools.
