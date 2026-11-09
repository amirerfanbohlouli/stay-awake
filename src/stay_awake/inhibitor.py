import ctypes, platform, shutil, subprocess
SYSTEM = platform.system()
class Inhibitor:
    def __init__(self) -> None:
        self._active = False
        self._process = None
    @property
    def active(self) -> bool: return self._active
    def start(self) -> None:
        if self._active: return
        if SYSTEM == "Windows": self._start_windows()
        elif SYSTEM == "Darwin": self._start_macos()
        elif SYSTEM == "Linux": self._start_linux()
        self._active = True
    def stop(self) -> None:
        if not self._active: return
        if SYSTEM == "Windows": ctypes.windll.kernel32.SetThreadExecutionState(0x80000000)
        elif self._process is not None:
            self._process.terminate(); self._process = None
        self._active = False
    def _start_windows(self) -> None:
        ctypes.windll.kernel32.SetThreadExecutionState(0x80000000 | 0x00000001 | 0x00000002)
    def _start_macos(self) -> None:
        self._process = subprocess.Popen(["caffeinate", "-i", "-d", "-m"], stdout=subprocess.DEVNULL)
    def _start_linux(self) -> None:
        if shutil.which("systemd-inhibit"):
            self._process = subprocess.Popen(["systemd-inhibit", "--what=sleep:idle", "--why=StayAwake", "--mode=block", "sleep", "infinity"], stdout=subprocess.DEVNULL)