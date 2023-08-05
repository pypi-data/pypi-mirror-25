from groundwork_validation.patterns import GwDbValidatorsPattern


class GwDbValidator(GwDbValidatorsPattern):
    """
    Automatically adds and activate validation to eahc database model.
    """

    def __init__(self, app, **kwargs):
        self.name = self.__class__.__name__
        super(GwDbValidator, self).__init__(app, **kwargs)

    def activate(self):
        """
        During activation, a receiver is created and listing for new database models.
        Existing database models are collected and validation gets activated.

        :return: None
        """
        dbs = self.app.databases.get()
        for key, db in dbs.items():
            models = db.classes.get()
            for key, model in models.items():
                self._register_db_model(db, model)

        self.signals.connect(receiver="db_validation_setup",
                             signal="db_class_registered",
                             function=self._receiver_db_validation,
                             description="Setups the validations checks for newly registered database classes")

    def deactivate(self):
        """
        Currently nothing happens here *sigh*

        :return: None
        """
        pass

    def _receiver_db_validation(self, plugin, *args, **kwargs):
        """
        Receiver functions, which gets called, if a new database model is registered.
        Will activate validation for the new database model.

        :param plugin: Plugin instance, which has send the signal
        :param args: arguments
        :param kwargs: keyword arguments ("database" and "db_class" are expected)
        :return: None
        """
        database = kwargs.get("database", None)
        db_class = kwargs.get("db_class", None)

        if database is None or db_class is None:
            return

        self._register_db_model(database, db_class)

    def _register_db_model(self, database, db_class):
        """
        Registers a new database validator for the given db model.

        :param database: database instance
        :param db_class: database model
        :return: DatabaseValidator
        """
        # We must not validate our own hash database tables.
        # If we do so, this would lead to an infinity loop.
        if database.name == "hash_db":
            return

        return self.validators.db.register(name="%s_db_validator" % db_class.name,
                                           description="Database validator for %s" % db_class.name,
                                           db_class=db_class)
