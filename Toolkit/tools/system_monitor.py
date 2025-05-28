#!/usr/bin/env python3
"""
System Monitor Tool
Monitor system resources and generate alerts
"""

import json
import sys
import time
import psutil
from datetime import datetime

def monitor_system(inputs):
    """Monitor system resources"""
    check_type = inputs['check_type'].lower()
    threshold = inputs['threshold']
    duration = inputs['duration']
    
    print(f"🖥️  System Monitor Started")
    print(f"📊 Monitoring: {check_type}")
    print(f"⚠️  Alert threshold: {threshold}%")
    print(f"⏱️  Duration: {duration} minutes")
    print("-" * 50)
    
    start_time = time.time()
    end_time = start_time + (duration * 60)  # Convert to seconds
    alert_count = 0
    check_count = 0
    
    try:
        while time.time() < end_time:
            check_count += 1
            timestamp = datetime.now().strftime("%H:%M:%S")
            
            alerts = []
            
            # CPU Check
            if check_type in ['cpu', 'all']:
                cpu_percent = psutil.cpu_percent(interval=1)
                print(f"[{timestamp}] 🔄 CPU Usage: {cpu_percent:.1f}%", end="", flush=True)
                if cpu_percent > threshold:
                    alerts.append(f"CPU: {cpu_percent:.1f}%")
                    print(" ⚠️  HIGH!", flush=True)
                else:
                    print(" ✅", flush=True)
            
            # Memory Check  
            if check_type in ['memory', 'all']:
                memory = psutil.virtual_memory()
                memory_percent = memory.percent
                print(f"[{timestamp}] 🧠 Memory Usage: {memory_percent:.1f}%", end="", flush=True)
                if memory_percent > threshold:
                    alerts.append(f"Memory: {memory_percent:.1f}%")
                    print(" ⚠️  HIGH!", flush=True)
                else:
                    print(" ✅", flush=True)
            
            # Disk Check
            if check_type in ['disk', 'all']:
                disk = psutil.disk_usage('/')
                disk_percent = (disk.used / disk.total) * 100
                print(f"[{timestamp}] 💾 Disk Usage: {disk_percent:.1f}%", end="", flush=True)
                if disk_percent > threshold:
                    alerts.append(f"Disk: {disk_percent:.1f}%")
                    print(" ⚠️  HIGH!", flush=True)
                else:
                    print(" ✅", flush=True)
            
            # Handle alerts
            if alerts:
                alert_count += 1
                print(f"🚨 ALERT #{alert_count}: {', '.join(alerts)}", flush=True)
                
                # You could add email notifications, logging, etc. here
                log_alert(alerts, timestamp)
            
            print(f"   💤 Sleeping for 30 seconds...", flush=True)
            time.sleep(30)  # Check every 30 seconds
            
    except KeyboardInterrupt:
        print(f"\n⏹️  Monitoring stopped by user")
    
    # Summary
    elapsed_minutes = (time.time() - start_time) / 60
    print("-" * 50)
    print(f"📊 Monitoring Summary:")
    print(f"   ⏱️  Total runtime: {elapsed_minutes:.1f} minutes")
    print(f"   🔍 Total checks: {check_count}")
    print(f"   🚨 Total alerts: {alert_count}")
    
    return 0

def log_alert(alerts, timestamp):
    """Log alerts to a file"""
    try:
        with open('system_alerts.log', 'a') as f:
            f.write(f"[{timestamp}] ALERT: {', '.join(alerts)}\n")
        print(f"   📝 Alert logged to system_alerts.log")
    except Exception as e:
        print(f"   ❌ Failed to log alert: {e}")

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("❌ No input provided")
        return 1
    
    try:
        inputs = json.loads(sys.argv[1])
        return monitor_system(inputs)
    except json.JSONDecodeError:
        print("❌ Invalid input format")
        return 1
    except ImportError:
        print("❌ psutil library not installed. Install with: pip install psutil")
        return 1
    except Exception as e:
        print(f"💥 Unexpected error: {str(e)}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
