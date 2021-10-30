from flask_restful import Resource
from models.store import StoreModel
from schemas.store import StoreSchema
from libs.strings import gettext

store_schema = StoreSchema()
store_list_schema = StoreSchema(many=True)


class Store(Resource):
    @classmethod
    def get(cls, name: str):
        s = []
        store = StoreModel.find_by_name(name)
        if store:
            store_items = list(map(lambda x: x.json(), store.items)), 200
            for i in store_items:
                s.append(i)
        return s
        # return {"message": gettext("store_not_found")}, 404

    @classmethod
    def post(cls, name: str):
        if StoreModel.find_by_name(name):
            return {"message": gettext("store_name_exists").format(name)}, 400

        store = StoreModel(name=name)
        try:
            store.save_to_db()
        except:
            return {"message": gettext("store_error_inserting")}, 500

        return store_schema.dump(store), 201

    @classmethod
    def delete(cls, name: str):
        store = StoreModel.find_by_name(name)
        if store:
            store.delete_from_db()
            return {"message": gettext("store_deleted")}, 200

        return {"message": gettext("store_not_found")}, 404


class StoreList(Resource):
    @classmethod
    def get(cls):
        return {"stores": list(map(lambda x: x.json(), StoreModel.query.all()))}, 200
