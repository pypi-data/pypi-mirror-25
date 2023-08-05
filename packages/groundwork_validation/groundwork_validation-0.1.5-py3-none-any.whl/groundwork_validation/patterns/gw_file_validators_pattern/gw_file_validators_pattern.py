from groundwork_validation.patterns import GwValidatorsPattern


class GwFileValidatorsPattern(GwValidatorsPattern):
    """
    Allows the creation and validation of hashes for given files.

    Usage::

        from groundwork_validation.patterns import GwFileValidatorsPattern

        class My_Plugin(GwFileValidatorsPattern):
            def __init__(self, app, **kwargs):
                self.name = "My_Plugin"
                super(My_Plugin, self).__init__(app, **kwargs)

            def activate(self):
                my_hash = self.validators.file.hash("/path/to/file.txt")
                self.validators.file.validate("/path/to/file.txt", my_hash)

    """
    def __init__(self, app, **kwargs):
        super(GwFileValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app
        self.validators.file = FileValidatorsPlugin(self)


class FileValidatorsPlugin:
    def __init__(self, plugin):
        self.plugin = plugin
        self._validator = None

    def hash(self, file, validator=None, hash_file=None, blocksize=65536, return_hash_object=False):
        """
        Creates a hash of a given file.

        :param file: file path of the hashable file
        :param validator: validator, which shall be used. If none is given, a default validator will be used.
                          validator should be registered be the GwValidatorsPattern. Default is None
        :param hash_file: Path to a file, which is used to store the calculated hash value. Default is None
        :param blocksize: Size of each file block, which is used to update the hash. Default is 65536
        :param return_hash_object: Returns the hash object instead of the hash itself. Default is False
        :return: string, which represents the hash (hexdigest)
        """
        if validator is None:
            if self._validator is None:
                self._validator = self.plugin.validators.register("cmd_validator_%s" % self.plugin.name,
                                                                  "CMD validator for plugin %s" % self.plugin.name)
            validator = self._validator

        with open(file, 'rb') as afile:
            buf = afile.read(blocksize)
            hash_object = validator.get_hash_object()
            while len(buf) > 0:
                hash_object = validator.hash(buf, hash_object=hash_object, return_hash_object=True)
                buf = afile.read(blocksize)

        if hash_file is not None:
            with open(hash_file, "w") as hfile:
                hfile.write(hash_object.hexdigest())

        if return_hash_object:
            return hash_object
        else:
            return hash_object.hexdigest()

    def validate(self, file, hash_value=None, hash_file=None, validator=None, blocksize=65536):
        """
        Validates a file against a given hash.
        The given hash can be a string or a hash file, which must contain the hash on the first row.

        :param file: file path as string
        :param hash_value: hash, which is used for comparision
        :param hash_file:  file, which contains a hash value
        :param validator: groundwork validator, which shall be used. If None is given, a default one is used.
        :param blocksize: Size of each file block, which is used to update the hash.
        :return: True, if validation is correct. Otherwise False
        """
        if hash_value is None and hash_file is None:
            raise ValueError("hash_value or hash_file must be set.")
        if hash_value is not None and hash_file is not None:
            raise ValueError("Only hash_value OR hash_file must be set.")

        if hash_file is not None:
            with open(hash_file) as hfile:
                hash_value = hfile.readline()

        current_hash = self.hash(file, validator=validator, blocksize=blocksize)
        if current_hash == hash_value:
            return True
        return False
