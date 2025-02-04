import uuid

from flask import request
from flask.views import MethodView
from flask_smorest import Blueprint, abort
from sqlalchemy.exc import IntegrityError, SQLAlchemyError

from db import db
from models import StoreModel
from schemas import StoreSchema

blp = Blueprint("stores", __name__, description="Operations on stores")

@blp.route("/store/<int:store_id>")
class Store(MethodView):
    @blp.response(200, StoreSchema)
    def get(self, store_id):

        ## ver1
        # try:
        #     return stores[store_id]
        # except KeyError:
        #     abort(404, message= "Store not found.")

        # ver2
        store = StoreModel.query.get_or_404(store_id)
        return store

    def delete(self, store_id):
        store = StoreModel.query.get_or_404(store_id)
        db.session.delete(store)
        db.session.commit()
        return {"message": "Store deleted"}
        # raise NotImplementedError("Deleting a store is not implemented.")


@blp.route("/store")
class StoreList(MethodView):
    @blp.response(200, StoreSchema(many=True))
    def get(self):
        # a = [
        #         {
        #             "id": "test",
        #             "name": "test"
        #         }
        #     ]
        # return a
        # return stores.values()
        # return {"stores": list(stores.values())}
        return StoreModel.query.all()
    
    @blp.arguments(StoreSchema)
    @blp.response(201, StoreSchema)
    def post(self, store_data):

        ## ver 1
        # store_data = request.get_json()
        # if "name" not in store_data:
        #     abort(
        #         400,
        #         message="Bad request. Ensure 'name' is included in the JSON payload.",
        #     )

        ## ver 2
        # for store in stores.values():
        #     if store_data["name"] == store["name"]:
        #         abort(400, message=f"Store already exists.")

        # store_id = uuid.uuid4().hex
        # store = { **store_data, "id": store_id}
        # stores[store_id] = store

        
        # ver3
        store = StoreModel(**store_data)
        try:
            db.session.add(store)
            db.session.commit()
        except IntegrityError:
            abort(
                400,
                message="A store with that name already exists.",
            )
        except SQLAlchemyError:
            abort(500, message="An error occurred creating the store.")


        # return store, 201
        return store

