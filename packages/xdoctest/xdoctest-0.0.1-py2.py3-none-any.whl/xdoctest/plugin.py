# encoding: utf-8
"""
plugin file for registration with pytest.

discover and run doctests in modules and test files.

Adapted from the original `pytest/_pytest/doctest.py` module at:
    https://github.com/pytest-dev/pytest
"""
from __future__ import absolute_import, division, print_function
# import traceback
import pytest
from _pytest._code.code import ExceptionInfo, ReprFileLocation, TerminalRepr  # NOQA
from _pytest.fixtures import FixtureRequest


def pytest_addoption(parser):
    group = parser.getgroup("collect")
    group.addoption("--xdoctest-modules",
                    action="store_true", default=False,
                    help="run doctests in all .py modules using new style parsing",
                    dest="xdoctestmodules")
    group.addoption("--xdoctest-glob",
                    action="append", default=[], metavar="pat",
                    help="xdoctests file matching pattern, default: test*.txt",
                    dest="xdoctestglob")
    group.addoption("--xdoctest-ignore-syntax-errors",
                    action="store_true", default=False,
                    help="ignore xdoctest SyntaxErrors",
                    dest="xdoctest_ignore_syntax_errors")

    # parser.addini('xdoctest_optionflags', 'option flags for xdoctests',
    #               type="args", default=["ELLIPSIS"])
    # parser.addini("xdoctest_encoding", 'encoding used for xdoctest files', default="utf-8")
    # group.addoption("--xdoctest-report",
    #                 type=str.lower, default="udiff",
    #                 help="choose another output format for diffs on xdoctest failure",
    #                 choices=DOCTEST_REPORT_CHOICES,
    #                 dest="xdoctestreport")
    # group.addoption("--xdoctest-glob",
    #                 action="append", default=[], metavar="pat",
    #                 help="xdoctests file matching pattern, default: test*.txt",
    #                 dest="xdoctestglob")


def pytest_collect_file(path, parent):
    config = parent.config
    if path.ext == ".py":
        if config.option.xdoctestmodules:
            return XDoctestModule(path, parent)


class ReprFailXDoctest(TerminalRepr):

    def __init__(self, reprlocation, lines):
        self.reprlocation = reprlocation
        self.lines = lines

    def toterminal(self, tw):
        for line in self.lines:
            tw.line(line)
        self.reprlocation.toterminal(tw)


class XDoctestItem(pytest.Item):
    def __init__(self, name, parent, example=None):
        super(XDoctestItem, self).__init__(name, parent)
        self.example = example
        self.obj = None
        self.fixture_request = None

    def setup(self):
        if self.example is not None:
            self.fixture_request = _setup_fixtures(self)
            globs = dict(getfixture=self.fixture_request.getfixturevalue)
            for name, value in self.fixture_request.getfixturevalue('xdoctest_namespace').items():
                globs[name] = value
            self.example.globs.update(globs)

    def runtest(self):
        # _check_all_skipped(self.example)
        #     if all_skipped:
        #         pytest.skip('all tests skipped by +SKIP option')
        import re
        m = re.match(r'>>>\s*#\s*pytest.skip', self.example.docsrc, flags=re.IGNORECASE)
        if m is not None:
            pytest.skip('doctest encountered skip directive')
        self.example.run()
        # self.runner.run(self.example)

    def repr_failure(self, excinfo):
        return super(XDoctestItem, self).repr_failure(excinfo)
        # return self.dtest.repr_failure()
        # import doctest
        # if excinfo.errisinstance((doctest.DocTestFailure,
        #                           doctest.UnexpectedException)):
        #     doctestfailure = excinfo.value
        #     example = doctestfailure.example
        #     test = doctestfailure.test
        #     filename = test.filename
        #     if test.lineno is None:
        #         lineno = None
        #     else:
        #         lineno = test.lineno + example.lineno + 1
        #     message = excinfo.type.__name__
        #     reprlocation = ReprFileLocation(filename, lineno, message)
        #     checker = _get_checker()
        #     report_choice = _get_report_choice(self.config.getoption("doctestreport"))
        #     if lineno is not None:
        #         lines = doctestfailure.test.docstring.splitlines(False)
        #         # add line numbers to the left of the error message
        #         lines = ["%03d %s" % (i + test.lineno + 1, x)
        #                  for (i, x) in enumerate(lines)]
        #         # trim docstring error lines to 10
        #         lines = lines[example.lineno - 9:example.lineno + 1]
        #     else:
        #         lines = ['EXAMPLE LOCATION UNKNOWN, not showing all tests of that example']
        #         indent = '>>>'
        #         for line in example.source.splitlines():
        #             lines.append('??? %s %s' % (indent, line))
        #             indent = '...'
        #     if excinfo.errisinstance(doctest.DocTestFailure):
        #         lines += checker.output_difference(example,
        #                                            doctestfailure.got, report_choice).split("\n")
        #     else:
        #         inner_excinfo = ExceptionInfo(excinfo.value.exc_info)
        #         lines += ["UNEXPECTED EXCEPTION: %s" %
        #                   repr(inner_excinfo.value)]
        #         lines += traceback.format_exception(*excinfo.value.exc_info)
        #     return ReprFailXDoctest(reprlocation, lines)
        # else:

    def reportinfo(self):
        return self.fspath, self.example.lineno, "[xdoctest] %s" % self.name


