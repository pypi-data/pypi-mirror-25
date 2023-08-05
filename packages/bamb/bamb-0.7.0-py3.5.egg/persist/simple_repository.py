from pymongo import MongoClient
from service import repositories
from domain import base as ab
from bson.objectid import ObjectId
from domain import exceptions
from io import StringIO
from common import constants
import bamb


class SimpleMongoDbRepository(repositories.CrudRepository):

    def __init__(self, app=None):
        if not isinstance(app, bamb.Bamb):
            app = bamb.Bamb.singleton()
        self.__client = MongoClient(host=app.conf.MONGODB_HOST, port=app.conf.MONGODB_PORT,
                                    tz_aware=app.conf.MONGODB_TZ_AWARE)
        self._app = app

    def load(self, key):
        if key is None:
            return None

        if isinstance(key, str):
            try:
                i = key.index("[")
            except ValueError:
                i = -1
            if i > 0:
                path = eval(key[i:])
                key = ObjectId(key[0:i])
                return self.load_partial(key, path)

        coll = self.get_collection()
        d = coll.find_one(SimpleMongoDbRepository.get_oid(key))
        return SimpleMongoDbRepository.load_from_document(d)

    def delete(self, key):
        coll = self.get_collection()
        d = coll.find_one_and_delete(SimpleMongoDbRepository.get_oid(key))
        return SimpleMongoDbRepository.load_from_document(d)

    def insert(self, obj, key=None):
        d = SimpleMongoDbRepository.prepare_document(obj, key)
        if constants.FIELD_ID in d.keys():
            i = d[constants.FIELD_ID]
            if i is None:
                d.pop(constants.FIELD_ID)
        coll = self.get_collection()
        return coll.insert_one(d).inserted_id

    def update(self, obj, key=None, upsert=False):
        d = SimpleMongoDbRepository.prepare_document(obj, key)
        coll = self.get_collection()
        key = d.get(constants.FIELD_ID, None)
        if key is None and not upsert:
            raise exceptions.IllegalArgumentException("can not update document, key missing")
        r = coll.update_one({constants.FIELD_ID: key}, {"$set": d}, upsert=upsert)
        if r.matched_count == 1:
            return d.get(constants.FIELD_ID, None)
        else:
            if r.upserted_id is None:
                raise exceptions.NotFoundException("document not found, oid is : " +
                                                   d.get(constants.FIELD_ID, "None").__str__())
            else:
                return r.upserted_id

    def update_partial(self, obj, path=None):
        if not isinstance(obj, ab.ListTree):
            raise exceptions.IllegalArgumentException("partial update can only be applied to ListTrees!")
        if obj.is_root:
            raise exceptions.IllegalOperationException("partial update can not be applied to root!")
        root_id = SimpleMongoDbRepository.get_oid(obj.lt_root().object_id)
        if root_id is None:
            raise exceptions.IllegalOperationException("root element has not been saved!")
        if path is None:
            p = obj.lt_path()
        else:
            p = path
        s = SimpleMongoDbRepository.compose_path(p)
        d = SimpleMongoDbRepository.prepare_document(obj)
        coll = self.get_collection()
        r = coll.update_one({constants.FIELD_ID: root_id}, {"$set": {s: d}}, upsert=True)

        if r.matched_count == 1:
            return root_id
        else:
            raise exceptions.OperationFailedException("failed to apply partial update on : " +
                                                      str(root_id))

    #coll.findOne({_id:ObjectId("a203efcd023942a203efcd02")},{_ListTree__lt_children:{"$slice":[1,1]}})

    def load_partial(self, key, path):
        f = SimpleMongoDbRepository.compose_path(path)
        coll = self.get_collection()
        d = coll.find_one({constants.FIELD_ID: SimpleMongoDbRepository.get_oid(key)},
                          {constants.FIELD_CHILDREN: {"$slice":[path[0], 1]}})
        obj = SimpleMongoDbRepository.load_from_document(d)
        path[0] = 0
        o = obj.child(path)
        return o

    def save(self, obj, key=None, path=None):
        if isinstance(obj, ab.ListTree):
            if not obj.is_root:
                return self.update_partial(obj, path)
        if key is None:
            i = obj._id
            if i is None:
                return self.insert(obj)
            else:
                return self.update(obj, None, upsert=True)
        else:
            return self.update(obj, key, upsert=True)

    @staticmethod
    def check_document(obj):
        if not isinstance(obj, ab.EasySerializable):
            raise exceptions.IllegalArgumentException("object should be instance of EasySerializable!")
        return True

    def get_collection(self):
        db = self.__client.get_database(self._app.conf.MONGODB_DB)
        colls = db.collection_names(include_system_collections=False)
        if self.table_name not in colls:
            db.create_collection(self.table_name)
        return db.get_collection(self.table_name)

    @staticmethod
    def oid_accommodation(doc, oid_as_object=False):
        if doc is None:
            return None
        if isinstance(doc, dict):
            d = doc
        else:
            if isinstance(doc, ab.EasySerializable):
                d = doc.__dict__
            else:
                raise exceptions.IllegalArgumentException("invalid document!")

        oid = d.get(constants.FIELD_ID, None)
        if oid is not None:
            if oid_as_object:
                if not isinstance(oid, ObjectId):
                    d[constants.FIELD_ID] = ObjectId(oid)
            else:
                if isinstance(oid, ObjectId):
                    d[constants.FIELD_ID] = oid.__str__()

    @staticmethod
    def get_oid(oid):
        if oid is None:
            return None
        if isinstance(oid, ObjectId):
            return oid
        return ObjectId(oid)

    @staticmethod
    def prepare_document(obj, key=None):
        if isinstance(obj, ab.EasySerializable):
            obj = obj.es_to_dict()
        if not isinstance(obj, dict):
            raise exceptions.IllegalArgumentException("invalid document!")
        SimpleMongoDbRepository.oid_accommodation(obj, oid_as_object=True)
        if key is not None:
            obj[constants.FIELD_ID] = SimpleMongoDbRepository.get_oid(key)
        return obj

    @staticmethod
    def load_from_document(doc):
        if doc is None:
            return None
        if not isinstance(doc, dict):
            raise exceptions.IllegalArgumentException("document is not a dict!")
        if ab.EasySerializable.is_wrapped_dict(doc):
            doc = ab.EasySerializable.es_load(doc)
        SimpleMongoDbRepository.oid_accommodation(doc, False)
        return doc

    #coll.update({_id:ObjectId("a203efcd023942a203efcd02")},{$set:{"_ListTree__lt_children.1._ListTree__lt_children.1.name":"definite update"}})

    @staticmethod
    def compose_path(path):
        f = StringIO()
        for i, v in enumerate(path):
            f.write(constants.FIELD_CHILDREN)
            f.write(".")
            f.write(str(v))
            if i < len(path) - 1:
                f.write(".")
        return f.getvalue()

