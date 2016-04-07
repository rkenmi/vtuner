class Track(object):
    def __init__(self, gain, peak=1.0, ref_level=89):
        self.gain = gain
        self.peak = peak
        self.ref_level = ref_level
        self.title = None
        self.genre = None
        self.artist = None
        self.album = None

    def __str__(self):
        return ("gain=%.2f dB; peak=%.8f; reference-level=%i dB" % (self.gain, self.peak, self.ref_level))

    def __eq__(self, other):
        return other is not None and (self.gain == other.gain and self.peak == other.peak and self.ref_level == other.ref_level)
