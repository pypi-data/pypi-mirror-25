from sqlalchemy import Column, Integer, String, inspect, event
from groundwork_database.patterns import GwSqlPattern
from groundwork_validation.patterns import GwValidatorsPattern
from groundwork.util import gw_get


class GwDbValidatorsPattern(GwSqlPattern, GwValidatorsPattern):
    """
    Allows the validation of database model requests.

    Builds automatically hashes of table rows/model instances and validates these hashes, if a request
    is made on these rows.
    """
    def __init__(self, app, **kwargs):
        super(GwDbValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app
        self.validators.db = DbValidatorsPlugin(self)
        if not hasattr(self.app.validators, "db"):
            self.app.validators.db = DbValidatorsApplication(self.app)


class DbValidatorsPlugin:
    """
    Cares about database validators on plugin level
    """
    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app

    def register(self, name, description, db_class):
        """
        Registers a new database model and starts its validation.

        :param name: Unique name
        :param description: Meaningful description
        :param db_class: sqlalchemy based database model

        :return: Instance of DbValidator
        """
        return self.app.validators.db.register(name, description, db_class, self.plugin)

    def unregister(self, name):
        self.app.validators.db.unregister(name)

    def get(self, name):
        self.app.validators.db.get(name, self.plugin)


class DbValidatorsApplication:
    """
        Cares about database validators on application level
        """
    def __init__(self, app):
        self.app = app
        self._db_validators = {}

        self.db = self.app.databases.register("hash_db",
                                              self.app.config.get("HASH_DB", "sqlite://"),
                                              "database for hash values")

        class Hashes(self.db.Base):
            __tablename__ = "hashes"
            id = Column(Integer, primary_key=True)
            hash_id = Column(String(512), nullable=False, unique=True)
            hash = Column(String(2048), nullable=False)

        self.Hashes = self.db.classes.register(Hashes)
        self.db.create_all()

    def register(self, name, description, db_class, plugin):
        """
                Registers a new database model and starts its validation.

                :param name: Unique name
                :param description: Meaningful description
                :param db_class: sqlalchemy based database model
                :param plugin: Plugin, which registers the DbValidator

                :return: Instance of DbValidator
                """
        if name in self._db_validators.keys():
            raise KeyError("Database validator %s already registered" % name)

        self._db_validators[name] = DbValidator(name,
                                                description=description,
                                                db_class=db_class,
                                                db=self.db,
                                                hash_model=self.Hashes,
                                                plugin=plugin)

        return self._db_validators[name]

    def unregister(self, name):
        if name in self._db_validators.keys():
            del (self._db_validators[name])
        else:
            raise KeyError("Database validator %s does not exist" % name)

    def get(self, name, plugin):
        gw_get(self._db_validators, name, plugin)


class DbValidator:
    """
    Class for storing a database validator.
    For each registered database validator an instance of this class gets created and configured.
    """
    def __init__(self, name, description, db_class, db, hash_model, plugin=None):
        """

        :param name: Unique name
        :param description: Meaningful description
        :param db_class: Database model
        :param db: Database
        :param hash_model: Database model, which is used to store the hashes
        :param plugin: Plugin, which has registered the DbValidator
        """
        self.name = name
        self.description = description
        self.db = db
        self.hash_model = hash_model
        self.db_class = db_class
        self.tablename = db_class.__tablename__
        self.hash_id = ".".join([self.name, self.tablename])
        self.attributes = inspect(self.db_class).columns.keys()  # Only columns/attributes, which were defined by user
        self.plugin = plugin

        self.validator = plugin.validators.register(self.hash_id, description, attributes=self.attributes)

        # http://docs.sqlalchemy.org/en/latest/orm/events.html#instance-events
        # Calls _check_hash, if given database model instance is refreshed from a query
        event.listen(self.db_class, "refresh", self._check_hash)

        # Calls _store_hash, if given database model instance was updated by user
        event.listen(self.db_class, "after_update", self._store_hash)
        event.listen(self.db_class, "after_insert", self._store_hash)

    def _check_hash(self, target, context, attrs):
        hash_id = self._calculate_hash_id(target)
        hash_row = self.db.query(self.hash_model).filter_by(hash_id=hash_id).first()
        hash_current = hash_row.hash

        if not self.validator.validate(target, hash_current):
            raise ValidationError("Stored hash %s not valid. Calculated %s " % (hash_current,
                                                                                self.validator.hash(target)))

    def _store_hash(self, mapper, connection, target):
        new_hash = self.validator.hash(target)
        hash_id = self._calculate_hash_id(target)
        current_hash_row = self.db.query(self.hash_model).filter_by(hash_id=hash_id).first()
        if current_hash_row is None:
            current_hash_row = self.hash_model(hash_id=hash_id, hash=new_hash)
        else:
            current_hash_row.hash = new_hash

        self.db.add(current_hash_row)
        self.db.commit()

    def _calculate_hash_id(self, target):
        # We need a unique id, which identifies our hash value inside the database.
        # But the ID must not be related to the content of the db model itself, as this will change.
        return ".".join([self.hash_id, str(target.id)])


class ValidationError(BaseException):
    """
    Exception, which is thrown if a validation fails.
    """
    pass
