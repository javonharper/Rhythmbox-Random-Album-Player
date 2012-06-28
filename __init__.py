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

import gtk
import rb
import rhythmdb
import random

ui_str = \
"""
<ui>
  <menubar name="MenuBar">
    <menu name="ControlMenu" action="Control">
      <menuitem name="Random Album" action="RandomAlbum"/>
    </menu>
  </menubar>
  <toolbar name="ToolBar">
    <toolitem name="Random Album" action="RandomAlbum"/>
  </toolbar>
</ui>
"""

class RandomAlbumPlugin (rb.Plugin): 
  def __init__(self):
    rb.Plugin.__init__(self)
  
  def queue_random_album(self):
    #find all of the albums in the user's library
    albums = []
    library = self.shell.props.library_source
    for row in library.props.query_model:
      entry = row[0]
      album_name = self.shell.props.db.entry_get(entry, rhythmdb.PROP_ALBUM)
      if (album_name not in albums):
        albums.append(album_name)
    
    #choose a random album
    selected_album = albums[random.randint(0, len(albums) - 1)]
    print 'queuing ' + selected_album
    
    #find all the songs from that album
    song_info = []
    for row in library.props.query_model:
      entry = row[0]
      album = self.shell.props.db.entry_get(entry, rhythmdb.PROP_ALBUM)
      if (album == selected_album):
        song_uri = entry.get_playback_uri()
        track_num = self.shell.props.db.entry_get(entry, rhythmdb.PROP_TRACK_NUMBER)
        song_info.append((song_uri, track_num))
    
    #sort the songs
    song_info = sorted(song_info, key=lambda song_info: song_info[1])
        
    #add the songs to the play queue      
    for info in song_info:
      self.shell.add_to_queue(info[0])
        
  #loads the plugin  
  def activate(self, shell):
    self.shell = shell
    print 'Activating Random Album Plugin'
    
    #displays the icon on the toolbar
    icon_file_name = '/usr/share/icons/gnome/22x22/apps/zen-icon.png'
    iconsource = gtk.IconSource();
    iconsource.set_filename(icon_file_name)
    iconset = gtk.IconSet()
    iconset.add_source(iconsource)
    iconfactory = gtk.IconFactory()
    iconfactory.add('random-album-button', iconset)
    iconfactory.add_default();
    
    #sets up the ui
    action = gtk.Action('RandomAlbum', 'Random Album', 'Random Album', 'random-album-button')
    action.connect ('activate', self.random_album, shell)
   
    self.action_group = gtk.ActionGroup ('RandomAlbumActionGroup')
    self.action_group.add_action(action)
    
    ui_manager = shell.get_ui_manager()
    ui_manager.insert_action_group (self.action_group)
    self.ui_id = ui_manager.add_ui_from_string(ui_str)
    ui_manager.ensure_update()  
  
  #removed the ui modifications and unloads the plugin 
  def deactivate(self, shell):
    print 'Deactivating RandomAlbumPlugin'
    ui_manager = shell.get_ui_manager()
    ui_manager.remove_ui(self.ui_id)
    del self.shell
    
  def random_album(self, event, shell):
    #get URIs of all the songs in the queue and remove them
    print 'Removing songs from play queue'
    play_queue = self.shell.props.queue_source
    for row in play_queue.props.query_model:
      entry = row[0]
      song_uri = entry.get_playback_uri()
      shell.remove_from_queue(song_uri)
    
    
    #queue a random album
    self.queue_random_album()
     
    
    #start the music!(well, first stop it, but it'll start up again.)
    print 'Playing Album'
    player = shell.props.shell_player
    player.stop()
    player.set_playing_source(shell.props.queue_source)
    player.playpause()
      
    #scroll to song playing
    shell.props.shell_player.play()
    library = shell.props.library_source
    content_viewer = library.get_entry_view()
    #content_viewer.scroll_to_entry(player.get_playing_entry())
