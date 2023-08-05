"""
Annotations
===========

"""

import csv

import matplotlib.patches as mpatches
import numpy as np
import pandas as pd


class Annotations(object):

    def __init__(self, filename=None, legacy=False):
        """
        Args:
            filename: path to an annotations file (usually a `csv`)
            legacy: set to ``True`` if the file is in the older format
        """
        self.tracks = []

        if filename:
            if legacy:
                self.load_from_legacy_csv(filename)
            else:
                self.load_from_csv(filename)
        self.filename = filename

    def __repr__(self):
        repr = "Annotations: {} tracks".format(len(self.tracks))
        if self.tracks:
            for track in self.tracks:
                repr += "\n  {}".format(track.__repr__())
            repr += "\n"
        return repr

    def load_from_csv(self, csvfile):
        """Read annotations from CSV file exported by pythonVideoAnnotator.

        File structure::

            | T | Number of events in this track  |     |     | Color | Label |
            | P | Lock status | Begin frame | End frame | Comment | Color |   |
        """

        with open(csvfile, 'r') as f:
            track_id = -1
            for line in f.readlines():
                elements = line.strip().split(',')

                if len(elements) == 3:
                    track_id += 1
                    _, name, color = elements
                    self.tracks.append(Track(track_id, name, color))
                elif len(elements) == 7:
                    _, _, ti, tf, comment, _, _ = elements
                    ti = int(ti)
                    tf = int(tf)
                    event = Event(ti, tf - ti, comment)
                    self.tracks[track_id].add_event(event)
                else:
                    continue

    def load_from_legacy_csv(self, csvfile):
        """Read annotations from CSV file exported by VidA.

        File structure::

            --- CSV FILE BEGIN ---
            Track info line
            Event info line
            Event info line
            ...
            Empty line
            Track info line
            Event info line
            Event info line
            ...
            Empty line
            Track info line
            Event info line
            Event info line
            ...
            Empty line
            --- CSV FILE END ---


        Track info line format::

            | Id | Total number of events in this track |  |  | Color | Label |


        Event info line format::

            | Lock status | Begin frame | End frame | Comment | Color |       |
        """

        with open(csvfile, 'r') as f:
            track_id = None
            for line in f.readlines():
                contents = line.strip().split(',')
                empty_line = not bool("".join(contents))

                if not track_id and not empty_line:
                    # Track
                    track_id, _, _, _, color, name = contents
                    self.tracks.append(Track(int(track_id), name, color))

                elif empty_line:
                    # Changing to another track
                    track_id = None

                else:
                    # Annotations
                    _, begin, end, comment, _ = contents
                    t = int(begin)
                    duration = int(end) - t
                    self.tracks[-1].add_event(Event(t, duration, comment))

    def save_to_csv(self, csvfile):
        """Write annotations to a CSV file using the format supported by VidA.
        """
        outputstream = []
        for track in self.tracks:
            row_track_info = [str(track.id),
                              str(track.nevents),
                              '',
                              '',
                              str(track.color),
                              str(track.name)]
            outputstream.append(row_track_info)

            for event in track.events:
                row_event_info = ['True',
                                  str(event.time),
                                  str(event.time + event.duration),
                                  str(event.comment),
                                  str(track.color)]
                outputstream.append(row_event_info)

            row_sep = ["" for item in range(len(row_track_info))]
            outputstream.append(row_sep)

        with open(csvfile, 'w', encoding='utf-8') as f:
            csvwriter = csv.writer(f, dialect='excel', lineterminator='\n')
            for row in outputstream:
                csvwriter.writerow(row)

    def get_track(self, track_name, track_color=None):
        """Returns a Track object with the name `track_name`. If there
        is no track with that name, returns `None`.
        In the possibility of having more than one track named the same,
        you can also specify its color. If it is not possible to get
        only one track after name and color filtering, an error is
        raised.
        """
        tracks_found = []

        for t in self.tracks:
            if t.name == track_name:
                tracks_found.append(t)

        if tracks_found:
            if len(tracks_found) == 1:
                return tracks_found[0]
            else:
                # Found more than one; try to select one based on color
                track_colors = [t.color for t in tracks_found]
                if track_color in track_colors:
                    i = track_colors.index(track_color)
                    return tracks_found[i]
                else:
                    raise UserWarning(("I found more than one Track with"
                                       " name '{}'".format(track_name)))
        else:
            # No tracks found with the name provided
            return None


