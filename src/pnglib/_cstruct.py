
from dataclasses import dataclass
from ._cenum import TextCompression, TextKeyword

@dataclass
class Color:
    """color structure"""
    red: int = None
    """red (RGB*)"""
    green: int = None
    """green (RGB*)"""
    blue: int = None
    """blue (RGB*)"""
    gray: int = None
    """luminance (G*)"""
    alpha: int = None
    """alpha channel (*A)"""
    index: int = None
    """index in palette"""

    def __post_index__(self):
        assert self.is_rgb != self.is_gray, 'invalid colortype'

    @property
    def is_rgb(self):
        return all(c is not None for c in [self.red, self.green, self.blue])

    @property
    def is_grayscale(self):
        return self.gray is not None

    @property
    def is_palette(self):
        return self.index is not None

    @property
    def has_alpha(self):
        return self.alpha is not None

    def pixel(self):
        if self.is_rgb:
            px = [self.red, self.green, self.blue]
        elif self.is_grayscale:
            px = [self.gray]
        if self.has_alpha:
            px.append(self.alpha)
        return px


@dataclass
class Text:
    """"""
    compression: TextCompression
    """"""
    key: TextKeyword
    """"""
    text: str
    """"""

    def __len__(self):
        """length of text"""
        return len(self.text)
    
    def __repr__(self):
        if len(self.text) > 10:
            text = self.text[:10] + ' ...'
        return (
            'Text(' +
            f'compression={self.compression}, ' +
            f'key="{self.key}", ' +
            f'text="{text}" [length={len(self.text)}] ' +
            ')'
        )
