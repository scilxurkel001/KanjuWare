# KanjuWare - 绀珠纯粹异变模拟器

一个基于 Python + Pymem + Tkinter 开发的娱乐项目，向 2017 年经典粉丝梗 **Rensenware** 致敬。

> **免责声明：** 本程序仅用于技术交流、虚拟机实验及团组成员娱乐。它**不会**实际加密任何文件，也**不会**上传任何数据；本质上它是一个完全自动化的、无害的文件重命名重复执行器。

---

## 特性

1. **纯粹伪装**：激活后，它会自动请求管理员权限 (UAC)，然后在后台以极高的速度遍历整个磁盘，将 `.LoLK`（Legacy of Lunatic Kingdom）后缀追加到具有指定扩展名的文件名末尾。
2. **狂气弹幕解密**：界面将被锁定并显示“高压勒索信”。唯一的合法解密方式是启动《东方Project》第15作《东方绀珠传》（Touhou 15: Legacy of Lunatic Kingdom，th15.exe）的试玩版或正式版，并在任何难度下获得 **50,000,000（5000万）** 的全满分。
3. **灵力同步**：后台线程采用无锁设计，每 200 毫秒实时读取 ZUN 神圣的内存基地址 `0x004E40BC` 和 `004E740C`。你在游戏中每获得一个分数，界面上的分数都会同步飙升。
4. **开发者仁慈**：界面右下角隐藏着一个不可见的像素点；双击该像素点将触发隐藏后门，直接完成关卡（自救通道）。

## 与 Rensenware 的对比

1. Rensenware 使用的是真正的加密，而 KanjuWare 仅仅是更改文件名。这意味着一旦 Rensenware 出错，文件将无法恢复；然而使用 KanjuWare 时，即使进程被意外终止或软件意外崩溃，你仍然可以使用批量重命名工具来恢复文件。
2. Rensenware 需要 .NET Framework 3.5 环境，这对于物理 Windows 10/11 用户来说实际上是一件好事，因为这给了他们至少一个选择退出（拒绝安装）的机会（毕竟你可以选择不安装 .NET Framework 3.5，从而避免触发病毒）。然而，对于虚拟机测试来说，这是一场灾难；自 Windows 8.1 起，微软不再随 Windows 预装 .NET Framework 3.5，如果你想安装此运行时，不仅需要将虚拟机连接到互联网（这对虚拟机测试是致命的），还需要等待至少 15 分钟（倒霉的用户可能要等半个多小时）。相比之下，KanjuWare 使用 Python 3.8 + PyInstaller。虽然它的缺点是如果你想在 Windows 7 上测试它，则需要应用完整的累积更新（例如 KB2533623、KB3063858 等；为了虚拟机安全，建议使用 UpdatePack7R2 进行完整更新），但它的优点是 KanjuWare 在任何现代系统（如 Windows 10 和 Windows 11）上都不需要任何额外的运行时——开箱即用。
3. Rensenware 在读取只读文件时经常崩溃，而 KanjuWare 拥有完美的文件的可访问性检测机制，这意味着你不再需要移除光驱了。
4. Rensenware 要求在正式版的《东方星莲船》LUNATIC 难度下达到 2 亿分；因此，首先，你必须拥有《东方星莲船》的正版（因为它不支持试用版）；否则，你只能下载盗版或在 Steam 上购买。其次，Rensenware 要求在 LUNATIC 难度下获得 2 亿分几乎是不可能实现的——请记住，全世界只有不到 1 万人能在 LUNATIC 难度下通关《东方星莲船》，更不用说拿到这么高的分数了。一个纯新手至少需要练习 3-5 年才能实现这一点。相比之下，KanjuWare 支持免费试用版，并将要求设定为在任何难度下获得 5000 万分；根据作者本人的测试，这只需要在 EASY 难度下到达三面道中，这对许多人来说大约需要一两个小时（完美无缺模式），对于熟练玩家只需 15 分钟（传统遗产模式），更不用说还有一个可以直接恢复文件的后门。
5. Rensenware 的作者事后才提供了依赖游戏的解锁工具，而 KanjuWare 的作者原生就提供了用于解锁的后门和 RPY 文件。
6. Rensenware 在没有任何警告的情况下运行，而 KanjuWare 会显式弹出警告窗口询问是否要运行它。

### 5000万分是什么？

这意味着满足以下任一条件（由作者测试。由于作者在测试 HARD、LUNATIC 难度及 EX Stage 时使用了修改器，数据可能不准确）：
- 在 EASY / NORMAL 难度下到达三面道中以后。
- 在 HARD / LUNATIC 难度下到达并击败二面关底 Boss。
- （正式版，练习模式）在 EASY / NORMAL / HARD 难度下通关第三面/四面/五面/六面。
- （正式版，练习模式）在 LUNATIC 难度下通过五面道中。
- （正式版，练习模式）在 LUNATIC 难度下通关第三面/四面/六面。
- （正式版）通关 EX Stage。

