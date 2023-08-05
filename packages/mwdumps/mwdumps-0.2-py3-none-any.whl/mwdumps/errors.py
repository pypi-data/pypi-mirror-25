class Error(Exception):
    pass


class WikiConnectionError(Error):
    pass


class DumpCompletionStateUncertainError(Error):
    pass


class NoCompleteDumpsError(Error):
    pass
