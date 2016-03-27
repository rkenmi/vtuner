import os.path
import warnings
import mutagen
from mutagen.id3 import TXXX

# Only basic MP3!
class TagReadWrite(object):
    TAG_TRACK_GAIN = u'replaygain_track_gain'
    TAG_ALBUM_GAIN = u'replaygain_album_gain'
    TAG_TRACK_PEAK = u'replaygain_track_peak'
    TAG_ALBUM_PEAK = u'replaygain_album_peak'
    TAG_REF_LOUDNESS = u'replaygain_reference_loudness'

    def __init__(self, filename):
        print 'mp3/' + filename
        tags = self._get_tags_obj(filename)
        #print os.path
        track_data = []
        album_data = []
        track_data.append(self.read_obj(tags, u'TXXX:' + self.TAG_TRACK_GAIN, u'TXXX:' + self.TAG_TRACK_PEAK))
        album_data.append(self.read_obj(tags, u'TXXX:' + self.TAG_ALBUM_GAIN, u'TXXX:' + self.TAG_ALBUM_PEAK))
        print track_data
        print album_data

    def _get_tags_obj(self, filename):
        try:
            return mutagen.File(filename)
        except:
            Exception('Error loading file with mutagen')

    def read_obj(self, tags, gain_tag, peak_tag):
        if gain_tag in tags:
            return tags[gain_tag], tags[peak_tag]
        else:
            return None

    def write_obj(self, filename, track):
        tags = self._get_tags_obj(filename)
        if tags is None:
            raise Exception('No tags can be loaded. Is the file a proper format?')

        try:
            if track:
                tags[u'TXXX:' + self.TAG_TRACK_GAIN] = TXXX(encoding = 0, desc = self.TAG_TRACK_GAIN, text=[u'%.3f dB' % track.gain])
                tags[u'TXXX:' + self.TAG_TRACK_PEAK] = TXXX(encoding = 0, desc = self.TAG_TRACK_PEAK, text=[u'%.3f' % track.peak])
                tags.save()
                print 'dun'
        except:
            raise Exception('Something is wrong with the track.')
