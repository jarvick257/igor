from .content import Content


class Renderer:
    def render(self, content: Content):
        _ = content
        raise NotImplementedError()
