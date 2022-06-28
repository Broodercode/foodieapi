from flask import jsonify
import bcrypt
from db_helpers import run_query


def client_patcher(email, username, password, first_name, last_name, picture_url):
    updated = ''
    if email != None:
        
        run_query("UPDATE clients SET email= ? WHERE username= ?", [email, username])
        updated += 'email '
    if password != None:
        salt = bcrypt.gensalt()
        hash_pass = bcrypt.hashpw(password.encode(), salt)
  
        run_query("UPDATE clients SET password= ? WHERE username=?", [hash_pass, username])
        updated += 'password '
    if first_name != None:

        run_query("UPDATE clients SET first_name= ? WHERE username=?", [first_name, username])
        updated += 'first name '
    if last_name != None:

        run_query("UPDATE clients SET last_name= ? WHERE username=?", [last_name, username])
        updated += 'last name '
    if picture_url != None:

        run_query("UPDATE clients SET picture_url= ? WHERE username=?", [picture_url, username])
        updated += 'image '
    updated += 'updated'
    return updated

def menu_patcher(menuId, name, description, price, imageUrl):
    update = ''
    if menuId == None:
        return jsonify('Something went wrong')
    if name != None:
        run_query("UPDATE menu SET name= ? WHERE id=?", [name, menuId])
        update += 'name, '
    if description != None:
        run_query("UPDATE menu SET description= ? WHERE id=?", [description, menuId])
        update += 'description, '
    if price != None:
        run_query("UPDATE menu SET price= ? WHERE id=?", [price, menuId])
        updated += 'price, '
    if imageUrl != None:
        run_query("UPDATE menu SET image_url= ? WHERE id=?", [imageUrl, menuId])
        updated += 'image '
    updated += 'updated!'
    return jsonify(updated)


def restaurant_patcher(name, address, banner, bio, city, email, phone, profile, password, restaurantId):
    updated = ''
    if restaurantId == None:
        return jsonify('Something went wrong')
    if email != None:
        run_query("UPDATE clients SET email= ? WHERE username= ?", [email, restaurantId])
        updated += 'email '
    if password != None:
        salt = bcrypt.gensalt()
        hash_pass = bcrypt.hashpw(password.encode(), salt)
        run_query("UPDATE clients SET password= ? WHERE restaurantId=?", [hash_pass, restaurantId])
        updated += 'password '
    if name != None:
        run_query("UPDATE clients SET name= ? WHERE restaurantId=?", [name, restaurantId])
        updated += 'name '
    if address != None:
        run_query("UPDATE clients SET address= ? WHERE restaurantId=?", [address, restaurantId])
        updated += 'address '
    if banner != None:
        run_query("UPDATE clients SET banner_url= ? WHERE restaurantId=?", [banner, restaurantId])
        updated += 'banner '
    if bio != None:
        run_query("UPDATE clients SET bio= ? WHERE restaurantId=?", [bio, restaurantId])
        updated += 'bio '
    if city != None:
        run_query("UPDATE clients SET city= ? WHERE restaurantId=?", [city, restaurantId])
        updated += 'city '
    if phone != None:
        run_query("UPDATE clients SET phone_number= ? WHERE restaurantId=?", [phone, restaurantId])
        updated += 'phone '
    if profile != None:
        run_query("UPDATE clients SET profile_url= ? WHERE restaurantId=?", [profile, restaurantId])
        updated += 'profile '
    updated += 'updated'
    return jsonify(updated)

