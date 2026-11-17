import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

DATABASE_DIR = os.path.join(BASE_DIR, "database")
REPORT_DIR = os.path.join(BASE_DIR, "reports")

DATABASE_PATH = os.path.join(DATABASE_DIR, "network_monitor.db")

os.makedirs(DATABASE_DIR, exist_ok=True)
os.makedirs(REPORT_DIR, exist_ok=True)

SECRET_KEY = "network-monitoring-secret-key"