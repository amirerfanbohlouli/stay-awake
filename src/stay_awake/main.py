import atexit
import os
import sys
import tkinter as tk
import customtkinter as ctk

# ایمپورت مطلق (Absolute) برای جلوگیری از خطای PyInstaller
from stay_awake.inhibitor import Inhibitor

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

BG_ACTIVE = "#b33a3a"
BG_IDLE = "#1f6aa5"

class StayAwakeApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Stay Awake")
        self.geometry("340x230")
        self.resizable(False, False)
        self._set_icon()

        self.inhibitor = Inhibitor()
        atexit.register(self._safe_stop)

        self.status_label = ctk.CTkLabel(
            self, text="\u26aa  غیرفعال",
            font=ctk.CTkFont(size=16, weight="bold"),
        )
        self.status_label.pack(pady=(34, 12))

        self.toggle_btn = ctk.CTkButton(
            self, text="فعال‌سازی",
            width=220, height=46, corner_radius=12,
            font=ctk.CTkFont(size=15, weight="bold"),
            fg_color=BG_IDLE, command=self.toggle,
        )
        self.toggle_btn.pack(pady=10)

        self.hint_label = ctk.CTkLabel(
            self,
            text="از خواب رفتن سیستم و خاموشی نمایشگر جلوگیری می‌کند",
            font=ctk.CTkFont(size=11), text_color="gray",
        )
        self.hint_label.pack(side="bottom", pady=16)

    def _resource(self, name: str) -> str:
        base = getattr(sys, "_MEIPASS", os.path.dirname(__file__))
        return os.path.join(base, "assets", name)

    def _set_icon(self) -> None:
        try:
            self.iconbitmap(self._resource("icon.ico"))
        except Exception:
            pass
        try:
            png = self._resource("icon.png")
            if os.path.exists(png):
                img = tk.PhotoImage(file=png)
                self.iconphoto(True, img)
                self._tk_icon = img
        except Exception:
            pass

    def toggle(self) -> None:
        if not self.inhibitor.active:
            try:
                self.inhibitor.start()
                self.status_label.configure(
                    text="\U0001f7e2  فعال — سیستم بیدار می‌ماند",
                    text_color="white",
                )
                self.toggle_btn.configure(text="غیرفعال‌سازی", fg_color=BG_ACTIVE)
            except Exception as exc:
                self.status_label.configure(text=f"خطا: {exc}", text_color="red")
        else:
            self._safe_stop()
            self.status_label.configure(text="\u26aa  غیرفعال", text_color="white")
            self.toggle_btn.configure(text="فعال‌سازی", fg_color=BG_IDLE)

    def _safe_stop(self) -> None:
        try:
            self.inhibitor.stop()
        except Exception:
            pass


def main() -> None:
    StayAwakeApp().mainloop()