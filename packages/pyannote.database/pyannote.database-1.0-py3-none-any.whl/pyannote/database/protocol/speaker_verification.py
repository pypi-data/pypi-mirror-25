#!/usr/bin/env python
# encoding: utf-8

# The MIT License (MIT)

# Copyright (c) 2016 CNRS

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


from .protocol import Protocol


class SpeakerVerificationProtocol(Protocol):
    """Speaker verification protocol

    Parameters
    ----------
    preprocessors : dict or (key, preprocessor) iterable
        When provided, each protocol item (dictionary) are preprocessed, such
        that item[key] = preprocessor(**item). In case 'preprocessor' is not
        callable, it should be a string containing placeholder for item keys
        (e.g. {'wav': '/path/to/{uri}.wav'})
    """
    def trn_iter(self):
        raise NotImplementedError(
            'Custom speaker verification protocol should implement "trn_iter".')

    def dev_enroll_iter(self):
        raise NotImplementedError(
            'Custom speaker verification protocol should implement "dev_enroll_iter".')

    def dev_test_iter(self):
        raise NotImplementedError(
            'Custom speaker verification protocol should implement "dev_test_iter".')

    def tst_enroll_iter(self):
        raise NotImplementedError(
            'Custom speaker verification protocol should implement "tst_enroll_iter".')

    def tst_test_iter(self):
        raise NotImplementedError(
            'Custom speaker verification protocol should implement "tst_test_iter".')

    def train(self):
        """Iterate over the training set

This will yield dictionaries with the followings keys:

* uri: str
  unique recording identifier
* database: str
  unique database identifier
* channel: int
  index of resource channel to use
* target: str
  unique target identifier

as well as keys coming from the provided preprocessors.

Usage
-----
>>> for item in protocol.train():
...     uri = item['uri']
...     channel = item['channel']
...     target = item['target']
        """
        for item in self.trn_iter():
            yield self.preprocess(item)

    def development_enroll(self):
        """Iterate over the development set enrollments

This will yield dictionaries with the followings keys:

* uri: str
  uniform (or unique) resource identifier
* channel: int
  index of resource channel to use

as well as keys coming from the provided preprocessors.

Usage
-----
>>> for item in protocol.development_enroll():
...     uri = item['uri']
...     channel = item['channel']
        """
        for item in self.dev_enroll_iter():
            yield self.preprocess(item)

    def development_test(self):
        """Iterate over the development set tests

This will yield dictionaries with the followings keys:

* uri: str
  uniform (or unique) resource identifier
* channel: int
  index of resource channel to use

as well as keys coming from the provided preprocessors.

Usage
-----
>>> for item in protocol.development_test():
...     uri = item['uri']
...     channel = item['channel']
        """
        for item in self.dev_tst_iter():
            yield self.preprocess(item)

    def test_enroll(self):
        """Iterate over the test set targets

This will yield dictionaries with the followings keys:

* uri: str
  uniform (or unique) resource identifier
* channel: int
  index of resource channel to use
* target: str
  unique target identifier

as well as keys coming from the provided preprocessors.

Usage
-----
>>> for item in protocol.test_enroll():
...     uri = item['uri']
...     channel = item['channel']
...     target = item['target']
        """
        for item in self.tst_enroll_iter():
            yield self.preprocess(item)

    def test_test(self):
        """Iterate over the test set tests

This will yield dictionaries with the followings keys:

* uri: str
  uniform (or unique) resource identifier
* channel: int
  index of resource channel to use

as well as keys coming from the provided preprocessors.

Usage
-----
>>> for item in protocol.test_test():
...     uri = item['uri']
...     channel = item['channel']
        """
        for item in self.dev_tst_iter():
            yield self.preprocess(item)

#     def stats(self, subset):
#         """Obtain global statistics on a given subset
#
# Parameters
# ----------
# subset : {'train', 'development', 'test'}
#
# Returns
# -------
# stats : dict
#     Dictionary with the followings keys:
#     * annotated: float
#       total duration (in seconds) of the parts that were manually annotated
#     * annotation: float
#       total duration (in seconds) of actual (speech) annotations
#     * n_files: int
#       number of files in the subset
#     * labels: dict
#       maps speakers with their total speech duration (in seconds)
#         """
#
#         annotated = 0.
#         annotation = 0.
#         n_files = 0
#         speakers = {}
#
#         for item in getattr(self, subset)():
#             annotated += item['annotated'].duration()
#             annotation += item['annotation'].get_timeline().duration()
#             for label, duration in item['annotation'].chart():
#                 if label not in labels:
#                     labels[label] = 0.
#                 labels[label] += duration
#             n_files += 1
#
#         return {'annotated': annotated,
#                 'annotation': annotation,
#                 'n_files': n_files,
#                 'labels': labels}
