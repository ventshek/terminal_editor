import os
import gi
gi.require_version("Gtk", "3.0")
gi.require_version('Vte', '2.91')
from gi.repository import Gtk, GObject, GLib, Vte

# Gobject VTE entry.
GObject.type_register(Vte.Terminal)

# Sets dark theme.
settings = Gtk.Settings.get_default()
settings.set_property("gtk-application-prefer-dark-theme", True)

class Handler:

    def on_destroy(self, *args):
        Gtk.main_quit()

    def on_button_clicked(self, button):
        buffer = text_view.get_buffer()
        start, end = buffer.get_bounds()
        script = buffer.get_text(start, end, False)
        with open("/tmp/temp_script.sh", "w", encoding="utf-8") as script_file:
            script_file.write(script)
            script_file.write("\nbash\n")
        os.chmod("/tmp/temp_script.sh", 0o755)
        terminal.spawn_sync(
            Vte.PtyFlags.DEFAULT,
            os.environ['HOME'],
            ["/bin/bash", "-c", "/tmp/temp_script.sh"],
            [],
            GLib.SpawnFlags.DO_NOT_REAP_CHILD,
            None,
            None,
        )

    def on_open_activate(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Please choose a file",
            parent=builder.get_object("main_window"),
            action=Gtk.FileChooserAction.OPEN,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OPEN, Gtk.ResponseType.OK)
        )
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            with open(filename, "r", encoding="utf-8") as file:
                text = file.read()
            buffer = text_view.get_buffer()
            buffer.set_text(text)
        dialog.destroy()

    def on_save_activate(self, button):
        dialog = Gtk.FileChooserDialog(
            title="Save File",
            parent=builder.get_object("main_window"),
            action=Gtk.FileChooserAction.SAVE,
            buttons=(Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_SAVE, Gtk.ResponseType.OK)
        )
        filter_text = Gtk.FileFilter()
        filter_text.set_name("Text files")
        filter_text.add_mime_type("text/plain")
        dialog.add_filter(filter_text)
        response = dialog.run()
        if response == Gtk.ResponseType.OK:
            filename = dialog.get_filename()
            buffer = text_view.get_buffer()
            start_iter, end_iter = buffer.get_bounds()
            text = buffer.get_text(start_iter, end_iter, False)
            with open(filename, "w", encoding="utf-8") as file:
                file.write(text)
        dialog.destroy()

builder = Gtk.Builder()
builder.add_from_file("./terminal_editor/ui_main.glade")
builder.connect_signals(Handler())
terminal = builder.get_object("main_terminal")
text_view = builder.get_object("text_view")
save_menu_button = builder.get_object("save_menu_button")
open_menu_button = builder.get_object("open_menu_button")
window = builder.get_object("main_window")

terminal.spawn_sync(
    Vte.PtyFlags.DEFAULT,
    os.environ['HOME'],
    ["/bin/bash"],
    [],
    GLib.SpawnFlags.DO_NOT_REAP_CHILD,
    None,
    None,
    )

window.show_all()

Gtk.main()
