from flask import Blueprint, request, jsonify, render_template
from helpers import token_required
from models import db, User, Wine, wine_schema, wines_schema

api = Blueprint('api',__name__, url_prefix='/api')


@api.route('/wines', methods = ['POST'])
@token_required
def create_wine(current_user_token):
    type = request.json['type']
    brand = request.json['brand']
    color = request.json['color']
    alcohol_percentage = request.json['alcohol_percentage']
    upc = request.json['upc']
    user_token = current_user_token.token

    wine = Wine(upc, type, brand, color, alcohol_percentage, user_token = user_token )

    db.session.add(wine)
    db.session.commit()

    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines', methods = ['GET'])
@token_required
def get_contact(current_user_token):
    a_user = current_user_token.token
    wines = Wine.query.filter_by(user_token = a_user).all()
    response = wines_schema.dump(wines)
    return jsonify(response)

@api.route('/wines/<upc>', methods = ['GET'])
@token_required
def get_single_wine(current_user_token, upc):
    wine = Wine.query.get(upc)
    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines/<upc>', methods = ['POST','PUT'])
@token_required
def update_wine(current_user_token,upc):
    wine = Wine.query.get(upc) 
    wine.upc = request.json['upc']
    wine.type = request.json['type']
    wine.brand = request.json['brand']
    wine.color = request.json['color']
    wine.alcohol_percentage = request.json['alcohol_percentage']
    wine.user_token = current_user_token.token

    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)

@api.route('/wines/<upc>', methods = ['DELETE'])
@token_required
def delete_wine(current_user_token, upc):
    wine = Wine.query.get(upc)
    db.session.delete(wine)
    db.session.commit()
    response = wine_schema.dump(wine)
    return jsonify(response)

