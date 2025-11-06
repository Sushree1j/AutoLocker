#!/usr/bin/env python3
"""
Bluetooth Signal Strength Monitor - Simple Version
A cross-platform tool to monitor Bluetooth device signal strength
This version provides a basic implementation that works on most systems
"""

import sys
import time
import platform
import subprocess
from typing import List, Optional, Tuple

PLATFORM = platform.system()

# Constants
MIN_UPDATE_INTERVAL = 0.1  # Minimum update interval in seconds
MAX_UPDATE_INTERVAL = 60   # Maximum update interval in seconds


def discover_devices_pybluez() -> List[Tuple[str, str]]:
    """
    Discover Bluetooth devices using PyBluez
    Returns list of (address, name) tuples
    """
    try:
        import bluetooth
        print("Scanning for Bluetooth devices...")
        print("This may take up to 10 seconds...\n")
        
        devices = bluetooth.discover_devices(
            duration=8,
            lookup_names=True,
            flush_cache=True,
            lookup_class=False
        )
        return devices
    except ImportError:
        return []
    except Exception as e:
        print(f"Error during device discovery: {e}")
        return []


def discover_devices_bluetoothctl() -> List[Tuple[str, str]]:
    """
    Discover Bluetooth devices using bluetoothctl (Linux)
    Returns list of (address, name) tuples
    """
    devices = []
    try:
        # Start scanning
        subprocess.run(['bluetoothctl', 'scan', 'on'], 
                      capture_output=True, 
                      timeout=1)
        
        time.sleep(8)  # Scan for 8 seconds
        
        # Stop scanning
        subprocess.run(['bluetoothctl', 'scan', 'off'], 
                      capture_output=True, 
                      timeout=1)
        
        # Get paired devices
        result = subprocess.run(['bluetoothctl', 'devices'], 
                               capture_output=True, 
                               text=True, 
                               timeout=5)
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Device'):
                    parts = line.split(maxsplit=2)
                    if len(parts) >= 3:
                        address = parts[1]
                        name = parts[2] if len(parts) > 2 else "Unknown"
                        devices.append((address, name))
        
        return devices
    except Exception as e:
        print(f"Error with bluetoothctl: {e}")
        return []


