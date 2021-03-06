from app import app
from verifyToken import token_validate
from flask import request, jsonify
from db_helpers import run_query
from patcher import menu_patcher

@app.post('/api/menu')
def menu_post():
    data = request.json
    token = data.get('token')
    token_validate(token, 'restaurant')
    if not token_validate:
        return jsonify('Invalid Session')
    elif token_validate:
  
        getRestId = run_query("SELECT restaurantId from restaurant_session WHERE token = ?", [token])
        restId = getRestId[0][0]
        name = data.get('name')
        desc = data.get('description')
        price = data.get('price')
        img_url = data.get('img_url')

        run_query("INSERT INTO menu (restaurantId, name, description, price, image_url) VALUES(?,?,?,?,?)", [restId, name, desc, price, img_url])
        return jsonify('works')

@app.patch('/api/menu')
def menu_patch():
    data = request.json
    token = data.get('token')
    menu_id = data.get('menuId')
    name = data.get('name')
    desc = data.get('description')
    price = data.get('price')
    img_url = data.get('img_url')
    token_validate(token, 'restaurant')
    if not token_validate:
        return jsonify('Invalid Session')
    elif token_validate:
        menu_patcher(name, desc, price, img_url)
    return jsonify('Patch Successful')
    
@app.route('/api/menu', methods=['GET'])
def menu_get():

    rest = request.args.get('restaurant')
    menuId = request.args.get('menuId')

    if rest and menuId:
        return jsonify('something went wrong')
    elif menuId:

        menuItem = run_query("SELECT * from menu WHERE id=?", [menuId])

        return jsonify(menuItem)
    elif rest:

        restItems = run_query("SELECT * FROM menu WHERE restaurantID=?", [rest])

        return jsonify(restItems)
    else: 
        menuList = run_query("SELECT * FROM menu")

        return jsonify(menuList)