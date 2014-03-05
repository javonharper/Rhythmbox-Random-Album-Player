import rb
from gi.repository import GObject, Gtk, PeasGtk, Gio

DIALOG_UI_FILE = 'RandomAlbumConfigDialog.glade'

class ConfigDialog(GObject.Object, PeasGtk.Configurable):
    __gtype_name__ = 'RandomAlbumConfigDialog'
    object = GObject.property(type=GObject.Object)
    
    def do_create_configure_widget(self):
        self.ui = Gtk.Builder()
        self.ui.add_from_file(rb.find_plugin_file(self,DIALOG_UI_FILE))
        
        self.settings = Gio.Settings('org.gnome.rhythmbox.plugins.randomalbumplayer')
        
        self.albums_to_play = self.ui.get_object('countSpinButton')
        self.albums_to_play.set_value(self.settings['albums-to-play'])
        
        self.ignored_albums = self.ui.get_object('ignoreEntry')
        self.ignored_albums.set_text(self.settings['ignored-albums'])
        
        self.albums_to_play.connect('value-changed', self.on_albums_to_play_changed)
        self.ignored_albums.connect('changed', self.on_ignored_albums_changed)
        
        return self.ui.get_object('dialog')
    
    def on_albums_to_play_changed(self, widget):
        self.settings['albums-to-play'] = self.albums_to_play.get_value();
    
    def on_ignored_albums_changed(self, widget):
        self.settings['ignored-albums'] = self.ignored_albums.get_text();