**看吧，用正规方式“解锁”文件比使用 Rensenware 要容易得多！**

## 如何解锁？

尝试以下方法之一：
1. （正规）在《东方绀珠传》的正版或试用版中获得 5000 万分数。
2. （简单）使用 Cheat Engine 或修改器更改你的分数。
3. （更简单）从发布包中下载 RPY 文件，将其放入 `%APPDATA%\ShanghaiAlice\th15tr\replay`，然后启动《东方绀珠传》试用版进行回放。
4. （作弊）使用后门。
5. （系统操作）直接在任务管理器中关闭窗口，并手动重命名文件。

---

## 🛠️ 构建与安装

您需要：
- Python 3.8（这是为了兼容 Windows 7）
- Windows 7/10/11（建议使用 Windows 10 或 11）

**强烈建议使用 [uv](https://github.com/astral-sh/uv) 进行高效的依赖管理。**

### 编译方法 1（强烈推荐）

如果您已安装 `uv`，请直接执行 `uv sync` 命令，并在安装完成后进入下一步。

### 编译方法 2（传统方法）

如果您没有安装 `uv`，请确保您的 Python 版本在 3.8 或更高版本，然后...
首先，执行命令 `python -m venv .venv` 来创建虚拟环境。
接着，执行命令 `.venv\Scripts\activate` (Windows) 或 `source .venv/bin/activate` (macOS / Linux) 来激活环境。
最后，执行命令 `pip install -r requirements.txt` 来安装依赖项。
如果安装成功完成，您可以进行下一步。如果在安装过程中发生错误，请删除虚拟环境并重试，或者使用 `uv` 以获得更顺畅的安装体验。

## 调试与运行

在文件根目录执行 `uv run main.py`。
或者执行命令 `.venv\Scripts\activate`（Windows）或 `source .venv/bin/activate`（macOS / Linux）来激活环境，然后执行 `python main.py`。
请注意，**不建议**这样做，因为这会导致主机文件被重命名。

## 发行包封装

执行 `uv run pyinstaller -F --noconsole --add-data "assets;assets" --icon="kanju.ico" --name "KanjuWare" main.py`。
或者执行命令 `.venv\Scripts\activate` (Windows) 或 `source .venv/bin/activate` (macOS / Linux) 来激活环境，然后执行 `pyinstaller -F --noconsole --add-data "assets;assets" --icon="kanju.ico" --name "KanjuWare" main.py`。

---

## 注意事项

- 对杀毒软件的“最高敬意”：由于涉及全盘遍历和文件扩展名修改，本程序生成的 EXE 文件可能会被各种杀毒软件立即检测并隔离。在虚拟机中进行测试时，请务必禁用杀毒软件（如 Windows Defender）。
- 请在虚拟机中使用：虽然本程序具有核心路径过滤功能（已跳过 Windows、Program Files 等系统目录），但强烈建议仅在隔离的虚拟机环境中运行测试，以避免影响您日常软件的正常配置！
- 不允许将最新发布的版本上传至病毒分析网站（例如：VirusTotal），但可以将旧版本上传进行分析。

## 系统配置要求

这是针对虚拟机的配置要求。

建议配置：
- CPU：2 核及 2.5 GHz 或更高（Core 2 Duo 或更快的处理器）
- RAM：2048 MB 或更高
- GPU：支持 Shader Model 2.0，建议开启 3D 加速
- DirectX 版本：9.0c
- 存储空间：800 MB
- 声卡：兼容 DirectSound
- 操作系统：已完整补丁的 Windows 7，或 Windows 8.1 / Windows 10 / Windows 11。

关于 VMware 17 中的 3D 加速问题，建议使用 VMware 15/16。虽然 VirtualBox 提供 3D 加速，但其实现效果不及 VMware；Hyper-V 在基本会话和增强会话中都缺乏 3D 加速，导致无法运行游戏；Linux KVM 则需要启用 VirtIO-GPU 并结合 Mesa（或其他基于 Vulkan 的渲染器）以及 DXVK，才能维持 60 FPS 的帧率。

## 许可协议
MIT 许可证 - 欢迎随意分叉（fork）和尝试，但请不要将其用于任何真正的恶意目的。作者对因使用本项目而导致的任何意外不承担任何责任（例如：玩家因为打不过《东方绀珠传》而摔键盘、砸电脑或执行真人快打）。

## 灵感来源
[RensenWare](https://github.com/0x00000FF/rensenware-cut) - by [@0x00000FF](https://github.com/0x00000FF)
