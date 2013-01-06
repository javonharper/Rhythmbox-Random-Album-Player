SCHEMA_DIR=/usr/share/glib-2.0/schemas/
PLUGIN_SCHEMA=com.javonharper.rhythmbox.plugins.randomalbumplayer.gschema.xml

echo "Installing plugin scripts"
mkdir -p ~/.local/share/rhythmbox/plugins/RhythmboxRandomAlbumPlayer/
cp -rf * ~/.local/share/rhythmbox/plugins/RhythmboxRandomAlbumPlayer/

echo "Installing plugin schema"
sudo cp "$PLUGIN_SCHEMA" "$SCHEMA_DIR"
sudo glib-compile-schemas /usr/share/glib-2.0/schemas/

echo "Installation done. Enjoy!"
