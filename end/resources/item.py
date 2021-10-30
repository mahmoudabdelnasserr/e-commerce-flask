from flask_restful import Resource, reqparse
from flask import request
from flask_jwt_extended import jwt_required
from models.item import ItemModel
from schemas.item import ItemSchema
from libs.strings import gettext

item_schema = ItemSchema()
item_list_schema = ItemSchema(many=True)


class Item(Resource):
    @classmethod
    def get(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            return item.json(), 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    def delete(cls, name):
        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
            return {"message": gettext("item_deleted")}, 200

        return {"message": gettext("item_not_found")}, 404

    @classmethod
    def put(cls, name):
        item_json = request.get_json()
        item = ItemModel.find_by_name(name)

        if item:
            item.price = item_json["price"]
        # else:
        #     item_json["name"] = name
        #     item = item_schema.load(item_json)

        item.save_to_db()

        return item_schema.dump(item), 200


class ItemPost(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('name',
                        type=str,
                        required=True,
                        help="You can't keep title empty."
                        )

    parser.add_argument('price',
                        type=int,
                        required=True,
                        help="You can't keep event date empty."
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="You can't keep event date empty."
                        )


    @jwt_required()
    def post(self):
        data = ItemPost.parser.parse_args()
        # user = UserModel.find_by_userid(owner_id)

        item = ItemModel(**data)
        try:
            item.save_to_db()
        except:
            return {'message': 'item with this name is already exists'}
        return item.json()


class ItemList(Resource):
    @classmethod
    def get(cls):
        return {'items': list(map(lambda x: x.json(), ItemModel.query.all()))}, 200
