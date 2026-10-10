<div align="center">

# ClearSort

### The professional, non-destructive way to organize your Windows files.

<p>
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white" alt="Python 3.10+">
  <img src="https://img.shields.io/badge/Platform-Windows-0078D4?style=flat-square&logo=windows&logoColor=white" alt="Windows">
  <img src="https://img.shields.io/badge/UI-CustomTkinter-1F6FEB?style=flat-square" alt="CustomTkinter">
  <img src="https://img.shields.io/badge/Integrity-SHA--256-2EA043?style=flat-square" alt="SHA-256">
  <img src="https://img.shields.io/badge/Deletes-nothing-D97706?style=flat-square" alt="Deletes nothing">
</p>

<p>
  A focused Windows desktop utility that sorts loose files, compares up to five
  folders for exact duplicates, and moves duplicates into a reviewable quarantine
  folder — never straight to the Recycle Bin.
</p>

</div>

---

## 🚀 ClearSort at a glance

| Capability | What it delivers |
|:--|:--|
| 🗂️ **Structured organization** | Routes files into `Photos`, `Videos`, `Documents`, and `Others`, then groups them by extension |
| 🔍 **Exact duplicate detection** | Uses SHA-256 content hashing to find identical files across selected folders |
| 📁 **Multi-folder workspace** | Select and scan up to five sibling folders as one controlled operation |
| 🛡️ **Safe quarantine** | Moves duplicates to `Duplicates_To_Delete` instead of permanently deleting them |
| 🧭 **Predictable results** | Preserves filenames, source-relative paths, and never overwrites existing files |
| 📊 **Visible operations** | Shows progress, timestamps, moved counts, warnings, and failures inside the app |

## ✨ Why ClearSort

File cleanup should not feel like gambling with your own data.

ClearSort is designed around a simple principle:

> **Automate the repetitive work. Keep the final decision with the person.**

It does not silently delete files. It does not overwrite collisions. It does
not hide permission failures behind a green success message. Every duplicate
is moved into a clearly named location that you can inspect before deleting
anything yourself.

## 🧭 Core workflow

| Step | Action | Result |
|:--:|:--|:--|
| **01** | **Choose a folder group** | Open a parent folder and view its child folders |
| **02** | **Select up to five folders** | Use `Ctrl + Click`, `Shift + Click`, **Select all**, or **Clear** |
| **03** | **Sort files** | Build a clean category/extension structure without overwriting files |
| **04** | **Find duplicates** | Compare file contents across the complete selected workspace |
| **05** | **Review quarantine** | Inspect `Duplicates_To_Delete` before removing anything |

## 📦 The result

### Organized files

```text
Photos/
├── JPG/
├── PNG/
└── HEIC/

Videos/
├── MP4/
└── MOV/

Documents/
├── PDF/
├── DOCX/
└── XLSX/

Others/
└── ZIP/
```

### Duplicates kept recoverable

```text
<source-folder>/
└── Duplicates_To_Delete/
    └── original-relative-path/
        └── duplicate-file.ext
```

The first deterministic file in an exact-match group is retained. Additional
copies are moved to quarantine with their relative location preserved.

## 🛡️ Safety guarantees

| Rule | ClearSort behavior |
|:--|:--|
| **No permanent deletion** | Duplicates are moved, never automatically deleted |
| **No overwrites** | Collisions become `filename (2).ext`, `filename (3).ext`, and so on |
| **No hidden failures** | Permission and move errors are written to the activity log and surfaced to the user |
| **No duplicate reprocessing** | `Duplicates_To_Delete` is excluded from future scans |
| **No overlapping sources** | Nested or repeated folder selections are rejected before processing |
| **No frozen UI** | File operations run in background worker threads |

> Review quarantine folders before removing anything, especially in OneDrive,
> network shares, or other synchronized locations.

## 🖥️ Interface

ClearSort is built as a focused desktop workspace, not a disposable script:

- Persistent source-folder rail
- Clear primary and secondary actions
- Live operation status
- Progress feedback
- Timestamped activity log
- Explicit success, warning, and error states
- Safe multi-selection dialog
- Dark, low-distraction Windows interface

## ⚡ One-click setup

### Windows

Double-click [`start.bat`](./start.bat).

The launcher will:

1. Create a local `.venv` environment if needed.
2. Install the dependency from [`requirements.txt`](./requirements.txt).
3. Start ClearSort.

### Manual setup

```powershell
git clone https://github.com/Anirban4ru/DupeCleaner-Pro.git
cd DupeCleaner-Pro

py -3 -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
.venv\Scripts\python.exe main.py
```

## 🔧 Technical foundation

| Layer | Implementation |
|:--|:--|
| Language | Python |
| Desktop interface | Tkinter + CustomTkinter |
| Duplicate identity | SHA-256 content hashing |
| File operations | `pathlib` + `shutil` |
| Responsiveness | Background worker threads |
| Supported platform | Windows 10 / Windows 11 |
| Runtime dependency | `customtkinter>=5.2.2` |

The folder selector intentionally avoids fragile manual COM pointer or vtable
calls. ClearSort uses standard Windows folder selection followed by a safe,
tested in-app multi-selection view.

## 🗺️ Roadmap

- [ ] Dry-run preview before moving files
- [ ] Undo for the most recent operation
- [ ] Windows installer and signed release builds
- [ ] Custom categories and extension rules
- [ ] Improved large-tree scan performance
- [ ] Automated regression tests for edge cases

## 📁 Repository

```text
ClearSort/
├── main.py
├── requirements.txt
├── start.bat
├── .gitignore
└── README.md
```

## 📄 License

No open-source license has been selected yet. Until a license is added, this
repository is **all rights reserved** and should not be redistributed as a
packaged product.

---

<div align="center">

### ClearSort

**Make order visible. Keep control.**

</div>
