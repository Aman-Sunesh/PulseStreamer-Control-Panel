import tkinter as tk
from tkinter import ttk, messagebox
from pulsestreamer import PulseStreamer, findPulseStreamers, OutputState
import threading
import time

# Constants for testing
DIGITAL_TEST_DURATION = 1000  # in nanoseconds
ANALOG_TEST_VOLTAGE = 0.5     # in Volts
ANALOG_TEST_DURATION = 1000   # in nanoseconds

class PulseStreamerTester:
    def __init__(self, root):
        self.root = root
        self.root.title("Pulse Streamer Pin Tester")
        self.ps = None  # PulseStreamer instance

        # Device Selection Frame
        device_frame = ttk.LabelFrame(root, text="Select Pulse Streamer Device")
        device_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(device_frame, text="Available Devices:").pack(side="left", padx=5, pady=5)
        self.device_var = tk.StringVar()
        self.device_dropdown = ttk.Combobox(device_frame, textvariable=self.device_var, state="readonly", width=50)
        self.device_dropdown.pack(side="left", padx=5, pady=5)

        refresh_button = ttk.Button(device_frame, text="Refresh Devices", command=self.refresh_devices)
        refresh_button.pack(side="left", padx=5, pady=5)

        connect_button = ttk.Button(device_frame, text="Connect", command=self.connect_device)
        connect_button.pack(side="left", padx=5, pady=5)

        # Testing Parameters Frame
        params_frame = ttk.LabelFrame(root, text="Testing Parameters")
        params_frame.pack(fill="x", padx=10, pady=5)

        ttk.Label(params_frame, text="Digital Pulse Duration (ns):").grid(row=0, column=0, padx=5, pady=5, sticky="e")
        self.digital_duration_var = tk.IntVar(value=DIGITAL_TEST_DURATION)
        self.digital_duration_entry = ttk.Entry(params_frame, textvariable=self.digital_duration_var, width=10)
        self.digital_duration_entry.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(params_frame, text="Analog Test Voltage (V):").grid(row=1, column=0, padx=5, pady=5, sticky="e")
        self.analog_voltage_var = tk.DoubleVar(value=ANALOG_TEST_VOLTAGE)
        self.analog_voltage_entry = ttk.Entry(params_frame, textvariable=self.analog_voltage_var, width=10)
        self.analog_voltage_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        ttk.Label(params_frame, text="Analog Pulse Duration (ns):").grid(row=2, column=0, padx=5, pady=5, sticky="e")
        self.analog_duration_var = tk.IntVar(value=ANALOG_TEST_DURATION)
        self.analog_duration_entry = ttk.Entry(params_frame, textvariable=self.analog_duration_var, width=10)
        self.analog_duration_entry.grid(row=2, column=1, padx=5, pady=5, sticky="w")

        # Channel Status Frame
        status_frame = ttk.LabelFrame(root, text="Channel Status")
        status_frame.pack(fill="both", expand=True, padx=10, pady=5)

        # Digital Channels
        digital_frame = ttk.LabelFrame(status_frame, text="Digital Channels")
        digital_frame.pack(fill="both", expand=True, side="left", padx=5, pady=5)

        self.digital_channels = []
        self.digital_labels = {}

        # Analog Channels
        analog_frame = ttk.LabelFrame(status_frame, text="Analog Channels")
        analog_frame.pack(fill="both", expand=True, side="right", padx=5, pady=5)

        self.analog_channels = []
        self.analog_labels = {}

        # Control Buttons Frame
        control_frame = ttk.Frame(root)
        control_frame.pack(fill="x", padx=10, pady=5)

        test_digital_btn = ttk.Button(control_frame, text="Test Digital Channels", command=self.test_digital_channels)
        test_digital_btn.pack(side="left", padx=5, pady=5)

        test_analog_btn = ttk.Button(control_frame, text="Test Analog Channels", command=self.test_analog_channels)
        test_analog_btn.pack(side="left", padx=5, pady=5)

        test_all_btn = ttk.Button(control_frame, text="Test All Channels", command=self.test_all_channels)
        test_all_btn.pack(side="left", padx=5, pady=5)

        # Initialize by refreshing devices
        self.refresh_devices()

    def refresh_devices(self):
        devices = findPulseStreamers()
        device_list = []
        for dev in devices:
            info = f"{dev.hostname} ({dev.ip}) - Serial: {dev.serial}"
            device_list.append(info)
        self.device_dropdown['values'] = device_list
        if device_list:
            self.device_dropdown.current(0)
        else:
            self.device_dropdown.set("No devices found")

    def connect_device(self):
        selected = self.device_var.get()
        if not selected or selected == "No devices found":
            messagebox.showerror("Connection Error", "No Pulse Streamer device selected or found.")
            return
        # Extract IP from selected string
        try:
            ip = selected.split('(')[1].split(')')[0]
        except IndexError:
            messagebox.showerror("Parsing Error", "Failed to parse the device IP address.")
            return
        try:
            self.ps = PulseStreamer(ip)
            messagebox.showinfo("Connection Successful", f"Connected to Pulse Streamer at {ip}")
            self.populate_channels()
        except Exception as e:
            messagebox.showerror("Connection Error", f"Failed to connect to Pulse Streamer at {ip}.\nError: {e}")

    def populate_channels(self):
        if not self.ps:
            return
        # Reset existing channels
        for label in self.digital_labels.values():
            label.destroy()
        for label in self.analog_labels.values():
            label.destroy()
        self.digital_channels = []
        self.analog_channels = []
        self.digital_labels = {}
        self.analog_labels = {}

        # Assuming Pulse Streamer 8/2 has 8 digital and 2 analog channels
        # Adjust based on actual hardware
        num_digital = 8
        num_analog = 2

        digital_frame = self.root.nametowidget('.!labelframe2.!labelframe')
        analog_frame = self.root.nametowidget('.!labelframe2.!labelframe2')

        for ch in range(num_digital):
            self.digital_channels.append(ch)
            lbl = ttk.Label(digital_frame, text=f"Channel {ch}", background="red", width=20)
            lbl.pack(padx=5, pady=2)
            self.digital_labels[ch] = lbl

        for ch in range(num_analog):
            self.analog_channels.append(ch)
            lbl = ttk.Label(analog_frame, text=f"Analog {ch}", background="red", width=20)
            lbl.pack(padx=5, pady=2)
            self.analog_labels[ch] = lbl

    def test_digital_channels(self):
        if not self.ps:
            messagebox.showerror("Error", "No Pulse Streamer connected.")
            return
        threading.Thread(target=self._test_digital_channels_thread, daemon=True).start()

    def _test_digital_channels_thread(self):
        for ch in self.digital_channels:
            try:
                self.update_label(self.digital_labels[ch], "Testing...", "yellow")
                # Create a sequence to set the channel high, wait, then low
                seq = self.ps.createSequence()
                # Define the pulse pattern: High for DIGITAL_TEST_DURATION ns, then Low
                pulse_patt = [(self.digital_duration_var.get(), 1), (self.digital_duration_var.get(), 0)]
                seq.setDigital([ch], pulse_patt)
                # Stream the sequence once
                self.ps.stream(seq, n_runs=1, final=OutputState.ZERO)
                # Allow some time for the pulse to be sent
                time.sleep(self.digital_duration_var.get() * 1e-6 * 2)  # Convert ns to seconds
                self.update_label(self.digital_labels[ch], "Tested", "green")
            except Exception as e:
                self.update_label(self.digital_labels[ch], "Error", "red")
                messagebox.showerror("Digital Channel Test Error", f"Channel {ch} failed.\nError: {e}")

    def test_analog_channels(self):
        if not self.ps:
            messagebox.showerror("Error", "No Pulse Streamer connected.")
            return
        threading.Thread(target=self._test_analog_channels_thread, daemon=True).start()

    def _test_analog_channels_thread(self):
        for ch in self.analog_channels:
            try:
                self.update_label(self.analog_labels[ch], "Testing...", "yellow")
                # Create a sequence to set the analog channel to ANALOG_TEST_VOLTAGE, wait, then reset to 0V
                seq = self.ps.createSequence()
                analog_patt = [
                    (self.analog_duration_var.get(), self.analog_voltage_var.get()),
                    (self.analog_duration_var.get(), 0.0)
                ]
                seq.setAnalog([ch], analog_patt)
                # Stream the sequence once
                self.ps.stream(seq, n_runs=1, final=OutputState.ZERO)
                # Allow some time for the pulse to be sent
                time.sleep(self.analog_duration_var.get() * 1e-6 * 2)  # Convert ns to seconds
                self.update_label(self.analog_labels[ch], "Tested", "green")
            except Exception as e:
                self.update_label(self.analog_labels[ch], "Error", "red")
                messagebox.showerror("Analog Channel Test Error", f"Analog Channel {ch} failed.\nError: {e}")

    def test_all_channels(self):
        if not self.ps:
            messagebox.showerror("Error", "No Pulse Streamer connected.")
            return
        threading.Thread(target=self._test_all_channels_thread, daemon=True).start()

    def _test_all_channels_thread(self):
        # Test Digital Channels
        for ch in self.digital_channels:
            try:
                self.update_label(self.digital_labels[ch], "Testing...", "yellow")
                seq = self.ps.createSequence()
                pulse_patt = [(self.digital_duration_var.get(), 1), (self.digital_duration_var.get(), 0)]
                seq.setDigital([ch], pulse_patt)
                self.ps.stream(seq, n_runs=1, final=OutputState.ZERO)
                time.sleep(self.digital_duration_var.get() * 1e-6 * 2)
                self.update_label(self.digital_labels[ch], "Tested", "green")
            except Exception as e:
                self.update_label(self.digital_labels[ch], "Error", "red")
                messagebox.showerror("Digital Channel Test Error", f"Channel {ch} failed.\nError: {e}")

        # Test Analog Channels
        for ch in self.analog_channels:
            try:
                self.update_label(self.analog_labels[ch], "Testing...", "yellow")
                seq = self.ps.createSequence()
                analog_patt = [
                    (self.analog_duration_var.get(), self.analog_voltage_var.get()),
                    (self.analog_duration_var.get(), 0.0)
                ]
                seq.setAnalog([ch], analog_patt)
                self.ps.stream(seq, n_runs=1, final=OutputState.ZERO)
                time.sleep(self.analog_duration_var.get() * 1e-6 * 2)
                self.update_label(self.analog_labels[ch], "Tested", "green")
            except Exception as e:
                self.update_label(self.analog_labels[ch], "Error", "red")
                messagebox.showerror("Analog Channel Test Error", f"Analog Channel {ch} failed.\nError: {e}")

    def update_label(self, label, text, color):
        label.config(text=text, background=color)
        self.root.update_idletasks()

def main():
    root = tk.Tk()
    app = PulseStreamerTester(root)
    root.mainloop()

if __name__ == "__main__":
    main()