class XDoctestTextfile(pytest.Module):
    obj = None

    def collect(self):
        pass
        # import doctest

        # inspired by doctest.testfile; ideally we would use it directly,
        # but it doesn't support passing a custom checker
        # encoding = self.config.getini("xdoctest_encoding")
        # text = self.fspath.read_text(encoding)
        # filename = str(self.fspath)
        # name = self.fspath.basename
        # globs = {'__name__': '__main__'}

        # optionflags = get_optionflags(self)
        # runner = doctest.DebugRunner(verbose=0, optionflags=optionflags,
        #                              checker=_get_checker())
        # _fix_spoof_python2(runner, encoding)

        # from xdoctest import doctest_patch  # NOQA
        # DocTestParser = doctest_patch.XDocTestParser
        # # DocTestParser = doctest.DocTestParser  # NOQA

        # parser = DocTestParser()
        # test = parser.get_doctest(text, globs, name, filename, 0)
        # if test.examples:
        #     yield XDoctestItem(test.name, self, runner, test)


# def _check_all_skipped(test):
#     """raises pytest.skip() if all examples in the given DocTest have the SKIP
#     option set.
#     """
#     import doctest
#     all_skipped = all(x.options.get(doctest.SKIP, False) for x in test.examples)
#     if all_skipped:
#         pytest.skip('all tests skipped by +SKIP option')


class XDoctestModule(pytest.Module):
    def collect(self):
        from xdoctest import core
        modpath = str(self.fspath)

        try:
            calldefs = core.module_calldefs(modpath)
        except SyntaxError:
            if self.config.getvalue('xdoctest_ignore_syntax_errors'):
                pytest.skip('unable to import module %r' % self.fspath)
            else:
                raise

        for callname, calldef in calldefs.items():
            docstr = calldef.docstr
            if calldef.docstr is not None:
                # TODO: handle more than just google-style
                lineno = calldef.doclineno
                for example in core.parse_google_docstr_examples(docstr, callname, modpath, lineno=lineno):
                    if not example.is_disabled():
                        name = example.unique_callname
                        yield XDoctestItem(name, self, example)

        # import doctest
        # if self.fspath.basename == "conftest.py":
        #     module = self.config.pluginmanager._importconftest(self.fspath)

        # uses internal doctest module parsing mechanism
        # from xdoctest import doctest_patch  # NOQA
        # DocTestParser = doctest_patch.XDocTestParser
        # # DocTestParser = doctest.DocTestParser  # NOQA

        # parser = DocTestParser()
        # finder = doctest.DocTestFinder(parser=parser)
        # optionflags = get_optionflags(self)
        # runner = doctest.DebugRunner(verbose=0, optionflags=optionflags,
        #                              checker=_get_checker())

        # for test in finder.find(module, module.__name__):
        #     if test.examples:  # skip empty doctests
        #         yield XDoctestItem(test.name, self, runner, test)


def _setup_fixtures(xdoctest_item):
    """
    Used by XDoctestTextfile and XDoctestItem to setup fixture information.
    """
    def func():
        pass

    xdoctest_item.funcargs = {}
    fm = xdoctest_item.session._fixturemanager
    xdoctest_item._fixtureinfo = fm.getfixtureinfo(node=xdoctest_item, func=func,
                                                   cls=None, funcargs=False)
    fixture_request = FixtureRequest(xdoctest_item)
    fixture_request._fillfixtures()
    return fixture_request


# def _get_checker():
#     """
#     Returns a doctest.OutputChecker subclass that takes in account the
#     ALLOW_UNICODE option to ignore u'' prefixes in strings and ALLOW_BYTES
#     to strip b'' prefixes.
#     Useful when the same doctest should run in Python 2 and Python 3.

#     An inner class is used to avoid importing "doctest" at the module
#     level.
#     """
#     if hasattr(_get_checker, 'LiteralsOutputChecker'):
#         return _get_checker.LiteralsOutputChecker()

#     import doctest
#     import re

#     class LiteralsOutputChecker(doctest.OutputChecker):
#         """
#         Copied from doctest_nose_plugin.py from the nltk project:
#             https://github.com/nltk/nltk

#         Further extended to also support byte literals.
#         """

#         _unicode_literal_re = re.compile(r"(\W|^)[uU]([rR]?[\'\"])", re.UNICODE)
#         _bytes_literal_re = re.compile(r"(\W|^)[bB]([rR]?[\'\"])", re.UNICODE)

#         def check_output(self, want, got, optionflags):
#             res = doctest.OutputChecker.check_output(self, want, got,
#                                                      optionflags)
#             if res:
#                 return True

