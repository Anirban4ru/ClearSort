# ClearSort

### A calm, safe way to bring order to your Windows files.

ClearSort is a Windows desktop utility for organizing loose files and isolating exact duplicates without destructive cleanup. Select up to five folders, review what will happen, and keep full control over every file movement.

> **Nothing is permanently deleted.** Exact duplicates are moved to a clearly named quarantine folder so you can review them before removing anything yourself.

## Why ClearSort

Most file-cleanup tools make a destructive promise: scan, delete, hope. ClearSort takes the safer approach:

- **Organize by intent** — files are placed into `Photos`, `Videos`, `Documents`, or `Others`.
- **Keep file types discoverable** — each category is split into extension folders such as `Photos/JPG` or `Documents/PDF`.
- **Compare across folders** — scan up to five selected folders in one workspace.
- **Quarantine, never destroy** — duplicates move to `Duplicates_To_Delete` inside their original source folder.
- **Stay recoverable** — original relative paths are preserved inside quarantine folders.
- **See every outcome** — progress, errors, moved counts, and activity are visible in the app.

## Features

### Structured organization

ClearSort uses a predictable destination structure:

```text
Selected folder/
├── Photos/
│   ├── JPG/
│   └── PNG/
├── Videos/
│   └── MP4/
├── Documents/
│   └── PDF/
└── Others/
    └── ZIP/
```

The original file name is retained. If a destination already contains that name, ClearSort creates a numbered alternative such as `report (2).pdf` instead of overwriting anything.

### Exact duplicate detection

Duplicate detection uses SHA-256 hashes and reads files in 1 MB chunks. Files with identical content are grouped together; the first deterministic match is retained and the remaining copies are moved to:

```text
<source folder>/Duplicates_To_Delete/
```

Existing quarantine folders are excluded from future scans, so repeated runs do not re-process the same files.

### Multi-folder workspace

Choose a parent folder, then select up to five child folders together using:

- `Ctrl + Click` for individual folders
- `Shift + Click` for a range
- **Select all** and **Clear** controls

ClearSort rejects duplicate selections and overlapping folders before any scan begins.

## Safety model

ClearSort is designed around reversible operations:

1. No automatic deletion.
2. No overwriting of existing files.
3. Permission and move failures are surfaced in the activity log.
4. Duplicate quarantine keeps source-relative paths.
5. Existing managed folders are excluded from source scans.

Always review `Duplicates_To_Delete` before removing files, especially when working with synchronized or shared folders.

## Run on Windows

### Recommended

Double-click [`start.bat`](./start.bat). It creates a local virtual environment, installs the dependency, and launches ClearSort.

### Manual

```powershell
py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- CustomTkinter 5.2.2 or newer

## Project structure

```text
ClearSort/
├── main.py           # Desktop application
├── requirements.txt  # Runtime dependency
├── start.bat         # Windows launcher
├── .gitignore
└── README.md
```

## Development notes

The application uses:

- Python
- Tkinter
- CustomTkinter
- SHA-256 content hashing
- Background worker threads for file operations

File operations run away from the UI thread so the interface remains responsive during larger scans. The project intentionally avoids unsafe native COM pointer manipulation for folder selection.

## Roadmap

- Windows installer package
- Dry-run preview before moving files
- Undo history for the latest operation
- Larger-folder scan performance improvements
- Optional custom category rules

## License

License terms have not yet been selected. Add a license before distributing ClearSort publicly.
