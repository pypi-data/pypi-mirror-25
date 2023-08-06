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