'''
Plugin for Rhythmbox that random plays songs sorted by album (in correct disc order), track-number randomly
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

import random

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
  __gtype_name__ = 'RandomAlbumPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(RandomAlbumPlugin, self).__init__()

  def do_activate(self):
    shell = self.object
    print "Activating Random Album Plugin"
    action = Gtk.Action ('RandomAlbum', _('Random Album'), _('Play a Random Album'), "")
    action.connect ('activate', self.random_album, shell)
    action_group = Gtk.ActionGroup('RandomAlbumActionGroup')
    action_group.add_action_with_accel (action, "<alt>R")
    
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
    
    # Start the music!(well, first stop it, but it'll start up again.)
    print 'Playing Album'
    player = shell.props.shell_player
    player.stop()
    player.set_playing_source(shell.props.queue_source)
    player.playpause(True)

  def queue_random_album(self):
    shell = self.object
    library = shell.props.library_source
    albums = {}
    #ignore_albums = ["Single", "Unknown"]
    for row in library.props.query_model:
      entry = row[0]
      album_name = entry.get_string(RB.RhythmDBPropType.ALBUM)
      #if album_name in ignore_albums:
      #  continue
      album_struct = albums.get(album_name, { "songs" : [], "count": 0 })
      album_struct["count"] = album_struct["count"] + 1
      album_struct["songs"].append(entry)
      albums[album_name] = album_struct
  
    # Choose a random album
    album_names = albums.keys()
    num_albums = len(albums)
    selected_album = album_names[random.randint(0, num_albums - 1)]
    # optionally only queue album over a certain length
    # but only try a few times, don't want to get bogged down
    # trying to find one (filtering up front may be better?)
    #tries = 0
    #while(albums[selected_album]["count"] < 5 and tries < 10):
    #  selected_album = album_names[random.randint(0, num_albums - 1)]
    #  tries = tries + 1
    print 'Queuing ' + selected_album+ '.'
  
    # Find all the songs from that album
    songs = albums[selected_album]["songs"]
  
    # Sort the songs by disc number, track number
    songs = sorted(songs, key=lambda song: song.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER))
    songs = sorted(songs, key=lambda song: song.get_ulong(RB.RhythmDBPropType.DISC_NUMBER))
        
    # Add the songs to the play queue      
    for song in songs:
      shell.props.queue_source.add_entry(song, -1)
