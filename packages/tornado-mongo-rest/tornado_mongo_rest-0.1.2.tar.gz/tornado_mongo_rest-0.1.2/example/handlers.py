from tornado_mongo_rest.handlers import BaseRestHandler
from example.trick import Trick


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
