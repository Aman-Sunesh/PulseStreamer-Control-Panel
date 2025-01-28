import time
import threading
from pulsestreamer import PulseStreamer, findPulseStreamers, OutputState


def find_and_connect():
    try:
        ps = PulseStreamer('169.254.8.2')
        print(f"Connected to Pulse Streamer at {'169.254.8.2'}")
        return ps
    
    except Exception as e:
        print(f"Failed to connect to the Pulse Streamer at {'169.254.8.2'}.\nError: {e}")
        return None
    
def populate_channels(ps):
    num_digital = 8
    num_analog = 2

    digital_channels = list(range(num_digital))
    analog_channels = list(range(num_analog))

    print("\nDigital Channels:", digital_channels)
    print("Analog Channels:", analog_channels)

    return digital_channels, analog_channels


def test_one_channel(ps, choice, channels):
    if choice.lower() == 'd':
        ch = int(input("Enter channel no.: "))

        if ch in channels:
            patt = [(10000,1),(10000,0)]   # Can be changed according to need
            patt.append(patt[0])

            # Define the number of pulses (each pulse consists of a high and a low state)
            num_pulses = 100  # Adjust this number as needed
            
            for _ in range(num_pulses):
                patt.append(patt[0])
                patt.append(patt[1])

            ''''print("Enter the duration and state for each pulse (e.g., 1000 for duration and 1 for state): ")

            for i in range(n):
                duration, state = map(int, input(f"Pulse {i+1}: ").split())
                patt.append((duration, state))'''

            seq = ps.createSequence()
            seq.setDigital([ch], patt)

            try:
                # Stream indefinitely
                ps.stream(seq, n_runs=999999999) 
                print("Digital Channel Test: Streaming indefinitely...")
                input("Press ENTER to stop streaming.")

                ps.forceFinal()
                print("Stopped digital channel streaming")

            except Exception as e:
                print(f"Error streaming to digital channel: {e}")
                

    elif choice.lower() == 'a':
        ch = int(input("Enter channel no.: "))

        if ch in channels:
            duration_high = 1000  # duration in nanoseconds
            voltage_high = 0.5    # high voltage level
            voltage_low = -0.5    # low voltage level

            # Define the number of pulses (each pulse consists of a high and a low state)
            num_pulses = 100  # Adjust this number as needed

            patt = []
            for _ in range(num_pulses): # As in th digital case, pattern can be adjusted as needed
                patt.append((duration_high, voltage_high))  # High state
                patt.append((duration_high, voltage_low))   # Low state

            seq = ps.createSequence()
            seq.setAnalog([ch], patt)

            try:
                # Stream indefinitely
                ps.stream(seq, n_runs=999999999)
                print("Analog Channel Test: Streaming indefinitely...")
                input("Press ENTER to stop streaming.")

                ps.forceFinal()  
                print("Stopped analog channel streaming.")

            except Exception as e:
                print(f"Error streaming to analog channel: {e}")



def main():
    print("=== Pulse Streamer Pin Tester ===\n")
    ps = find_and_connect()
    if not ps:
        return

    digital_channels, analog_channels = populate_channels(ps)

    while True:
        print("\nSelect Test Option:")
        print("1. Test a Specific Channel")
        print("2. Exit")

        choice = input("Enter your choice [1-2]: ")

        if choice == '1':
            print("\nDigital Channels:", digital_channels)
            print("Analog Channels:", analog_channels)

            choice = input("Do you want to test a digital channel or an analog channel (D/A): ")

            if choice.lower() == 'd':
                test_one_channel(ps, choice, digital_channels)
            elif choice.lower() == 'a':
                test_one_channel(ps, choice, analog_channels)

        elif choice == '2':
            print("Exiting Pulse Streamer Pin Tester.")
            break

        else:
            print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    main()