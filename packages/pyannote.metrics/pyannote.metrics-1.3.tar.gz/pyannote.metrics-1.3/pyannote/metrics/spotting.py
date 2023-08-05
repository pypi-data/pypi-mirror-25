#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2017 CNRS

# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:

# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.

# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

# AUTHORS
# Hervé BREDIN - http://herve.niderb.fr

from __future__ import unicode_literals

import numpy as np
from .base import BaseMetric
from pyannote.core import Segment

NEVER = np.inf


class LowLatencySpeakerSpotting(BaseMetric):
    """Evaluation of low-latency speaker spotting

    Parameters
    ----------
    thresholds : (n_thresholds, ) array
        Detection thresholds.
    latencies : (n_latencies, ) array
        Allowed latencies.
    """

    @classmethod
    def metric_name(cls):
        return "Low-latency speaker spotting"

    @classmethod
    def metric_components(cls):
        return ['target', 'non_target',
                'true_positive', 'false_positive',
                'true_negative', 'false_negative']

    def __init__(self, thresholds=None, latencies=None, **kwargs):
        super(LowLatencySpeakerSpotting, self).__init__(**kwargs)
        self.thresholds = thresholds
        self.latencies = latencies

    def compute_components(self, reference, scores, **kwargs):
        """

        Parameters
        ----------
        reference : Annotation
            Target speaker occurrences. Empty reference stands for non-target
            trials.
        scores : SlidingWindowFeature
            Each score is the result of processing "up to" the end of the
            corresponding window.

        """

        n = len(scores.data)
        n_thresholds = len(self.thresholds)
        n_latencies = len(self.latencies)

        # find first time scores is greater or equal to each threshold
        maxcum = np.maximum.accumulate(scores.data)
        indices = np.searchsorted(maxcum, self.thresholds, side='left')

        # compute corresponding timestamps as the "end" of each window
        # inf means alarm is never triggered
        triggered = np.array([
            scores.sliding_window[i].end if i < n else NEVER
            for i in indices])

        timeline = reference.get_timeline(copy=False)
        expected = timeline[0].start if timeline else np.inf

        # "target trial"
        if expected < NEVER:

            target, non_target = 1, 0

            # for target trial, a negative can never be a true negative
            true_negative = 0

            # if the system triggers an alarm too early,
            # this is a false positive, whatever the allowed latency
            false_positive = triggered < expected
            # NOTE this does not depend on the allowed latency

            # if the system triggers an alarm within the expected time range (i.e.
            # after the expected time and before the end of the allowed latency),
            # this is a true positive
            true_positive = \
                (triggered[:, np.newaxis] <= expected + self.latencies[np.newaxis, :]) & \
                (triggered[:, np.newaxis] >= expected)

            # if the system triggers an alarm after the allowed latency
            # (or not all), this is a false negative
            false_negative = \
                triggered[:, np.newaxis] > expected + self.latencies[np.newaxis, :]

        # "non-target trial"
        else:
            target, non_target = 0, 1

            # for non-target trial, a positive can never be a true positive
            # whatever the threshold nor the allowed latency
            true_positive = 0

            # for non-target trial, a negative can never be a false negative
            # whatever the threshold nor the allowed latency
            false_negative = 0

            # as soon as the system triggers an alarm,
            # this is necessary a false positive
            false_positive = triggered < NEVER
            # NOTE this does not depend on the allowed latency

            # if it doesn't trigger an alarm,
            # this is a true negative
            true_negative = triggered == NEVER
            # NOTE this does not depend on the allowed latency

        return {
            'target': target,
            'non_target': non_target,
            'true_positive': true_positive,
            'false_positive': false_positive,
            'true_negative': true_negative,
            'false_negative': false_negative
        }

    def compute_metric(self, detail):

        fpr = detail['false_positive'] / max(1, detail['non_target'])
        fnr = detail['false_negative'] / max(1, detail['target'])

        return {
            'false_positive_rate': fpr,
            'false_negative_rate': fnr,
        }




