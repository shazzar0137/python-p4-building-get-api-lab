#!/usr/bin/env python3

from flask import Flask, make_response, jsonify
from flask_migrate import Migrate

from models import db, Bakery, BakedGood

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def index():
    return '<h1>Bakery GET API</h1>'

@app.route('/bakeries')
def bakeries():
    bakeries = [bakery.to_dict() for bakery in Bakery.query.all()]

    response = make_response(
        bakeries,
        200,
        {"Content-Type": "application/json"}
    )

    return response
    

@app.route('/bakeries/<int:id>')
def bakery_by_id(id):
    bakery = Bakery.query.filter(Bakery.id == id).first()

    bakery_dict = bakery.to_dict()


    response = make_response(
        bakery_dict,
        200
    )

    return response
@app.route('/baked_goods/by_price')
def baked_goods_by_price():
    baked_goods = [goods.to_dict() for goods in BakedGood.query.order_by(BakedGood.price.desc()).all()]

    response = make_response(
        jsonify(baked_goods), 
        200
    )
    return response

@app.route('/baked_goods/most_expensive')
def most_expensive_baked_good():
    baked_goods = BakedGood.query.order_by(BakedGood.price.desc()).first()
    baked_goods_dict = baked_goods.to_dict()
    response = make_response(
        jsonify(baked_goods_dict), 200
    )
    return response

if __name__ == '__main__':
    app.run(port=5555, debug=True)
