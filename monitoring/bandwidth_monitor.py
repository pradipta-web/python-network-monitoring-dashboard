import psutil
import time


previous_stats = None
previous_time = None


def get_bandwidth_stats():
    global previous_stats, previous_time

    current_stats = psutil.net_io_counters()
    current_time = time.time()

    if previous_stats is None:
        previous_stats = current_stats
        previous_time = current_time

        return {
            "download_speed": 0,
            "upload_speed": 0,
            "total_downloaded": current_stats.bytes_recv,
            "total_uploaded": current_stats.bytes_sent
        }

    elapsed = current_time - previous_time

    if elapsed <= 0:
        elapsed = 1

    download_speed = (
        current_stats.bytes_recv - previous_stats.bytes_recv
    ) / elapsed

    upload_speed = (
        current_stats.bytes_sent - previous_stats.bytes_sent
    ) / elapsed

    previous_stats = current_stats
    previous_time = current_time

    return {
        "download_speed": round(download_speed * 8 / 1_000_000, 2),
        "upload_speed": round(upload_speed * 8 / 1_000_000, 2),
        "total_downloaded": current_stats.bytes_recv,
        "total_uploaded": current_stats.bytes_sent
    }