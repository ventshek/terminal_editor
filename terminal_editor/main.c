#include <gtk/gtk.h>
#include <vte/vte.h>
#include <stdlib.h>
#include <unistd.h>
#include <fcntl.h>
#include <sys/stat.h>

static GtkWidget *text_view;
static VteTerminal *terminal;
static GtkBuilder *builder;

const char *glade_file_content = 
"<?xml version=\"1.0\" encoding=\"UTF-8\"?>"
"<!-- Generated with glade 3.40.0 -->"
"<interface>"
"  <requires lib=\"gtk+\" version=\"3.24\"/>"
"  <requires lib=\"vte-2.91\" version=\"0.76\"/>"
"  <object class=\"GtkMenu\" id=\"file_menu_list\">"
"    <property name=\"visible\">True</property>"
"    <property name=\"can-focus\">False</property>"
"    <child>"
"      <object class=\"GtkMenuItem\" id=\"open_menu_button\">"
"        <property name=\"visible\">True</property>"
"        <property name=\"can-focus\">False</property>"
"        <property name=\"label\" translatable=\"yes\">Open</property>"
"        <property name=\"use-underline\">True</property>"
"        <signal name=\"activate\" handler=\"on_open_activate\" swapped=\"no\"/>"
"      </object>"
"    </child>"
"    <child>"
"      <object class=\"GtkMenuItem\" id=\"save_menu_button\">"
"        <property name=\"visible\">True</property>"
"        <property name=\"can-focus\">False</property>"
"        <property name=\"label\" translatable=\"yes\">Save</property>"
"        <property name=\"use-underline\">True</property>"
"        <signal name=\"activate\" handler=\"on_save_activate\" swapped=\"no\"/>"
"      </object>"
"    </child>"
"  </object>"
"  <object class=\"GtkApplicationWindow\" id=\"main_window\">"
"    <property name=\"visible\">True</property>"
"    <property name=\"can-focus\">True</property>"
"    <property name=\"title\" translatable=\"yes\">Bash ISE</property>"
"    <property name=\"default-width\">800</property>"
"    <property name=\"default-height\">600</property>"
"    <property name=\"icon-name\">application-x-executable</property>"
"    <signal name=\"destroy\" handler=\"on_destroy\" swapped=\"no\"/>"
"    <child>"
"      <object class=\"GtkBox\" id=\"main_box\">"
"        <property name=\"can-focus\">True</property>"
"        <property name=\"orientation\">vertical</property>"
"        <child>"
"          <object class=\"GtkBox\">"
"            <property name=\"visible\">True</property>"
"            <property name=\"can-focus\">False</property>"
"            <property name=\"margin-start\">4</property>"
"            <property name=\"margin-end\">4</property>"
"            <property name=\"margin-top\">4</property>"
"            <property name=\"margin-bottom\">4</property>"
"            <child>"
"              <object class=\"GtkButton\" id=\"run_button\">"
"                <property name=\"label\">Run</property>"
"                <property name=\"visible\">True</property>"
"                <property name=\"can-focus\">True</property>"
"                <property name=\"receives-default\">False</property>"
"                <property name=\"always-show-image\">True</property>"
"                <signal name=\"clicked\" handler=\"on_button_clicked\" swapped=\"no\"/>"
"              </object>"
"              <packing>"
"                <property name=\"expand\">False</property>"
"                <property name=\"fill\">True</property>"
"                <property name=\"position\">0</property>"
"              </packing>"
"            </child>"
"            <child>"
"              <object class=\"GtkMenuButton\" id=\"file_menu\">"
"                <property name=\"visible\">True</property>"
"                <property name=\"can-focus\">True</property>"
"                <property name=\"focus-on-click\">False</property>"
"                <property name=\"receives-default\">False</property>"
"                <property name=\"popup\">file_menu_list</property>"
"                <child>"
"                  <placeholder/>"
"                </child>"
"              </object>"
"              <packing>"
"                <property name=\"expand\">False</property>"
"                <property name=\"fill\">True</property>"
"                <property name=\"pack-type\">end</property>"
"                <property name=\"position\">4</property>"
"              </packing>"
"            </child>"
"          </object>"
"          <packing>"
"            <property name=\"expand\">False</property>"
"            <property name=\"fill\">True</property>"
"            <property name=\"position\">0</property>"
"          </packing>"
"        </child>"
"        <child>"
"          <object class=\"GtkScrolledWindow\" id=\"script_scrolled_window\">"
"            <property name=\"visible\">True</property>"
"            <property name=\"can-focus\">False</property>"
"            <child>"
"              <object class=\"GtkTextView\" id=\"text_view\">"
"                <property name=\"visible\">True</property>"
"                <property name=\"can-focus\">True</property>"
"                <property name=\"margin-start\">4</property>"
"                <property name=\"margin-end\">4</property>"
"                <property name=\"margin-bottom\">2</property>"
"                <property name=\"wrap-mode\">word</property>"
"                <property name=\"left-margin\">4</property>"
"                <property name=\"right-margin\">4</property>"
"                <property name=\"monospace\">True</property>"
"              </object>"
"            </child>"
"          </object>"
"          <packing>"
"            <property name=\"expand\">True</property>"
"            <property name=\"fill\">True</property>"
"            <property name=\"position\">2</property>"
"          </packing>"
"        </child>"
"        <child>"
"          <object class=\"GtkScrolledWindow\" id=\"output_scrolled_window\">"
"            <property name=\"visible\">True</property>"
"            <property name=\"can-focus\">False</property>"
"            <child>"
"              <object class=\"VteTerminal\" id=\"main_terminal\">"
"                <property name=\"visible\">True</property>"
"                <property name=\"can-focus\">True</property>"
"                <property name=\"margin-left\">4</property>"
"                <property name=\"margin-right\">4</property>"
"                <property name=\"margin-top\">2</property>"
"                <property name=\"margin-bottom\">4</property>"
"                <property name=\"hscroll-policy\">natural</property>"
"                <property name=\"vscroll-policy\">natural</property>"
"                <property name=\"cursor-blink-mode\">on</property>"
"                <property name=\"cursor-shape\">underline</property>"
"                <property name=\"encoding\">UTF-8</property>"
"                <property name=\"scroll-on-keystroke\">True</property>"
"                <property name=\"scroll-on-output\">False</property>"
"              </object>"
"            </child>"
"          </object>"
"          <packing>"
"            <property name=\"expand\">True</property>"
"            <property name=\"fill\">True</property>"
"            <property name=\"position\">3</property>"
"          </packing>"
"        </child>"
"      </object>"
"    </child>"
"  </object>"
"</interface>";


