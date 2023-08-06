#!/usr/bin/env python
from __future__ import print_function

import argparse
import fnmatch
import inspect
import os
import re
import sys

REGEXP_SEMICOLON_OK = re.compile(r'(?:\s*;;\s*|\s+\\;\s*)$')
REGEXP_SEMICOLON_WARN = re.compile('.*\s*;\s*$')

W201 = "W201 Trailing whitespace"
W202 = "W202 Blank line contains whitespace"
W203 = "W203 Trailing semicolon"
W204 = "W204 No newline at end of file"
W205 = "W205 Multiple newlines at end of file"


def filename_match(filename, patterns, default=True):
    """Check if patterns contains a pattern that matches filename.

    If patterns is not specified, this always returns True.
    """
    if not patterns:
        return default
    return any(fnmatch.fnmatch(filename, pattern) for pattern in patterns)


def checker_trailing_whitespace(physical_line, **args):
    """Trailing whitespace is superfluous.

    Okay: echo Test#
    W201: echo Test #
    Okay: #
    W202:  #
    """
    physical_line = physical_line.rstrip('\n')    # chr(10), newline
    physical_line = physical_line.rstrip('\r')    # chr(13), carriage return
    physical_line = physical_line.rstrip('\x0c')  # chr(12), form feed, ^L
    stripped = physical_line.rstrip(' \t\v')
    if physical_line != stripped:
        if stripped:
            return len(stripped), W201
        else:
            return 0, W202


def checker_no_newline_on_last_line(physical_line, last_line=False, **args):
    """No newline on last line."""
    if not last_line:
        return

    if physical_line.rstrip() == physical_line:
        return len(physical_line), W204


def checker_multiple_newlines_at_end_of_file(physical_line, last_line=False, **args):
    """Multiple newlines at end of file."""
    if not last_line:
        return

    if not physical_line.strip():
        return 0, W205


def checker_trailing_semicolon(physical_line, **args):
    """Trailing semicolon is superfluous.

    Okay: echo Test#
    W203: echo Test;#
    """
    if not REGEXP_SEMICOLON_OK.search(physical_line):
        if REGEXP_SEMICOLON_WARN.search(physical_line):
            return physical_line.rfind(';'), W203


class Violation(object):
    """Represents a single violation."""

    __slots__ = ['_filename', '_line', '_line_number', '_offset', '_text']

    def __init__(self, filename, line, line_number, offset, text):
        self._filename = filename
        self._line = line
        self._line_number = line_number
        self._offset = offset
        self._text = text

    def __str__(self):
        return "%s:%s:%s: %s" % (self._filename, self._line_number,
                                 self._offset, self._text)

    @property
    def line(self):
        return self._line[:-1]

    @property
    def pointer(self):
        return ' '*self._offset + '^'


