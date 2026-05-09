#!/usr/bin/env python3
# --------------------------------------------------------------
# PokeEngine - Desktop UI Window
# --------------------------------------------------------------

import importlib.util
import json
import os
import py_compile
import shutil
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, simpledialog, ttk


APP_DIR = os.path.dirname(os.path.abspath(__file__))
GENERATOR_FILE = os.path.join(APP_DIR, "Pokeengine_core.py")
SETTINGS_FILE = os.path.join(APP_DIR, "pokeengine_settings.json")
BACKUP_DIR = os.path.join(APP_DIR, "generator_backups")


class RoundedButton(tk.Canvas):
    def __init__(self, parent, text, bg, fg, border, radius=8, height=36):
        parent_bg = parent.cget("bg") if hasattr(parent, "cget") else "#ffffff"
        super().__init__(
            parent,
            bg=parent_bg,
            highlightthickness=0,
            borderwidth=0,
            height=height,
            cursor="hand2",
        )
        self.text = text
        self._fill = bg
        self._fg = fg
        self._border = border
        self._radius = radius
        self._font = ("Segoe UI", 10, "bold")
        self.bind("<Configure>", lambda _event: self.redraw())
        self.redraw()

    def configure(self, cnf=None, **kwargs):
        if cnf:
            kwargs.update(cnf)
        redraw = False
        if "bg" in kwargs:
            self._fill = kwargs.pop("bg")
            redraw = True
        if "background" in kwargs:
            self._fill = kwargs.pop("background")
            redraw = True
        if "fg" in kwargs:
            self._fg = kwargs.pop("fg")
            redraw = True
        if "foreground" in kwargs:
            self._fg = kwargs.pop("foreground")
            redraw = True
        if "text" in kwargs:
            self.text = kwargs.pop("text")
            redraw = True
        if "border" in kwargs:
            self._border = kwargs.pop("border")
            redraw = True
        result = super().configure(**kwargs) if kwargs else None
        if redraw:
            self.redraw()
        return result

    config = configure

    def cget(self, option):
        if option in ("bg", "background"):
            return self._fill
        if option in ("fg", "foreground"):
            return self._fg
        if option == "text":
            return self.text
        return super().cget(option)

    def redraw(self):
        self.delete("all")
        width = max(2, self.winfo_width())
        height = max(2, self.winfo_height())
        radius = min(self._radius, width // 2, height // 2)
        x2 = width - 1
        y2 = height - 1

        self.create_rectangle(radius, 1, x2 - radius, y2, fill=self._fill, outline=self._fill)
        self.create_rectangle(1, radius, x2, y2 - radius, fill=self._fill, outline=self._fill)
        self.create_oval(1, 1, 1 + radius * 2, 1 + radius * 2, fill=self._fill, outline=self._fill)
        self.create_oval(x2 - radius * 2, 1, x2, 1 + radius * 2, fill=self._fill, outline=self._fill)
        self.create_oval(1, y2 - radius * 2, 1 + radius * 2, y2, fill=self._fill, outline=self._fill)
        self.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=self._fill, outline=self._fill)
        if self._border != self._fill:
            self.create_arc(1, 1, 1 + radius * 2, 1 + radius * 2, start=90, extent=90, style=tk.ARC, outline=self._border)
            self.create_arc(x2 - radius * 2, 1, x2, 1 + radius * 2, start=0, extent=90, style=tk.ARC, outline=self._border)
            self.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, extent=90, style=tk.ARC, outline=self._border)
            self.create_arc(1, y2 - radius * 2, 1 + radius * 2, y2, start=180, extent=90, style=tk.ARC, outline=self._border)
            self.create_line(1 + radius, 1, x2 - radius, 1, fill=self._border)
            self.create_line(1 + radius, y2, x2 - radius, y2, fill=self._border)
            self.create_line(1, 1 + radius, 1, y2 - radius, fill=self._border)
            self.create_line(x2, 1 + radius, x2, y2 - radius, fill=self._border)
        self.create_text(width / 2, height / 2, text=self.text, fill=self._fg, font=self._font)


