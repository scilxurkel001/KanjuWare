# KanjuWare - Kanju Pure Mutation Simulator

An entertainment project developed based on Python + Pymem + Tkinter, paying tribute to the 2017 classic fan trope **Rensenware**.

> **Disclaimer:** This program is intended solely for technical exchange, virtual machine experimentation, and group member entertainment. It **will NOT** actually encrypt any files, NOR will it upload any data; it is essentially a fully automated, harmless file-renaming repeater.

---

## Features

1. **Pure Disguise**: Upon activation, it will automatically request administrator privileges (UAC), then traverse the entire disk in the background at extremely high speeds, appending `.LoLK` (Legacy of Lunatic Kingdom) to the end of filenames with specified extensions.
2. **Madness Danmaku Decryption**: The interface is locked and displays a "High-Pressure Ransom Note." The only legitimate way to decrypt it is to launch the trial or full version of *Touhou 15: Legacy of Lunatic Kingdom* (th15.exe) and score a full **50,000,000 (50 million)** points on any difficulty level.
3. **Spiritual Synchronization**: The background thread employs a lock-free design, performing real-time reads of ZUN's sacred memory base address `0x004E40BC` and `004E740C` every 200ms. Every time you score a point in the game, the score on the interface will simultaneously soar.
4. **Developer's Mercy**: An invisible pixel is hidden in the bottom-right corner of the interface; double-clicking it will trigger a hidden backdoor to complete the level directly (self-rescue channel).

## Compare to Rensenware

1. Rensenware uses true encryption, whereas KanjuWare only changes file names. This means that once something goes wrong with Rensenware, files will be unrecoverable; however, with KanjuWare, even if the process is accidentally killed or the software unexpectedly crashes, you can still recover files using bulk renaming tools.
2. Rensenware requires a .NET Framework 3.5 environment, which is actually a good thing for physical Windows 10/11 users because it gives them at least a chance to opt out (after all, you can choose not to install .NET Framework 3.5, thus avoiding the virus trigger). However, for virtual machine testing, this is a disaster; since Windows 8.1, Microsoft no longer pre-installs .NET Framework 3.5 with Windows, and if you want to install this runtime, you not only need to connect your VM to the internet (which is fatal for VM testing) but also have to wait at least 15 minutes (and unlucky users might wait over half an hour). In contrast, KanjuWare uses Python 3.8 + PyInstaller. While its downside is that if you want to test it on Windows 7, you will need to apply full cumulative updates (such as KB2533623, KB3063858, etc.; using UpdatePack7R2 for a complete update is recommended for the sake of the VM), its advantage is that KanjuWare does not require any extra runtimes on any modern system (such as Windows 10 and Windows 11)—it works right out of the box.
3. Rensenware often crashes when reading read-only files, but KanjuWare has a perfect file accessibility detection mechanism, which means you don't need to remove your disc drive anymore.
4. Rensenware requires scoring 200 million points on LUNATIC difficulty in the official version of "Touhou Seirensen"; therefore, first, you must have the official version of "Touhou Seirensen" (as it does not support the Trial version); otherwise, you can only download a pirated copy or purchase it on Steam. Secondly, Rensenware's requirement to score 200 million points on Lunatic difficulty is almost impossible to achieve—keep in mind that there are fewer than 10,000 people in the entire world who have cleared "Touhou Seirensen" on LUNATIC difficulty, let alone scored such high points. A complete noob will practice at least 3-5 years to achieve it. In comparison, KanjuWare supports a free Trial version and sets a requirement of scoring 50 million points on any difficulty; according to testing by the author himself, this only requires reaching stage three mid-boss on EASY difficulty, which takes about one or two hours for many people (Pointdevice mode) or just 15 minutes for skilled players (Legacy mode), not to mention the backdoor available to directly restore files.
5. The author of Rensenware only provided a game-dependent unlocking tool after the fact, whereas the author of KanjuWare natively provided backdoors and RPY files for unlocking.
6. Rensenware runs without any warning, whereas KanjuWare will explicitly pop up a warning window asking whether you want to run it.

### What does 50 million mean?

This means any one of the following (tested by the author. The data may be inaccurate because the author used trainers while testing the HARD and LUNATIC difficulties and the EX Stage.):
- Reach and beat the midway of Stage 3 on EASY / NORMAL difficulty.
- Reach and beat the final boss of Stage 2 on HARD / LUNATIC difficulty.
- (In full version, practice mode) Beat Stage 3/4/5/6 on EASY / NORMAL / HARD difficulty.
- (In full version, practice mode) Beat the midway of Stage 5 on LUNATIC difficulty.
- (In full version, practice mode) Beat Stage 3/4/6 on LUNATIC difficulty.
- (In full version) Beat EX stage.

**See, it is easier to "unlock" file in legit way than Rensenware！**

## How to unlock it?

Try one of these methods:
1. (Legit) Reach 50 million points in *Touhou 15: Legacy of Lunatic Kingdom* in full or trial version.
2. (Easy) Use Cheat Engine or trainers to change your score.
3. (Easier) Download RPY file from release, place it in `%APPDATA%\th15tr\replay`, and launch *Touhou 15: Legacy of Lunatic Kingdom* trial version to replay it.
4. (Cheat) Use backdoor.
5. (In system) Juse shut the window in Task Manager, and rename the files manually.

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

Execute `uv run pyinstaller -F --noconsole --add-data "assets;assets" --icon="kanju.ico" --name "KanjuWare" main.py`. 
Or execute the command `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (macOS / Linux) to activate the environment, and execute `pyinstaller -F --noconsole --add-data "assets;assets" --icon="kanju.ico" --name "KanjuWare" main.py`.

---

## Note

- The "highest tribute" to antivirus software: Due to the involvement of full-disk traversal and file extension modification, the EXE files generated by this program may be immediately detected and quarantined by various antivirus software. Please be sure to disable antivirus software (such as Windows Defender) when testing in a virtual machine. 
- Please use in a virtual machine: Although this program has core path filtering (Windows, Program Files, and other system directories have been skipped), it is strongly recommended to run tests only in an isolated virtual machine environment to avoid affecting the normal configuration of your daily software!
- Uploading the latest release to Virus Analyzing Website (for example: VirusTotal) is not allowed, but older release can be uploaded to analyze.

## System Requirements

This is for the Virtual Machine configuration.

Recomended:
- CPU: 2 cores & 2.5 GHz CPU or higher (Core 2 Duo or faster)
- RAM: 2048 MB or higher
- GPU: Shader Model 2.0 compatible, 3D Acceleration recommended.
- DirectX Version: 9.0c
- Storage: 800 MB
- Sound Card: DirectSound compatible
- Operating System: Full-Patched Windows 7, or Windows 8.1 / Windows 10 / Windows 11.

As for 3D acceleration issues in VMware 17, the VMware 15/16 is recommended. Although VirtualBox offers 3D acceleration, its implementation falls short of VMware's; Hyper-V lacks 3D acceleration in both basic and enhanced sessions, making it impossible to run games; Linux KVM requires enabling VirtIO-GPU and using Mesa (or another Vulkan-based renderer) combined with DXVK to maintain a frame rate of 60 FPS.

## License
MIT License - Feel free to fork and mess around, but please do not use it for any truly malicious purposes. The author bears no responsibility for any accidents caused by the use of this project (such as victims smashing keyboards, computers, or engaging in real-life fighting because they cannot beat "Touhou Legacy of Lunatic Kingdom").

## Inspired by
[RensenWare](https://github.com/0x00000FF/rensenware-cut) - by [@0x00000FF](https://github.com/0x00000FF)
