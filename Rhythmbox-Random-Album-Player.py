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
    print "Activating Random Album Plugin"
    shell = self.object
    action = Gtk.Action ('RandomAlbum', _('Random Album'), _('Play a Random Album'), "")
    action.connect ('activate', self.random_album, shell)
    action_group = Gtk.ActionGroup('RandomAlbumActionGroup')
    action_group.add_action(action)
    ui_manager = shell.props.ui_manager
    ui_manager.insert_action_group(action_group)
    ui_manager.add_ui_from_string(random_album_menu_item)

  def do_deactivate(self):
    print 'Deactivating Random Album Plugin'

  def random_album(self, event, shell):
    print 'Playing Random Album'