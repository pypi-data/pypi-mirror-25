# coding: utf-8

import abc

import six

from il2fb.commons.exceptions import IL2FBParsingException
from il2fb.commons.structures import BaseStructure


class Event(six.with_metaclass(abc.ABCMeta, BaseStructure)):
    """
    Base event structure.

    """

    def __init__(self, **kwargs):
        for key in self.__slots__:
            setattr(self, key, kwargs[key])

        super(Event, self).__init__()

    @property
    def name(self):
        return self.__class__.__name__

    @abc.abstractproperty
    def verbose_name(self):
        """
        Human-readable name of event.

        """

    def to_primitive(self, context=None):
        primitive = super(Event, self).to_primitive(context)
        primitive.update({
            'name': self.name,
            'verbose_name': six.text_type(self.verbose_name),
        })
        return primitive

    def __repr__(self):
        return "<Event {0} {1}>".format(self.name, self.to_primitive())


class ParsableEvent(Event):
    """
    Base event which can be parsed from string.

    """
    transformers = tuple()

    @classmethod
    def transform(cls, data):
        for transformer in cls.transformers:
            transformer(data)

        return data

    @abc.abstractproperty
    def matcher(self):
        """
        A callable for matching strings.

        """

    @classmethod
    def from_s(cls, s):
        match = cls.matcher(s)

        if match:
            data = cls.transform(match.groupdict())
            return cls(**data)


class EventParsingException(IL2FBParsingException):
    pass
