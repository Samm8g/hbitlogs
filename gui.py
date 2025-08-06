

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, Gdk
from db import list_hbits, add_hbit, log_hbit, show_stats, remove_hbit

class HBitLogsWindow(Gtk.ApplicationWindow):
    def __init__(self, app):
        Gtk.ApplicationWindow.__init__(self, application=app)
        self.set_title("H-Bit Logs")
        self.set_default_size(400, 300)

        self.header_bar = Gtk.HeaderBar()
        self.set_titlebar(self.header_bar)

        self.add_button = Gtk.Button(label="Add")
        self.header_bar.pack_start(self.add_button)
        self.add_button.connect("clicked", self.on_add_clicked)

        self.box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_child(self.box)

        self.scrolled_window = Gtk.ScrolledWindow()
        self.scrolled_window.set_hexpand(True)
        self.scrolled_window.set_vexpand(True)
        self.box.append(self.scrolled_window)

        self.list_box = Gtk.ListBox()
        self.list_box.set_selection_mode(Gtk.SelectionMode.SINGLE)
        self.scrolled_window.set_child(self.list_box)

        self.action_bar = Gtk.ActionBar()
        self.box.append(self.action_bar)

        self.log_button = Gtk.Button(label="Log")
        self.stats_button = Gtk.Button(label="Stats")
        self.remove_button = Gtk.Button(label="Remove")

        self.action_bar.pack_start(self.log_button)
        self.action_bar.pack_start(self.stats_button)
        self.action_bar.pack_start(self.remove_button)

        self.log_button.connect("clicked", self.on_log_clicked)
        self.stats_button.connect("clicked", self.on_stats_clicked)
        self.remove_button.connect("clicked", self.on_remove_clicked)

        self.populate_habit_list()
        self.load_css()

    def populate_habit_list(self):
        for child in self.list_box.get_rows():
            self.list_box.remove(child)

        habits = list_hbits()
        if habits:
            for name, created in habits:
                row = Gtk.ListBoxRow()
                grid = Gtk.Grid()
                grid.set_column_spacing(10)
                row.set_child(grid)

                name_label = Gtk.Label(label=name, xalign=0)
                created_label = Gtk.Label(label=f"(since {created})", xalign=1)
                grid.attach(name_label, 0, 0, 1, 1)
                grid.attach(created_label, 1, 0, 1, 1)

                self.list_box.append(row)

    def on_add_clicked(self, widget):
        dialog = Gtk.Dialog(title="Add Habit", transient_for=self, flags=0)
        dialog.add_buttons("Cancel", Gtk.ResponseType.CANCEL, "OK", Gtk.ResponseType.OK)

        entry = Gtk.Entry()
        entry.set_placeholder_text("Enter habit name")
        box = dialog.get_content_area()
        box.append(entry)
        dialog.show()

        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            name = entry.get_text()
            if name:
                status = add_hbit(name)
                if status == "added":
                    self.populate_habit_list()
                    self.show_info(f"✅ Added habit: {name}")
                elif status == "already_exists":
                    self.show_info(f"⚠️ Habit already exists: {name}")
        dialog.destroy()

    def on_log_clicked(self, widget):
        row = self.list_box.get_selected_row()
        if row:
            grid = row.get_child()
            name_label = grid.get_child_at(0, 0)
            name = name_label.get_label()
            status = log_hbit(name)
            if status == "logged":
                self.show_info(f"🗓️ Logged {name} for today!")
            elif status == "already_logged":
                self.show_info(f"⏱️ Already logged today for: {name}")
            elif status == "not_found":
                self.show_info(f"⚠️ Habit not found: {name}")

    def on_stats_clicked(self, widget):
        row = self.list_box.get_selected_row()
        if row:
            grid = row.get_child()
            name_label = grid.get_child_at(0, 0)
            name = name_label.get_label()
            total, last = show_stats(name)
            if total is not None:
                self.show_info(f"📊 Stats for '{name}':\n"
                               f" - Total logged: {total} times\n"
                               f" - Last entry : {last if last else 'Never'}")
            else:
                self.show_info(f"⚠️ Habit not found: {name}")

    def on_remove_clicked(self, widget):
        row = self.list_box.get_selected_row()
        if row:
            grid = row.get_child()
            name_label = grid.get_child_at(0, 0)
            name = name_label.get_label()
            dialog = Gtk.MessageDialog(transient_for=self, modal=True, message_type=Gtk.MessageType.QUESTION,
                buttons=Gtk.ButtonsType.YES_NO, text=f"Are you sure you want to remove {name}?")
            response = dialog.run()
            if response == Gtk.ResponseType.YES:
                status = remove_hbit(name)
                if status == "removed":
                    self.populate_habit_list()
                    self.show_info(f"❌ Removed habit: {name}")
                elif status == "not_found":
                    self.show_info(f"⚠️ Habit not found: {name}")
            dialog.destroy()

    def show_info(self, message):
        dialog = Gtk.MessageDialog(transient_for=self, modal=True, message_type=Gtk.MessageType.INFO,
            buttons=Gtk.ButtonsType.OK, text=message)
        dialog.run()
        dialog.destroy()

    def load_css(self):
        css_provider = Gtk.CssProvider()
        try:
            css_provider.load_from_path("style.css")
            Gtk.StyleContext.add_provider_for_display(Gdk.Display.get_default(), css_provider,
                                                     Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
        except Exception as e:
            print(f"Error loading CSS: {e}")

class HBitLogsApplication(Gtk.Application):
    def __init__(self):
        Gtk.Application.__init__(self, application_id="org.hbitlogs.HBitLogs",
                                 flags=0)
        self.connect("activate", self.on_activate)

    def on_activate(self, app):
        win = HBitLogsWindow(app)
        win.present()

if __name__ == "__main__":
    app = HBitLogsApplication()
    app.run()
