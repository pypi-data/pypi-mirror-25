from zope.interface import Interface, implementer
import attr


class Diffable(Interface):
    """
    Something that can be `diff`ed.

    """

    def __diff__(other):
        """
        Diff this object with ``other``, returning the `Difference`.

        """


class Difference(Interface):
    def explain():
        """
        Explain this difference.

        Returns:

            str: a representation of the difference

        """


@implementer(Difference)
@attr.s
class Constant(object):

    _explanation = attr.ib()

    def explain(self):
        return self._explanation


@attr.s
class _NoSpecificDiff(object):

    _one = attr.ib()

    def __diff__(self, other):
        return "{} != {}".format(self._one, other)


def diff(one, two):
    if one == two:
        return

    difference = Diffable(one, _NoSpecificDiff(one)).__diff__(two)
    return Difference(difference, Constant(explanation=difference))
