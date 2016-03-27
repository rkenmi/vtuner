import calc
import sys
from gi.repository import GObject
import util


def CalcGain(filename):
    exc_slot = [None]

    def on_track_start(evsrc, filename):
        print "Calculating gain from %s" % filename.decode("utf-8")
        sys.stdout.flush()

    def on_track_end(evsrc, filename, gaindata):
        if gaindata:
            print "\tComplete. \nAlbum Gain : %.2f dB" % gaindata.gain
            print "\tTrack Title : %s" % gaindata.title
            print "\tTrack Album : %s" % gaindata.album
            print "\tTrack Artist : %s" % gaindata.artist
            print "\tTrack Genre : %s" % gaindata.genre
        else:
            print "done"
        loop.quit()

    def on_error(evsrc, exc):
        print exc.__unicode__()
        exc_slot[0] = exc
        loop.quit()

    A = calc.ReplayGain(filename)
    with util.gobject_signals(A,
        ("track-start", on_track_start),
        ("track-end", on_track_end),
        ("error", on_error),):
        loop = GObject.MainLoop()
        A.start()
        loop.run()

    if exc_slot[0] is not None:
        raise exc_slot[0]
    return A.track_data, A.album_data
