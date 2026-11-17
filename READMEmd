# Python Network Monitoring Dashboard

A web-based network monitoring application built with Python and Flask. This project provides real-time system resource monitoring, network bandwidth tracking, device status monitoring, and historical monitoring reports through an interactive dashboard.

## Features

### 1. Dashboard
- Real-time CPU usage monitoring.
- RAM usage monitoring.
- Disk usage monitoring.
- Network download and upload speed.
- Bandwidth visualization using charts.
- System information overview.

### 2. Device Management
- Add network devices using IP addresses.
- IP address validation.
- Prevent duplicate IP addresses.
- Check device connectivity.
- Display device status and latency.
- Delete registered devices.

### 3. Automatic Device Monitoring
- Automatically checks registered devices every 30 seconds.
- Updates device status and latency.
- Detects device status changes.
- Displays toast notifications when device status changes.

### 4. Monitoring History
- Store device monitoring records in SQLite.
- View historical monitoring data.
- Search devices by name or IP address.
- Filter records by Online or Offline status.
- Export monitoring reports to CSV.

### 5. System Monitoring
- CPU usage.
- Memory usage.
- Disk usage.
- Network bandwidth statistics.
- Operating system information.

## Technologies Used

- Python
- Flask
- SQLite
- HTML5
- CSS3
- JavaScript
- Chart.js
- psutil

## Project Structure

```text
python-network-monitoring-dashboard/
│
├── app.py
├── config.py
├── database.py
├── requirements.txt
├── README.md
├── .gitignore
│
├── monitoring/
│   ├── __init__.py
│   ├── device_monitor.py
│   ├── bandwidth_monitor.py
│   └── system_monitor.py
│
├── templates/
│   ├── index.html
│   ├── devices.html
│   └── history.html
│
├── static/
│   ├── css/
│   │   └── style.css
│   └── js/
│       └── dashboard.js
│
├── database/
│   └── .gitkeep
│
└── reports/
    └── .gitkeep
```

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/yourusername/python-network-monitoring-dashboard.git
```

### 2. Navigate to the Project Directory

```bash
cd python-network-monitoring-dashboard
```

### 3. Create a Virtual Environment

```bash
python -m venv venv
```

### 4. Activate the Virtual Environment

Windows:

```powershell
.\venv\Scripts\Activate.ps1
```

### 5. Install Dependencies

```bash
pip install -r requirements.txt
```

### 6. Run the Application

```bash
python app.py
```

### 7. Open in Browser

```text
http://127.0.0.1:5000
```

## Usage

1. Open the dashboard in your browser.
2. View system resource and network bandwidth information.
3. Navigate to the Devices page.
4. Add devices using their IP addresses.
5. Check device connectivity and latency.
6. Monitor device status automatically.
7. View monitoring records in the History page.
8. Export monitoring history as a CSV report.

## Database

This project uses SQLite to store:

- Registered network devices.
- Device monitoring history.
- Connectivity status.
- Latency information.
- Packet loss records.

The database is initialized automatically when the application starts.

## Notes

- Automatic device monitoring runs while the Devices page is open.
- Device connectivity checks use the system ping command.
- Network monitoring results depend on the local network environment.
- Monitor only devices that you own or are authorized to monitor.

## Future Improvements

- Configurable monitoring intervals.
- Background monitoring service.
- Advanced network analytics.
- Monitoring alerts.
- Improved reporting and visualization.

## Author

**Kinervaaa**

GitHub: https://github.com/pradipta-web

---

If you find this project useful, feel free to explore the repository.