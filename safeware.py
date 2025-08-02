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
    QLabel, QPushButton, QTabWidget
)

class SafeWareWindow(QWidget):
    def __init__(self):
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

        self.button = QPushButton("Scan to check system information")
        self.button.setFixedHeight(40)
        self.button.setFixedWidth(200)

        tab1_layout.addWidget(self.label)
        tab1_layout.addWidget(self.button)
        tab1_layout.addStretch() 

        tab1.setLayout(tab1_layout)
        tabs.addTab(tab1, "Port Scanner")

        tab2 = QWidget()
        tab2_layout = QVBoxLayout()
        tab2_layout.addWidget(QLabel("This is tab 2 content"))
        tab2.setLayout(tab2_layout)
        tabs.addTab(tab2, "Other Tab")

        self.button.clicked.connect(self.run_scan_threaded)

    def run_scan(self, start=1, end=100):
        ports = []
        self.label.setText("Scanning for open ports...")
        for port in range(start, end + 1):
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(0.5)
            result = sock.connect_ex(("INSERT IP ADDRESS", port))
            sock.close()
            if result == 0:
                ports.append(port)
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
