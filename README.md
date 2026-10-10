<div align="center">

# ClearSort

### File order, without the anxiety.

ClearSort is a Windows desktop utility for turning scattered folders into a
predictable file system — while keeping every destructive decision in your
hands.

<br />

**Organize by type · Compare across folders · Quarantine safely**

<br />

[Get started](#get-started) · [How it works](#how-it-works) · [Safety contract](#safety-contract)

</div>

---

## The short version

ClearSort is built for the moment when a folder has become too important,
too large, or too messy to clean manually.

Select up to **five folders**, choose an operation, and let ClearSort do the
repetitive work:

| Operation | Result |
| --- | --- |
| **Sort files** | Routes loose files into category and extension folders |
| **Find duplicates** | Compares file contents across all selected folders |
| **Review safely** | Moves duplicates into `Duplicates_To_Delete` instead of deleting them |

There is no automatic purge, no overwrite-by-default behavior, and no opaque
"clean everything" button.

> **ClearSort moves files. It does not permanently delete them.**

## Why it exists

Most cleanup tools optimize for speed by making the final decision for you.
ClearSort optimizes for **confidence**.

- A predictable destination is better than a clever one.
- A visible quarantine is better than an irreversible delete.
- A clear activity log is better than a silent success message.
- A reversible file move is better than a recovery problem.

The product is intentionally small, focused, and explicit.

## What you can do

### 01 — Create a file system you can navigate

Loose files are classified into a stable structure:

```text
Selected folder/
├── Photos/
│   ├── JPG/
│   ├── PNG/
│   └── HEIC/
├── Videos/
│   ├── MP4/
│   └── MOV/
├── Documents/
│   ├── PDF/
│   ├── DOCX/
│   └── XLSX/
└── Others/
    ├── ZIP/
    └── NO_EXTENSION/
```

The original filename is preserved. When a destination already contains the
same name, ClearSort creates a numbered alternative such as
`report (2).pdf`; it does not overwrite the existing file.

### 02 — Find exact copies, not guesses

Duplicate detection is content-based. ClearSort hashes files with SHA-256 in
1 MB chunks, groups matching content, keeps the first deterministic match,
and moves the remaining copies for review.

```text
<source folder>/
└── Duplicates_To_Delete/
    └── original-relative-path/
        └── duplicate-file.ext
```

The original relative path is retained inside quarantine. Existing quarantine
folders are excluded from future scans, so a second run does not repeatedly
process the same moved files.

### 03 — Compare folders as one workspace

Use the folder-group picker to select child folders together:

- `Ctrl + Click` — select individual folders
- `Shift + Click` — select a range
- **Select all** — select the visible folder set
- **Clear** — reset the selection

ClearSort accepts a maximum of five folders and rejects duplicate or
overlapping selections before any file operation starts.

## Safety contract

ClearSort is designed around a simple rule: **the app should never make a
destructive decision on your behalf.**

| Guarantee | Behavior |
| --- | --- |
| No permanent deletion | Duplicates are moved to quarantine |
| No silent overwrite | Name collisions receive numbered filenames |
| No hidden failures | Move and permission errors appear in the activity log |
| No repeat quarantine scans | Managed folders are excluded from scanning |
| No frozen interface | File work runs in background worker threads |
| No unsafe folder API | Folder selection uses standard Windows dialogs plus a safe in-app multi-select view |

Review `Duplicates_To_Delete` before removing anything, especially when
working inside OneDrive, network shares, or synchronized folders.

## Get started

### Fastest path — Windows

1. Download or clone this repository.
2. Double-click [`start.bat`](./start.bat).
3. Choose a folder group.
4. Select up to five child folders.
5. Run **Sort files** or **Find duplicates**.
6. Review the activity log and quarantine folders before taking any further action.

`start.bat` creates a local virtual environment, installs the runtime
dependency, and launches ClearSort.

### Run from PowerShell

```powershell
git clone https://github.com/Anirban4ru/DupeCleaner-Pro.git
cd DupeCleaner-Pro

py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## Requirements

- Windows 10 or Windows 11
- Python 3.10 or newer
- CustomTkinter 5.2.2 or newer

## Product surface

ClearSort is intentionally a native-feeling desktop tool rather than a web
dashboard:

- Dark, low-distraction workspace UI
- Persistent source-folder rail
- Visible operation status and progress
- Activity log with timestamps
- Explicit success, warning, and error states
- Responsive background processing
- Safe filename collision handling

## Technical profile

| Layer | Choice |
| --- | --- |
| Runtime | Python |
| Desktop UI | Tkinter + CustomTkinter |
| Duplicate identity | SHA-256 content hash |
| File movement | `pathlib` + `shutil` |
| Responsiveness | Background worker threads |
| Distribution entry point | Windows `start.bat` |

The implementation deliberately avoids manual COM vtable or pointer
manipulation for folder selection. Reliability is more important than
pretending that a standard Windows folder dialog supports a feature it does
not provide.

## Repository layout

```text
ClearSort/
├── main.py
├── requirements.txt
├── start.bat
├── .gitignore
└── README.md
```

## Roadmap

The next product-quality steps are:

- Preview mode before moving files
- Undo for the latest operation
- Windows installer and signed release builds
- Configurable category and extension rules
- Improved progress reporting for very large trees
- Automated regression coverage for file-operation edge cases

## Contributing

Keep changes conservative around file operations. Any contribution that moves
or classifies files should include:

1. A clear description of the behavior change.
2. Explicit handling for permissions, collisions, and partial failure.
3. A test or reproducible verification path.
4. Documentation updates when the user-facing behavior changes.

## License

No open-source license has been selected yet. Until a license is added, the
repository should be treated as **all rights reserved** and not redistributed
as a packaged product.

---

<div align="center">

**ClearSort** — make order visible, keep control.

</div>
