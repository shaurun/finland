import datetime
from django.contrib.sessions.backends.base import SessionBase, CreateError

from FinLand.mango import database


class SessionStore(SessionBase):
    """
    Implements MongoDB session store.
    """
    def load(self):
        s = database.sessions.find_one( {
                'session_key': self.session_key,
                'expire_date': {'$gt': datetime.datetime.now()}})
        if s:
            return self.decode(s['session_data'])
        else:
            self.create()
            return {}

    def exists(self, session_key):
        if database.sessions.find_one( {'session_key': session_key} ):
            return True
        else:
            return False

    def create(self):
        while True:
            self.session_key = self._get_new_session_key()
            try:
                # Save immediately to ensure we have a unique entry in the
                # database.
                self.save(must_create=True)
            except CreateError:
                # Key wasn't unique. Try again.
                continue
            self.modified = True
            self._session_cache = {}
            return

    def save(self, must_create=False):
        """
        Saves the current session data to the database. If 'must_create' is
        True, a database error will be raised if the saving operation doesn't
        create a *new* entry (as opposed to possibly updating an existing
        entry).
        """
        obj = {
            'session_key': self.session_key,
            'session_data': self.encode(self._get_session(no_load=must_create)),
            'expire_date': self.get_expiry_date()
            }
        res = database.sessions.update(
                {'session_key': self.session_key},
                {'$set': obj},
                upsert=True,
                safe=True,
                )
        if res['err'] is not None and must_create:
            raise CreateError

    def delete(self, session_key=None):
        if session_key is None:
            if self._session_key is None:
                return
            session_key = self._session_key
        database.sessions.remove({'session_key': session_key})