# Quick Start Guide

## Getting Started in 3 Steps

### 1. Install Dependencies

**Linux (Debian/Ubuntu):**
```bash
# Install system packages
sudo apt-get update
sudo apt-get install python3 python3-pip bluez bluetooth

# Install Python dependencies (optional, for full version)
pip3 install -r requirements.txt
```

**Linux (Fedora/RHEL):**
```bash
# Install system packages
sudo dnf install python3 python3-pip bluez

# Install Python dependencies (optional)
pip3 install -r requirements.txt
```

**Windows:**
```bash
# Install Python dependencies
pip install -r requirements.txt
```

### 2. Choose Your Version

This project provides two versions:

#### Simple Version (Recommended for Linux)
- **File:** `bluetooth_monitor_simple.py`
- **Requirements:** Only system Bluetooth tools (bluez)
- **No extra Python packages needed**
- **Best for:** Quick testing, minimal setup

```bash
sudo python3 bluetooth_monitor_simple.py
```

#### Full Version
- **File:** `bluetooth_monitor.py`
- **Requirements:** PyBluez library
- **Best for:** Cross-platform use, enhanced features

```bash
sudo python3 bluetooth_monitor.py
```

### 3. Run the Tool

**On Linux:**
```bash
# Using the simple version (recommended)
sudo python3 bluetooth_monitor_simple.py

# Or using the full version
sudo python3 bluetooth_monitor.py
```

**On Windows (run Command Prompt as Administrator):**
```bash
python bluetooth_monitor.py
```

## Example Session

```
==================================================================
  Bluetooth Signal Strength Monitor
  Platform: Linux
==================================================================

Using: hcitool

Scanning for Bluetooth devices...
This may take up to 10 seconds...

Found 1 device(s):

1. MyDevice
   Address: 00:11:22:33:44:55
   Signal:  -45 dBm [████████████] (Excellent)

Auto-selecting the only device found...

Update interval in seconds (default: 1.0): 2

Monitoring device: MyDevice
Address: 00:11:22:33:44:55
Update interval: 2.0 second(s)

Press Ctrl+C to stop
======================================================================
[15:30:00] Signal:  -45 dBm [████████████] (Excellent)
[15:30:02] Signal:  -52 dBm [█████████░░░] (Good)
[15:30:04] Signal:  -58 dBm [█████████░░░] (Good)
[15:30:06] Signal:  -65 dBm [██████░░░░░░] (Fair)
[15:30:08] Signal:  -72 dBm [███░░░░░░░░░] (Poor)
```

## Understanding Signal Strength

The signal strength is displayed in **dBm** (decibels relative to one milliwatt):

| dBm Range | Quality | Visual Bar | Typical Distance |
|-----------|---------|------------|------------------|
| -50 or better | Excellent | ████████████ | Very close (< 1m) |
| -60 to -50 | Good | █████████░░░ | Close (1-5m) |
| -70 to -60 | Fair | ██████░░░░░░ | Medium (5-10m) |
| Below -70 | Poor | ███░░░░░░░░░ | Far (> 10m) |

**Important:** As you move away from the device, the dBm value becomes MORE NEGATIVE (e.g., -80 dBm is weaker than -60 dBm).

## Troubleshooting

### "No devices found"

**Linux:**
1. Check if Bluetooth is enabled:
   ```bash
   sudo systemctl status bluetooth
   ```

2. Enable Bluetooth adapter:
   ```bash
   sudo hciconfig hci0 up
   ```

3. Pair your device:
   ```bash
   bluetoothctl
   # In bluetoothctl:
   power on
   agent on
   scan on
   # Wait for device to appear
   pair <MAC_ADDRESS>
   connect <MAC_ADDRESS>
   ```

**Windows:**
1. Open Settings → Devices → Bluetooth
2. Ensure Bluetooth is ON
3. Pair the device you want to monitor

### "Permission denied"

On Linux, Bluetooth operations require root access:
```bash
sudo python3 bluetooth_monitor_simple.py
```

### "hcitool not found"

Install bluez package:
```bash
# Debian/Ubuntu
sudo apt-get install bluez

# Fedora/RHEL
sudo dnf install bluez
```

### Signal shows as "N/A"

1. Make sure the device is **connected** (not just paired)
2. Some devices need to be actively used to report RSSI
3. Try the simple version if the full version doesn't work

## Tips for Best Results

1. **Connect the device first** - Most systems require an active connection to read RSSI
2. **Use lower update intervals** - 1-2 seconds works best for real-time monitoring
3. **Keep the device active** - Play audio or transfer data for consistent readings
4. **Walk slowly** - Give the tool time to detect signal changes

## Need Help?

If you encounter issues:
1. Check that you're using `sudo` on Linux
2. Verify Bluetooth is enabled and device is connected
3. Try both the simple and full versions
4. Check the detailed README.md for more information