class RoundedFrame(tk.Canvas):
    def __init__(self, parent, bg, border=None, radius=10, height=None, padx=0, pady=0, **kwargs):
        parent_bg = parent.cget("bg") if hasattr(parent, "cget") else "#ffffff"
        super().__init__(
            parent,
            bg=parent_bg,
            highlightthickness=0,
            borderwidth=0,
            height=height or 2,
            **kwargs,
        )
        self._fill = bg
        self._border = border or bg
        self._radius = radius
        self._padx = padx
        self._pady = pady
        self.inner = tk.Frame(self, bg=bg, borderwidth=0, highlightthickness=0)
        self._window = self.create_window(padx, pady, anchor="nw", window=self.inner)
        self.bind("<Configure>", lambda _event: self.redraw())
        self.inner.bind("<Configure>", lambda _event: self.sync_height())
        self.redraw()

    def configure(self, cnf=None, **kwargs):
        if cnf:
            kwargs.update(cnf)
        redraw = False
        if "bg" in kwargs:
            self._fill = kwargs.pop("bg")
            self.inner.configure(bg=self._fill)
            redraw = True
        if "background" in kwargs:
            self._fill = kwargs.pop("background")
            self.inner.configure(bg=self._fill)
            redraw = True
        if "border" in kwargs:
            self._border = kwargs.pop("border")
            redraw = True
        result = super().configure(**kwargs) if kwargs else None
        if redraw:
            self.redraw()
        return result

    config = configure

    def cget(self, option):
        if option in ("bg", "background"):
            return self._fill
        if option == "border":
            return self._border
        return super().cget(option)

    def sync_height(self):
        requested = self.inner.winfo_reqheight() + self._pady * 2
        if requested > 2 and int(float(self.cget("height"))) != requested:
            self.configure(height=requested)
        self.redraw()

    def redraw(self):
        self.delete("shape")
        width = max(2, self.winfo_width())
        height = max(2, int(float(self.cget("height"))))
        radius = min(self._radius, width // 2, height // 2)
        x1, y1 = 1, 1
        x2, y2 = width - 1, height - 1
        self.create_rectangle(x1 + radius, y1, x2 - radius, y2, fill=self._fill, outline=self._fill, tags="shape")
        self.create_rectangle(x1, y1 + radius, x2, y2 - radius, fill=self._fill, outline=self._fill, tags="shape")
        self.create_oval(x1, y1, x1 + radius * 2, y1 + radius * 2, fill=self._fill, outline=self._fill, tags="shape")
        self.create_oval(x2 - radius * 2, y1, x2, y1 + radius * 2, fill=self._fill, outline=self._fill, tags="shape")
        self.create_oval(x1, y2 - radius * 2, x1 + radius * 2, y2, fill=self._fill, outline=self._fill, tags="shape")
        self.create_oval(x2 - radius * 2, y2 - radius * 2, x2, y2, fill=self._fill, outline=self._fill, tags="shape")
        if self._border != self._fill:
            self.create_arc(x1, y1, x1 + radius * 2, y1 + radius * 2, start=90, extent=90, style=tk.ARC, outline=self._border, tags="shape")
            self.create_arc(x2 - radius * 2, y1, x2, y1 + radius * 2, start=0, extent=90, style=tk.ARC, outline=self._border, tags="shape")
            self.create_arc(x2 - radius * 2, y2 - radius * 2, x2, y2, start=270, extent=90, style=tk.ARC, outline=self._border, tags="shape")
            self.create_arc(x1, y2 - radius * 2, x1 + radius * 2, y2, start=180, extent=90, style=tk.ARC, outline=self._border, tags="shape")
            self.create_line(x1 + radius, y1, x2 - radius, y1, fill=self._border, tags="shape")
            self.create_line(x1 + radius, y2, x2 - radius, y2, fill=self._border, tags="shape")
            self.create_line(x1, y1 + radius, x1, y2 - radius, fill=self._border, tags="shape")
            self.create_line(x2, y1 + radius, x2, y2 - radius, fill=self._border, tags="shape")
        self.coords(self._window, self._padx, self._pady)
        self.itemconfigure(self._window, width=max(1, width - self._padx * 2))
        self.itemconfigure(self._window, height=max(1, height - self._pady * 2))
        self.tag_lower("shape")


def load_generator_module():
    spec = importlib.util.spec_from_file_location("Pokeengine_core", GENERATOR_FILE)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Could not load generator script: {GENERATOR_FILE}")

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


class PokeEngineWindow:
    def __init__(self, root):
        self.root = root
        self.root.title("PokeEngine - Project Builder")
        self.root.geometry("1160x820")
        self.root.minsize(980, 680)
        self.root.option_add("*Font", ("Segoe UI", 10))

        self.generator_module = self.load_generator_safely()
        self.settings = self.load_settings()

        default_path = getattr(self.generator_module, "DEFAULT_PROJECT_PATH", os.path.join(os.path.expanduser("~"), "Desktop", "Pokemon_Game"))
        default_name = getattr(self.generator_module, "DEFAULT_PROJECT_NAME", os.path.basename(default_path))
        default_destination = getattr(self.generator_module, "DEFAULT_PROJECT_DESTINATION", os.path.dirname(default_path))
        unity_version = getattr(self.generator_module, "UNITY_EDITOR_VERSION", "2022.3.62f3")

        self.unity_version = tk.StringVar(value=unity_version)
        self.project_name = tk.StringVar(value=self.settings.get("project_name", default_name))
        self.project_destination = tk.StringVar(value=self.settings.get("project_destination", default_destination))
        self.project_path = tk.StringVar(value=self.get_project_path())
        self.status_text = tk.StringVar(value="Ready")
        self.animation_jobs = {}
        self.status_pulse_step = 0
        self.status_accent = None
        self.sidebar_tabs = {}

        try:
            self.root.attributes("-alpha", 0.0)
            self.fade_supported = True
        except tk.TclError:
            self.fade_supported = False

        self.setup_theme()
        self.setup_ui()
        self.start_ui_animations()
        self.log("PokeEngine UI ready.")
        self.log(f"Generator script: {GENERATOR_FILE}")

    def setup_theme(self):
        self.colors = {
            "app": "#f6eef5",
            "panel": "#ffffff",
            "panel2": "#fff9fd",
            "panel3": "#f0edf3",
            "sidebar": "#ffffff",
            "header": "#111111",
            "text": "#171717",
            "muted": "#5a5860",
            "subtle": "#817d89",
            "border": "#d8d0d9",
            "accent": "#f0a800",
            "accent_dark": "#cf8300",
            "red": "#e4003a",
            "red_dark": "#b8002d",
            "yellow": "#1e9fe8",
            "yellow2": "#61c6ff",
            "yellow3": "#0f7fc4",
            "blue_text": "#064b73",
            "blue_card": "#7ed3ff",
            "blue_card_hover": "#aee6ff",
            "blue_border": "#1675aa",
            "black": "#101010",
            "success": "#19b36b",
            "success_dark": "#0c8f52",
            "danger": "#e4003a",
            "danger_dark": "#b8002d",
            "input": "#fffdf8",
            "log_bg": "#262626",
            "log_fg": "#ffffff",
        }
        self.root.configure(bg=self.colors["app"])

        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TNotebook", background=self.colors["app"], borderwidth=0)
        style.configure(
            "TNotebook.Tab",
            background=self.colors["panel3"],
            foreground=self.colors["muted"],
            padding=(22, 11),
            font=("Segoe UI", 10, "bold"),
            borderwidth=0,
        )
        style.map(
            "TNotebook.Tab",
            background=[("selected", self.colors["panel"])],
            foreground=[("selected", self.colors["red"])],
        )
        style.configure(
            "TCombobox",
            fieldbackground=self.colors["input"],
            background=self.colors["panel3"],
            foreground=self.colors["text"],
            arrowcolor=self.colors["text"],
            padding=6,
        )

    def setup_ui(self):
        root_frame = tk.Frame(self.root, bg=self.colors["app"])
        root_frame.pack(fill=tk.BOTH, expand=True)

        sidebar = tk.Frame(root_frame, bg=self.colors["sidebar"], width=342)
        sidebar.pack(side=tk.LEFT, fill=tk.Y)
        sidebar.pack_propagate(False)

        hero = tk.Frame(sidebar, bg=self.colors["sidebar"])
        hero.pack(fill=tk.X, padx=18, pady=(14, 6))
        tk.Label(
            hero,
            text="PokeEngine",
            fg=self.colors["black"],
            bg=self.colors["sidebar"],
            font=("Segoe UI Black", 23, "bold"),
        ).pack(side=tk.LEFT)
        tk.Label(
            hero,
            text="ENGINE TOOLS",
            fg=self.colors["muted"],
            bg=self.colors["sidebar"],
            font=("Segoe UI", 9, "bold"),
        ).pack(side=tk.LEFT, padx=(10, 0), pady=(16, 0))

        sidebar_body = tk.Frame(sidebar, bg=self.colors["sidebar"])
        sidebar_body.pack(fill=tk.BOTH, expand=True, padx=18, pady=(0, 14))

        self.bag_row(sidebar_body, "Logs", "Console", "Live", "L").pack(fill=tk.X, pady=5)
        self.bag_row(sidebar_body, "Generator Patch", "Core Script", "Backup", "G").pack(fill=tk.X, pady=5)
        self.bag_row(sidebar_body, "Settings", "Project", "Saved", "S").pack(fill=tk.X, pady=5)

        path_card = RoundedFrame(sidebar_body, "#f8f8f8", self.colors["border"], radius=10, padx=0, pady=0)
        path_card.pack(fill=tk.X, pady=(20, 8))
        tk.Label(path_card.inner, text="PROJECT PATH", fg=self.colors["muted"], bg="#f8f8f8", font=("Segoe UI", 8, "bold")).pack(anchor="w", padx=14, pady=(10, 2))
        tk.Label(path_card.inner, textvariable=self.project_path, fg=self.colors["text"], bg="#f8f8f8", font=("Segoe UI", 9), wraplength=280, justify=tk.LEFT).pack(anchor="w", padx=14, pady=(0, 12))

        self.add_button(sidebar_body, "Browse Destination", self.browse_destination, "#f2f2f2", "#e6e6e6").pack(fill=tk.X, pady=(6, 8), ipady=8)
        self.add_button(sidebar_body, "Generate Full RPG Prototype", self.generate_project, self.colors["black"], "#303030", "white").pack(fill=tk.X, pady=(0, 14), ipady=11)

        status_card = RoundedFrame(sidebar_body, self.colors["black"], self.colors["black"], radius=14, padx=14, pady=3)
        status_card.pack(fill=tk.X, side=tk.BOTTOM, pady=(10, 0))
        self.status_accent = tk.Frame(status_card.inner, bg=self.colors["yellow"], height=5)
        self.status_accent.pack(fill=tk.X)
        tk.Label(status_card.inner, textvariable=self.status_text, fg="white", bg=self.colors["black"], font=("Segoe UI", 10, "bold"), justify=tk.LEFT, wraplength=255).pack(anchor="w", padx=0, pady=12)

        main = tk.Frame(root_frame, bg=self.colors["yellow"])
        main.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.tab_buttons = {}
        self.tab_frames = {}
        self.active_tab = None
        self.tab_content = tk.Frame(main, bg=self.colors["yellow"])
        self.tab_content.pack(fill=tk.BOTH, expand=True, padx=26, pady=18)

        self.patch_frame = self.add_tab("Generator Patch")
        self.settings_frame = self.add_tab("Settings")
        self.logs_frame = self.add_tab("Logs", bg=self.colors["log_bg"])

        self.setup_patch_tab()
        self.setup_settings_tab()
        self.setup_logs_tab()
        self.select_tab("Logs")

    def add_tab(self, title, bg=None):
        frame = tk.Frame(self.tab_content, bg=bg or self.colors["yellow"])
        frame.place(relx=0, rely=0, relwidth=1, relheight=1)
        self.tab_frames[title] = frame

        return frame

    def select_tab(self, title):
        if title not in self.tab_frames:
            return
        self.active_tab = title
        self.tab_frames[title].tkraise()
        for name in self.sidebar_tabs:
            self.update_sidebar_tab_visual(name, selected=(name == title))

    def set_tab_hover(self, title, hovering):
        if title == self.active_tab or title not in self.sidebar_tabs:
            return
        parts = self.sidebar_tabs[title]
        target = "#f3f3f3" if hovering else "white"
        self.set_sidebar_row_bg(parts, target)
        parts["title"].configure(fg=self.colors["black"])

    def update_sidebar_tab_visual(self, title, selected=False):
        parts = self.sidebar_tabs[title]
        bg = self.colors["black"] if selected else "white"
        fg = "white" if selected else self.colors["black"]
        muted = "#dbeafe" if selected else self.colors["muted"]
        value_fg = self.colors["yellow2"] if selected else self.colors["black"]
        icon_bg = self.colors["yellow2"] if selected else "#f3f1f7"
        row_widgets = (parts["row"], parts["row_content"], parts["text_frame"], parts["title"], parts["subtitle"], parts["value"])
        if selected:
            for widget in row_widgets:
                self.set_color_now(widget, "bg", bg)
        else:
            for widget in row_widgets:
                self.animate_color(widget, "bg", widget.cget("bg"), bg, 9)
        parts["title"].configure(fg=fg)
        parts["subtitle"].configure(fg=muted)
        parts["value"].configure(fg=value_fg, padx=0, pady=0)
        parts["icon"].configure(bg=bg)
        parts["icon"].itemconfigure(parts["icon_circle"], fill=icon_bg)
        parts["icon"].itemconfigure(parts["icon_text"], fill=self.colors["black"])

    def add_sidebar_label(self, parent, text):
        tk.Label(
            parent,
            text=text,
            fg=self.colors["muted"],
            bg=self.colors["sidebar"],
            font=("Segoe UI", 9, "bold"),
        ).pack(anchor="w", pady=(0, 8))

    def status_chip(self, parent, text):
        chip = tk.Frame(parent, bg="#bdeaff", highlightthickness=0)
        tk.Label(
            chip,
            text=text,
            fg="#06202b",
            bg="#bdeaff",
            font=("Segoe UI", 9, "bold"),
            padx=12,
            pady=4,
        ).pack()
        return chip

    def bag_row(self, parent, title, subtitle, value, icon_text=None):
        row = RoundedFrame(parent, "white", "#d5cbd5", radius=14, height=62, padx=14, pady=3, cursor="hand2")
        row_content = row.inner
        icon = tk.Canvas(row_content, width=44, height=44, bg="white", highlightthickness=0)
        icon.pack(side=tk.LEFT, padx=(0, 6), pady=5)
        icon_circle = icon.create_oval(7, 7, 37, 37, fill="#f3f1f7", outline="#d7d1dc", width=2)
        icon_text_item = icon.create_text(22, 22, text=icon_text or title[:1], fill=self.colors["black"], font=("Segoe UI", 14, "bold"))
        text_frame = tk.Frame(row_content, bg="white")
        text_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        title_label = tk.Label(text_frame, text=title, fg=self.colors["black"], bg="white", font=("Segoe UI", 11, "bold"))
        title_label.pack(anchor="w", pady=(6, 0))
        subtitle_label = tk.Label(text_frame, text=subtitle, fg=self.colors["muted"], bg="white", font=("Segoe UI", 8))
        subtitle_label.pack(anchor="w")
        value_label = tk.Label(row_content, text=value, fg=self.colors["black"], bg="white", font=("Segoe UI", 9, "bold"), padx=0, pady=0, borderwidth=0, highlightthickness=0)
        value_label.pack(side=tk.RIGHT, padx=(8, 0))
        self.sidebar_tabs[title] = {
            "row": row,
            "row_content": row_content,
            "icon": icon,
            "icon_circle": icon_circle,
            "icon_text": icon_text_item,
            "text_frame": text_frame,
            "title": title_label,
            "subtitle": subtitle_label,
            "value": value_label,
        }

        def enter(_event):
            self.set_tab_hover(title, True)

        def leave(_event):
            pointer_x = row.winfo_pointerx()
            pointer_y = row.winfo_pointery()
            inside_x = row.winfo_rootx() <= pointer_x <= row.winfo_rootx() + row.winfo_width()
            inside_y = row.winfo_rooty() <= pointer_y <= row.winfo_rooty() + row.winfo_height()
            if inside_x and inside_y:
                return
            self.set_tab_hover(title, False)

        def click(_event):
            self.select_tab(title)

        for widget in row_content.winfo_children() + [row, row_content, text_frame, title_label, subtitle_label, value_label, icon]:
            widget.bind("<Enter>", enter)
            widget.bind("<Leave>", leave)
            widget.bind("<Button-1>", click)
        return row

    def set_sidebar_row_bg(self, parts, color):
        for widget in (parts["row"], parts["row_content"], parts["text_frame"]):
            self.animate_color(widget, "bg", widget.cget("bg"), color, 8)
        for label in (parts["title"], parts["subtitle"], parts["value"]):
            self.animate_color(label, "bg", label.cget("bg"), color, 8)
        try:
            parts["icon"].configure(bg=color)
        except tk.TclError:
            pass
        if color == self.colors["black"]:
            parts["icon"].itemconfigure(parts["icon_circle"], fill=self.colors["yellow2"])
        elif color == "white":
            parts["icon"].itemconfigure(parts["icon_circle"], fill="#f3f1f7")

    def add_button(self, parent, text, command, bg=None, active_bg=None, fg=None):
        bg = bg or self.colors["panel3"]
        active_bg = active_bg or self.colors["border"]
        button = RoundedButton(parent, text, bg, fg or self.colors["text"], self.colors["border"], radius=10, height=36)
        press_bg = self.mix_color(active_bg, "#000000", 0.08)
        button.bind("<Enter>", lambda _event: self.animate_color(button, "bg", button.cget("bg"), active_bg, 7))
        button.bind("<Leave>", lambda _event: self.animate_color(button, "bg", button.cget("bg"), bg, 8))
        button.bind("<ButtonPress-1>", lambda _event: self.animate_color(button, "bg", button.cget("bg"), press_bg, 3))

        def release(event):
            self.animate_color(button, "bg", button.cget("bg"), active_bg, 5)
            if 0 <= event.x <= button.winfo_width() and 0 <= event.y <= button.winfo_height():
                command()

        button.bind("<ButtonRelease-1>", release)
        return button

    def setup_patch_tab(self):
        body = self.content_frame(self.patch_frame)
        self.heading(body, "Generator Script Patch")
        self.copy(
            body,
            "Paste a complete replacement for `Pokeengine_core.py` below. "
            "When applied, the UI backs up the old generator first, validates the new code, then reloads it.",
        )

        actions = tk.Frame(body, bg=self.colors["yellow"])
        actions.pack(fill=tk.X, pady=(14, 10))
        self.add_button(actions, "Load Current Generator", self.load_current_generator_into_patch_box).pack(side=tk.LEFT, ipadx=10, ipady=6)
        self.add_button(actions, "Apply Replacement + Backup", self.apply_generator_replacement, self.colors["red"], self.colors["red_dark"], "white").pack(
            side=tk.LEFT, padx=10, ipadx=10, ipady=6
        )
        self.add_button(actions, "Clear Box", self.clear_patch_box).pack(side=tk.LEFT, ipadx=10, ipady=6)

        self.patch_text = tk.Text(
            body,
            bg="#e8f8ff",
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief=tk.FLAT,
            wrap=tk.NONE,
            undo=True,
            font=("Consolas", 10),
            padx=12,
            pady=12,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )
        self.patch_text.pack(fill=tk.BOTH, expand=True)

    def setup_settings_tab(self):
        body = self.content_frame(self.settings_frame)
        self.heading(body, "Settings")

        self.form_label(body, "Project Name")
        self.entry(body, self.project_name).pack(fill=tk.X, ipady=7, pady=(4, 14))

        self.form_label(body, "Destination Folder")
        self.entry(body, self.project_destination).pack(fill=tk.X, ipady=7, pady=(4, 8))
        self.add_button(body, "Browse Destination", self.browse_destination).pack(anchor="w", ipadx=10, ipady=6, pady=(0, 18))

        self.add_button(body, "Save Settings", self.save_settings, self.colors["success"], self.colors["success_dark"]).pack(
            anchor="w", ipadx=14, ipady=7
        )

    def setup_logs_tab(self):
        wrapper = tk.Frame(self.logs_frame, bg=self.colors["yellow"])
        wrapper.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        self.heading(wrapper, "Logs")
        log_panel = RoundedFrame(wrapper, self.colors["black"], self.colors["black"], radius=10, padx=6, pady=6)
        log_panel.pack(fill=tk.BOTH, expand=True, pady=(10, 0))
        self.log_box = tk.Text(
            log_panel.inner,
            bg=self.colors["log_bg"],
            fg=self.colors["log_fg"],
            insertbackground=self.colors["log_fg"],
            relief=tk.FLAT,
            font=("Consolas", 10),
            wrap=tk.WORD,
            padx=14,
            pady=14,
        )
        self.log_box.pack(fill=tk.BOTH, expand=True)

    def content_frame(self, parent):
        frame = tk.Frame(parent, bg=self.colors["yellow"])
        frame.pack(fill=tk.BOTH, expand=True, padx=0, pady=0)
        return frame

    def heading(self, parent, text):
        tk.Label(
            parent,
            text=text,
            fg=self.colors["text"],
            bg=self.colors["yellow"],
            font=("Segoe UI Black", 22, "bold"),
        ).pack(anchor="w", pady=(0, 8))
        tk.Frame(parent, bg=self.colors["black"], height=5, width=120).pack(anchor="w", pady=(0, 10))

    def copy(self, parent, text):
        tk.Label(
            parent,
            text=text,
            fg=self.colors["muted"],
            bg=self.colors["yellow"],
            font=("Segoe UI", 10),
            justify=tk.LEFT,
            wraplength=760,
        ).pack(anchor="w")

    def card(self, parent, title, text, accent=None):
        accent = accent or self.colors["accent"]
        frame = RoundedFrame(parent, self.colors["blue_card"], self.colors["blue_border"], radius=10, padx=0, pady=0)
        frame.pack(fill=tk.X, pady=7)
        accent_bar = tk.Frame(frame.inner, bg=accent, width=9)
        accent_bar.pack(side=tk.LEFT, fill=tk.Y)
        content = tk.Frame(frame.inner, bg=self.colors["blue_card"])
        content.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        title_label = tk.Label(content, text=title, fg=self.colors["text"], bg=self.colors["blue_card"], font=("Segoe UI", 13, "bold"))
        title_label.pack(
            anchor="w", padx=16, pady=(13, 2)
        )
        body_label = tk.Label(content, text=text, fg=self.colors["blue_text"], bg=self.colors["blue_card"], font=("Segoe UI", 10), justify=tk.LEFT, wraplength=760)
        body_label.pack(
            anchor="w", padx=16, pady=(0, 13)
        )
        animated_parts = (frame, content, title_label, body_label)

        def set_card_bg(color):
            for part in animated_parts:
                self.animate_color(part, "bg", part.cget("bg"), color, 8)

        def on_enter(_event):
            accent_bar.configure(width=14)
            set_card_bg(self.colors["blue_card_hover"])

        def on_leave(_event):
            pointer_x = frame.winfo_pointerx()
            pointer_y = frame.winfo_pointery()
            inside_x = frame.winfo_rootx() <= pointer_x <= frame.winfo_rootx() + frame.winfo_width()
            inside_y = frame.winfo_rooty() <= pointer_y <= frame.winfo_rooty() + frame.winfo_height()
            if inside_x and inside_y:
                return
            accent_bar.configure(width=9)
            set_card_bg(self.colors["blue_card"])

        for widget in (frame, content, title_label, body_label, accent_bar):
            widget.bind("<Enter>", on_enter)
            widget.bind("<Leave>", on_leave)

    def form_label(self, parent, text):
        tk.Label(parent, text=text, fg=self.colors["text"], bg=self.colors["yellow"], font=("Segoe UI", 10, "bold")).pack(anchor="w")

    def entry(self, parent, variable):
        return tk.Entry(
            parent,
            textvariable=variable,
            bg=self.colors["input"],
            fg=self.colors["text"],
            insertbackground=self.colors["text"],
            relief=tk.FLAT,
            highlightbackground=self.colors["border"],
            highlightthickness=1,
        )

    def start_ui_animations(self):
        if self.fade_supported:
            self.fade_in_window()
        self.animate_status_pulse()

    def fade_in_window(self, step=0):
        if not self.fade_supported:
            return
        try:
            alpha = min(1.0, step / 12)
            self.root.attributes("-alpha", alpha)
            if step < 12:
                self.root.after(18, lambda: self.fade_in_window(step + 1))
        except tk.TclError:
            self.fade_supported = False

    def animate_status_pulse(self):
        if self.status_accent is None:
            return
        try:
            phase = (self.status_pulse_step % 40) / 39
            triangle = 1 - abs(phase * 2 - 1)
            color = self.mix_color(self.colors["yellow"], self.colors["red"], triangle * 0.28)
            self.status_accent.configure(bg=color)
            self.status_pulse_step += 1
            self.root.after(80, self.animate_status_pulse)
        except tk.TclError:
            return

    def animate_color(self, widget, option, start, end, steps=8, delay=16):
        key = (str(widget), option)
        old_job = self.animation_jobs.pop(key, None)
        if old_job is not None:
            try:
                self.root.after_cancel(old_job)
            except tk.TclError:
                pass

        try:
            start_rgb = self.color_to_rgb(start)
            end_rgb = self.color_to_rgb(end)
        except tk.TclError:
            widget.configure(**{option: end})
            return

        def tick(index):
            try:
                amount = index / max(1, steps)
                eased = 1 - (1 - amount) * (1 - amount)
                color = self.rgb_to_hex(tuple(
                    round(start_rgb[channel] + (end_rgb[channel] - start_rgb[channel]) * eased)
                    for channel in range(3)
                ))
                widget.configure(**{option: color})
                if index < steps:
                    self.animation_jobs[key] = self.root.after(delay, lambda: tick(index + 1))
                else:
                    self.animation_jobs.pop(key, None)
            except tk.TclError:
                self.animation_jobs.pop(key, None)

        tick(0)

    def set_color_now(self, widget, option, color):
        key = (str(widget), option)
        old_job = self.animation_jobs.pop(key, None)
        if old_job is not None:
            try:
                self.root.after_cancel(old_job)
            except tk.TclError:
                pass
        try:
            widget.configure(**{option: color})
        except tk.TclError:
            pass

    def color_to_rgb(self, color):
        red, green, blue = self.root.winfo_rgb(color)
        return (red // 257, green // 257, blue // 257)

    def rgb_to_hex(self, rgb):
        return "#{:02x}{:02x}{:02x}".format(*rgb)

    def mix_color(self, first, second, amount):
        amount = max(0.0, min(1.0, amount))
        first_rgb = self.color_to_rgb(first)
        second_rgb = self.color_to_rgb(second)
        return self.rgb_to_hex(tuple(
            round(first_rgb[channel] + (second_rgb[channel] - first_rgb[channel]) * amount)
            for channel in range(3)
        ))

    def load_generator_safely(self):
        try:
            return load_generator_module()
        except Exception as e:
            messagebox.showerror("Generator Load Error", str(e))
            raise

    def load_settings(self):
        if not os.path.exists(SETTINGS_FILE):
            return {}
        try:
            with open(SETTINGS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            return data if isinstance(data, dict) else {}
        except Exception as e:
            messagebox.showwarning("Settings Warning", f"Could not load saved settings: {e}")
            return {}

    def save_settings(self):
        self.project_path.set(self.get_project_path())
        data = {
            "project_name": self.project_name.get().strip(),
            "project_destination": self.project_destination.get().strip(),
        }
        try:
            with open(SETTINGS_FILE, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
        except Exception as e:
            messagebox.showerror("Settings Error", f"Could not save settings: {e}")
            return

        self.log(f"Settings saved: {SETTINGS_FILE}")
        messagebox.showinfo("Settings Saved", "Settings saved successfully.")

    def get_project_path(self):
        destination = self.project_destination.get().strip() if hasattr(self, "project_destination") else ""
        project_name = self.project_name.get().strip() if hasattr(self, "project_name") else ""
        return os.path.join(destination, project_name)

    def browse_destination(self):
        path = filedialog.askdirectory(title="Choose Project Destination")
        if not path:
            return
        self.project_destination.set(path)
        self.project_path.set(self.get_project_path())
        self.log(f"Destination set: {path}")

    def generate_project(self):
        name = simpledialog.askstring(
            "Project Name",
            "Enter a project name:",
            initialvalue=self.project_name.get().strip(),
            parent=self.root,
        )
        if name is None:
            self.log("Generation cancelled.")
            return
        name = name.strip()
        if not name:
            messagebox.showwarning("Project Name Needed", "Please enter a project name.")
            return

        self.project_name.set(name)
        self.project_path.set(self.get_project_path())
        self.save_settings()

        try:
            self.generator_module = load_generator_module()
            builder = self.generator_module.PokemonProjectBuilder(logger=self.log)
            builder.generate(self.project_path.get())
        except Exception as e:
            self.log(f"Generation failed: {e}")
            messagebox.showerror("Generation Error", str(e))
            return

        self.log(f"Generated project: {self.project_path.get()}")
        messagebox.showinfo("Generation Complete", "Full prototype project generated.")

    def load_current_generator_into_patch_box(self):
        try:
            with open(GENERATOR_FILE, "r", encoding="utf-8") as f:
                code = f.read()
        except Exception as e:
            messagebox.showerror("Patch Error", f"Could not read generator script: {e}")
            return

        self.patch_text.delete("1.0", tk.END)
        self.patch_text.insert("1.0", code)
        self.log("Loaded current generator into patch editor.")

    def clear_patch_box(self):
        self.patch_text.delete("1.0", tk.END)

    def show_logs(self):
        self.select_tab("Logs")

    def apply_generator_replacement(self):
        self.show_logs()
        self.log("Patch requested. Validating replacement generator code...")
        new_code = self.patch_text.get("1.0", tk.END).strip()
        if not new_code:
            messagebox.showwarning("Patch Empty", "Paste replacement generator code first.")
            self.log("Patch cancelled: patch box is empty.")
            return

        if "class PokemonProjectBuilder" not in new_code:
            messagebox.showerror("Patch Error", "Replacement code must define class PokemonProjectBuilder.")
            self.log("Patch rejected: missing PokemonProjectBuilder class.")
            return

        try:
            compile(new_code, GENERATOR_FILE, "exec")
        except SyntaxError as e:
            messagebox.showerror("Syntax Error", f"Replacement code has a syntax error:\n{e}")
            self.log(f"Patch rejected: syntax error at line {e.lineno}.")
            return

        os.makedirs(BACKUP_DIR, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = os.path.join(BACKUP_DIR, f"Pokeengine_core_{timestamp}.py")

        try:
            shutil.copy2(GENERATOR_FILE, backup_path)
            self.log(f"Backup created: {backup_path}")
            with open(GENERATOR_FILE, "w", encoding="utf-8") as f:
                f.write(new_code.rstrip() + "\n")
            py_compile.compile(GENERATOR_FILE, doraise=True)
            self.generator_module = load_generator_module()
            if not hasattr(self.generator_module, "PokemonProjectBuilder"):
                raise RuntimeError("Replacement generator does not expose PokemonProjectBuilder.")
        except Exception as e:
            if os.path.exists(backup_path):
                shutil.copy2(backup_path, GENERATOR_FILE)
            messagebox.showerror("Patch Failed", f"Generator was restored from backup.\n\n{e}")
            self.log(f"Patch failed; restored backup: {backup_path}")
            return

        self.log(f"Generator replaced. Backup saved: {backup_path}")
        messagebox.showinfo("Patch Applied", f"Generator replaced successfully.\n\nBackup:\n{backup_path}")

    def log(self, message):
        timestamp = datetime.now().strftime("%H:%M:%S")
        line = f"[{timestamp}] {message}\n"
        if hasattr(self, "log_box"):
            self.log_box.insert(tk.END, line)
            self.log_box.see(tk.END)
            if hasattr(self, "status_text"):
                self.status_text.set(message)
            self.root.update_idletasks()
        else:
            print(line, end="")


if __name__ == "__main__":
    root = tk.Tk()
    app = PokeEngineWindow(root)
    root.mainloop()
