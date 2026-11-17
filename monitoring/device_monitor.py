import subprocess
import platform
import re


def check_device(ip_address):
    system = platform.system().lower()

    try:
        if system == "windows":
            command = [
                "ping", "-n", "1", "-w", "2000", ip_address
            ]
        else:
            command = [
                "ping", "-c", "1", "-W", "2", ip_address
            ]

        result = subprocess.run(
            command,
            capture_output=True,
            text=True,
            timeout=5
        )

        match = re.search(
            r"time[=<]([\d.]+)\s*ms",
            result.stdout,
            re.IGNORECASE
        )

        if result.returncode == 0 and match:
            return {
                "status": "Online",
                "latency": float(match.group(1))
            }

        return {
            "status": "Offline",
            "latency": None
        }

    except (subprocess.TimeoutExpired, OSError):
        return {
            "status": "Offline",
            "latency": None
        }