class Track(object):

    """
    Track

    A Track is a collection of events. May have a `name` and a `color`.
    """

    def __init__(self, id, name, color):
        self.id = id
        self.name = name
        self.color = color
        self.events = []

    def __repr__(self):
        return "[ {} ] color: {} | events: {:>2} | name: {}".format(
            self.__class__.__name__, self.color, self.nevents, self.name)

    def add_event(self, event):
        """Add an event to the Track.
        If the event added has a property named `time`, the Track
        events are sorted accordingly.
        """
        self.events.append(event)
        self.events.sort(key=lambda event: event.time)

    def as_series(self, minimum=0, maximum=None):
        """Returns the annotated events as a ``pandas.Series``.

        Args:
            minimum (int): minimum time to consider
            maximum (int): maximum time to consider; defaults to last
                           event end time

        Returns:
            pandas.Series

        """
        maximum = maximum or self.events[-1].time_interval[1]
        series = pd.Series(0, index=range(minimum, maximum + 1), dtype=bool)
        for event in self.events:
            if event.duration > 0:
                series.loc[slice(*event.time_interval)] = True
            else:
                if event.time in series.index:
                    series.loc[event.time] = True
        return series

    def get_mask(self, max, min=0):
        """Get boolean mask.
        Returns a `numpy.array()` with True entries where there are
        events, and False otherwise.
        """
        mask = np.zeros(max - min + 1, dtype=bool)
        for event in self.events:
            if event.duration > 0:
                for t in range(*event.time_interval):
                    try:
                        mask[t] = True
                    except IndexError:
                        pass
            else:
                mask[event.time] = True
        return mask

    def intersection_with(self, track):
        """Intersect this track with another.
        Returns a list with all the times found in both tracks events
        lists.
        """

        def events_list_to_set(events):
            """Create a set with all event times and fill in those implicit
            by the events with a duration."""
            s = set()
            for event in events:
                if event.duration > 0:
                    for t in range(*event.time_interval):
                        s.add(t)
                else:
                    s.add(event.time)
            return s

        self_events = events_list_to_set(self.events)
        other_track_events = events_list_to_set(track.events)

        return sorted(list(self_events.intersection(other_track_events)))

    def invert(self):
        raise NotImplementedError

    def get_duration(self, t, ti=0):
        """
        Get the annotated duration constrained to a time interval [ti, t].
        """
        sum_ = 0
        for e in self.events:
            begin, end = e.time_interval
            # Check first all the events that completly fit inside the interval
            if begin >= ti and end <= t:
                sum_ += e.duration
                continue
            # Events that cross the ti instant
            if begin < ti and end > ti:
                if end > t:
                    sum_ += t - ti
                else:
                    sum_ += end - ti
                continue
            # Events that cross the t instant
            if begin < t and end > t:
                sum_ += t - begin
                # This assumes that it went through the other conditions
                continue
        return sum_

    def get_full_duration(self):
        """Sums up all its events duration and returns that."""
        return sum([e.duration for e in self.events])

    def plot(self, ax, y=0, h=1, ignore_duration=True, offset=5, **kwargs):
        """
        Plot the Track in a given `Axes` object.

        Each event in the Track is represented by a Rectangle or by a
        vertical line, depending if you want to ignore its duration.

        Args:
            ax: maptlotlib Axes object to plot
            y: y position of the bottom edge /point
            h: height of the rectangle / line
            ignore_duration: if True, event duration is ignored
            offset: percentage to shrink the drawn patch

        Returns:
            Axes: maptlotlib Axes object

        .. warning:: Barely tested!

        """
        offset /= 100

        for event in self.events:

            if event.duration > 0 and ignore_duration is False:
                xy = (event.time, y + (h * offset))
                w = event.duration
                rect = mpatches.Rectangle(xy, w, h - 2 * (h * offset),
                                          lw=0, **kwargs)
                ax.add_patch(rect)
            else:
                if 'lw' not in kwargs.keys():
                    kwargs['lw'] = 1
                ax.vlines(event.time, y + (h * offset),
                          (y + h) - (h * offset), **kwargs)

        return ax

    @property
    def nevents(self):
        """Number of events."""
        return len(self.events)


class Event(object):

    """
    Event

    An event happening at time `t`. Can also last for a certain `duration`
    and have some `comment`.
    """

    def __init__(self, t, duration=0, comment=""):
        self.time = t
        self.duration = duration
        self.comment = comment

    def __repr__(self):
        t = self.time_interval if self.duration > 0 else self.time
        return "[ {} ] t={}".format(self.__class__.__name__, t)

    @property
    def time_interval(self):
        if self.duration > 0:
            return (self.time, self.time + self.duration)
        else:
            return 0
