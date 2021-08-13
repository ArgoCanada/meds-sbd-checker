
import os
import tempfile


class FileSBDOrganizer:

    def __init__(self, root=None):
        if root is None:
            self._temp_dir = tempfile.TemporaryDirectory()
            self._root = self._temp_dir.name
        else:
            if not os.path.isdir(root):
                raise ValueError(f"'{root}' is not a directory")
            self._root = root

    def __del__(self):
        if self._temp_dir is not None:
            self._temp_dir.cleanup()

    def has_file(self, name):
        return os.path.exists(self._path(name))
    
    def list_files(self, imei=None):
        if imei is None:
            files = []
            for f in os.listdir(self._root):
                if os.path.isdir(f):
                    for item in self.list_files(f):
                        files.append(item)
            return files
        else:
            imei_dir = os.path.join(self._root, str(imei))
            files = os.listdir(imei_dir)
            return [os.path.join(imei_dir, f) for f in files if f.endswith('.sbd')]
    
    def put_file_content(self, name, content):
        if not isinstance(content, bytes):
            raise TypeError('`content` must be a bytes() string')

        path = self._path(name)
        if not os.path.exists(os.path.dirname(path)):
            os.mkdir(os.path.dirname(path))
        
        with open(path, 'wb') as f:
            f.write(content)
    
    def get_file_content(self, name):
        with open(self._path(name), 'rb') as f:
            return f.read()

    def _path(self, name):
        if '_' not in name:
            raise ValueError(f"Can't extract imei number from '{name}'")
        if not name.endswith('.sbd'):
            raise ValueError(f"'{name}' does not end with .sbd")
        
        imei_no = name[:name.find('_')]
        return os.path.join(self._root, imei_no, name)


