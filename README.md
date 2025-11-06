# Bluetooth Signal Strength Monitor

A cross-platform tool for monitoring Bluetooth device signal strength in real-time on Windows and Linux.

## Features

- 🔍 **Device Discovery**: Automatically scans and lists nearby Bluetooth devices
- 📊 **Real-time Monitoring**: Continuously displays signal strength in dBm
- 📉 **Live Updates**: Shows signal strength changes as you move away from the device
- 🎯 **Quality Indicators**: Categorizes signal as Excellent, Good, Fair, or Poor
- 💻 **Cross-Platform**: Works on both Windows and Linux
- ⚡ **Configurable**: Adjustable update intervals

## Signal Strength Scale

The tool displays signal strength in dBm (decibels relative to one milliwatt):

- **-50 dBm or higher**: Excellent signal
- **-60 dBm to -50 dBm**: Good signal
- **-70 dBm to -60 dBm**: Fair signal
- **Below -70 dBm**: Poor signal

As you move away from the device, the dBm value becomes more negative, indicating weaker signal strength.

## Requirements

### Linux
- Python 3.6 or higher
- BlueZ (Bluetooth stack)
- PyBluez library
- Root/sudo access for Bluetooth operations

### Windows
- Python 3.6 or higher
- Bluetooth adapter
- PyBluez library
- Optional: WMI library for enhanced functionality

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/Sushree1j/AutoLocker.git
   cd AutoLocker
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

### Platform-Specific Setup

#### Linux
Install BlueZ tools:
```bash
# Debian/Ubuntu
sudo apt-get install bluez bluetooth libbluetooth-dev

# Fedora/RHEL
sudo dnf install bluez bluez-libs-devel

# Arch Linux
sudo pacman -S bluez bluez-utils
```

Enable Bluetooth service:
```bash
sudo systemctl start bluetooth
sudo systemctl enable bluetooth
```

#### Windows
Install Microsoft Visual C++ Build Tools if PyBluez installation fails:
- Download from: https://visualstudio.microsoft.com/visual-cpp-build-tools/

Optional WMI library:
```bash
pip install WMI
```

## Usage

### Basic Usage

Run the monitor with sudo/administrator privileges:

**Linux:**
```bash
sudo python3 bluetooth_monitor.py
```

**Windows (as Administrator):**
```bash
python bluetooth_monitor.py
```

### Interactive Steps

1. The tool will scan for nearby Bluetooth devices (takes ~8-10 seconds)
2. Select a device from the list by entering its number
3. Choose an update interval (default: 1 second)
4. Monitor the live signal strength
5. Press `Ctrl+C` to stop monitoring

### Example Output

```
============================================================
Bluetooth Signal Strength Monitor
Platform: Linux
============================================================

Scanning for Bluetooth devices...
This may take up to 10 seconds...

Found 2 device(s):

1. My Bluetooth Headset
   Address: AA:BB:CC:DD:EE:FF
   Signal: -45 dBm (Excellent)

2. Smartphone
   Address: 11:22:33:44:55:66
   Signal: -67 dBm (Fair)

Select device to monitor (1-2): 1

Update interval in seconds (default: 1): 1

Monitoring device: My Bluetooth Headset (AA:BB:CC:DD:EE:FF)
Update interval: 1 second(s)
Press Ctrl+C to stop

------------------------------------------------------------
[14:23:45] Signal Strength: -45 dBm (Excellent)
[14:23:46] Signal Strength: -48 dBm (Excellent)
[14:23:47] Signal Strength: -52 dBm (Good)
[14:23:48] Signal Strength: -58 dBm (Good)
[14:23:49] Signal Strength: -65 dBm (Fair)
[14:23:50] Signal Strength: -72 dBm (Poor)
```

## How It Works

The tool uses different methods depending on the platform:

### Linux
- Uses `hcitool rssi` command to query RSSI (Received Signal Strength Indicator)
- Falls back to `bluetoothctl info` if hcitool is unavailable
- Provides accurate real-time signal strength measurements

### Windows
- Uses PyBluez library for device discovery
- Attempts to use WMI for signal strength when available
- Note: Windows has more limitations for RSSI access due to API restrictions

## Troubleshooting

### Linux Issues

**"Operation not permitted" error:**
```bash
# Run with sudo
sudo python3 bluetooth_monitor.py
```

**"hcitool not found" error:**
```bash
# Install bluez tools
sudo apt-get install bluez
```

**No devices found:**
```bash
# Check if Bluetooth is running
sudo systemctl status bluetooth

# Enable Bluetooth adapter
sudo hciconfig hci0 up

# Scan manually
sudo hciscan
```

### Windows Issues

**PyBluez installation fails:**
- Install Microsoft Visual C++ Build Tools
- Or use pre-built wheels: `pip install pybluez-win10`

**No devices found:**
- Ensure Bluetooth is enabled in Windows Settings
- Make sure devices are paired and connected
- Run Command Prompt as Administrator

## Permissions

### Linux
The tool requires root access to query Bluetooth RSSI values. Run with `sudo`.

### Windows
Run the Command Prompt or PowerShell as Administrator.

## Limitations

- **Windows**: RSSI access is limited by Windows Bluetooth API. Some features may not work as expected.
- **Connection Required**: On some systems, the device must be connected (not just paired) for RSSI readings.
- **Update Rate**: Very fast update intervals (<0.5s) may not show changes due to OS caching.

## Contributing

Contributions are welcome! Please feel free to submit issues or pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Author

Swarnabha (Sushree1j)

## Acknowledgments

- PyBluez library for Bluetooth communication
- BlueZ stack for Linux Bluetooth support
