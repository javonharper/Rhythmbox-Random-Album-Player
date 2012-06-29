'''
Plugin for Rhythmbox that random plays songs sorted by album, track-number randomly
Copyright (C) 2012  Javon Harper <javon.d.harper@gmail.com>

This program is free software; you can redistribute it and/or
modify it under the terms of the GNU General Public License
as published by the Free Software Foundation; either version 2
of the License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program; if not, write to the Free Software
Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.
'''

from gi.repository import GObject
from gi.repository import Peas
from gi.repository import RB
from gi.repository import Gtk

#finding a file
# rb_find_plugin_data_file("myfile")
random_album_menu_item = '''
  <ui>
    <menubar name="MenuBar">
      <menu name="ControlMenu" action="Control">
        <menuitem name="RandomAlbumItem" action="RandomAlbum"/>
      </menu>
    </menubar>
  </ui>
'''

class RandomAlbumPlugin(GObject.Object, Peas.Activatable):
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(RandomAlbumPlugin, self).__init__()

  def do_activate(self):
    shell = self.object
    print "Activating Random Album Plugin"
    action = Gtk.Action ('RandomAlbum', _('Random Album'), _('Play a Random Album'), "")
    action.connect ('activate', self.random_album, shell)
    action_group = Gtk.ActionGroup('RandomAlbumActionGroup')
    action_group.add_action(action)
    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    self.ui_id = ui_manager.add_ui_from_string(random_album_menu_item)

  def do_deactivate(self):
    print 'Deactivating Random Album Plugin'
    shell = self.object
    ui_manager = shell.props.ui_manager
    ui_manager.remove_ui(self.ui_id)

  def random_album(self, event, shell):
    # Get URIs of all the songs in the queue and remove them
    play_queue = shell.props.queue_source
    for row in play_queue.props.query_model:
      entry = row[0]
      play_queue.remove_entry(entry)
  
    # Queue a random album
    self.queue_random_album()
    
    # #start the music!(well, first stop it, but it'll start up again.)
    # print 'Playing Album'
    # player = shell.props.shell_player
    # player.stop()
    # player.set_playing_source(shell.props.queue_source)
    # player.playpause()
      
    # #scroll to song playing
    # shell.props.shell_player.play()
    # library = shell.props.library_source
    # content_viewer = library.get_entry_view()


  def queue_random_album(self):
    # Find all of the albums in the user's library
    shell = self.object
    library = shell.props.library_source
    albums = []
    for row in library.props.query_model:
      entry = row[0]
      album_name = entry.get_string(RB.RhythmDBPropType.ALBUM)
      if (album_name not in albums):
        albums.append(album_name)
    print albums
  
  # #choose a random album
  # selected_album = albums[random.randint(0, len(albums) - 1)]
  # print 'queuing ' + selected_album
  
  # #find all the songs from that album
  # song_info = []
  # for row in library.props.query_model:
  #   entry = row[0]
  #   album = self.shell.props.db.entry_get(entry, rhythmdb.PROP_ALBUM)
  #   if (album == selected_album):
  #     song_uri = entry.get_playback_uri()
  #     track_num = self.shell.props.db.entry_get(entry, rhythmdb.PROP_TRACK_NUMBER)
  #     song_info.append((song_uri, track_num))
  
  # #sort the songs
  # song_info = sorted(song_info, key=lambda song_info: song_info[1])
      
  # #add the songs to the play queue      
  # for info in song_info:
  #   self.shell.add_to_queue(info[0])