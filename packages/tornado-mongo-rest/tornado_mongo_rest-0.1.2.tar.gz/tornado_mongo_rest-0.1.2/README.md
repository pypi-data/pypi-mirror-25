# tornado_mongo_rest

## Description

**tornado_mongo_rest** is a lightweight and extensible implementation of REST specification on top of MongoDB documents 
for 
the 
Tornado web server.

## Usage

Three steps:

#### Create your own ConcreteDocument 
Extend **BaseMongoDocument** class

```python
from tornado_mongo_rest.model import BaseMongoDocument


class Trick(BaseMongoDocument):
    COLLECTION = 'trick'

    @classmethod
    def get_collection(cls) -> str:
        """
        returns the name of the mongodb collection
        """
        return Trick.COLLECTION

    def __init__(self, dict_repr: dict) -> None:
        """
        :param dict_repr: 
        """
        super(Trick, self).__init__(dict_repr)

        """
        The title of this trick
        """
        self.title = dict_repr['title']
        """
        Tags associated to this trick i.e. #css #javascript
        """
        self.tags = dict_repr['tags']
        """
        The content of the trick, could be an html content
        """
        self.content = dict_repr['content']

    def __validate_init_values(self, dict_repr):
        """
        :param dict_repr: 
        :return: 
        """
        assert 'title' in dict_repr and 'tags' in dict_repr and 'content' in dict_repr, 'Invalid init data'

    def __validate_input_values(self, dict_repr: dict):
        """
        :param dict_repr: 
        :return: 
        """
        assert 'title' in dict_repr and 'tags' in dict_repr and 'content' in dict_repr, 'Invalid init data'
```

### Create your own ConcreteHandler 
Extend **BaseRestHandler** class

```python
from tornado_mongo_rest.handlers import BaseRestHandler
from trick_book.trick import Trick


class TrickHandler(BaseRestHandler):
    """
    Handler for Trick resources
    """

    def get_resources(self):
        tags = self.get_arguments('tags')

        if len(tags) > 0:
            return self.get_resource_type().find({"tags": {"$in": tags}}, self.db)
        else:
            return self.get_resource_type().find({}, self.db)

    def get_resource_type(self):
        return Trick
```
### Register your handler 
Use **make_rest_endpoint_rule** method and add it to tornado.web.Application

```python
import tornado.ioloop
import tornado.web
from pymongo import MongoClient

from tornado_mongo_rest.handlers import make_rest_endpoint_rule
from trick_book.handlers import TrickHandler

db = MongoClient(host=MONGODB_URI)[MONGODB_DATABASE]


def make_app():
    handlers = make_rest_endpoint_rule('trick', TrickHandler, db)

    return tornado.web.Application(handlers=handlers, debug=True)
```

And that's it!