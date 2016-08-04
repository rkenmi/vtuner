import os.path
import sys
import util
import gi

gi.require_version('Gst', '1.0')

#from gi.repository import GObject, Gst
from gi.repository import GObject, Gst
from track import * # import Track class from Track.py


# Initialize threading
GObject.threads_init()

import threading
threading.Thread(target=lambda: None).start()

class GSTError(Exception):
    def __init__(self, gerror, debug):
        self.domain = gerror.domain
        self.code = gerror.code
        self.message = gerror.message.decode("utf-8")
        self.debug = debug.decode("utf-8")

    def __unicode__(self):
        return u"GST error: %s (%s)" % (self.message, self.debug)

class ReplayGain(GObject.GObject):
    REF_LVL = 89

    __gsignals__ = {
    "track-start": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
        (GObject.TYPE_STRING,)),
    "track-end": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
        (GObject.TYPE_STRING, GObject.TYPE_PYOBJECT)),
    "error": (GObject.SIGNAL_RUN_LAST, GObject.TYPE_NONE,
        (GObject.TYPE_PYOBJECT,)),
    }

    def __init__(self, file):
        GObject.GObject.__init__(self)
        self.file = file

        self._create_pipe()
        bus = self.pipe.get_bus()
        bus.add_signal_watch()
        bus.connect("message", self._on_message)

        self.src.set_property("location", self.file.encode(util.getfilesystemencoding()))

        self.track_data = Track(0)
        self.album_data = Track(0)

    def start(self):
        if self.file:
            self.pipe.set_state(Gst.State.PLAYING)
            self.emit("track-start", self.file)
        else:
            raise ValueError("u dun goofed")

    def _create_pipe(self):
        Gst.init()
        self.pipe = Gst.Pipeline()

        self.src = Gst.ElementFactory.make("filesrc", "src")
        self.pipe.add(self.src)

        self.decbin = Gst.ElementFactory.make("decodebin", "decbin")
        self.decbin.connect('pad-added', self._on_pad_added)
        self.decbin.connect('pad-removed', self._on_pad_removed)
        self.pipe.add(self.decbin)

        self.conv = Gst.ElementFactory.make("audioconvert", "conv")
        self.pipe.add(self.conv)

        self.resample = Gst.ElementFactory.make("audioresample", "resample")
        self.pipe.add(self.resample)

        self.rg = Gst.ElementFactory.make("rganalysis", "rg")
        self.rg.set_property("forced", True)
        self.rg.set_property("reference-level", self.REF_LVL)
        self.pipe.add(self.rg)

        self.sink = Gst.ElementFactory.make("fakesink", "sink")
        self.pipe.add(self.sink)

        self.src.link(self.decbin)
        self.conv.link(self.resample)
        self.resample.link(self.rg)
        self.rg.link(self.sink)


    def _process_tags(self, msg):
        tags = msg.parse_tag()
        #trackdata = self.track_data.setdefault(self.file, Track(0))
        trackdata = self.track_data

        def handle_tag(taglist, tag):
            #print taglist, ": ", tag, "\t", taglist.get_string(tag)
            if trackdata.title is None and tag == Gst.TAG_TITLE:
                _, trackdata.title = taglist.get_string(tag)
            elif trackdata.artist is None and tag == Gst.TAG_ARTIST:
                _, trackdata.artist = taglist.get_string(tag)
            elif trackdata.album is None and tag == Gst.TAG_ALBUM:
                _, trackdata.album = taglist.get_string(tag)
            elif trackdata.genre is None and tag == Gst.TAG_GENRE:
                _, trackdata.genre = taglist.get_string(tag)
            elif tag == Gst.TAG_TRACK_GAIN:
                _, trackdata.gain = taglist.get_double(tag)
            elif tag == Gst.TAG_TRACK_PEAK:
                _, trackdata.peak = taglist.get_double(tag)
            elif tag == Gst.TAG_REFERENCE_LEVEL:
                _, trackdata.ref_level = taglist.get_double(tag)

            elif tag == Gst.TAG_ALBUM_GAIN:
                _, self.album_data.gain = taglist.get_double(tag)
            elif tag == Gst.TAG_ALBUM_PEAK:
                _, self.album_data.peak = taglist.get_double(tag)

        tags.foreach(handle_tag)
        #print '\n'

    def _on_pad_added(self, decbin, new_pad):
        sinkpad = self.conv.get_compatible_pad(new_pad, None)
        if sinkpad is not None:
            new_pad.link(sinkpad)

    def _on_pad_removed(self, decbin, old_pad):
        peer = old_pad.get_peer()
        if peer is not None:
            old_pad.unlink(peer)

    def _on_message(self, bus, msg):
        if msg.type == Gst.MessageType.TAG: # a tag, i.e. AlbumGain
            self._process_tags(msg)
        elif msg.type == Gst.MessageType.EOS: # end of stream
            self.emit("track-end", self.file, self.track_data)
            self.pipe.set_state(Gst.State.NULL)
            self.rg.set_locked_state(False)
        elif msg.type == Gst.MessageType.ERROR:
            self.pipe.set_state(Gst.State.NULL)
            err, debug = msg.parse_error()
            self.emit("error", GSTError(err, debug))
