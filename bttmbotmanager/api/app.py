from flask_restplus import Resource, Namespace

api = Namespace("bttmbot", description="bttmbot manager generics endpoints")


@api.route("/health")
class Health(Resource):
    def get(self):
        return {"status": "health test"}

    # TODO check binance conectivity, check mongodb, check passivot?, check storage
