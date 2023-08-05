from collections import defaultdict


class EntityDb:
    # Contains {logged user id: EntityDb}, since it seems that the ID/hash
    # combination every user has of everyone else depends on who's logged in.
    # It's also static since this won't change
    _databases = {}

    @staticmethod
    def get_db(user_id):
        return EntityDb._databases.get(user_id, EntityDb())

    def __init__(self):
        self._enabled = True
        self._id_entity = {}
        self._username_entity = {}

    def __getitem__(self, item):
        if isinstance(item, int):
            return self._id_entity[item]
        elif isinstance(item, str):
            if item.startswith('@'):
                item = item.strip('@')
            item = item.lower()
            return self._username_entity[item]
        else:
            raise KeyError('Invalid key')

    def __contains__(self, item):
        if isinstance(item, int):
            return item in self._id_entity
        elif isinstance(item, str):
            if item.startswith('@'):
                item = item.strip('@')
            return item.lower() in self._username_entity
        else:
            return False

    def add(self, entity):
        if not self._enabled:
            return

        username = getattr(entity, 'username', '').lower()
        old_entity = self._id_entity.get(entity.id)
        if old_entity:
            # Update the username dictionary iff the username has changed
            old_username = getattr(old_entity, 'username', '').lower()
            if username != old_username:
                try:
                    del self._username_entity[old_username]
                except KeyError:
                    pass

                if username:
                    self._username_entity[username] = old_entity

            # Update the old entity rather than changing the reference,
            # so all the old references can be kept and still be valid.
            old_entity.__dict__.update(entity.__dict__)
        else:
            # Adding a new one, no need to update old references
            self._id_entity[entity.id] = entity
            if username:
                self._username_entity[username] = entity

    def clear(self, disable=None):
        if disable:
            self.enabled = False

        self._id_entity.clear()
        self._username_entity.clear()
