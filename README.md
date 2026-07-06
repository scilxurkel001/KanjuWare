# KanjuWare - Kanju Pure Mutation Simulator

An entertainment project developed based on Python + Pymem + Tkinter, paying tribute to the 2017 classic fan trope **Rensenware**.

> **Disclaimer:** This program is intended solely for technical exchange, virtual machine experimentation, and group member entertainment. It **will NOT** actually encrypt any files, NOR will it upload any data; it is essentially a fully automated, harmless file-renaming repeater.

---

## Features

1. **Pure Disguise**: Upon activation, it will automatically request administrator privileges (UAC), then traverse the entire disk in the background at extremely high speeds, appending `.LoLK` (Legacy of Lunatic Kingdom) to the end of filenames with specified extensions.
2. **Madness Danmaku Decryption**: The interface is locked and displays a "High-Pressure Ransom Note." The only legitimate way to decrypt it is to launch the trial or full version of *Touhou 15: Legacy of Lunatic Kingdom* (th15.exe) and score a full **50,000,000 (50 million)** points on any difficulty level.
3. **Spiritual Synchronization**: The background thread employs a lock-free design, performing real-time reads of ZUN's sacred memory base address `0x004E40BC` and `004E740C` every 200ms. Every time you score a point in the game, the score on the interface will simultaneously soar.
4. **Developer's Mercy**: An invisible pixel is hidden in the bottom-right corner of the interface; double-clicking it will trigger a hidden backdoor to complete the level directly (self-rescue channel).

# Compare to Rensenware

1. Rensenware uses true encryption, whereas KanjuWare only changes file names. This means that once something goes wrong with Rensenware, files will be unrecoverable; however, with KanjuWare, even if the process is accidentally killed or the software unexpectedly crashes, you can still recover files using bulk renaming tools.
2. Rensenware often crashes when reading read-only files, but KanjuWare has a perfect file accessibility detection mechanism, which means you don't need to remove your disc drive anymore.
3. Rensenware requires scoring 200 million points on Lunatic difficulty in the official version of "Touhou Seiranbu"; therefore, first, you must have the official version of "Touhou Seiranbu" (as it does not support the Trial version); otherwise, you can only download a pirated copy or purchase it on Steam. Secondly, Rensenware's requirement to score 200 million points on Lunatic difficulty is almost impossible to achieve—keep in mind that there are fewer than 1,000 people in the entire world who have cleared "Touhou Seiranbu" on Lunatic difficulty, let alone scored such high points. In comparison, KanjuWare supports a free Trial version and sets a requirement of scoring 50 million points on any difficulty; according to testing by the author himself, this only requires reaching stage three mid-boss on EASY difficulty, which takes about an hour for many people, not to mention the backdoor available to directly restore files.
4. The author of Rensenware only provided a game-dependent unlocking tool after the fact, whereas the author of KanjuWare natively provided backdoors and RPY files for unlocking.


---

## 🛠️ Building and Installation

You need:
- Python 3.8 (This is for compatibility with Windows 7)
- Windows 7/10/11 (Windows 10 or 11 is recommended)

**It is highly recommended to use [uv](https://github.com/astral-sh/uv) for efficient dependency management.**

### Compilation Method 1 (Highly Recommended)

If you have `uv`, please execute the `uv sync` command directly and proceed to the next step once the installation is complete.

### Compilation Method 2 (Traditional)

If you do not have `uv`, please ensure your Python version is 3.8 or higher, and then... 
First, execute the command `python -m venv .venv` to create a virtual environment. 
Then, execute the command `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS / Linux) to activate the environment. 
Finally, execute the command `pip install -r requirements.txt` to install the dependencies. 
If the installation is completed successfully, you can proceed to the next step. If an error occurs during the installation process, please delete the virtual environment and try again, or use `uv` to complete a smooth installation process. 

## Debug and Run

Execute `uv run main.py` in the file root directory. 
Or execute the command `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS / Linux) to activate the environment, and execute `python main.py`. 
Note, it is **NOT recommended** to do this, as it will cause the host files to be renamed. 

## Production Packaging

Execute `uv run pyinstaller -F --noconsole --icon="kanju.ico" --name "KanjuWare" main.py`. 
Or execute the command `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS / Linux) to activate the environment, and execute `pyinstaller -F --noconsole --icon="kanju.ico" --name "KanjuWare" main.py`.

---

## Note

- The "highest tribute" to antivirus software: Due to the involvement of full-disk traversal and file extension modification, the EXE files generated by this program may be immediately detected and quarantined by various antivirus software. Please be sure to disable antivirus software (such as Windows Defender) when testing in a virtual machine. 
- Please use in a virtual machine: Although this program has core path filtering (Windows, Program Files, and other system directories have been skipped), it is strongly recommended to run tests only in an isolated virtual machine environment to avoid affecting the normal configuration of your daily software!

## License
MIT License - Feel free to fork and mess around, but please do not use it for any truly malicious purposes. The author bears no responsibility for any accidents caused by the use of this project (such as victims smashing keyboards, computers, or engaging in real-life fighting because they cannot beat "Touhou Legacy of Lunatic Kingdom").

## Inspired by
[RensenWare](https://github.com/0x00000FF/rensenware-cut) - by [@0x00000FF](https://github.com/0x00000FF)
