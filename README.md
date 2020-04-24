# iTunesPlaylistExporter

### Usage:

Open up your commandline and navigate to your "python.exe", then type:
```
python.exe X:\path\to\playlist_exporter.py
```
**Mandatory Arguments:**  
* *iml_path:*
This should be the path to your iTunes Music Library, usually located in "C:\Users\User\Music\iTunes"
  ```
  iml_path="X:\path\to\iTunes Music Library.xml"
  ```
  
* *p_name*:
The name of the playlist you want to export.
   ```
  p_name="PlaylistName"
  ```

**Obligatory Arguments:**  
* *dst:*
With this argument you can specify a folder, where the exported tracks should be copied to. If you don't provide a path, a directory is created for you at the location of the script.
  ```
  dst="X:\path\to\desired\output
  ```
