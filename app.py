import csv
import io

from flask import send_file
from flask import Flask, jsonify, request
from flask import render_template
from monitoring.system_monitor import get_system_stats
from monitoring.bandwidth_monitor import get_bandwidth_stats
from config import SECRET_KEY
from database import (
    initialize_database,
    get_connection,
    get_monitoring_history
)
from monitoring.device_monitor import check_device

import ipaddress
import sqlite3

app = Flask(__name__)

app.config["SECRET_KEY"] = SECRET_KEY

initialize_database()


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/api/status")
def api_status():
    return jsonify({
        "application": "Python Network Monitoring Dashboard",
        "status": "running"
    })


# Get all registered devices
@app.route("/api/devices", methods=["GET"])
def get_devices():
    connection = get_connection()

    devices = connection.execute(
        "SELECT * FROM devices ORDER BY id DESC"
    ).fetchall()

    connection.close()

    return jsonify([dict(device) for device in devices])


# Add a new device
@app.route("/api/devices", methods=["POST"])
def add_device():
    data = request.get_json(silent=True) or {}

    name = data.get("name", "").strip()
    ip_address = data.get("ip_address", "").strip()
    description = data.get("description", "").strip()

    if not name or not ip_address:
        return jsonify({
            "error": "Name and IP address are required"
        }), 400

    try:
        ipaddress.ip_address(ip_address)
    except ValueError:
        return jsonify({
            "error": "Invalid IP address"
        }), 400

    connection = get_connection()

    try:
        connection.execute(
            """
            INSERT INTO devices (name, ip_address, description)
            VALUES (?, ?, ?)
            """,
            (name, ip_address, description)
        )

        connection.commit()

        return jsonify({
            "message": "Device added successfully"
        }), 201

    except sqlite3.IntegrityError:
        return jsonify({
            "error": "IP address already exists"
        }), 409

    finally:
        connection.close()


# Delete a device
@app.route("/api/devices/<int:device_id>", methods=["DELETE"])
def delete_device(device_id):
    connection = get_connection()

    cursor = connection.execute(
        "DELETE FROM devices WHERE id = ?",
        (device_id,)
    )

    connection.commit()
    connection.close()

    if cursor.rowcount == 0:
        return jsonify({
            "error": "Device not found"
        }), 404

    return jsonify({
        "message": "Device deleted successfully"
    })


# Check device connectivity
@app.route("/api/devices/<int:device_id>/check", methods=["GET"])
def monitor_device(device_id):
    connection = get_connection()

    device = connection.execute(
        "SELECT * FROM devices WHERE id = ?",
        (device_id,)
    ).fetchone()

    if device is None:
        connection.close()
        return jsonify({
            "error": "Device not found"
        }), 404

    previous = connection.execute("""
    SELECT status
    FROM monitoring_history
    WHERE device_id = ?
    ORDER BY id DESC
    LIMIT 1
 """, (device_id,)).fetchone()

    result = check_device(device["ip_address"])

    previous_status = previous["status"] if previous else None

    status_changed = (
    previous_status is not None
    and previous_status != result["status"]
    )

    connection.execute(
        """
        INSERT INTO monitoring_history
        (device_id, status, latency, packet_loss)
        VALUES (?, ?, ?, ?)
        """,
        (
            device_id,
            result["status"],
            result["latency"],
            0 if result["status"] == "Online" else 100
        )
    )

    connection.commit()
    connection.close()

    return jsonify ({
        "device": device["name"],
        "ip_address": device["ip_address"],
        "status": result["status"],
        "latency": result["latency"],
        "status_changed": status_changed,
        "previous_status": previous_status,
        })

@app.route("/api/bandwidth", methods=["GET"])
def bandwidth():
    stats = get_bandwidth_stats()

    return jsonify({
        "download_speed": stats["download_speed"],
        "upload_speed": stats["upload_speed"],
        "total_downloaded": stats["total_downloaded"],
        "total_uploaded": stats["total_uploaded"],
        "unit": "Mbps"
    })

@app.route("/api/system", methods=["GET"])
def system():
    stats = get_system_stats()

    return jsonify(stats)

@app.route("/devices")
def devices_page():
    return render_template("devices.html")

@app.route("/history")
def history_page():
    return render_template("history.html")


@app.route("/api/history", methods=["GET"])
def api_history():
    history = get_monitoring_history()

    return jsonify(history)

@app.route("/api/history/export", methods=["GET"])
def export_history():
    history = get_monitoring_history()

    output = io.StringIO()

    writer = csv.writer(output)

    writer.writerow([
        "ID",
        "Device Name",
        "IP Address",
        "Status",
        "Latency (ms)",
        "Packet Loss (%)",
        "Checked At"
    ])

    for item in history:
        writer.writerow([
            item["id"],
            item["name"],
            item["ip_address"],
            item["status"],
            item["latency"],
            item["packet_loss"],
            item["checked_at"]
        ])

    output.seek(0)

    csv_file = io.BytesIO(
        output.getvalue().encode("utf-8-sig")
    )

    return send_file(
        csv_file,
        mimetype="text/csv",
        as_attachment=True,
        download_name="network_monitoring_report.csv"
    )

if __name__ == "__main__":
    app.run(debug=True)