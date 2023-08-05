class Datasource(object):
    """
    The data source object. The object does not maintain any stateful information.
    """

    def __init__(self, driver, **kwargs):
        self.driver = driver
        self.attributes = kwargs

    @property
    def protocol(self):
        return self.attributes['protocol'] if 'protocol' in self.attributes else None

    @property
    def host(self):
        return self.attributes['host'] if 'host' in self.attributes else None

    @property
    def port(self):
        return self.attributes['port'] if 'port' in self.attributes else None

    @property
    def user(self):
        return self.attributes['user'] if 'user' in self.attributes else None

    @property
    def password(self):
        return self.attributes['password'] if 'password' in self.attributes else None

    @property
    def db(self):
        return self.attributes['db'] if 'db' in self.attributes else None

    @property
    def uri(self):
        return self.attributes['uri'] if 'uri' in self.attributes else None


class Connection(object):
    """
    The connection object, which is opened with data source and its implementation is also
    related to the context
    """

    def __init__(self, datasource):
        assert isinstance(datasource, Datasource), 'Invalid connection provided'
        self.datasource = datasource

    def load(self, table, **kwargs):
        raise NotImplementedError

    def load_query(self, query, **kwargs):
        raise NotImplementedError

    def store(self, df, table, **kwargs):
        raise NotImplementedError

    def init_record_if_absent(self):
        raise NotImplementedError

    @property
    def accept(self):
        raise NotImplementedError

    @property
    def can_produce(self):
        raise NotImplementedError

    def last_record(self, task_name):
        raise NotImplementedError

    def create_record(self, task_name, new_checkpoint):
        raise NotImplementedError

    def commit_record(self, txn_id):
        raise NotImplementedError

    def rollback_record(self, txn_id, err):
        raise NotImplementedError
