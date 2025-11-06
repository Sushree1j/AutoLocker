#!/usr/bin/env python3
"""
Unit tests for Bluetooth Signal Strength Monitor
Tests the utility functions without requiring actual Bluetooth hardware
"""

import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_format_signal_strength():
    """Test signal strength formatting function"""
    print("Testing signal strength formatting...")
    
    # Import from bluetooth_monitor_simple
    from bluetooth_monitor_simple import format_signal_strength
    
    # Test excellent signal
    result = format_signal_strength(-45)
    assert "-45" in result and "dBm" in result and "Excellent" in result
    print(f"  ✓ Excellent signal: {result}")
    
    # Test good signal
    result = format_signal_strength(-55)
    assert "-55" in result and "dBm" in result and "Good" in result
    print(f"  ✓ Good signal: {result}")
    
    # Test fair signal
    result = format_signal_strength(-65)
    assert "-65" in result and "dBm" in result and "Fair" in result
    print(f"  ✓ Fair signal: {result}")
    
    # Test poor signal
    result = format_signal_strength(-75)
    assert "-75" in result and "dBm" in result and "Poor" in result
    print(f"  ✓ Poor signal: {result}")
    
    # Test None signal
    result = format_signal_strength(None)
    assert "N/A" in result
    print(f"  ✓ No signal: {result}")
    
    print("✓ All format_signal_strength tests passed!\n")


def test_platform_detection():
    """Test platform detection"""
    print("Testing platform detection...")
    
    import platform
    current_platform = platform.system()
    
    print(f"  Current platform: {current_platform}")
    
    if current_platform in ["Linux", "Windows", "Darwin"]:
        print(f"  ✓ Platform detected: {current_platform}")
    else:
        print(f"  ⚠ Unsupported platform: {current_platform}")
    
    print("✓ Platform detection test passed!\n")


def test_imports():
    """Test that required modules can be imported"""
    print("Testing module imports...")
    
    try:
        import bluetooth_monitor
        print("  ✓ bluetooth_monitor.py imports successfully")
    except (ImportError, SystemExit) as e:
        print(f"  ⚠ bluetooth_monitor.py requires PyBluez (expected in test environment)")
    
    try:
        import bluetooth_monitor_simple
        print("  ✓ bluetooth_monitor_simple.py imports successfully")
    except (ImportError, SystemExit) as e:
        print(f"  ✗ Failed to import bluetooth_monitor_simple: {e}")
        raise
    
    print("✓ Import tests passed!\n")


def test_rssi_parsing():
    """Test RSSI value parsing logic"""
    print("Testing RSSI value categorization...")
    
    from bluetooth_monitor_simple import format_signal_strength
    
    # Test boundary values
    test_cases = [
        (-49, "Excellent"),
        (-50, "Excellent"),
        (-51, "Good"),
        (-59, "Good"),
        (-60, "Good"),
        (-61, "Fair"),
        (-69, "Fair"),
        (-70, "Fair"),
        (-71, "Poor"),
        (-80, "Poor"),
        (-100, "Poor"),
    ]
    
    for rssi, expected_quality in test_cases:
        result = format_signal_strength(rssi)
        assert expected_quality in result, f"Expected {expected_quality} for RSSI {rssi}, got {result}"
        print(f"  ✓ RSSI {rssi:4d} dBm → {expected_quality}")
    
    print("✓ All RSSI categorization tests passed!\n")


def main():
    """Run all tests"""
    print("=" * 70)
    print("Bluetooth Signal Strength Monitor - Unit Tests")
    print("=" * 70)
    print()
    
    try:
        test_imports()
        test_platform_detection()
        test_format_signal_strength()
        test_rssi_parsing()
        
        print("=" * 70)
        print("✓ ALL TESTS PASSED!")
        print("=" * 70)
        return 0
        
    except AssertionError as e:
        print(f"\n✗ TEST FAILED: {e}")
        return 1
    except Exception as e:
        print(f"\n✗ UNEXPECTED ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
