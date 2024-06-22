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

glade_string = """
<?xml version="1.0" encoding="UTF-8"?>
<!-- Generated with glade 3.40.0 -->
<interface>
  <requires lib="gtk+" version="3.24"/>
  <requires lib="vte-2.91" version="0.76"/>
  <object class="GtkMenu" id="file_menu_list">
    <property name="visible">True</property>
    <property name="can-focus">False</property>
    <child>
      <object class="GtkMenuItem" id="open_menu_button">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="label" translatable="yes">Open</property>
        <property name="use-underline">True</property>
        <signal name="activate" handler="on_open_activate" swapped="no"/>
      </object>
    </child>
    <child>
      <object class="GtkMenuItem" id="save_menu_button">
        <property name="visible">True</property>
        <property name="can-focus">False</property>
        <property name="label" translatable="yes">Save</property>
        <property name="use-underline">True</property>
        <signal name="activate" handler="on_save_activate" swapped="no"/>
      </object>
    </child>
  </object>
  <object class="GtkApplicationWindow" id="main_window">
    <property name="visible">True</property>
    <property name="can-focus">True</property>
    <property name="title" translatable="yes">Bash ISE</property>
    <property name="default-width">800</property>
    <property name="default-height">600</property>
    <property name="icon-name">application-x-executable</property>
    <signal name="destroy" handler="on_destroy" swapped="no"/>
    <child>
      <object class="GtkBox" id="main_box">
        <property name="can-focus">True</property>
        <property name="orientation">vertical</property>
        <child>
          <object class="GtkBox">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <property name="margin-start">4</property>
            <property name="margin-end">4</property>
            <property name="margin-top">4</property>
            <property name="margin-bottom">4</property>
            <child>
              <object class="GtkButton" id="run_button">
                <property name="label">Run</property>
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="receives-default">False</property>
                <property name="always-show-image">True</property>
                <signal name="clicked" handler="on_button_clicked" swapped="no"/>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="position">0</property>
              </packing>
            </child>
            <child>
              <object class="GtkMenuButton" id="file_menu">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="focus-on-click">False</property>
                <property name="receives-default">False</property>
                <property name="popup">file_menu_list</property>
                <child>
                  <placeholder/>
                </child>
              </object>
              <packing>
                <property name="expand">False</property>
                <property name="fill">True</property>
                <property name="pack-type">end</property>
                <property name="position">4</property>
              </packing>
            </child>
          </object>
          <packing>
            <property name="expand">False</property>
            <property name="fill">True</property>
            <property name="position">0</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="script_scrolled_window">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <child>
              <object class="GtkTextView" id="text_view">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="margin-start">4</property>
                <property name="margin-end">4</property>
                <property name="margin-bottom">2</property>
                <property name="wrap-mode">word</property>
                <property name="left-margin">4</property>
                <property name="right-margin">4</property>
                <property name="monospace">True</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">2</property>
          </packing>
        </child>
        <child>
          <object class="GtkScrolledWindow" id="output_scrolled_window">
            <property name="visible">True</property>
            <property name="can-focus">False</property>
            <child>
              <object class="VteTerminal" id="main_terminal">
                <property name="visible">True</property>
                <property name="can-focus">True</property>
                <property name="margin-left">4</property>
                <property name="margin-right">4</property>
                <property name="margin-top">2</property>
                <property name="margin-bottom">4</property>
                <property name="hscroll-policy">natural</property>
                <property name="vscroll-policy">natural</property>
                <property name="cursor-blink-mode">on</property>
                <property name="cursor-shape">underline</property>
                <property name="encoding">UTF-8</property>
                <property name="scroll-on-keystroke">True</property>
                <property name="scroll-on-output">False</property>
              </object>
            </child>
          </object>
          <packing>
            <property name="expand">True</property>
            <property name="fill">True</property>
            <property name="position">3</property>
          </packing>
        </child>
      </object>
    </child>
  </object>
</interface>
"""

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
builder.add_from_string(glade_string)
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
