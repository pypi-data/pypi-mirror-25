from traitlets import HasTraits, Unicode, default


class BuildInfo(HasTraits):

    version = Unicode()

    @default('version')
    def default_version(self):
        return "UNKNOWN"