#             allow_unicode = optionflags & _get_allow_unicode_flag()
#             allow_bytes = optionflags & _get_allow_bytes_flag()
#             if not allow_unicode and not allow_bytes:
#                 return False

#             else:  # pragma: no cover
#                 def remove_prefixes(regex, txt):
#                     return re.sub(regex, r'\1\2', txt)

#                 if allow_unicode:
#                     want = remove_prefixes(self._unicode_literal_re, want)
#                     got = remove_prefixes(self._unicode_literal_re, got)
#                 if allow_bytes:
#                     want = remove_prefixes(self._bytes_literal_re, want)
#                     got = remove_prefixes(self._bytes_literal_re, got)
#                 res = doctest.OutputChecker.check_output(self, want, got,
#                                                          optionflags)
#                 return res

#     _get_checker.LiteralsOutputChecker = LiteralsOutputChecker
#     return _get_checker.LiteralsOutputChecker()


# def _get_allow_unicode_flag():
#     """
#     Registers and returns the ALLOW_UNICODE flag.
#     """
#     import doctest
#     return doctest.register_optionflag('ALLOW_UNICODE')


# def _get_allow_bytes_flag():
#     """
#     Registers and returns the ALLOW_BYTES flag.
#     """
#     import doctest
#     return doctest.register_optionflag('ALLOW_BYTES')


# def _get_report_choice(key):
#     """
#     This function returns the actual `doctest` module flag value, we want to do it as late as possible to avoid
#     importing `doctest` and all its dependencies when parsing options, as it adds overhead and breaks tests.
#     """
#     import doctest

#     return {
#         DOCTEST_REPORT_CHOICE_UDIFF: doctest.REPORT_UDIFF,
#         DOCTEST_REPORT_CHOICE_CDIFF: doctest.REPORT_CDIFF,
#         DOCTEST_REPORT_CHOICE_NDIFF: doctest.REPORT_NDIFF,
#         DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE: doctest.REPORT_ONLY_FIRST_FAILURE,
#         DOCTEST_REPORT_CHOICE_NONE: 0,
#     }[key]
# DOCTEST_REPORT_CHOICE_NONE = 'none'
# DOCTEST_REPORT_CHOICE_CDIFF = 'cdiff'
# DOCTEST_REPORT_CHOICE_NDIFF = 'ndiff'
# DOCTEST_REPORT_CHOICE_UDIFF = 'udiff'
# DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE = 'only_first_failure'

# DOCTEST_REPORT_CHOICES = (
#     DOCTEST_REPORT_CHOICE_NONE,
#     DOCTEST_REPORT_CHOICE_CDIFF,
#     DOCTEST_REPORT_CHOICE_NDIFF,
#     DOCTEST_REPORT_CHOICE_UDIFF,
#     DOCTEST_REPORT_CHOICE_ONLY_FIRST_FAILURE,
# )


# def _fix_spoof_python2(runner, encoding):
#     """
#     Installs a "SpoofOut" into the given DebugRunner so it properly deals with unicode output. This
#     should patch only doctests for text files because they don't have a way to declare their
#     encoding. Doctests in docstrings from Python modules don't have the same problem given that
#     Python already decoded the strings.

#     This fixes the problem related in issue #2434.
#     """
#     from _pytest.compat import _PY2
#     if not _PY2:
#         return

#     from doctest import _SpoofOut

#     class UnicodeSpoof(_SpoofOut):

#         def getvalue(self):
#             result = _SpoofOut.getvalue(self)
#             if encoding:
#                 result = result.decode(encoding)
#             return result

#     runner._fakeout = UnicodeSpoof()

# def _get_flag_lookup():
#     import doctest
#     return dict(DONT_ACCEPT_TRUE_FOR_1=doctest.DONT_ACCEPT_TRUE_FOR_1,
#                 DONT_ACCEPT_BLANKLINE=doctest.DONT_ACCEPT_BLANKLINE,
#                 NORMALIZE_WHITESPACE=doctest.NORMALIZE_WHITESPACE,
#                 ELLIPSIS=doctest.ELLIPSIS,
#                 IGNORE_EXCEPTION_DETAIL=doctest.IGNORE_EXCEPTION_DETAIL,
#                 COMPARISON_FLAGS=doctest.COMPARISON_FLAGS,
#                 ALLOW_UNICODE=_get_allow_unicode_flag(),
#                 ALLOW_BYTES=_get_allow_bytes_flag(),
#                 )


# def get_optionflags(parent):
#     optionflags_str = parent.config.getini("xdoctest_optionflags")
#     flag_lookup_table = _get_flag_lookup()
#     flag_acc = 0
#     for flag in optionflags_str:
#         flag_acc |= flag_lookup_table[flag]
#     return flag_acc


@pytest.fixture(scope='session')
def xdoctest_namespace():
    """
    Inject names into the xdoctest namespace.
    """
    return dict()