def get_rssi_linux_hcitool(address: str) -> Optional[int]:
    """Get RSSI using hcitool on Linux"""
    try:
        result = subprocess.run(
            ['hcitool', 'rssi', address],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            output = result.stdout.strip()
            if "RSSI return value:" in output:
                rssi_str = output.split("RSSI return value:")[1].strip()
                return int(rssi_str)
        
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return None


def get_rssi_linux_bluetoothctl(address: str) -> Optional[int]:
    """Get RSSI using bluetoothctl on Linux"""
    try:
        result = subprocess.run(
            ['bluetoothctl', 'info', address],
            capture_output=True,
            text=True,
            timeout=5
        )
        
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                line = line.strip()
                if 'RSSI:' in line:
                    rssi_str = line.split('RSSI:')[1].strip()
                    # Remove any non-numeric characters except minus
                    rssi_str = ''.join(c for c in rssi_str if c.isdigit() or c == '-')
                    # Validate format before converting
                    if rssi_str and rssi_str != '-' and rssi_str.lstrip('-').isdigit():
                        return int(rssi_str)
        
        return None
    except (FileNotFoundError, subprocess.TimeoutExpired, ValueError):
        return None


def get_signal_strength(address: str) -> Optional[int]:
    """
    Get signal strength (RSSI) for a Bluetooth device
    Returns RSSI value in dBm or None if unavailable
    """
    if PLATFORM == "Linux":
        # Try hcitool first
        rssi = get_rssi_linux_hcitool(address)
        if rssi is not None:
            return rssi
        
        # Fall back to bluetoothctl
        rssi = get_rssi_linux_bluetoothctl(address)
        if rssi is not None:
            return rssi
    
    elif PLATFORM == "Windows":
        print("Note: Windows RSSI detection requires additional setup")
        # Windows implementation would require WMI or other methods
        # This is a placeholder
        return None
    
    return None


def format_signal_strength(rssi: Optional[int]) -> str:
    """Format RSSI value with quality indicator"""
    if rssi is None:
        return "N/A (not available)"
    
    if rssi >= -50:
        quality = "Excellent"
        bars = "████████████"
    elif rssi >= -60:
        quality = "Good"
        bars = "█████████░░░"
    elif rssi >= -70:
        quality = "Fair"
        bars = "██████░░░░░░"
    else:
        quality = "Poor"
        bars = "███░░░░░░░░░"
    
    return f"{rssi:4d} dBm [{bars}] ({quality})"


def monitor_device(address: str, name: str, interval: float = 1.0):
    """
    Monitor signal strength of a specific device continuously
    """
    print(f"\nMonitoring device: {name}")
    print(f"Address: {address}")
    print(f"Update interval: {interval} second(s)")
    print("\nPress Ctrl+C to stop")
    print("=" * 70)
    
    try:
        consecutive_failures = 0
        max_failures = 5
        
        while True:
            rssi = get_signal_strength(address)
            signal_str = format_signal_strength(rssi)
            timestamp = time.strftime("%H:%M:%S")
            
            if rssi is None:
                consecutive_failures += 1
                if consecutive_failures >= max_failures:
                    print(f"\n[{timestamp}] Warning: No signal detected for {max_failures} attempts")
                    print("Device may be out of range or disconnected")
                    consecutive_failures = 0  # Reset counter
            else:
                consecutive_failures = 0
            
            # Clear line and print
            print(f"\r[{timestamp}] Signal: {signal_str}", end='', flush=True)
            
            time.sleep(interval)
            
    except KeyboardInterrupt:
        print("\n" + "=" * 70)
        print("Monitoring stopped")


def main():
    """Main entry point"""
    print("=" * 70)
    print("  Bluetooth Signal Strength Monitor")
    print(f"  Platform: {PLATFORM}")
    print("=" * 70)
    print()
    
    # Check platform support
    if PLATFORM not in ["Linux", "Windows"]:
        print(f"Error: Unsupported platform '{PLATFORM}'")
        print("This tool supports Windows and Linux only")
        sys.exit(1)
    
    # Check for Linux tools
    if PLATFORM == "Linux":
        has_hcitool = subprocess.run(
            ['which', 'hcitool'], 
            capture_output=True
        ).returncode == 0
        
        has_bluetoothctl = subprocess.run(
            ['which', 'bluetoothctl'], 
            capture_output=True
        ).returncode == 0
        
        if not has_hcitool and not has_bluetoothctl:
            print("Error: Neither hcitool nor bluetoothctl found")
            print("Please install bluez package:")
            print("  sudo apt-get install bluez  # Debian/Ubuntu")
            print("  sudo dnf install bluez      # Fedora/RHEL")
            sys.exit(1)
        
        print(f"Using: {'hcitool' if has_hcitool else 'bluetoothctl'}")
        print()
    
    # Discover devices - try PyBluez first
    devices = discover_devices_pybluez()
    
    # If PyBluez not available or no devices, try platform-specific method
    if not devices and PLATFORM == "Linux":
        print("PyBluez not available, trying bluetoothctl...\n")
        devices = discover_devices_bluetoothctl()
    
    if not devices:
        print("No Bluetooth devices found.")
        print("\nTroubleshooting:")
        print("- Ensure Bluetooth is enabled on your system")
        print("- Make sure target device is powered on and in range")
        
        if PLATFORM == "Linux":
            print("- You may need sudo: sudo python3 bluetooth_monitor_simple.py")
            print("- Check Bluetooth service: sudo systemctl status bluetooth")
        elif PLATFORM == "Windows":
            print("- Run as Administrator")
            print("- Install PyBluez: pip install pybluez")
        
        sys.exit(1)
    
    # Display discovered devices
    print(f"Found {len(devices)} device(s):")
    print()
    
    for idx, (addr, name) in enumerate(devices, 1):
        print(f"{idx}. {name}")
        print(f"   Address: {addr}")
        
        # Try to get current signal strength
        rssi = get_signal_strength(addr)
        signal_str = format_signal_strength(rssi)
        print(f"   Signal:  {signal_str}")
        print()
    
    # Let user select a device
    if len(devices) == 1:
        print("Auto-selecting the only device found...")
        selected_idx = 0
    else:
        try:
            selection = input(f"Select device to monitor (1-{len(devices)}): ").strip()
            selected_idx = int(selection) - 1
            
            if selected_idx < 0 or selected_idx >= len(devices):
                print("Invalid selection")
                sys.exit(1)
        except (ValueError, KeyboardInterrupt):
            print("\nCancelled")
            sys.exit(0)
    
    selected_addr, selected_name = devices[selected_idx]
    
    # Ask for update interval
    try:
        interval_input = input("\nUpdate interval in seconds (default: 1.0): ").strip()
        interval = float(interval_input) if interval_input else 1.0
        
        if interval < MIN_UPDATE_INTERVAL:
            print(f"Interval too short, using {MIN_UPDATE_INTERVAL} seconds")
            interval = MIN_UPDATE_INTERVAL
        elif interval > MAX_UPDATE_INTERVAL:
            print(f"Interval too long, using {MAX_UPDATE_INTERVAL} seconds")
            interval = MAX_UPDATE_INTERVAL
            
    except (ValueError, KeyboardInterrupt):
        interval = 1.0
        print(f"Using default interval: {interval} second(s)")
    
    # Start monitoring
    monitor_device(selected_addr, selected_name, interval)


if __name__ == "__main__":
    main()
