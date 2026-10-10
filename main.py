import hashlib
import os
import shutil
import threading
from collections import defaultdict
from datetime import datetime
from pathlib import Path
from tkinter import END, Listbox, filedialog, messagebox

import customtkinter as ctk


ctk.set_appearance_mode("Dark")
ctk.set_default_color_theme("blue")

CATEGORIES = {
    "Photos": {".jpg", ".jpeg", ".png", ".gif", ".webp", ".heic"},
    "Videos": {".mp4", ".mkv", ".avi", ".mov", ".wmv"},
    "Documents": {".pdf", ".docx", ".doc", ".txt", ".xlsx", ".csv", ".pptx"},
}
DUPLICATES_FOLDER = "Duplicates_To_Delete"
MANAGED_FOLDERS = set(CATEGORIES) | {"Others", DUPLICATES_FOLDER, "Duplicates_Found"}

COLORS = {
    "background": "#0E1116",
    "sidebar": "#151A21",
    "surface": "#191F27",
    "surface_alt": "#232B35",
    "border": "#2E3845",
    "text": "#F5F7FA",
    "muted": "#A7B0BC",
    "accent": "#4D8DFF",
    "accent_hover": "#6B9FFF",
    "success": "#37C98A",
    "warning": "#F2B84B",
    "danger": "#F07178",
}


class FileOrganizerApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("ClearSort — Workspace")
        self.geometry("1180x760")
        self.minsize(980, 660)
        self.configure(fg_color=COLORS["background"])

        self.selected_folder = Path()
        self.selected_folders = []
        self.is_busy = False
        self.file_count = 0
        self.last_action = "Ready"

        self._build_layout()
        self._set_status("Choose a folder to get started.", "muted")

    def _build_layout(self):
        self.grid_columnconfigure(0, weight=0, minsize=286)
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.sidebar = ctk.CTkFrame(self, width=286, corner_radius=0, fg_color=COLORS["sidebar"])
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        self.sidebar.grid_propagate(False)
        self._build_sidebar()

        self.content = ctk.CTkFrame(self, corner_radius=0, fg_color=COLORS["background"])
        self.content.grid(row=0, column=1, sticky="nsew", padx=42, pady=34)
        self.content.grid_columnconfigure(0, weight=1)
        self.content.grid_rowconfigure(4, weight=1)
        self._build_content()

    def _build_sidebar(self):
        self.sidebar.grid_rowconfigure(6, weight=1)
        ctk.CTkLabel(
            self.sidebar, text="CLEARSORT", text_color=COLORS["accent"],
            font=ctk.CTkFont(size=12, weight="bold"),
        ).pack(anchor="w", padx=26, pady=(28, 5))
        ctk.CTkLabel(
            self.sidebar, text="Sources", text_color=COLORS["text"],
            font=ctk.CTkFont(size=25, weight="bold"),
        ).pack(anchor="w", padx=26, pady=(0, 8))
        ctk.CTkLabel(
            self.sidebar, text="Choose the folders you want to clean together.",
            text_color=COLORS["muted"], justify="left", wraplength=224,
            font=ctk.CTkFont(size=12),
        ).pack(anchor="w", padx=26, pady=(0, 22))

        self.folder_card = ctk.CTkFrame(
            self.sidebar, fg_color=COLORS["surface"], corner_radius=8,
            border_width=1, border_color=COLORS["border"],
        )
        self.folder_card.pack(fill="both", expand=False, padx=18, pady=0)
        ctk.CTkLabel(
            self.folder_card, text="SELECTED FOLDERS", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold"),
        ).pack(anchor="w", padx=15, pady=(15, 7))
        self.folder_list = ctk.CTkScrollableFrame(
            self.folder_card, height=220, fg_color="transparent",
            scrollbar_button_color=COLORS["border"],
        )
        self.folder_list.pack(fill="x", padx=8, pady=(0, 8))

        self.browse_button = ctk.CTkButton(
            self.sidebar, text="Add folders  ·  0/5", height=42, corner_radius=7,
            fg_color=COLORS["accent"], hover_color=COLORS["accent_hover"],
            command=self.select_folder,
        )
        self.browse_button.pack(fill="x", padx=18, pady=(14, 7))
        self._render_folder_list()

        self.sidebar_hint = ctk.CTkLabel(
            self.sidebar,
            text=f"Up to five folders can be scanned together. Nothing is deleted: duplicates are moved to {DUPLICATES_FOLDER} for review.",
            text_color=COLORS["muted"], justify="left", wraplength=230,
            font=ctk.CTkFont(size=11),
        )
        self.sidebar_hint.pack(side="bottom", anchor="w", padx=26, pady=26)

    def _build_content(self):
        header = ctk.CTkFrame(self.content, fg_color="transparent")
        header.grid(row=0, column=0, sticky="ew", pady=(0, 30))
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="Clean up your workspace", text_color=COLORS["text"],
            font=ctk.CTkFont(size=28, weight="bold"),
        ).grid(row=0, column=0, sticky="w")
        ctk.CTkLabel(
            header, text="Organize files by type or safely isolate exact duplicates.",
            text_color=COLORS["muted"], font=ctk.CTkFont(size=13),
        ).grid(row=1, column=0, sticky="w", pady=(5, 0))
        self.status_pill = ctk.CTkLabel(
            header, text="READY", text_color=COLORS["success"],
            fg_color="#163529", corner_radius=6, padx=12, pady=6,
            font=ctk.CTkFont(size=10, weight="bold"),
        )
        self.status_pill.grid(row=0, column=1, rowspan=2, sticky="e")

        self.stats = ctk.CTkFrame(self.content, fg_color="transparent")
        self.stats.grid(row=1, column=0, sticky="ew", pady=(0, 24))
        for column in range(3):
            self.stats.grid_columnconfigure(column, weight=1)
        self.stat_files = self._stat_card(self.stats, 0, "FILES IN FOLDER", "—")
        self.stat_sorted = self._stat_card(self.stats, 1, "LAST SORTED", "—")
        self.stat_duplicates = self._stat_card(self.stats, 2, "DUPLICATES MOVED", "—")

        actions = ctk.CTkFrame(
            self.content, fg_color=COLORS["surface"], corner_radius=8,
            border_width=1, border_color=COLORS["border"],
        )
        actions.grid(row=2, column=0, sticky="ew", pady=(0, 24))
        actions.grid_columnconfigure(0, weight=1)
        actions.grid_columnconfigure(1, weight=1)
        ctk.CTkLabel(
            actions, text="Actions", text_color=COLORS["text"],
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, columnspan=2, sticky="w", padx=20, pady=(17, 13))
        self.sort_button = self._action_button(
            actions, 0, "Sort files", "Place loose files into Photos, Videos, Documents, and Others.", self.sort_files,
        )
        self.duplicates_button = self._action_button(
            actions, 1, "Find duplicates", f"Move exact copies into {DUPLICATES_FOLDER} for safe review and removal.", self.find_duplicates,
        )
        self.sort_button.configure(state="disabled")
        self.duplicates_button.configure(state="disabled")

        activity = ctk.CTkFrame(self.content, fg_color="transparent")
        activity.grid(row=3, column=0, sticky="nsew")
        activity.grid_columnconfigure(0, weight=1)
        activity.grid_rowconfigure(1, weight=1)
        ctk.CTkLabel(
            activity, text="Activity log", text_color=COLORS["text"],
            font=ctk.CTkFont(size=15, weight="bold"),
        ).grid(row=0, column=0, sticky="w", pady=(0, 10))
        self.log_box = ctk.CTkTextbox(
            activity, fg_color=COLORS["surface"], border_width=1,
            border_color=COLORS["border"], corner_radius=8, wrap="word",
            text_color=COLORS["muted"], font=ctk.CTkFont(size=13),
        )
        self.log_box.grid(row=1, column=0, sticky="nsew")
        self.log_box.configure(state="disabled")
        self.progress = ctk.CTkProgressBar(
            self.content, height=7, corner_radius=4, fg_color=COLORS["surface_alt"],
            progress_color=COLORS["accent"],
        )
        self.progress.grid(row=4, column=0, sticky="ew", pady=(14, 0))
        self.progress.set(0)

    def _stat_card(self, parent, column, title, value):
        card = ctk.CTkFrame(
            parent, fg_color=COLORS["surface"], corner_radius=8,
            border_width=1, border_color=COLORS["border"],
        )
        card.grid(row=0, column=column, sticky="ew", padx=(0 if column == 0 else 6, 6 if column < 2 else 0))
        ctk.CTkLabel(
            card, text=title, text_color=COLORS["muted"],
            font=ctk.CTkFont(size=10, weight="bold"),
        ).pack(anchor="w", padx=16, pady=(13, 3))
        value_label = ctk.CTkLabel(
            card, text=value, text_color=COLORS["text"],
            font=ctk.CTkFont(size=21, weight="bold"),
        )
        value_label.pack(anchor="w", padx=16, pady=(0, 13))
        return value_label

    def _action_button(self, parent, column, title, description, command):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        frame.grid(row=1, column=column, sticky="ew", padx=20, pady=(0, 18))
        frame.grid_columnconfigure(0, weight=1)
        button = ctk.CTkButton(
            frame, text=title, height=42, anchor="w", corner_radius=7,
            fg_color=COLORS["accent"] if column == 0 else COLORS["surface_alt"],
            hover_color=COLORS["accent_hover"] if column == 0 else COLORS["border"],
            font=ctk.CTkFont(size=13, weight="bold"),
            command=command,
        )
        button.grid(row=0, column=0, sticky="ew")
        ctk.CTkLabel(
            frame, text=description, text_color=COLORS["muted"],
            justify="left", wraplength=330, font=ctk.CTkFont(size=11),
        ).grid(row=1, column=0, sticky="w", pady=(8, 0))
        return button

    def select_folder(self):
        if self.is_busy:
            return
        folders = self._choose_multiple_folders()
        if not folders:
            return
        available_slots = 5 - len(self.selected_folders)
        if len(folders) > available_slots:
            self._set_status("Maximum of 5 folders reached.", "warning")
            messagebox.showwarning(
                "Folder limit reached",
                f"You can add {available_slots} more folder(s). Select no more than five folders total.",
            )
            return

        candidates = self.selected_folders + folders
        duplicate_folders = len({folder.casefold() for folder in map(str, candidates)}) != len(candidates)
        overlapping = any(
            left != right and (left in right.parents or right in left.parents)
            for index, left in enumerate(candidates)
            for right in candidates[index + 1:]
        )
        if duplicate_folders or overlapping:
            self._set_status("Folders overlap or repeat.", "warning")
            messagebox.showwarning(
                "Invalid folder selection",
                "Folders must be unique and cannot contain one another. No folders were added.",
            )
            return

        self.selected_folders.extend(folders)
        self.selected_folder = self.selected_folders[0]
        self._render_folder_list()
        self.sort_button.configure(state="normal")
        self.duplicates_button.configure(state="normal")
        self._refresh_file_count()
        self._set_status("Folders selected. Choose an action.", "success")
        self._log(f"Added {len(folders)} folder(s); {len(self.selected_folders)}/5 selected.")

    def _choose_multiple_folders(self):
        parent = filedialog.askdirectory(
            title="Choose a folder group",
            mustexist=True,
        )
        if not parent:
            return []

        parent_path = Path(parent)
        try:
            children = sorted(
                (item for item in parent_path.iterdir() if item.is_dir()),
                key=lambda item: item.name.casefold(),
            )
        except OSError as error:
            self._set_status("Folder could not be read.", "danger")
            messagebox.showerror(
                "Unable to read folder",
                f"The selected folder could not be opened.\n\n{error}",
            )
            return []
        if not children:
            return [parent_path]

        dialog = ctk.CTkToplevel(self)
        dialog.title("Select folders")
        dialog.geometry("720x590")
        dialog.minsize(600, 480)
        dialog.transient(self)
        dialog.grab_set()
        dialog.grid_columnconfigure(0, weight=1)
        dialog.grid_rowconfigure(2, weight=1)

        ctk.CTkLabel(
            dialog, text="Select folders to scan",
            text_color=COLORS["text"], font=ctk.CTkFont(size=20, weight="bold"),
        ).grid(row=0, column=0, sticky="w", padx=24, pady=(22, 4))
        ctk.CTkLabel(
            dialog,
            text=f"Choose up to five folders inside:\n{parent_path}\nHold Ctrl to pick individual folders or Shift to select a range.",
            text_color=COLORS["muted"], justify="left", font=ctk.CTkFont(size=12),
        ).grid(row=1, column=0, sticky="w", padx=24, pady=(0, 14))

        listbox = Listbox(
            dialog, selectmode="extended", exportselection=False,
            bg=COLORS["surface"], fg=COLORS["text"],
            selectbackground=COLORS["accent"], selectforeground=COLORS["text"],
            activestyle="none", highlightthickness=1,
            highlightcolor=COLORS["accent"], highlightbackground=COLORS["border"],
            relief="flat", font=("Segoe UI", 11), selectborderwidth=0,
        )
        listbox.grid(row=2, column=0, sticky="nsew", padx=24, pady=(0, 8))
        for child in children:
            listbox.insert(END, str(child))

        result = []
        selection_label = ctk.CTkLabel(
            dialog, text="0 folders selected", text_color=COLORS["muted"],
            font=ctk.CTkFont(size=11),
        )
        selection_label.grid(row=3, column=0, sticky="w", padx=24, pady=(0, 10))

        def update_selection_count(_event=None):
            selection_label.configure(
                text=f"{len(listbox.curselection())} folder(s) selected  ·  maximum 5",
            )

        listbox.bind("<<ListboxSelect>>", update_selection_count)

        def confirm():
            indexes = listbox.curselection()
            if not indexes:
                messagebox.showwarning("No folders selected", "Select at least one folder.", parent=dialog)
                return
            if len(indexes) > 5:
                messagebox.showwarning("Folder limit reached", "Select no more than five folders.", parent=dialog)
                return
            result.extend(Path(listbox.get(index)) for index in indexes)
            dialog.destroy()

        footer = ctk.CTkFrame(dialog, fg_color="transparent")
        footer.grid(row=4, column=0, sticky="ew", padx=24, pady=(0, 22))
        footer.grid_columnconfigure(0, weight=1)
        utility = ctk.CTkFrame(footer, fg_color="transparent")
        utility.grid(row=0, column=0, sticky="w")
        ctk.CTkButton(
            utility, text="Select all", width=92, height=34,
            fg_color=COLORS["surface_alt"], hover_color=COLORS["border"],
            command=lambda: (listbox.selection_set(0, END), update_selection_count()),
        ).pack(side="left", padx=(0, 7))
        ctk.CTkButton(
            utility, text="Clear", width=78, height=34,
            fg_color="transparent", border_width=1, border_color=COLORS["border"],
            hover_color=COLORS["surface_alt"],
            command=lambda: (listbox.selection_clear(0, END), update_selection_count()),
        ).pack(side="left")
        ctk.CTkButton(
            footer, text="Cancel", width=110, height=36, fg_color=COLORS["surface_alt"],
            hover_color=COLORS["border"], command=dialog.destroy,
        ).grid(row=0, column=1, padx=(10, 7))
        ctk.CTkButton(
            footer, text="Add selected", width=140, height=36, command=confirm,
        ).grid(row=0, column=2, sticky="e")
        self.wait_window(dialog)
        return result

    def _render_folder_list(self):
        for child in self.folder_list.winfo_children():
            child.destroy()
        if not self.selected_folders:
            ctk.CTkLabel(
                self.folder_list, text="No folders added", text_color=COLORS["muted"],
            ).pack(anchor="w", padx=6, pady=8)
        for index, folder in enumerate(self.selected_folders, 1):
            row = ctk.CTkFrame(self.folder_list, fg_color=COLORS["surface_alt"], corner_radius=6)
            row.pack(fill="x", pady=3)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(
                row, text=f"{index}  {folder.name or folder.anchor}",
                text_color=COLORS["text"], anchor="w", wraplength=175,
            ).grid(row=0, column=0, sticky="ew", padx=(8, 2), pady=7)
            ctk.CTkButton(
                row, text="×", width=28, height=26, corner_radius=5,
                fg_color="transparent", hover_color=COLORS["danger"],
                command=lambda item=folder: self.remove_folder(item),
            ).grid(row=0, column=1, padx=(0, 4), pady=4)
        self.browse_button.configure(text=f"Add folders  ·  {len(self.selected_folders)}/5")

    def remove_folder(self, folder):
        if self.is_busy:
            return
        self.selected_folders.remove(folder)
        self.selected_folder = self.selected_folders[0] if self.selected_folders else Path()
        self._render_folder_list()
        self.sort_button.configure(state="normal" if self.selected_folders else "disabled")
        self.duplicates_button.configure(state="normal" if self.selected_folders else "disabled")
        self._refresh_file_count()
        self._set_status("Folder removed.", "muted")
        self._log(f"Removed folder: {folder}")

    def _refresh_file_count(self):
        if not self.selected_folder:
            return
        count = 0
        for folder in self.selected_folders:
            for root, directories, names in os.walk(folder):
                directories[:] = [
                    directory for directory in directories
                    if directory not in {DUPLICATES_FOLDER, "Duplicates_Found"}
                ]
                count += len(names)
        self.file_count = count
        self.stat_files.configure(text=str(count))

    def _set_status(self, text, tone):
        colors = {
            "muted": (COLORS["muted"], COLORS["surface_alt"]),
            "success": (COLORS["success"], "#163529"),
            "warning": (COLORS["warning"], "#3A2E17"),
            "danger": (COLORS["danger"], "#3B1F24"),
        }
        foreground, background = colors[tone]
        self.status_pill.configure(text=text.upper(), text_color=foreground, fg_color=background)

    def _log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        self.log_box.configure(state="normal")
        self.log_box.insert("end", f"{timestamp}  {message}\n")
        self.log_box.see("end")
        self.log_box.configure(state="disabled")

    def _set_busy(self, busy):
        self.is_busy = busy
        state = "disabled" if busy else "normal"
        self.browse_button.configure(state=state)
        self.sort_button.configure(state=state)
        self.duplicates_button.configure(state=state)
        if not busy:
            self.progress.set(0)

    def _start_worker(self, title, worker):
        if not self.selected_folder or self.is_busy:
            if not self.selected_folder:
                self._set_status("Select a folder first.", "warning")
            return
        self._set_busy(True)
        self._set_status(title, "warning")
        self._log(f"{title} started.")
        threading.Thread(target=self._run_worker, args=(title, worker), daemon=True).start()

    def _run_worker(self, title, worker):
        try:
            worker()
        except (OSError, PermissionError, ValueError, RuntimeError) as error:
            self.after(0, self._finish_failure, title, error)

    def _finish_failure(self, title, error):
        self._set_busy(False)
        self._set_status(f"{title} stopped", "danger")
        self._log(f"{title} stopped safely: {error}")
        messagebox.showerror(
            f"{title} could not finish",
            f"No files were deleted. Review the activity log and try again.\n\n{error}",
        )

    def sort_files(self):
        self._start_worker("Sorting", self._sort_files_worker)

    def _sort_files_worker(self):
        moved = 0
        errors = 0
        items = sorted(
            (
                item
                for folder in self.selected_folders
                for item in folder.iterdir()
                if item.is_file() and not self._is_quarantine_path(item)
            ),
            key=lambda item: str(item).casefold(),
        )
        total = max(len(items), 1)
        for index, item in enumerate(items, 1):
            category = "Others"
            for name, extensions in CATEGORIES.items():
                if item.suffix.lower() in extensions:
                    category = name
                    break
            type_folder = item.suffix.lower().lstrip(".").upper() or "NO_EXTENSION"
            source_folder = self._source_folder_for(item)
            target = source_folder / category / type_folder
            target.mkdir(parents=True, exist_ok=True)
            destination = self._unique_destination(target / item.name)
            try:
                shutil.move(str(item), str(destination))
                moved += 1
            except OSError as error:
                errors += 1
                self.after(0, self._log, f"Could not move {item.name}: {error}")
            self.after(0, self.progress.set, index / total)
        self.after(0, self._finish_sort, moved, errors)

    def _finish_sort(self, moved, errors):
        self._set_busy(False)
        self.last_action = str(moved)
        self.stat_sorted.configure(text=str(moved))
        self._refresh_file_count()
        self._set_status("Sort complete", "success" if not errors else "warning")
        self._log(f"Sort complete: {moved} moved, {errors} errors.")
        messagebox.showinfo(
            "Sort complete",
            f"{moved} file(s) organized into category/type folders."
            + (f"\n{errors} file(s) could not be moved." if errors else ""),
        )

    def find_duplicates(self):
        self._start_worker("Scanning", self._duplicates_worker)

    def _duplicates_worker(self):
        files = sorted([
            Path(root) / filename
            for source_folder in self.selected_folders
            for root, directories, names in os.walk(source_folder)
            if not self._is_quarantine_path(Path(root))
            for filename in names
        ], key=lambda filepath: str(filepath).casefold())
        hashes = defaultdict(list)
        total = max(len(files), 1)
        for index, filepath in enumerate(files, 1):
            try:
                hashes[self._file_hash(filepath)].append(filepath)
            except OSError as error:
                self.after(0, self._log, f"Could not read {filepath.name}: {error}")
            self.after(0, self.progress.set, index / total)

        moved = 0
        for group in hashes.values():
            for duplicate in group[1:]:
                source_folder = self._source_folder_for(duplicate)
                relative_parent = duplicate.parent.relative_to(source_folder)
                destination_dir = source_folder / DUPLICATES_FOLDER / relative_parent
                destination_dir.mkdir(parents=True, exist_ok=True)
                try:
                    shutil.move(
                        str(duplicate),
                        str(self._unique_destination(destination_dir / duplicate.name)),
                    )
                    moved += 1
                except OSError as error:
                    self.after(0, self._log, f"Could not move duplicate {duplicate.name}: {error}")
        self.after(0, self._finish_duplicates, moved)

    def _finish_duplicates(self, moved):
        self._set_busy(False)
        self.stat_duplicates.configure(text=str(moved))
        self._refresh_file_count()
        self._set_status("Scan complete", "success")
        self._log(
            f"Duplicate scan complete across {len(self.selected_folders)} folder(s): "
            f"{moved} duplicate(s) moved to each source's {DUPLICATES_FOLDER}."
        )
        if moved:
            messagebox.showinfo(
                "Duplicates quarantined",
                f"{moved} exact duplicate(s) moved to the {DUPLICATES_FOLDER} folder inside their source folders.\n"
                "Review that folder before deleting anything.",
            )
        else:
            messagebox.showinfo("No duplicates", "No exact duplicates were found.")

    @staticmethod
    def _is_quarantine_path(path):
        return DUPLICATES_FOLDER in path.parts or "Duplicates_Found" in path.parts

    def _source_folder_for(self, filepath):
        for folder in self.selected_folders:
            try:
                filepath.relative_to(folder)
                return folder
            except ValueError:
                continue
        raise ValueError(f"File is outside the selected folders: {filepath}")

    @staticmethod
    def _file_hash(filepath):
        hasher = hashlib.sha256()
        with filepath.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                hasher.update(chunk)
        return hasher.hexdigest()

    @staticmethod
    def _unique_destination(destination):
        if not destination.exists():
            return destination
        stem, suffix = destination.stem, destination.suffix
        counter = 2
        while True:
            candidate = destination.with_name(f"{stem} ({counter}){suffix}")
            if not candidate.exists():
                return candidate
            counter += 1


if __name__ == "__main__":
    app = FileOrganizerApp()
    app.mainloop()
