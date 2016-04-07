from io import TagReadWrite
from calc_gain import *

def ReplayGain(filepath):
    tags = TagReadWrite(filepath)
    new_tags_data = calc_gain(filepath)
    tags.write_obj(filepath, new_tags_data[0])
    return new_tags_data[0]
