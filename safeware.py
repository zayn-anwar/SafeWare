# PLEASE INSERT YOUR IP ADDRESS
# WHEREVER NEEDED AS THE APP MIGHT
# NOT FUNCTION AS INTENDED WITHOUT
# DOING SO
# Created by Zayn Coding Incorporated

import sys
import socket
import threading

from PySide6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout,
    QLabel, QPushButton, QTabWidget, QSpinBox, QHBoxLayout, QTableWidget, QTableWidgetItem, QCheckBox
)

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

        super().__init__()

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
        tab2_layout.addWidget(QLabel("This is tab 2 content"))
        tab2.setLayout(tab2_layout)
        tabs.addTab(tab2, "Other Tab")

        self.button.clicked.connect(self.run_scan_threaded)

    def run_scan(self, start=None, end=None):
        self.portTable.setRowCount(0)
        if start is None and end is None:
            start = self.start_port.value()
            end = self.end_port.value()
        ports = []
        self.label.setText("Scanning for open ports...")
        for port in range(start, end + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(("192.168.1.11", port))
            sock.close()
            if result == 0:
                ports.append(port)
                row = self.portTable.rowCount()
                self.portTable.insertRow(row)
                self.portTable.setItem(row, 0, QTableWidgetItem(str(port)))
                self.portTable.setItem(row, 1, QTableWidgetItem("Open ✅"))
                if port in self.common_ports:
                    self.portTable.setItem(row, 2, QTableWidgetItem(str(self.common_ports[port])))
            else:
                if self.show_closed_checkbox.isChecked():
                    row= self.portTable.rowCount()
                    self.portTable.insertRow(row)
                    self.portTable.setItem(row, 0, QTableWidgetItem(str(port)))
                    self.portTable.setItem(row, 1, QTableWidgetItem("Closed"))
                    if port in self.common_ports:
                        self.portTable.setItem(row, 2, QTableWidgetItem(str(self.common_ports[port])))

        if ports:
            self.label.setText(f"Open port: {ports[0]}")
        else:
            self.label.setText("No open ports found")

    def run_scan_threaded(self):
        thread = threading.Thread(target=self.run_scan)
        thread.start()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = SafeWareWindow()
    window.show()
    sys.exit(app.exec())
