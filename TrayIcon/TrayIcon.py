from OperaPowerRelay import opr
import pystray
import threading
import time
from typing import Callable
from PIL import Image

class tray_icon():
    def __init__(self, name: str, icon: Image.Image, closing_callback: Callable):
        self.meta = {
            "name": name, 
            "icon": icon
            }
        
        
        self.closing_callback: Callable = closing_callback
        self.menu_callback: Callable = None # Function that returns title and menu
        self._icon_thread: threading.Thread = None
        self._stop_signal: threading.Event = threading.Event()

    def icon_thread(self) -> None:

        title, menu = self.menu_callback()
        i = pystray.Icon(self.meta["name"], self.meta["icon"], self.meta["name"], menu=menu)
        i.run_detached()

        while not self._stop_signal.is_set():
            try:
                title, menu = self.menu_callback()
                i.menu = menu
                i.title = f"{title}" or f"{self.meta['name']}"
                time.sleep(1)
            except Exception as e:
                self.error_handler(e)

        i.stop()

    def start_icon(self):
        if self._icon_thread.is_alive() or not self._stop_signal.is_set():
            return
        self._icon_thread = threading.Thread(target=self.icon_thread, daemon=True)
        self._icon_thread.start()
        self._stop_signal.clear()

    def stop_icon(self):
        if not self._icon_thread.is_alive() or self._stop_signal.is_set():
            return
        self._stop_signal.set()
        self._icon_thread.join()
        self.closing_callback()

    def error_handler(self, error):
        opr.error_pretty(exc=error, name="TrayIcon", message=f"Error in TrayIcon - {error}")

    def set_menu_callback(self, menu_callback):
        self.menu_callback = menu_callback

def get_tray_icon(name: str, icon: Image.Image, closing_callback: Callable) -> tray_icon:
    return tray_icon(name=name, icon=icon, closing_callback=closing_callback)