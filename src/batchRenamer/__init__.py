# MIT License
#
# Copyright (c) 2023 Divine Decimate Darkey ( D.Cube )
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import re
import os
from string import Template


__version__ = 1.0


class BatchRenamer(Template):

    """
    A simple but powerful batch renamer.

    Rename multiple files or directories elegantly with
    rich features such as
    - fully customizable numeric sequence
    - upper or lowercase alphabetic sequence
    - replace substrings in old name with new one (works with pattern matching)
    - able to reuse old file name in new one
    """

    delimiter = "%"

    def __init__(self, path, template, pad=0):
        self.path = path
        self.pad = pad
        self.files = []

        super().__init__(template)

    @staticmethod
    def __fix_stop(_start, _stop, _step):
        """
        Change the `stop` value to adapt with the `step`
        whenever a change is made to it in order
        to produce the optimal number of items.
        """
        return _start + 1 + ((_stop - 1) * _step)

    def fetch_files(self):
        """Fetch files to seq_rename from `path`"""
        for entry in os.scandir(self.path):
            if entry.is_file():
                self.files.append(entry)

    def generate_a_seq(self, upper=False):
        """
        Generates an alphabetic sequence
        """
        start = 65 if upper else 97
        stop = ((len(self.files) % 26) + start)

        seq = (chr(n) for n in range(start, stop))
        return seq

    def generate_n_seq(self, start=1, step=1):
        """
        Generates a numeric sequence with the provided parameters.
        Args:
            `start`: the number at which the sequence should start
            `step`: the successive intervals that should be taken

        The end of the sequence is internally defaults to the
        number of files fetched.

        Returns a generator"""
        stop = self.__fix_stop(_start=start, _step=step, _stop=len(self.files))
        seq = (n for n in range(start, stop, step))
        return seq

    def rename(self, names):
        """
        Renames fetched files with provided names
        """
        for file_, name in zip(self.files, names):
            path, _ = os.path.split(file_.path)
            os.rename(src=file_.path, dst=os.path.join(path, name))

    def replace(self, old: str, new: str, *, match_case=True, count=1):
        """
        Replace the occurrence of substring `old` with
        the string `new`.
        The old string can be a RE pattern, in this case, a match
        will be replaced with new.

        Returns the new names
        NOTE: This does not rename the files but just performs the
        replacement and returns the new names which can later be supplied
        to `rename` to actually rename the files.
        """
        pattern = re.compile(old) if match_case else re.compile(old, re.IGNORECASE)
        new_names = [pattern.sub(new, file.name, count) for file in self.files]

        return new_names

    def expand_template(self, a_seq=None, n_seq=None, upper=False):
        """
        Renames fetched files using template.
        For further customization, you may provide
        custom sequence for alphabets or numbers.
        """
        template = self

        # set user args or generate sequence with default
        # parameters
        a_seq = a_seq or self.generate_a_seq(upper=upper)
        n_seq = n_seq or self.generate_n_seq()

        names = []

        for a, n, file in zip(a_seq, n_seq, self.files):
            basename, ext = os.path.splitext(file.name)
            # construct new name
            name = template.substitute(
                    d=basename, a=a, n=str(n).zfill(self.pad)) + ext
            names.append(name)
        
        return names


__all__ = [
    "BatchRenamer",
    "__version__"
]
