import psutil
import platform
import socket
import os


def get_system_stats():
    cpu_usage = psutil.cpu_percent(interval=0.5)

    memory = psutil.virtual_memory()

    disk = psutil.disk_usage(os.path.abspath(os.sep))

    return {
        "hostname": socket.gethostname(),
        "operating_system": platform.system(),
        "os_version": platform.version(),
        "processor": platform.processor(),
        "cpu_usage": cpu_usage,
        "ram_total": round(memory.total / (1024 ** 3), 2),
        "ram_used": round(memory.used / (1024 ** 3), 2),
        "ram_usage": memory.percent,
        "disk_total": round(disk.total / (1024 ** 3), 2),
        "disk_used": round(disk.used / (1024 ** 3), 2),
        "disk_usage": disk.percent
    }