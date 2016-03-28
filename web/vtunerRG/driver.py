from io import TagReadWrite
from calc_gain import CalcGain

def ReplayGain(filepath):
    tags = TagReadWrite(filepath)
    new_tags_data = CalcGain(filepath)
    tags.write_obj(filepath, new_tags_data[0])
