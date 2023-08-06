import json

import tornado.web
from bson import ObjectId
from pymongo import MongoClient
from tornado.escape import json_decode
from tornado.web import RequestHandler
from tornado_cors import CorsMixin

from trick_book.trick import Trick


class BaseRestHandler(CorsMixin, RequestHandler):
    """
    Implements an abstract Rest Api Handler for a Mongodb based resource set.
    
    Return codes adhere to the following stackoverflow post:
    https://stackoverflow.com/questions/2342579/http-status-code-for-update-and-delete
    """

    # Value for the Access-Control-Allow-Origin header.
    # Default: None (no header).
    CORS_ORIGIN = '*'

    # Value for the Access-Control-Allow-Headers header.
    # Default: None (no header).
    CORS_HEADERS = 'Content-Type, content-type'

    # Value for the Access-Control-Allow-Methods header.
    # Default: Methods defined in handler class.
    # None means no header.
    CORS_METHODS = 'POST, GET, PUT, PATCH, DELETE, OPTIONS'

    # Value for the Access-Control-Allow-Credentials header.
    # Default: None (no header).
    # None means no header.
    CORS_CREDENTIALS = True

    # Value for the Access-Control-Max-Age header.
    # Default: 86400.
    # None means no header.
    CORS_MAX_AGE = 21600

    # Value for the Access-Control-Expose-Headers header.
    # Default: None
    CORS_EXPOSE_HEADERS = 'Location, X-WP-TotalPages, content-type, Content-Types'

    def initialize(self, db: MongoClient):
        self.db = db

    def get_resource_type(self):
        """
        
        :return: 
        """
        return None

    def get_resources(self) -> []:
        """
        :return: 
        """
        return self.get_resource_type().find({}, self.db)

    def get(self, model_id=None):
        """
        Retrieves a resource from a given model_id.
        
        :param model_id: 
        :return: None 
        """
        if not model_id:
            resources = self.get_resources()
            self.write(json.dumps([dict(r) for r in resources]))
        else:
            resource = Trick.get({'_id': ObjectId(model_id)}, self.db)
            self.write(json.dumps(dict(resource)))

    def patch(self, model_id=None, *args, **kwargs):
        """
        Partially updates fields specified in data passed as JSON encoded request body.

        :param model_id: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        data = json_decode(self.request.body)

        instance = self.get_resource_type().get({'_id': ObjectId(model_id)}, self.db)

        instance.update_data(data, partial=True)

        instance.save(self.db, update=True)

        self.write(dict(instance))

    def put(self, model_id=None, *args, **kwargs):
        """
        Completely replaces an existing resource with data passed as JSON encoded request body.
        
        :param model_id: 
        :param args: 
        :param kwargs: 
        :return: 
        """
        data = json_decode(self.request.body)

        instance = self.get_resource_type().get({'_id': ObjectId(model_id)}, self.db)

        instance.update_data(data)

        instance.save(self.db, update=True)

        self.write(dict(instance))

    def post(self, *args, **kwargs):
        """
        Stores a new resource using data passed as JSON encoded request body.
        
        :param args: 
        :param kwargs: 
        :return: 
        """
        # Escaping body data as seen in https://stackoverflow.com/a/28140966/3909609

        data = json_decode(self.request.body)

        instance = self.get_resource_type()(data)

        instance.save(self.db)

        # Created status code
        self.set_status(201)

        self.write(dict(instance))

    def delete(self, model_id=None, *args, **kwargs):
        """
        Deletes an existing resource from storage.
        
        :param model_id: 
        :param args: 
        :param kwargs: 
        :return: 
        """

        instance = self.get_resource_type().get({'_id': ObjectId(model_id)}, self.db)

        instance.delete(self.db)

        self.write(model_id)


# Todo: in type hints PyCharm suggests me that any subclass of RequestHandler is not compatible with the hint,
# Todo: further inspection needed on type hints syntax

def make_rest_endpoint_rule(resource_name: str, handler: tornado.web.RequestHandler, db: MongoClient,
                            name: str = None, prefix: str = '') -> list:
    """
    Creates the urls for a certain resource with a given handler and a MongoClient db, supports custom reverse name 
    for the created url regex.
    
    The default url is r'/<resource_name>/<optional_id>/", it could be extended with a prefix obtaining the following
    r'<prefix>/<resource_name>/<optional_id>/"
    
    :param resource_name: str, the name of the resources provided by this endpoint 
    :param handler: RequestHandler, the class the handles requests for this endpoint 
    :param db: 
    :param name: 
    :return: 
    """
    return [
        tornado.web.url(r"%s/%s/([A-Za-z0-9]+)?/?" % (prefix, resource_name),
                        handler,
                        dict(db=db),
                        name=name if name is not None else resource_name)
    ]
