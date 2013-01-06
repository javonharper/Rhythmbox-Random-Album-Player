import rb
from gi.repository import GObject, Gtk, PeasGtk, Gio

DIALOG_UI_FILE = 'RandomAlbumConfigDialog.glade'

class ConfigDialog(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'RandomAlbumConfigDialog'
    object = GObject.property(type=GObject.Object)
    
    def do_create_configure_widget(self):
        self.ui = Gtk.Builder()
        self.ui.add_from_file(rb.find_plugin_file(self, DIALOG_UI_FILE))
        return self.ui.get_object('dialog')
