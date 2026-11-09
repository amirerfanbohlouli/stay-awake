import atexit, os, sys
import customtkinter as ctk
try:
    from .inhibitor import Inhibitor
except ImportError:
    from inhibitor import Inhibitor
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
BG_ACTIVE = "#b33a3a"; BG_IDLE = "#1f6aa5"

class StayAwakeApp(ctk.CTk):
    def __init__(self) -> None:
        super().__init__()
        self.title("Stay Awake"); self.geometry("340x230"); self.resizable(False, False)
        self.inhibitor = Inhibitor(); atexit.register(self._safe_stop)
        self.status_label = ctk.CTkLabel(self, text="\u26aa  ØºÛŒØ±ÙØ¹Ø§Ù„", font=ctk.CTkFont(size=16, weight="bold"))
        self.status_label.pack(pady=(34, 12))
        self.toggle_btn = ctk.CTkButton(self, text="ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ", width=220, height=46, corner_radius=12, font=ctk.CTkFont(size=15, weight="bold"), fg_color=BG_IDLE, command=self.toggle)
        self.toggle_btn.pack(pady=10)
        self.hint_label = ctk.CTkLabel(self, text="Ø§Ø² Ø®ÙˆØ§Ø¨ Ø±ÙØªÙ† Ø³ÛŒØ³ØªÙ… Ùˆ Ø®Ø§Ù…ÙˆØ´ÛŒ Ù†Ù…Ø§ÛŒØ´Ú¯Ø± Ø¬Ù„ÙˆÚ¯ÛŒØ±ÛŒ Ù…ÛŒâ€ŒÚ©Ù†Ø¯", font=ctk.CTkFont(size=11), text_color="gray")
        self.hint_label.pack(side="bottom", pady=16)
    def toggle(self) -> None:
        if not self.inhibitor.active:
            self.inhibitor.start()
            self.status_label.configure(text="\U0001f7e2  ÙØ¹Ø§Ù„ â€” Ø³ÛŒØ³ØªÙ… Ø¨ÛŒØ¯Ø§Ø± Ù…ÛŒâ€ŒÙ…Ø§Ù†Ø¯", text_color="white")
            self.toggle_btn.configure(text="ØºÛŒØ±ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ", fg_color=BG_ACTIVE)
        else:
            self._safe_stop()
            self.status_label.configure(text="\u26aa  ØºÛŒØ±ÙØ¹Ø§Ù„", text_color="white")
            self.toggle_btn.configure(text="ÙØ¹Ø§Ù„â€ŒØ³Ø§Ø²ÛŒ", fg_color=BG_IDLE)
    def _safe_stop(self) -> None:
        try: self.inhibitor.stop()
        except: pass
def main() -> None: StayAwakeApp().mainloop()
if __name__ == "__main__": main()