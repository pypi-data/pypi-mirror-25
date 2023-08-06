from abc import abstractmethod
from bson import ObjectId
from pymongo import MongoClient
from pymongo.results import UpdateResult, InsertOneResult


class BaseMongoDocument(object):
    """
    This class represents a structured version of a MongoDocument, it implements methods to interact with database 
    and defines base methods for every inherited document. Extend this class to create a specific document for your 
    purposes.
    """

    def __init__(self, dict_repr: dict) -> None:
        """
        Initialization and validation of init values, call it as first method in inner classes' __init__.
        
        :param dict_repr: 
        """
        self.__validate_init_values(dict_repr)
        self._id = dict_repr.get('_id', None)

    def __iter__(self) -> list:
        """
        Converts a MongoDocument instance in dict().
        :return: 
        """
        for x, y in self.__dict__.items():
            if x == '_id':
                if y is None:
                    pass
                else:
                    yield x, str(y)
            else:
                yield x, y

    def update_data(self, dict_repr: dict, partial=False) -> None:
        """
        Updates data from a dict_repr.
        
        :param dict_repr: dict 
        :return: 
        """
        self.__validate_input_values(dict_repr)

        for key in dict_repr.keys():
            if hasattr(self, key):
                setattr(self, key, dict_repr.get(key, getattr(self, key) if partial else None))

    @classmethod
    def get_collection(cls) -> str:
        """
        Returns the name of the collection of this Document. Usually it returns the class name lowered.
        
        :return: 
        """
        return cls.__name__.lower()

    @abstractmethod
    def __validate_init_values(self, dict_repr: dict) -> None:
        """
        Validates data passed as parameters for this document, make it raise an exception or use assert.
        
        :param dict_repr: dict 
        :return: None
        """
        pass

    @abstractmethod
    def __validate_input_values(self, dict_repr: dict) -> None:
        """
        Validates data passed as parameters for this document, make it raise an exception or use assert.

        :param dict_repr: dict 
        :return: None
        """
        pass

    def save(self, db: MongoClient, update=False) -> UpdateResult or InsertOneResult:
        """
        Stores this document and returns an UpdateResult or an InsertOneResult (see pymongo documentation).
        
        :param db: MongoClient
        :return: 
        """
        dict_ver = dict(self)

        if update:
            dict_ver["_id"] = dict_ver['_id'] if isinstance(dict_ver['_id'], ObjectId) else ObjectId(dict_ver["_id"])
            return db[self.__class__.get_collection()] \
                .replace_one({'_id': ObjectId(self._id)}, dict_ver)
        else:
            result = db[self.__class__.get_collection()] \
                .insert_one(dict_ver)
            self._id = result.inserted_id
            return result

    def delete(self, db: MongoClient):
        """
        Deletes this document.
        
        :param db: MongoClient
        :return: 
        """
        return db[self.__class__.get_collection()] \
            .delete_one({'_id': self._id})

    @classmethod
    def aggregate(cls, params: dict, db: MongoClient) -> list:
        """
        Returns pymongo .aggregate for this document.
        
        :param params: dict
        :param db: MongoClient
        :return: 
        """
        return db[cls.get_collection()].aggregate(params)

    @classmethod
    def find(cls, params: dict, db: MongoClient) -> list:
        """
        Returns pymongo .find for this document. Uses yield to create an iterator and instantiate a new object of 
        this document class.
        
        :param params: dict
        :param db: MongoClient
        :return: 
        """
        docs = []
        for doc in db[cls.get_collection()].find(params):
            docs.append(cls(doc))

        return docs

    @classmethod
    def get(cls, params: dict, db: MongoClient) -> object:
        """
        Returns pymongo .find_one for this document.
        
        :param params: dict
        :param db: MongoClient
        :return: 
        """
        tricks = db[cls.get_collection()].find_one(params)
        return cls(tricks)
