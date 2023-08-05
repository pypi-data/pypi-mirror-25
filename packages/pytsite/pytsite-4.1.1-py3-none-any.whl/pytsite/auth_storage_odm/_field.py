"""PytSite Auth Storage ODM Fields.
"""
from bson import DBRef as _DBRef
from typing import Tuple as _Tuple, List as _List, Iterable as _Iterable, Optional as _Optional
from pytsite import odm as _odm, auth as _auth

__author__ = 'Alexander Shepetko'
__email__ = 'a@shepetko.com'
__license__ = 'MIT'


class Roles(_odm.field.UniqueStringList):
    def _get_role(self, value) -> _auth.model.AbstractRole:
        """Helper function
        """
        if isinstance(value, _auth.model.AbstractRole):
            return value
        elif isinstance(value, str):
            return _auth.get_role(uid=value)
        elif isinstance(value, _DBRef):
            return _auth.get_role(uid=str(value.id))
        else:
            raise TypeError("Field '{}': role object, str or DB ref expected, got {}".format(self.name, type(value)))

    def _on_set_storable(self, value: _Iterable[str]):
        """Hook
        """
        return [self._get_role(r) for r in value]

    def _on_get_storable(self, value: _Iterable[_auth.model.AbstractRole]):
        """Hook
        """
        return [r.uid for r in value]

    def _on_set(self, value: _Iterable, **kwargs) -> _Iterable[_auth.model.AbstractRole]:
        """Hook
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError("Field '{}': list or tuple expected, got {}".format(self.name, type(value)))

        return [self._get_role(r) for r in value]

    def _on_add(self, internal_value, value_to_add, **kwargs):
        return super()._on_add(internal_value, self._get_role(value_to_add).uid)

    def _on_sub(self, internal_value, value_to_sub, **kwargs):
        return super()._on_sub(internal_value, self._get_role(value_to_sub).uid)

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        if isinstance(arg, _auth.model.AbstractRole):
            return arg.uid
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for role in arg:
                if isinstance(role, _auth.model.AbstractRole):
                    clean_arg.append(role.uid)
                else:
                    clean_arg.append(role)
            return clean_arg
        else:
            return arg


class User(_odm.field.Abstract):
    """Field to store reference to user.
    """

    def __init__(self, name: str, **kwargs):
        """Init.

        :param default:
        :param nonempty: bool
        :param allow_anonymous: bool
        :param allow_system: bool
        """
        self._allow_anonymous = kwargs.get('allow_anonymous', False)
        self._allow_system = kwargs.get('allow_system', False)

        super().__init__(name, **kwargs)

    def _resolve_user_uid(self, value) -> str:
        if isinstance(value, str):
            return value
        elif isinstance(value, _DBRef):
            return str(value.id)
        elif isinstance(value, _auth.model.AbstractUser):
            if value.is_anonymous:
                if not self._allow_anonymous:
                    raise ValueError('Anonymous user is not allowed here')
                return 'ANONYMOUS'
            elif value.is_system:
                if not self._allow_system:
                    raise ValueError('System user is not allowed here')
                return 'SYSTEM'
            else:
                return value.uid
        else:
            raise TypeError("Field '{}': user object, str or DB ref expected, got {}.".
                            format(self._name, type(value)))

    def _on_set_default(self, value) -> str:
        # Internally this field stores only user's UID as string
        return self._on_set(value) if value else value

    def _on_set(self, value, **kwargs) -> str:
        """Hook. Transforms externally set value to internal value.
        """
        # Internally this field stores only user's UID as string
        return self._resolve_user_uid(value)

    def _on_get(self, internal_value: str, **kwargs) -> _Optional[_auth.model.AbstractUser]:
        """Hook. Transforms internal value to external one.
        """
        if internal_value == 'ANONYMOUS':
            return _auth.get_anonymous_user()
        elif internal_value == 'SYSTEM':
            return _auth.get_system_user()
        elif internal_value:
            return _auth.get_user(uid=internal_value)
        else:
            return None

    def sanitize_finder_arg(self, arg):
        """Hook. Used for sanitizing Finder's query argument.
        """
        if isinstance(arg, _auth.model.AbstractUser):
            if arg.is_anonymous:
                return 'ANONYMOUS'
            elif arg.is_system:
                return 'SYSTEM'
            else:
                return arg.uid
        elif isinstance(arg, (list, tuple)):
            clean_arg = []
            for user in arg:
                if isinstance(user, _auth.model.AbstractUser):
                    clean_arg.append(user.uid)
                else:
                    clean_arg.append(user)
            return clean_arg
        else:
            return arg


class Users(User):
    """Field to store list of references to users.
    """

    def __init__(self, name: str, **kwargs):
        """Init.
        """
        super().__init__(name, default=kwargs.get('default', []), **kwargs)

    def _on_set_default(self, value):
        return self._on_set(value) if value else value

    def _on_set(self, value: _Iterable, **kwargs) -> list:
        """Hook. Transforms externally set value to internal value.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError("Field '{}': list or tuple expected, got {}.".format(self.name, type(value)))

        clean_value = []
        for v in value:
            clean_value.append(self._resolve_user_uid(v))

        return clean_value

    def _on_get(self, internal_value: list, **kwargs) -> _Tuple[_auth.model.AbstractUser, ...]:
        """Hook. Transforms internal value to external one.
        """
        if internal_value is None:
            internal_value = []

        r = []
        for uid in internal_value:
            try:
                r.append(_auth.get_user(uid=uid))
            except _auth.error.UserNotExist:
                pass

        return tuple(r)

    def _on_add(self, internal_value: list, value_to_add, **kwargs):
        if internal_value is None:
            internal_value = []

        internal_value.append(self._resolve_user_uid(value_to_add))

        return internal_value

    def _on_sub(self, internal_value: list, value_to_sub, **kwargs):
        if internal_value is None:
            internal_value = []

        value_to_sub = self._resolve_user_uid(value_to_sub)

        return [uid for uid in internal_value if uid != value_to_sub]