class LowLatencySpeakerSpotting2(BaseMetric):
    """Evaluation of low-latency speaker spotting

    Parameters
    ----------
    thresholds : (n_thresholds, ) array
        Detection thresholds.
    """

    @classmethod
    def metric_name(cls):
        return "Low-latency speaker spotting 2"

    @classmethod
    def metric_components(cls):
        return {
            'target': 0.,
            'non_target': 0.,
            'true_positive': 0.,
            'false_positive': 0.,
            'true_negative': 0.,
            'false_negative': 0.}

    def __init__(self, thresholds=None, **kwargs):
        super(LowLatencySpeakerSpotting2, self).__init__(**kwargs)
        self.thresholds = thresholds

    def compute_components(self, reference, scores, **kwargs):
        """

        Parameters
        ----------
        reference : Annotation
            Target speaker occurrences. Empty reference stands for non-target
            trials.
        scores : SlidingWindowFeature
            Each score is the result of processing "up to" the end of the
            corresponding window.

        """

        n = len(scores.data)
        n_thresholds = len(self.thresholds)

        extent = reference.get_timeline(copy=False).extent()
        # timeline = reference.get_timeline(copy=False)
        # first, last = (timeline[0].start, timeline[-1].end) if timeline \
        #               else (NEVER, NEVER)

        # find first time scores is greater or equal to each threshold
        maxcum = np.maximum.accumulate(scores.data)
        indices = np.searchsorted(maxcum, self.thresholds, side='left')

        # compute corresponding timestamps as the "end" of each window
        # NEVER (== np.inf) means alarm is never triggered
        triggered = np.array([
            scores.sliding_window[i].end if i < n else NEVER
            for i in indices])

        # "target trial"
        if extent.start < NEVER:

            target, non_target = 1, 0

            # for target trial, a negative can never be a true negative
            true_negative = 0

            ## if the system triggers an alarm too early,
            ## this is a false positive
            #false_positive = triggered < extent.start
            # even if the system triggers an alarm too early,
            # we assume this is correct
            false_positive = 0

            # if the system triggers an alarm after the extent.start time
            # this is a true positive
            true_positive = (triggered >= extent.start) * (triggered < NEVER)

            # if the system does not trigger an alarm, this is a false negative
            false_negative = triggered == NEVER

            # how long it took to trigger the alarm
            absolute_latency = triggered - extent.start
            absolute_latency[~true_positive] = np.nan

            # how much of target speaker did we need before the alarm
            speaker_latency = []
            for i, t in enumerate(triggered):
                if false_negative[i]:
                    speaker_latency.append(np.nan)
                    continue

                # heard = Segment(extent.start, t)
                # if not heard:
                #     speaker_latency.append(0.)
                #     continue
                # speaker_latency.append(
                #     reference.crop(heard).get_timeline(copy=False).duration())

                heard = Segment(extent.start, t)
                if not heard:
                    speaker_latency.append(0.)
                else:
                    speaker_latency.append(
                        reference.crop(heard).get_timeline(copy=False).duration())

            speaker_latency = np.array(speaker_latency)

        # "non-target trial"
        else:
            target, non_target = 0, 1

            # for non-target trial, a positive can never be a true positive
            # whatever the threshold nor the allowed latency
            true_positive = 0

            # for non-target trial, a negative can never be a false negative
            # whatever the threshold nor the allowed latency
            false_negative = 0

            # as soon as the system triggers an alarm,
            # this is necessary a false positive
            false_positive = triggered < NEVER

            # if it doesn't trigger an alarm,
            # this is a true negative
            true_negative = triggered == NEVER

            absolute_latency, speaker_latency = None, None

        return {
            'target': target,
            'non_target': non_target,
            'true_positive': true_positive,
            'false_positive': false_positive,
            'true_negative': true_negative,
            'false_negative': false_negative,
            'absolute_latency': absolute_latency,
            'speaker_latency': speaker_latency
        }

    def compute_metric(self, detail):

        fpr = detail['false_positive'] / max(1, detail['non_target'])
        fnr = detail['false_negative'] / max(1, detail['target'])

        return {
            'false_positive_rate': fpr,
            'false_negative_rate': fnr,
        }
