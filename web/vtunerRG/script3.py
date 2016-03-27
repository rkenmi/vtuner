track = data[0]
from io import TagReadWrite

C = TagReadWrite()
C.write_obj('ocala.mp3', track)
