# Usage Examples

This document provides practical examples of using the Bluetooth Signal Strength Monitor.

## Example 1: Basic Monitoring (Linux)

```bash
$ sudo python3 bluetooth_monitor_simple.py
======================================================================
  Bluetooth Signal Strength Monitor
  Platform: Linux
======================================================================

Using: hcitool

Scanning for Bluetooth devices...
This may take up to 10 seconds...

Found 2 device(s):

1. AirPods Pro
   Address: AA:BB:CC:DD:EE:FF
   Signal:   -48 dBm [████████████] (Excellent)

2. Bluetooth Mouse
   Address: 11:22:33:44:55:66
   Signal:   -62 dBm [██████░░░░░░] (Fair)

Select device to monitor (1-2): 1

Update interval in seconds (default: 1.0): 1

Monitoring device: AirPods Pro
Address: AA:BB:CC:DD:EE:FF
Update interval: 1.0 second(s)

Press Ctrl+C to stop
======================================================================
[14:25:30] Signal:  -48 dBm [████████████] (Excellent)
[14:25:31] Signal:  -49 dBm [████████████] (Excellent)
[14:25:32] Signal:  -51 dBm [█████████░░░] (Good)
[14:25:33] Signal:  -54 dBm [█████████░░░] (Good)
^C
======================================================================
Monitoring stopped
```

## Example 2: Testing Distance Effect

Monitor signal while walking away from device:

```bash
$ sudo python3 bluetooth_monitor_simple.py

# ... device selection ...

Monitoring device: Bluetooth Speaker
Address: 00:11:22:33:44:55
Update interval: 1.0 second(s)

Press Ctrl+C to stop
======================================================================
[15:00:00] Signal:  -42 dBm [████████████] (Excellent)  # Right next to device
[15:00:01] Signal:  -44 dBm [████████████] (Excellent)  
[15:00:02] Signal:  -47 dBm [████████████] (Excellent)  # 1 meter away
[15:00:03] Signal:  -51 dBm [█████████░░░] (Good)       # 2 meters away
[15:00:04] Signal:  -56 dBm [█████████░░░] (Good)       # 4 meters away
[15:00:05] Signal:  -61 dBm [██████░░░░░░] (Fair)       # 6 meters away
[15:00:06] Signal:  -66 dBm [██████░░░░░░] (Fair)       # 8 meters away
[15:00:07] Signal:  -71 dBm [███░░░░░░░░░] (Poor)       # 10 meters away
[15:00:08] Signal:  -76 dBm [███░░░░░░░░░] (Poor)       # 12 meters away
```

Notice how the dBm value becomes more negative as distance increases.

## Example 3: Slow Update Interval

For monitoring over longer periods:

```bash
$ sudo python3 bluetooth_monitor_simple.py

# ... device selection ...

Update interval in seconds (default: 1.0): 5

Monitoring device: Fitness Tracker
Address: FF:EE:DD:CC:BB:AA
Update interval: 5.0 second(s)

Press Ctrl+C to stop
======================================================================
[16:10:00] Signal:  -55 dBm [█████████░░░] (Good)
[16:10:05] Signal:  -56 dBm [█████████░░░] (Good)
[16:10:10] Signal:  -54 dBm [█████████░░░] (Good)
[16:10:15] Signal:  -57 dBm [█████████░░░] (Good)
```

## Example 4: Single Device Auto-Selection

When only one device is available:

```bash
$ sudo python3 bluetooth_monitor_simple.py
======================================================================
  Bluetooth Signal Strength Monitor
  Platform: Linux
======================================================================

Using: hcitool

Scanning for Bluetooth devices...
This may take up to 10 seconds...

Found 1 device(s):

1. Smart Watch
   Address: 12:34:56:78:90:AB
   Signal:   -50 dBm [████████████] (Excellent)

Auto-selecting the only device found...

Update interval in seconds (default: 1.0): 

Monitoring device: Smart Watch
Address: 12:34:56:78:90:AB
Update interval: 1.0 second(s)

Press Ctrl+C to stop
======================================================================
[17:00:00] Signal:  -50 dBm [████████████] (Excellent)
```

## Example 5: Device Out of Range

What happens when device loses connection:

```bash
[18:00:00] Signal:  -68 dBm [██████░░░░░░] (Fair)
[18:00:01] Signal:  -72 dBm [███░░░░░░░░░] (Poor)
[18:00:02] Signal:  -78 dBm [███░░░░░░░░░] (Poor)
[18:00:03] Signal: N/A (not available)
[18:00:04] Signal: N/A (not available)
[18:00:05] Signal: N/A (not available)
[18:00:06] Signal: N/A (not available)
[18:00:07] Signal: N/A (not available)

[18:00:08] Warning: No signal detected for 5 attempts
Device may be out of range or disconnected
```

## Example 6: Windows Usage

Running on Windows (Command Prompt as Administrator):

```cmd
C:\> python bluetooth_monitor.py
======================================================================
Bluetooth Signal Strength Monitor
Platform: Windows
======================================================================

Scanning for Bluetooth devices...
This may take up to 10 seconds...

Found 1 device(s):

1. Surface Headphones
   Address: 00:11:22:33:44:55
   Signal: N/A (not available)

Note: Windows RSSI detection requires additional setup
Auto-selecting the only device found...

Update interval in seconds (default: 1): 2

Monitoring device: Surface Headphones
Address: 00:11:22:33:44:55
Update interval: 2 second(s)
Press Ctrl+C to stop

------------------------------------------------------------
Note: Windows RSSI detection has limitations
```

## Example 7: Fast Updates

For real-time monitoring with quick updates:

```bash
$ sudo python3 bluetooth_monitor_simple.py

# ... device selection ...

Update interval in seconds (default: 1.0): 0.5

Monitoring device: Bluetooth Keyboard
Address: AA:BB:CC:DD:EE:FF
Update interval: 0.5 second(s)

Press Ctrl+C to stop
======================================================================
[19:00:00.0] Signal:  -52 dBm [█████████░░░] (Good)
[19:00:00.5] Signal:  -52 dBm [█████████░░░] (Good)
[19:00:01.0] Signal:  -53 dBm [█████████░░░] (Good)
[19:00:01.5] Signal:  -51 dBm [█████████░░░] (Good)
```

## Use Cases

### 1. Testing Bluetooth Range
Walk around with a device to see how far you can go before signal degrades:
- Start next to device (should show Excellent)
- Walk away slowly
- Watch signal drop from Excellent → Good → Fair → Poor → N/A

### 2. Finding Optimal Device Placement
Monitor signal strength while repositioning devices:
- Place device in different locations
- Check signal strength in your usual working area
- Find the location with best signal

### 3. Debugging Connection Issues
If Bluetooth keeps disconnecting:
- Monitor signal strength over time
- Identify if signal is consistently weak
- Check for interference patterns

### 4. Battery Conservation
Some devices reduce transmit power when battery is low:
- Monitor signal strength over battery life
- Notice if signal weakens as battery drains

### 5. Obstacle Detection
Test how walls and objects affect signal:
- Monitor signal in same position
- Place obstacles between device and receiver
- Observe signal degradation

## Tips

1. **Keep device active**: Some devices only report accurate RSSI during active use
2. **Connect before monitoring**: Most systems require an active connection
3. **Allow stabilization time**: Signal readings may fluctuate initially
4. **Use consistent intervals**: 1-2 seconds works well for most cases
5. **Monitor during activity**: Play music or transfer data for best results
