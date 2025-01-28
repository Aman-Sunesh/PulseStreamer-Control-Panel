import tkinter as tk
from tkinter import messagebox
from pulsestreamer import PulseStreamer, OutputState

class PulseStreamerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Pulse Streamer GUI")
        self.geometry("500x400")

        # PulseStreamer object reference
        self.ps = None

        # --- Widgets for Connection Section ---
        connection_frame = tk.LabelFrame(self, text="1. Connection", padx=10, pady=10)
        connection_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(connection_frame, text="Pulse Streamer IP:").grid(row=0, column=0, sticky="e")
        self.ip_entry = tk.Entry(connection_frame, width=20)
        self.ip_entry.insert(0, "169.254.8.2")  # Default fallback address
        self.ip_entry.grid(row=0, column=1, padx=5, pady=5)

        self.connect_button = tk.Button(connection_frame, text="Connect", command=self.connect_to_device)
        self.connect_button.grid(row=0, column=2, padx=5, pady=5)

        # --- Widgets for Configuration Section ---
        config_frame = tk.LabelFrame(self, text="2. Configuration", padx=10, pady=10)
        config_frame.pack(fill="x", padx=10, pady=5)

        tk.Label(config_frame, text="Select Mode (Digital/Analog):").grid(row=0, column=0, sticky="e")
        self.mode_var = tk.StringVar(value="Digital")
        tk.OptionMenu(config_frame, self.mode_var, "Digital", "Analog").grid(row=0, column=1, sticky="w")

        tk.Label(config_frame, text="Channel #:").grid(row=1, column=0, sticky="e")
        self.channel_entry = tk.Entry(config_frame, width=5)
        self.channel_entry.insert(0, "0")
        self.channel_entry.grid(row=1, column=1, padx=5, pady=5, sticky="w")

        # --- Pattern Entry Section ---
        pattern_frame = tk.LabelFrame(config_frame, text="Enter Pattern (one pair per line)", padx=5, pady=5)
        pattern_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="we")

        tk.Label(pattern_frame, text="For Digital:  duration  state\nFor Analog:   duration  voltage").pack(anchor="w")
        self.pattern_text = tk.Text(pattern_frame, width=30, height=5)
        self.pattern_text.pack(fill="both", expand=True)

        # --- Number of Runs (n_runs) ---
        tk.Label(config_frame, text="Number of Runs (e.g., -1=∞):").grid(row=3, column=0, sticky="e")
        self.runs_entry = tk.Entry(config_frame, width=5)
        self.runs_entry.insert(0, "-1")  # Default to infinite
        self.runs_entry.grid(row=3, column=1, padx=5, pady=5, sticky="w")

        # --- Stream Control Buttons ---
        button_frame = tk.Frame(self)
        button_frame.pack(pady=10)

        self.start_button = tk.Button(button_frame, text="Start Streaming", command=self.start_streaming, state="disabled")
        self.start_button.pack(side="left", padx=10)

        self.stop_button = tk.Button(button_frame, text="Stop Streaming", command=self.stop_streaming, state="disabled")
        self.stop_button.pack(side="left", padx=10)

    def connect_to_device(self):
        """Attempt to connect to the Pulse Streamer device using the IP provided."""
        ip_address = self.ip_entry.get().strip()
        try:
            self.ps = PulseStreamer(ip_address)
            messagebox.showinfo("Connection", f"Connected to Pulse Streamer at {ip_address}")
            self.start_button.config(state="normal")
            self.stop_button.config(state="normal")
        except Exception as e:
            self.ps = None
            messagebox.showerror("Connection Error", f"Failed to connect: {e}")

    def start_streaming(self):
        """Reads user inputs, creates the pattern, and streams to the chosen channel."""
        if not self.ps:
            messagebox.showwarning("Warning", "No Pulse Streamer connected.")
            return

        mode = self.mode_var.get().lower()    # 'digital' or 'analog'
        channel_str = self.channel_entry.get().strip()
        pattern_str = self.pattern_text.get("1.0", "end").strip()
        n_runs_str = self.runs_entry.get().strip()

        # Validate inputs
        try:
            ch = int(channel_str)
            n_runs = int(n_runs_str)
        except ValueError:
            messagebox.showerror("Input Error", "Channel and Number of Runs must be integers.")
            return

        # Parse pattern
        # For each line, we expect "duration  level/voltage"
        lines = pattern_str.splitlines()
        patt = []
        for idx, line in enumerate(lines, start=1):
            line = line.strip()
            if not line:
                continue
            parts = line.split()
            if len(parts) != 2:
                messagebox.showerror("Pattern Error", f"Line {idx} is invalid. Must be 'duration level'.")
                return
            try:
                duration = float(parts[0])
                level = float(parts[1])
            except ValueError:
                messagebox.showerror("Pattern Error", f"Invalid numbers on line {idx}: '{line}'")
                return

            # Convert to int if you want durations as integers
            duration = int(duration)

            # Append tuple (duration, state or voltage)
            patt.append((duration, level))

        if not patt:
            messagebox.showerror("Pattern Error", "No valid pattern entered.")
            return

        # Build the sequence
        seq = self.ps.createSequence()

        if mode == "digital":
            # Ensure the 'level' is 0 or 1 if it's truly digital
            # or let the user create patterns with 0/1 themselves
            seq.setDigital([ch], patt)
        else:
            # mode == "analog"
            seq.setAnalog([ch], patt)

        # Stream
        try:
            self.ps.stream(seq, n_runs=n_runs)
            messagebox.showinfo("Streaming", f"Pattern is now streaming on {mode} channel {ch}.")
        except Exception as e:
            messagebox.showerror("Stream Error", f"Error starting the stream: {e}")

    def stop_streaming(self):
        """Stops any ongoing streaming by forcing final state."""
        if not self.ps:
            return
        try:
            self.ps.forceFinal()
            messagebox.showinfo("Stopped", "Stopped streaming. Outputs set to final state.")
        except Exception as e:
            messagebox.showerror("Stop Error", f"Error stopping the stream: {e}")


def main():
    app = PulseStreamerApp()
    app.mainloop()

if __name__ == "__main__":
    main()
