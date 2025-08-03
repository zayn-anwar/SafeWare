# PLEASE INSERT YOUR IP ADDRESS
# WHEREVER NEEDED AS THE APP MIGHT
# NOT FUNCTION AS INTENDED WITHOUT
# DOING SO
# Created by Zayn Coding Incorporated

import sys
import socket
import threading
import subprocess
import platform
import ipaddress
import time
from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTabWidget, QSpinBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox, QLineEdit
)
from PySide6.QtGui import QIcon

class SafeWareWindow(QWidget):
    def __init__(self):

        self.common_ports = {
            20: "FTP Data",
            21: "FTP Control",
            22: "SSH",
            23: "Telnet",
            25: "SMTP",
            53: "DNS",
            67: "DHCP (Server)",
            68: "DHCP (Client)",
            69: "TFTP",
            80: "HTTP",
            110: "POP3",
            111: "RPCbind / portmapper",
            119: "NNTP",
            123: "NTP",
            135: "Microsoft RPC",
            137: "NetBIOS Name Service",
            138: "NetBIOS Datagram Service",
            139: "NetBIOS Session Service",
            143: "IMAP",
            161: "SNMP",
            162: "SNMP Trap",
            179: "BGP",
            194: "IRC",
            389: "LDAP",
            443: "HTTPS",
            445: "Microsoft-DS (SMB over IP)",
            465: "SMTPS",
            514: "Syslog",
            515: "LPD (Line Printer Daemon)",
            520: "RIP",
            587: "SMTP (submission)",
            631: "IPP (Internet Printing Protocol)",
            993: "IMAPS",
            995: "POP3S",
            1023: "Reserved",
            1024: "Reserved",
        }

        self.port_monitoring = {}

        super().__init__()

        self.setWindowIcon(QIcon("shieldico.ico"))

        self.setWindowTitle("SafeWare by ZCI")
        self.resize(400, 300)

        main_layout = QVBoxLayout(self)

        tabs = QTabWidget()
        main_layout.addWidget(tabs)

        tab1 = QWidget()
        tab1_layout = QVBoxLayout()
        tab1_layout.setSpacing(5)
        tab1_layout.setContentsMargins(10, 10, 10, 10)

        self.label = QLabel("Click to Start Scan")
        self.label.setFixedHeight(30)

        port_layout = QHBoxLayout()
        tab1_layout.addLayout(port_layout)

        self.start_port = QSpinBox()
        self.start_port.setRange(1, 65535)
        self.start_port.setValue(1)
        self.start_port.setPrefix("Start Port: ")

        self.end_port = QSpinBox()
        self.end_port.setRange(1, 65535)
        self.end_port.setValue(100)
        self.end_port.setPrefix("End Port: ")

        port_layout.addWidget(self.start_port)
        port_layout.addWidget(self.end_port)

        self.button = QPushButton("Scan to check system information")
        self.button.setFixedHeight(40)
        self.button.setFixedWidth(200)

        self.show_closed_checkbox = QCheckBox("Show closed ports")
        tab1_layout.addWidget(self.show_closed_checkbox)

        tab1_layout.addWidget(self.label)
        tab1_layout.addWidget(self.button)
        tab1_layout.addStretch()

        self.portTable = QTableWidget()
        self.portTable.setColumnCount(3)
        self.portTable.setHorizontalHeaderLabels(["Port", "Status", "Service"])

        tab1_layout.addWidget(self.portTable)

        tab1.setLayout(tab1_layout)
        tabs.addTab(tab1, "Port Scanner")

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()

        self.subnet_label = QLabel("Enter a subnet to scan")
        tab2_layout.addWidget(self.subnet_label)

        self.subnet_input = QLineEdit()
        self.subnet_input.setPlaceholderText("Enter Subnet (eg 192.168.1.0/24)")
        tab2_layout.addWidget(self.subnet_input)

        self.show_down_checkbox = QCheckBox("Show down hosts")
        tab2_layout.addWidget(self.show_down_checkbox)

        self.subnet_submit = QPushButton("Submit")
        self.subnet_submit.clicked.connect(self.discovery_request_threaded)
        tab2_layout.addWidget(self.subnet_submit)

        self.discovery_result = QTableWidget()
        self.discovery_result.setColumnCount(2)
        self.discovery_result.setHorizontalHeaderLabels(["IP Address", "Status"])
        tab2_layout.addWidget(self.discovery_result)

        tab2.setLayout(tab2_layout)
        tabs.addTab(tab2, "Find Alive Hosts")

        tab3 = QWidget()
        tab3_layout = QVBoxLayout()

        self.live_port_monitoring = QLabel("Monitor Port Status Live")
        tab3_layout.addWidget(self.live_port_monitoring)

        monitor_port_layout = QHBoxLayout()
        tab3_layout.addLayout(monitor_port_layout)

        self.start_monitor_port = QSpinBox()
        self.start_monitor_port.setRange(1, 65535)
        self.start_monitor_port.setValue(1)
        self.start_monitor_port.setPrefix("Start Port: ")

        self.end_monitor_port = QSpinBox()
        self.end_monitor_port.setRange(1, 65535)
        self.end_monitor_port.setValue(100)
        self.end_monitor_port.setPrefix("End Port: ")

        monitor_port_layout.addWidget(self.start_monitor_port)
        monitor_port_layout.addWidget(self.end_monitor_port)

        monitor_button = QPushButton("Monitor")
        monitor_button.clicked.connect(self.monitor_ports)
        tab3_layout.addWidget(monitor_button)

        self.status_table = QTableWidget()
        self.status_table.setColumnCount(3)
        self.status_table.setHorizontalHeaderLabels(["Port", "Status", "Service"])
        tab3_layout.addWidget(self.status_table)

        tab3.setLayout(tab3_layout)
        tabs.addTab(tab3, "Live Port Monitoring")

        self.button.clicked.connect(self.run_scan_threaded)

    def run_scan(self, start=None, end=None, on_status_check=None):
        self.portTable.setRowCount(0)
        if start is None and end is None:
            start = self.start_port.value()
            end = self.end_port.value()

        self.label.setText("Scanning for open ports...")

        for port in range(start, end + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            raw_result = sock.connect_ex(("INSERT IP ADDRESS HERE", port))
            sock.close()
            if raw_result == 0:
                row = self.portTable.rowCount()
                self.portTable.insertRow(row)
                self.portTable.setItem(row, 0, QTableWidgetItem(str(port)))
                self.portTable.setItem(row, 1, QTableWidgetItem("Open ✅"))

                if port in self.common_ports:
                    self.portTable.setItem(row, 2, QTableWidgetItem(str(self.common_ports[port])))

            else:
                if self.show_closed_checkbox.isChecked():
                    row = self.portTable.rowCount()
                    self.portTable.insertRow(row)
                    self.portTable.setItem(row, 0, QTableWidgetItem(str(port)))
                    self.portTable.setItem(row, 1, QTableWidgetItem("Closed"))
                    if port in self.common_ports:
                        self.portTable.setItem(row, 2, QTableWidgetItem(str(self.common_ports[port])))
        self.label.setText("Click to start scan")

    def run_scan_threaded(self):
        thread = threading.Thread(target=self.run_scan)
        thread.start()

    def ip_scan(self, ip):
        param = "-n" if platform.system().lower() == "windows" else "-c"
        command = ["ping", param, "1", str(ip)]
        try:
            subprocess.check_call(command, stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)
            return True
        except subprocess.CalledProcessError:
            return False
        except FileNotFoundError:
            print("Ping command not found! Is it available on your system?")
            return False

    def discovery_request(self):
        subnet_str = self.subnet_input.text().strip()
        if not subnet_str:
            self.subnet_label.setText("No subnet to scan")
            return

        try:
            subnet = ipaddress.ip_network(subnet_str, strict=False)
        except ValueError:
            self.subnet_label.setText("Invalid subnet format")
            return

        self.subnet_input.setText("Scanning subnet...")
        self.discovery_result.setRowCount(0)

        for ip in subnet.hosts():
            alive = self.ip_scan(ip)
            if alive:
                row = self.discovery_result.rowCount()
                self.discovery_result.insertRow(row)
                self.discovery_result.setItem(row, 0, QTableWidgetItem(str(ip)))
                self.discovery_result.setItem(row, 1, QTableWidgetItem("Alive"))
            else:
                if self.show_down_checkbox.isChecked():
                    row = self.discovery_result.rowCount()
                    self.discovery_result.insertRow(row)
                    self.discovery_result.setItem(row, 0, QTableWidgetItem(str(ip)))
                    self.discovery_result.setItem(row, 1, QTableWidgetItem("Down"))

    def discovery_request_threaded(self):
        thread = threading.Thread(target=self.discovery_request)
        thread.start()

    def monitor_ports(self):
        def monitor_loop():
            start = self.start_monitor_port.value()
            end = self.end_monitor_port.value()
            while True:
                self.status_table.setRowCount(0)
                for port in range(start, end + 1):
                    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    sock.settimeout(0.5)
                    raw_result = sock.connect_ex(("192.168.1.8", port))
                    sock.close()
                    status_text = "Open ✅" if raw_result == 0 else "Closed"
                    row = self.status_table.rowCount()
                    self.status_table.insertRow(row)
                    self.status_table.setItem(row, 0, QTableWidgetItem(str(port)))
                    self.status_table.setItem(row, 1, QTableWidgetItem(status_text))
                    if port in self.common_ports:
                        self.status_table.setItem(row, 2, QTableWidgetItem(str(self.common_ports[port])))
                    else:
                        self.status_table.setItem(row, 2, QTableWidgetItem(""))
                time.sleep(3)
        thread = threading.Thread(target=monitor_loop, daemon=True)
        thread.start()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeWareWindow()
    window.show()
    sys.exit(app.exec())
