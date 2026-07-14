import sys
import subprocess
import os
import shutil
from PyQt6.QtWidgets import (QApplication, QSystemTrayIcon, QMenu, 
                             QWidget, QStyle)
from PyQt6.QtGui import QIcon, QAction
from PyQt6.QtCore import QCoreApplication

class PlambabriconTray(QWidget):
    def __init__(self):
        super().__init__()
        
        # Look for system-wide executable first, fallback to local file
        self.gui_bin = shutil.which("plambabricongui")
        if not self.gui_bin:
            self.gui_bin = os.path.join(os.path.dirname(os.path.abspath(__file__)), "plambabricongui.py")
            
        self.gui_process = None
        self.init_systray()

    def init_systray(self):
        self.tray_icon = QSystemTrayIcon(self)
        
        # Load theme icon, fallback to a standard Qt icon
        icon = QIcon.fromTheme("display-brightness")
        if icon.isNull():
            icon = self.style().standardIcon(QStyle.StandardPixmap.SP_FileDialogListView)
        
        self.tray_icon.setIcon(icon) 
        
        # 1. Create context menu
        self.tray_menu = QMenu()
        
        # 2. Inhibit action
        self.inhibit_action = QAction("Inhibit Regulation", self)
        self.inhibit_action.setCheckable(True)
        self.inhibit_action.setChecked(False)
        self.inhibit_action.triggered.connect(self.toggle_inhibit)
        self.tray_menu.addAction(self.inhibit_action)
        
        self.tray_menu.addSeparator()
        
        # 3. Settings action (launches the GUI)
        settings_action = QAction("Settings...", self)
        settings_action.triggered.connect(self.open_existing_gui)
        self.tray_menu.addAction(settings_action)
        
        self.tray_menu.addSeparator()
        
        # 4. Exit action
        quit_action = QAction("Exit", self)
        quit_action.triggered.connect(self.clean_quit) 
        self.tray_menu.addAction(quit_action)
        
        self.tray_icon.setContextMenu(self.tray_menu)
        
        # Left click triggers settings action
        self.tray_icon.activated.connect(self.on_tray_icon_activated)
        self.tray_icon.show()

    def toggle_inhibit(self, checked):
        """Sends inhibit/uninhibit DBus signals to the daemon."""
        if checked:
            print("Auto-regulation: INHIBITED (Paused)")
            # DBus call placeholders for daemon inhibition
        else:
            print("Auto-regulation: ACTIVE (Resumed)")
            # DBus call placeholders for daemon activation

    def open_existing_gui(self):
        """Launches the settings GUI as a separate process safely."""
        if self.gui_process and self.gui_process.poll() is None:
            print("Settings GUI is already running.")
            return

        print(f"Launching GUI: {self.gui_bin}")
        try:
            if self.gui_bin.endswith(".py"):
                self.gui_process = subprocess.Popen([sys.executable, self.gui_bin])
            else:
                self.gui_process = subprocess.Popen([self.gui_bin])
        except Exception as e:
            print(f"Failed to launch GUI: {e}")

    def on_tray_icon_activated(self, reason):
        if reason == QSystemTrayIcon.ActivationReason.Trigger:
            self.open_existing_gui()

    def clean_quit(self):
        # Terminate GUI if it's still running when exiting tray
        if self.gui_process and self.gui_process.poll() is None:
            self.gui_process.terminate()
        QCoreApplication.quit()

def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)
    tray = PlambabriconTray()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()