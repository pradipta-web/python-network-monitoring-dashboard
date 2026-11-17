const bandwidthLabels = [];
const downloadData = [];
const uploadData = [];

const chartContext = document
    .getElementById("bandwidthChart")
    .getContext("2d");

const bandwidthChart = new Chart(chartContext, {
    type: "line",

    data: {
        labels: bandwidthLabels,

        datasets: [
            {
                label: "Download (Mbps)",
                data: downloadData,
                borderColor: "#38bdf8",
                backgroundColor: "rgba(56, 189, 248, 0.1)",
                fill: true,
                tension: 0.4
            },
            {
                label: "Upload (Mbps)",
                data: uploadData,
                borderColor: "#34d399",
                backgroundColor: "rgba(52, 211, 153, 0.1)",
                fill: true,
                tension: 0.4
            }
        ]
    },

    options: {
        responsive: true,
        maintainAspectRatio: false,

        plugins: {
            legend: {
                labels: {
                    color: "#e2e8f0"
                }
            }
        },

        scales: {
            x: {
                ticks: {
                    color: "#94a3b8"
                },
                grid: {
                    color: "#334155"
                }
            },

            y: {
                beginAtZero: true,
                ticks: {
                    color: "#94a3b8"
                },
                grid: {
                    color: "#334155"
                }
            }
        }
    }
});


async function updateSystem() {
    try {
        const response = await fetch("/api/system");

        if (!response.ok) {
            throw new Error("System API request failed");
        }

        const data = await response.json();

        document.getElementById("cpuUsage").textContent =
            data.cpu_usage + "%";

        document.getElementById("ramUsage").textContent =
            data.ram_usage + "%";

        document.getElementById("diskUsage").textContent =
            data.disk_usage + "%";

        document.getElementById("hostname").textContent =
            data.hostname;

        document.getElementById("operatingSystem").textContent =
            data.operating_system;

        document.getElementById("processor").textContent =
            data.processor || "Unknown";

        document.getElementById("totalRam").textContent =
            data.ram_total + " GB";

        document.getElementById("totalDisk").textContent =
            data.disk_total + " GB";

    } catch (error) {
        console.error("System monitoring error:", error);
    }
}


async function updateBandwidth() {
    try {
        const response = await fetch("/api/bandwidth");

        if (!response.ok) {
            throw new Error("Bandwidth API request failed");
        }

        const data = await response.json();

        document.getElementById("downloadSpeed").textContent =
            data.download_speed + " Mbps";

        document.getElementById("uploadSpeed").textContent =
            data.upload_speed + " Mbps";

        document.getElementById("totalDownloaded").textContent =
            formatBytes(data.total_downloaded);

        document.getElementById("totalUploaded").textContent =
            formatBytes(data.total_uploaded);

        document.getElementById("networkStatus").textContent =
            "Monitoring";

        const currentTime = new Date().toLocaleTimeString();

        document.getElementById("lastUpdated").textContent =
            currentTime;

        bandwidthLabels.push(currentTime);
        downloadData.push(data.download_speed);
        uploadData.push(data.upload_speed);

        if (bandwidthLabels.length > 20) {
            bandwidthLabels.shift();
            downloadData.shift();
            uploadData.shift();
        }

        bandwidthChart.update();

    } catch (error) {
        document.getElementById("networkStatus").textContent =
            "Unavailable";

        console.error("Bandwidth monitoring error:", error);
    }
}


function formatBytes(bytes) {
    const units = ["B", "KB", "MB", "GB", "TB"];

    if (bytes === 0) {
        return "0 B";
    }

    const index = Math.min(
        Math.floor(Math.log(bytes) / Math.log(1024)),
        units.length - 1
    );

    return (
        (bytes / Math.pow(1024, index)).toFixed(2)
        + " "
        + units[index]
    );
}


function updateDashboard() {
    updateSystem();
    updateBandwidth();
}


updateDashboard();

setInterval(updateDashboard, 2000);