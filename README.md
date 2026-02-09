# Arduloader

Arduloader is a small PyQt6 GUI tool for uploading a compiled Arduino
hex file to a board over a serial port.

![Arduloader screenshot](snapshot.png)

## Features
- GUI for selecting board, port, and hex file
- Remembers last used hex file, board, and port in `config.ini`
- GitHub Actions builds are manual. Use `gh workflow run build-packages -f runner=windows-latest -f python-version=3.11`
- Simple Windows exe packaging script

## Requirements
- Python 3.13+
- PyQt6
- pyserial (external dependency; no vendored `serial/` folder)

## Install and run (uv)
```bash
uv python install 3.13
uv sync
uv run arduloader
```

## Install and run (pip)
```bash
python -m venv .venv
. .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
python -m pip install -e .
arduloader
```

## Usage
1. Open Arduloader.
2. Select your board model from the board list.
3. Select the serial port.
4. Choose a `.hex` file.
5. Click Upload and watch the log output.

## Windows build
The repository includes `buildexe.py` which uses py2exe.

```bash
uv run python -m pip install py2exe
uv run python buildexe.py
```

Or without uv:

```bash
python -m pip install py2exe
python buildexe.py
```

## Linux build
There is no dedicated Linux packaging script in this repo. A common
approach is PyInstaller:

```bash
uv run python -m pip install pyinstaller
uv run pyinstaller --onefile --windowed main.py
```

Or without uv:

```bash
python -m pip install pyinstaller
pyinstaller --onefile --windowed main.py
```

PyQt apps may need extra Qt plugins on some distros. If the executable
fails to start, check Qt plugin paths and add data files as needed.

## GitHub Actions workflow (multi-platform build)
The workflow in `.github/workflows/windows-build.yml` is now a
multi-platform build. You pass the runner label and Python version
as inputs, then it installs build deps and packages for that OS.

Inputs:
- `runner`: runner label, e.g. `windows-latest`, `ubuntu-latest`, `macos-latest`,
  or a custom label like `ubuntu-22.04-arm` if available.
- `python-version`: Python version to use.

Artifacts:
- Windows: `dist/arduloader.exe`
- Linux: `dist/arduloader`
- macOS: `dist/arduloader.app`

GitHub 操作（触发构建）:
1. 打开仓库的 Actions。
2. 选择 `build-packages` workflow。
3. 点击 `Run workflow`，填入 `runner` 和 `python-version`。
4. 构建完成后在该次运行的 Artifacts 中下载文件。

GitHub CLI 示例:
```bash
gh workflow run build-packages -f runner=windows-latest -f python-version=3.11
gh workflow run build-packages -f runner=ubuntu-latest -f python-version=3.11
gh workflow run build-packages -f runner=macos-latest -f python-version=3.11

gh run list --workflow build-packages
gh run watch --workflow build-packages
gh run download --name arduloader-windows-latest
```

本地操作（等效构建）:
1. Windows: 用 `uv run` 执行 `buildexe.py`（见上文）。
2. Linux/macOS: 用 `uv run pyinstaller --onefile --windowed --name arduloader main.py`。

If you change the build tool or its dependencies, update the workflow
install steps accordingly (for example, py2exe vs pyinstaller).

## Project layout
- `main.py`: app entry point
- `ArduloaderWindow.py`: UI wiring and upload flow
- `Uploader.py`: upload worker
- `PortManager.py`: serial port detection
- `boards.txt`: board definitions
- `config.ini`: last used settings
