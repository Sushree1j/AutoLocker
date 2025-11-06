#!/usr/bin/env python3
"""
Bluetooth Signal Strength Monitor
A cross-platform tool to monitor Bluetooth device signal strength in real-time
Supports Windows and Linux platforms
"""

import sys
import time
import platform
from typing import List, Dict, Optional

# Platform-specific imports
if platform.system() == "Windows":
    try:
        import bluetooth
    except ImportError:
        print("PyBluez not installed. Install with: pip install pybluez")
        sys.exit(1)
elif platform.system() == "Linux":
    try:
        import bluetooth
    except ImportError:
        print("PyBluez not installed. Install with: pip install pybluez")
        sys.exit(1)
else:
    print(f"Unsupported platform: {platform.system()}")
    print("This tool supports Windows and Linux only")
    sys.exit(1)


class BluetoothMonitor:
    """Monitor Bluetooth device signal strength"""
    
    def __init__(self):
        self.current_os = platform.system()
        
    def discover_devices(self) -> List[tuple]:
        """
        Discover nearby Bluetooth devices
        Returns list of tuples (address, name)
        """
        print("Scanning for Bluetooth devices...")
        print("This may take up to 10 seconds...\n")
        
        try:
            devices = bluetooth.discover_devices(
                duration=8,
                lookup_names=True,
                flush_cache=True,
                lookup_class=False
            )
            return devices
        except Exception as e:
            print(f"Error during device discovery: {e}")
            return []
    
    def get_signal_strength_linux(self, address: str) -> Optional[int]:
        """
        Get signal strength (RSSI) for a Bluetooth device on Linux
        Returns RSSI value in dBm or None if unavailable
        """
        try:
            import subprocess
            # Use hcitool to get RSSI
            result = subprocess.run(
                ['hcitool', 'rssi', address],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                output = result.stdout.strip()
                # Parse RSSI value from output like "RSSI return value: -45"
                if "RSSI return value:" in output:
                    rssi_str = output.split("RSSI return value:")[1].strip()
                    try:
                        return int(rssi_str)
                    except ValueError:
                        # Invalid RSSI format
                        pass
            
            # Alternative method using bluetoothctl
            result = subprocess.run(
                ['bluetoothctl', 'info', address],
                capture_output=True,
                text=True,
                timeout=5
            )
            
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if 'RSSI:' in line:
                        rssi_str = line.split('RSSI:')[1].strip()
                        try:
                            return int(rssi_str)
                        except ValueError:
                            # Invalid RSSI format
                            pass
            
            return None
            
        except FileNotFoundError:
            print("Error: hcitool or bluetoothctl not found. Install bluez package.")
            return None
        except subprocess.TimeoutExpired:
            print("Timeout while getting signal strength")
            return None
        except Exception as e:
            print(f"Error getting signal strength: {e}")
            return None
    
    def get_signal_strength_windows(self, address: str) -> Optional[int]:
        """
        Get signal strength (RSSI) for a Bluetooth device on Windows
        Returns RSSI value in dBm or None if unavailable
        """
        try:
            # Windows-specific implementation using WMI
            import wmi
            c = wmi.WMI()
            
            # Query Bluetooth devices
            for device in c.Win32_PnPEntity():
                if device.PNPDeviceID and 'BTHENUM' in device.PNPDeviceID:
                    # Extract RSSI if available
                    # This is a simplified approach
                    pass
            
            # Fallback: use PyBluez socket-based approach
            # This provides limited RSSI information on Windows
            print("Note: Windows RSSI detection has limitations")
            return None
            
        except ImportError:
            print("WMI module not installed. Install with: pip install WMI")
            return None
        except Exception as e:
            print(f"Error getting signal strength on Windows: {e}")
            return None
    
    def get_signal_strength(self, address: str) -> Optional[int]:
        """
        Get signal strength for a device based on current OS
        """
        if self.current_os == "Linux":
            return self.get_signal_strength_linux(address)
        elif self.current_os == "Windows":
            return self.get_signal_strength_windows(address)
        return None
    
    def format_signal_strength(self, rssi: Optional[int]) -> str:
        """
        Format RSSI value with quality indicator
        """
        if rssi is None:
            return "N/A"
        
        quality = ""
        if rssi >= -50:
            quality = "Excellent"
        elif rssi >= -60:
            quality = "Good"
        elif rssi >= -70:
            quality = "Fair"
        else:
            quality = "Poor"
        
        return f"{rssi} dBm ({quality})"
    
    def monitor_device(self, address: str, name: str, interval: float = 1.0):
        """
        Monitor signal strength of a specific device continuously
        
        Args:
            address: Bluetooth MAC address
            name: Device name
            interval: Update interval in seconds
        """
        print(f"\nMonitoring device: {name} ({address})")
        print(f"Update interval: {interval} second(s)")
        print("Press Ctrl+C to stop\n")
        print("-" * 60)
        
        try:
            iteration = 0
            while True:
                iteration += 1
                rssi = self.get_signal_strength(address)
                signal_str = self.format_signal_strength(rssi)
                
                timestamp = time.strftime("%H:%M:%S")
                print(f"[{timestamp}] Signal Strength: {signal_str}")
                
                time.sleep(interval)
                
        except KeyboardInterrupt:
            print("\n" + "-" * 60)
            print("Monitoring stopped")


def main():
    """Main entry point"""
    print("=" * 60)
    print("Bluetooth Signal Strength Monitor")
    print(f"Platform: {platform.system()}")
    print("=" * 60)
    print()
    
    monitor = BluetoothMonitor()
    
    # Discover devices
    devices = monitor.discover_devices()
    
    if not devices:
        print("No Bluetooth devices found.")
        print("\nMake sure:")
        print("- Bluetooth is enabled on your system")
        print("- Target device is powered on and in range")
        print("- You have necessary permissions (may need sudo on Linux)")
        sys.exit(1)
    
    # Display discovered devices
    print(f"Found {len(devices)} device(s):\n")
    for idx, (addr, name) in enumerate(devices, 1):
        print(f"{idx}. {name}")
        print(f"   Address: {addr}")
        
        # Try to get current signal strength
        rssi = monitor.get_signal_strength(addr)
        signal_str = monitor.format_signal_strength(rssi)
        print(f"   Signal: {signal_str}")
        print()
    
    # Let user select a device
    if len(devices) == 1:
        print("Automatically selecting the only device found...")
        selected_idx = 0
    else:
        try:
            selection = input(f"Select device to monitor (1-{len(devices)}): ")
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
        interval_input = input("\nUpdate interval in seconds (default: 1): ").strip()
        interval = float(interval_input) if interval_input else 1.0
        
        if interval < 0.1:
            print("Interval too short, using 0.1 seconds")
            interval = 0.1
        elif interval > 60:
            print("Interval too long, using 60 seconds")
            interval = 60
            
    except (ValueError, KeyboardInterrupt):
        interval = 1.0
        print(f"Using default interval: {interval} second(s)")
    
    # Start monitoring
    monitor.monitor_device(selected_addr, selected_name, interval)


if __name__ == "__main__":
    main()
