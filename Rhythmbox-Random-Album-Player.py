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
from gi.repository import Gio

from RandomAlbumConfigDialog import ConfigDialog

#~ GLib.threads_init()
from random_rb3compat import ActionGroup
from random_rb3compat import Action
from random_rb3compat import ApplicationShell

ui_str = '''
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
    #~ shell = self.object
    print "Activating Random Album Plugin"
    #~ action = Gtk.Action ('RandomAlbum', _('Random Album'), _('Play a Random Album'), "")
    #~ action.connect ('activate', self.random_album, shell)
    #~ action_group = Gtk.ActionGroup('RandomAlbumActionGroup')
    #~ action_group.add_action_with_accel (action, "<alt>Z")
    
    self.shell = self.object
        
    self.action_group = ActionGroup(self.shell, 'RandomAlbumActionGroup')
    
    action = self.action_group.add_action_with_accel(func=self.random_album,
    action_name='RandomAlbum', label='RandomAlbum',
    action_type='app', action_state=ActionGroup.STANDARD,
    accel="<alt>Z")

    self._appshell = ApplicationShell(self.shell)
    self._appshell.insert_action_group(self.action_group)
    self._appshell.add_app_menuitems(ui_str, 'RandomAlbumActionGroup')
    
    self.settings = Gio.Settings('org.gnome.rhythmbox.plugins.randomalbumplayer')

  def do_deactivate(self):
    print 'Deactivating Random Album Plugin'
    shell = self.object
    #~ ui_manager = shell.props.ui_manager
    #~ ui_manager.remove_ui(self.ui_id)

  def random_album(self, *args):
    # Get URIs of all the songs in the queue and remove them
    play_queue = self.shell.props.queue_source
    for row in play_queue.props.query_model:
      entry = row[0]
      play_queue.remove_entry(entry)
  
    # Queue a random album
    for _ in range(self.settings['albums-to-play']):
        self.queue_random_album()
    
    # Start the music!(well, first stop it, but it'll start up again.)
    print 'Playing Album'
    player = self.shell.props.shell_player
    player.stop()
    player.set_playing_source(self.shell.props.queue_source)
    player.playpause(True)

  def queue_random_album(self):
    shell = self.object
    library = shell.props.library_source
    albums = {}
    
    ignore_albums = [ item.strip() for item in self.settings['ignored-albums'].split(',') ]

    for row in library.props.query_model:
      entry = row[0]
      album_name = entry.get_string(RB.RhythmDBPropType.ALBUM)
      
      if album_name in ignore_albums:
        continue
        
      album_struct = albums.get(album_name, { "songs" : [], "count": 0 })
      album_struct["count"] = album_struct["count"] + 1
      album_struct["songs"].append(entry)
      albums[album_name] = album_struct
  
    # Choose a random album with more than 5 songs
    while True:
        album_names = albums.keys()
        num_albums = len(albums)
        selected_album = album_names[random.randint(0, num_albums - 1)]

        print 'Queuing ' + selected_album+ '.'
  
        # Find all the songs from that album
        songs = albums[selected_album]["songs"]
    
        if len(songs) > 5:
            # album is long enough
            break
  
    # Sort the songs by disc number, track number
    songs = sorted(songs, key=lambda song: song.get_ulong(RB.RhythmDBPropType.TRACK_NUMBER))
    songs = sorted(songs, key=lambda song: song.get_ulong(RB.RhythmDBPropType.DISC_NUMBER))
        
    # Add the songs to the play queue      
    for song in songs:
      shell.props.queue_source.add_entry(song, -1)
