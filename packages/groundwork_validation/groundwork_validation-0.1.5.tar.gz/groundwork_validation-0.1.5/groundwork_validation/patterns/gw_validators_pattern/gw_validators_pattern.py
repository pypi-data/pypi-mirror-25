import hashlib
import pickle

from groundwork.patterns import GwBasePattern
from groundwork.util import gw_get


class GwValidatorsPattern(GwBasePattern):
    """
    Allows the creation of hashes for python objects (and its validation).
    """

    def __init__(self, app, **kwargs):
        super(GwValidatorsPattern, self).__init__(app, **kwargs)
        self.app = app

        self.validators = ValidatorsPlugin(self)
        if not hasattr(self.app, "validators"):
            self.app.validators = ValidatorsApplication(self)


class ValidatorsPlugin:
    """
    Cares about the Validator handling on plugin level.
    """

    def __init__(self, plugin):
        self.plugin = plugin
        self.app = plugin.app

    def register(self, name, description, algorithm=None, attributes=None):
        """
        Registers a new validator on plugin level.

        :param name: Unique name of the validator
        :param description: Helpful description of the validator
        :param algorithm: A hashlib compliant function. If None, hashlib.sha256 is taken.
        :param attributes: List of attributes, for which the hash must be created. If None, all contained
                           attributes are used.
        :return: Validator instance
        """
        if algorithm is None:
            algorithm = hashlib.sha256
        return self.app.validators.register(name, description, self.plugin, algorithm=algorithm, attributes=attributes)

    def unregister(self, name):
        self.app.validators.unregister(name)

    def get(self, name):
        """
        Returns a single or a list of validator instance, which were registered by the current plugin.

        :param name: Name of the validator. If None, all validators of the current plugin are returned.
        :return: Single or list of Validator instances
        """
        self.app.validators.get(name, self.plugin)


class ValidatorsApplication:
    """
    Cares about the Validator handling on application level.
    """
    def __init__(self, app):
        self.app = app
        self._validators = {}

    def register(self, name, description, plugin, algorithm=None, attributes=None):
        """
        Registers a new validator on application level.

        :param name: Unique name of the validator
        :param description: Helpful description of the validator
        :param algorithm: A hashlib compliant function. If None, hashlib.sha256 is taken.
        :param attributes: List of attributes, for which the hash must be created. If None, all contained
                           attributes are used.
        :param plugin: Plugin instance, for which the validator gets registered.
        :return: Validator instance
        """
        if name in self._validators.keys():
            raise KeyError("Validator %s already registered" % name)

        if algorithm is None:
            algorithm = hashlib.sha256

        self._validators[name] = Validator(name, description,
                                           algorithm=algorithm,
                                           attributes=attributes,
                                           plugin=plugin)

        return self._validators[name]

    def unregister(self, name):
        if name in self._validators.keys():
            del(self._validators[name])
        else:
            raise KeyError("Validator %s does not exist" % name)

    def get(self, name, plugin):
        """
        Returns a single or a list of validator instance

        :param name: Name of the validator. If None, all validators are returned.
        :param plugin: Plugin instance, which has registered the requested validator.
                       If None, all validators are returned.
        :return: Single or list of Validator instances
        """
        gw_get(self._validators, name, plugin)


class Validator:
    """
    Represent the final validator, which provides functions to hash a given python object and to validate a
    python object against a given hash.
    """
    def __init__(self, name, description, algorithm=None, attributes=None, plugin=None):
        self.name = name
        self.description = description
        self.plugin = plugin
        if algorithm is None:
            algorithm = hashlib.sha256
        self.algorithm = algorithm
        self.attributes = attributes

    def validate(self, data, hash_string, no_pickle=False):
        """
        Validates a python object against a given hash

        :param data: Python object
        :param hash_string: hash as string, which must be compliant to the configured hash algorithm of
                            the used validator.
        :param no_pickle: If True data is not pickled before hash is calculated.
                          Helpful, if data is already serialised (like file inputs)
        :return: True, if object got validated by hash. Else False
        """
        if self.hash(data, no_pickle=no_pickle) == hash_string:
            return True
        return False

    def hash(self, data, hash_object=None, return_hash_object=False, strict=False, no_pickle=False):
        """
        Generates a hash of a given Python object.

        :param data: Python object
        :param return_hash_object: If true, the complete hashlib object is returned
                                   instead of a hexdigest representation as string.
        :param hash_object: An existing  hash object, which will be updated. Instead of creating a new one.
        :param strict: If True, all configured attributes **must** exist in the given data, otherwise an exception
                       is thrown.
        :param no_pickle: If True data is not pickled before hash is calculated.
                          Helpful, if data is already serialised (like file inputs)
        :return: hash as string
        """
        if hash_object is None:
            current_hash = self.get_hash_object()
        else:
            current_hash = hash_object

        if self.attributes is None:
            if not no_pickle:
                current_hash.update(pickle.dumps(data))
            else:
                current_hash.update(data)
        else:
            for attribute in self.attributes:
                if strict and hasattr(data, attribute) is False:
                    raise AttributeError("Data has no attribute called %s" % attribute)
                current_hash.update(pickle.dumps(getattr(data, attribute, None)))

        if return_hash_object:
            return current_hash
        return current_hash.hexdigest()

    def get_hash_object(self):
        """
        Returns a hash object, which can be used as input for validate functions.

        :return: An unused hash object
        """
        return self.algorithm()