static void on_destroy(GtkWidget *widget, gpointer data) {
    gtk_main_quit();
}

static void on_button_clicked(GtkButton *button, gpointer data) {
    GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
    GtkTextIter start, end;
    gtk_text_buffer_get_bounds(buffer, &start, &end);
    gchar *script = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
    
    FILE *script_file = fopen("/tmp/temp_script.sh", "w");
    fprintf(script_file, "%s\nbash\n", script);
    fclose(script_file);
    chmod("/tmp/temp_script.sh", 0755);

    const char *argv[] = {"/bin/bash", "-c", "/tmp/temp_script.sh", NULL};
    vte_terminal_spawn_async(VTE_TERMINAL(terminal),
                             VTE_PTY_DEFAULT,
                             g_get_home_dir(),
                             (char **)argv,
                             NULL,
                             G_SPAWN_DO_NOT_REAP_CHILD,
                             NULL,
                             NULL,
                             NULL,
                             -1,
                             NULL,
                             NULL,
                             NULL);
    g_free(script);
}

static void on_open_activate(GtkButton *button, gpointer data) {
    GtkWidget *dialog = gtk_file_chooser_dialog_new("Please choose a file",
                                                    GTK_WINDOW(gtk_builder_get_object(builder, "main_window")),
                                                    GTK_FILE_CHOOSER_ACTION_OPEN,
                                                    "_Cancel", GTK_RESPONSE_CANCEL,
                                                    "_Open", GTK_RESPONSE_ACCEPT,
                                                    NULL);
    GtkFileFilter *filter = gtk_file_filter_new();
    gtk_file_filter_set_name(filter, "Text files");
    gtk_file_filter_add_mime_type(filter, "text/plain");
    gtk_file_chooser_add_filter(GTK_FILE_CHOOSER(dialog), filter);

    if (gtk_dialog_run(GTK_DIALOG(dialog)) == GTK_RESPONSE_ACCEPT) {
        char *filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(dialog));
        char *content;
        g_file_get_contents(filename, &content, NULL, NULL);
        GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
        gtk_text_buffer_set_text(buffer, content, -1);
        g_free(content);
        g_free(filename);
    }

    gtk_widget_destroy(dialog);
}

