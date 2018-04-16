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
import random_rb3compat
from random_rb3compat import ActionGroup
from random_rb3compat import Action
from random_rb3compat import ApplicationShell

menu_item_ui = '''
  <ui>
    <menubar name="MenuBar">
      <menu name="ControlMenu" action="Control">
        <menuitem name="RandomAlbumItem" action="RandomAlbum"/>
      </menu>
    </menubar>
  </ui>
'''

toolbar_button_ui = '''
  <ui>
    <toolbar name="ToolBar">
      <toolitem name="RandomAlbumItem" action="RandomAlbum" />
    </toolbar>
  </ui>
'''

class RandomAlbumPlugin(GObject.Object, Peas.Activatable):
  __gtype_name__ = 'RandomAlbumPlugin'
  object = GObject.property(type=GObject.Object)

  def __init__(self):
    super(RandomAlbumPlugin, self).__init__()

  def do_activate(self):
    print("Activating Random Album Plugin")
    self.shell = self.object

    self.action_group = ActionGroup(self.shell, 'RandomAlbumActionGroup')

    action = self.action_group.add_action_with_accel(func=self.random_album,
    action_name='RandomAlbum', label='Random Album',
    action_type='app', action_state=ActionGroup.STANDARD,
    accel="<shift><ctrl>R")

    self._appshell = ApplicationShell(self.shell)
    self._appshell.insert_action_group(self.action_group)
    self._appshell.add_app_menuitems(menu_item_ui, 'RandomAlbumActionGroup')

    if not random_rb3compat.is_rb3():
        #uim = self.shell.props.ui_manager
        self._appshell.add_app_menuitems(toolbar_button_ui, 'RandomAlbum')
        #uim.add_ui_from_string(toolbar_button_ui)

    self.settings = Gio.Settings('org.gnome.rhythmbox.plugins.randomalbumplayer')

  def do_deactivate(self):
    print('Deactivating Random Album Plugin')
    shell = self.object
    self._appshell.cleanup()

  def random_album(self, *args):
    self.clear_queue()
    self.queue_random_albums(self.settings['albums-to-play'])
    self.play_album()
    self.scroll_to_current_song()

  def clear_queue(self):
    play_queue = self.shell.props.queue_source
    for row in play_queue.props.query_model:
      entry = row[0]
      play_queue.remove_entry(entry)

  def queue_random_albums(self, album_count):
    for _ in range(album_count):
        self.queue_random_album()

  def play_album(self):
    print('Playing Album')
    player = self.shell.props.shell_player
    player.stop()
    player.set_playing_source(self.shell.props.queue_source)
    player.playpause()

  def scroll_to_current_song(self):
    song = self.shell.props.shell_player.get_playing_entry()
    src = self.shell.props.library_source
    lst = src.get_entry_view()
    lst.scroll_to_entry(song)

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
        album_names = list(albums.keys())
        num_albums = len(albums)
        selected_album = album_names[random.randint(0, num_albums - 1)]

        print('Queuing ' + selected_album + '.')

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
