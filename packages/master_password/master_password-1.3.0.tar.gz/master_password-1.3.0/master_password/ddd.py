import os
import sys

_PACKAGE_DIR = os.path.abspath(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), os.pardir)
)
# Ensure that the import can happen correctly
sys.path.insert(0, _PACKAGE_DIR)

try:
    from master_password import *
    import master_password
finally:
    sys.path.pop(0)

globals().update(vars(master_password))


class RemoveInheritanceMetaMeta(type):
    def __new__(mmcs, *allowed_bases):
        for base in allowed_bases:
            if base is object:
                break
        else:
            allowed_bases += (object,)
        mcs = type.__new__(
            RemoveInheritanceMetaMeta, 'RemoveInheritanceMeta', (type,), {'mro': mmcs._mro}
        )
        mcs._allowed_bases = allowed_bases
        return mcs

    @staticmethod
    def _mro(cls):
        return (cls,) + cls._allowed_bases


class A:
    def method_a(self):
        return 'A'

    def method_b(self):
        return 'A'


class B(A):
    def method_a(self):
        return 'B'

    def method_c(self):
        return 'B'


class C(B, metaclass=RemoveInheritanceMetaMeta(A)):
    # __mro__ = (A, object)
    # _allowed_inheritance = (A,)

    def method_d(self):
        return 'C'

c = C()