static void on_save_activate(GtkButton *button, gpointer data) {
    GtkWidget *dialog = gtk_file_chooser_dialog_new("Save File",
                                                    GTK_WINDOW(gtk_builder_get_object(builder, "main_window")),
                                                    GTK_FILE_CHOOSER_ACTION_SAVE,
                                                    "_Cancel", GTK_RESPONSE_CANCEL,
                                                    "_Save", GTK_RESPONSE_ACCEPT,
                                                    NULL);
    GtkFileFilter *filter = gtk_file_filter_new();
    gtk_file_filter_set_name(filter, "Text files");
    gtk_file_filter_add_mime_type(filter, "text/plain");
    gtk_file_chooser_add_filter(GTK_FILE_CHOOSER(dialog), filter);

    if (gtk_dialog_run(GTK_DIALOG(dialog)) == GTK_RESPONSE_ACCEPT) {
        char *filename = gtk_file_chooser_get_filename(GTK_FILE_CHOOSER(dialog));
        GtkTextBuffer *buffer = gtk_text_view_get_buffer(GTK_TEXT_VIEW(text_view));
        GtkTextIter start, end;
        gtk_text_buffer_get_bounds(buffer, &start, &end);
        char *text = gtk_text_buffer_get_text(buffer, &start, &end, FALSE);
        g_file_set_contents(filename, text, -1, NULL);
        g_free(text);
        g_free(filename);
    }

    gtk_widget_destroy(dialog);
}

int main(int argc, char *argv[]) {
    gtk_init(&argc, &argv);

    builder = gtk_builder_new();
    gtk_builder_add_from_string(builder, glade_file_content, -1, NULL);
    gtk_builder_connect_signals(builder, NULL);

    GtkWidget *window = GTK_WIDGET(gtk_builder_get_object(builder, "main_window"));
    terminal = VTE_TERMINAL(gtk_builder_get_object(builder, "main_terminal"));
    text_view = GTK_WIDGET(gtk_builder_get_object(builder, "text_view"));

    g_signal_connect(gtk_builder_get_object(builder, "run_button"), "clicked", G_CALLBACK(on_button_clicked), NULL);
    g_signal_connect(gtk_builder_get_object(builder, "open_menu_button"), "activate", G_CALLBACK(on_open_activate), NULL);
    g_signal_connect(gtk_builder_get_object(builder, "save_menu_button"), "activate", G_CALLBACK(on_save_activate), NULL);
    g_signal_connect(window, "destroy", G_CALLBACK(on_destroy), NULL);

    const char *argv_terminal[] = {"/bin/bash", NULL};
    vte_terminal_spawn_async(VTE_TERMINAL(terminal),
                             VTE_PTY_DEFAULT,
                             g_get_home_dir(),
                             (char **)argv_terminal,
                             NULL,
                             G_SPAWN_DO_NOT_REAP_CHILD,
                             NULL,
                             NULL,
                             NULL,
                             -1,
                             NULL,
                             NULL,
                             NULL);

    gtk_widget_show_all(window);
    gtk_main();

    return 0;
}
