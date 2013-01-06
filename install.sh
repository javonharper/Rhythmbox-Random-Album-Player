SCHEMA_DIR=/usr/share/glib-2.0/schemas/
PLUGIN_SCHEMA=org.gnome.rhythmbox.plugins.randomalbumplayer.gschema.xml

echo "Installing plugin scripts"
mkdir -p ~/.local/share/rhythmbox/plugins/RhythmboxRandomAlbumPlayer/
cp -rf * ~/.local/share/rhythmbox/plugins/RhythmboxRandomAlbumPlayer/

echo "Installing plugin schema"
sudo cp "$PLUGIN_SCHEMA" "$SCHEMA_DIR"
sudo glib-compile-schemas "$SCHEMA_DIR"

echo "Installation done. Enjoy!"