class StyleGuide(object):
    """Bash style guide."""

    def __init__(self, options):
        self._options = options
        self._reporter = Reporter(options.show_source)
        self._checkers = self._load_checkers()
        self._errors_count = 0
        self.excluded_dirs = []

    @property
    def errors_count(self):
        return self._errors_count

    def _load_checkers(self):
        """Load checkers from the current module."""
        checkers = []
        current_module = sys.modules.get(__name__)
        if current_module is not None:
            for name, func in inspect.getmembers(current_module,
                                                 inspect.isfunction):
                if name.startswith('checker'):
                    if name.endswith('trailing_semicolon') and \
                       not self._options.trailing_semicolon:
                        continue
                    elif (name.endswith('trailing_whitespace') and
                          not self._options.trailing_whitespace):
                        continue
                    elif (name.endswith('no_newline_on_last_line') and
                          not self._options.no_end_newline):
                        continue
                    elif (name.endswith('multiple_newlines_at_end_of_file') and
                          not self._options.multiple_newlines_at_end):
                        continue

                    checkers.append((name, func))

        if self._options.verbose > 1:
            print("Loaded %s checker(s)." % len(checkers))
            for name, checker in checkers:
                print(" - %s" % name)
            print()

        return checkers

    def check_paths(self, paths=None):
        """Run all checks on the paths."""
        try:
            for path in paths or ["."]:
                if os.path.isdir(path):
                    self._check_dir(path)
        except KeyboardInterrupt:
            print("... stopped")

    def _exclude_dir(self, root):
        if not self._options.exclude_dir:
            return False

        root_dirs = root.split('/')
        for exclude_dir in self._options.exclude_dir:
            for root_dir in root_dirs:
                if re.match(exclude_dir, root_dir):
                    if root_dir not in self.excluded_dirs:
                        self.excluded_dirs.append(root_dir)
                        if self._options.verbose > 2:
                            print("Excluding directory '%s'" % root_dir)
                    return True
        return False

    def _exclude_file(self, root, filename):
        if (self._options.include and not filename_match(
                filename, self._options.include)):
            if self._options.verbose > 2:
                print("Excluding file '%s' (not in includes '%s')" %
                      (os.path.join(root, filename), self._options.include))
            return True

        if not self._options.exclude:
            return False
        if filename_match(filename, self._options.exclude):
            if self._options.verbose > 2:
                print("Excluding file '%s' (matches exclude '%s')" %
                      (os.path.join(root, filename), self._options.exclude))
            return True
        return False

    def _check_dir(self, path):
        """Check all files in the given directory and all subdirectories."""
        for root, dirs, files in os.walk(path):
            if self._exclude_dir(root):
                continue
            for filename in sorted(files):
                if self._exclude_file(root, filename):
                    continue

                if filename_match(filename, self._options.file_patterns):
                    if self._options.verbose:
                        print("Checking %s" % filename)
                    self._check_file(os.path.join(root, filename))

    def _check_file(self, filename):
        """"Run checks for a given file."""
        with open(filename) as fp:
            lines = fp.readlines()

        for line_number, line in enumerate(lines, 1):
            for name, checker in self._checkers:
                result = checker(line, last_line=(line_number == len(lines)))
                if result is not None:
                    self._errors_count += 1
                    offset, text = result
                    violation = Violation(filename=filename,
                                          line=line,
                                          line_number=line_number,
                                          offset=offset,
                                          text=text)
                    self._report(violation)

    def _report(self, violation):
        """Report a violation using reporter."""
        self._reporter.report(violation)


class Reporter(object):
    """Standard output violations reporter."""

    def __init__(self, show_source=False):
        self._show_source = show_source

    def report(self, violation):
        """Report given violations."""
        print(violation)
        if self._show_source:
            print(violation.line)
            print(violation.pointer)


def parse_args():
    parser = argparse.ArgumentParser("Lint files for trailing characters")
    parser.add_argument('-v', '--verbose', action="count", default=0,
                        help='increase output verbosity')
    parser.add_argument('--version', action="store_true", help='show version')
    parser.add_argument('-p', '--file-patterns', action="append",
                        help="file pattern to match. Default: '%(default)s'")
    parser.add_argument('-ml', '--multiple-newlines-at-end', action="store_true",
                        help="warn about multiple empty lines at end of file.")
    parser.add_argument('-nel', '--no-end-newline', action="store_true",
                        help="warn about no newline at end of file'")
    parser.add_argument('--show-source', action='store_true',
                        help="show source code for each error")
    parser.add_argument('--include', action='append',
                        help="include files matching this pattern")
    parser.add_argument('--exclude', action='append',
                        help="exclude files matching this pattern")
    parser.add_argument('--exclude-dir', action='append',
                        help="exclude files in directories matching this pattern")
    parser.add_argument('--shell', action='store_true',
                        help="Check shell scripts. (Adds '*.sh' to --file-patterns)")
    parser.add_argument('--trailing-whitespace', action='store_true',
                        dest='trailing_whitespace', default=True,
                        help="Check trailing whitespace.")
    parser.add_argument('--no-trailing-whitespace', action='store_false',
                        dest='trailing_whitespace',
                        help="Check trailing whitespace.")
    parser.add_argument('--trailing-semicolon', action='store_true',
                        dest='trailing_semicolon', default=False,
                        help="Check trailing semicolon.")
    parser.add_argument('--no-trailing-semicolon', action='store_false',
                        dest='trailing_semicolon',
                        help="Check trailing semicolon.")
    parser.add_argument("paths",  nargs='+', help="input")
    return parser.parse_args()


def main():
    args = parse_args()
    if args.version:
        from whitespacelint import __version__
        print("Version: %s" % __version__)
        sys.exit()

    if args.shell:
        args.file_patterns.append(["*.sh"])
        args.trailing_semicolon = True

    guide = StyleGuide(args)
    guide.check_paths(args.paths)
    if guide.errors_count:
        sys.exit(1)


if __name__ == "__main__":
    main()
