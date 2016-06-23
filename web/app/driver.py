from io import TagReadWrite
from calc_gain import *

def ReplayGain(filepath, custom_gain):
    tags = TagReadWrite(filepath)
    new_tags_data = calc_gain(filepath)
    print custom_gain
    if custom_gain is not None:
        custom_gain = int(custom_gain)
        if custom_gain < 100 or custom_gain > -100:
            print 'Old gain : ', new_tags_data[0].gain
            new_tags_data[0].gain = custom_gain
            print 'Custom gain : ', new_tags_data[0].gain
    tags.write_obj(filepath, new_tags_data[0])
    return new_tags_data[0]
