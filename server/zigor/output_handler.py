from .content import Content


class OutputHandler:
    def render(self, content: Content):
        raise NotImplementedError()
