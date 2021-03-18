from flask_swagger_ui import get_swaggerui_blueprint
from flask import Flask,request,jsonify
from flask_mysqldb import MySQL
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

# Swagger Specifications #
SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
SWAGGERUI_BLUEPRINT = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "PokeCRUD Flask Backend"
    }
)
app.register_blueprint(SWAGGERUI_BLUEPRINT, url_prefix = SWAGGER_URL)
# End Swagger Specifications #

#MySQL Connection
app.config['MYSQL_HOST'] = 'b9l7iiupadf8mvxind2z-mysql.services.clever-cloud.com'
app.config['MYSQL_USER'] = 'uajht2lef1p3tiby'
app.config['MYSQL_PASSWORD'] = 'zARsW6mMsMhwD6Awvgp3'
app.config['MYSQL_DB'] = 'b9l7iiupadf8mvxind2z'

mysql = MySQL(app)

#settings
app.secret_key = 'mysecretkey'

@app.route('/api/pokemon', methods = ['POST','GET'])
def manage_pokemons():
    if request.method == 'POST':
        body = request.json
        name = body['name']
        tipo = body['type']
        ability = body['ability']
        h_ability = body['h_ability']
        habitat = body['habitat']
        img = body['img']
        cur = mysql.connection.cursor()
        cur.execute('INSERT INTO pokemons (name, type, ability, h_ability, habitat, img) VALUES (%s, %s, %s, %s, %s, %s)', (name, tipo, ability, h_ability, habitat, img))
        mysql.connection.commit()
        return jsonify({'name': body['name']})
    elif request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pokemons')
        result_list = cur.fetchall()
        field_list = cur.description
        column_list = []
        for i in field_list:
            column_list.append(i[0])
        jsonData_list = []
        for row in result_list:
            data_dict = {}
            for i in range(len(column_list)):
                data_dict[column_list[i]] = row[i]
            jsonData_list.append(data_dict)
        return jsonify(jsonData_list)

@app.route('/api/pokemon/<id>', methods = ['DELETE', 'GET', 'PUT'])
def delete_pokemon(id):
    if request.method == 'DELETE':
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM pokemons WHERE id = {0}'.format(id))
        mysql.connection.commit()
        return jsonify({'id': id})
    elif request.method == 'GET':
        cur = mysql.connection.cursor()
        cur.execute('SELECT * FROM pokemons WHERE id = {0}'.format(id))
        result = cur.fetchall()
        field = cur.description
        column = []
        for i in field:
            column.append(i[0])
        data_poke = {}
        for row in result:
            for i in range(len(column)):
                data_poke[column[i]] = row[i]
        return jsonify(data_poke)
    elif request.method == 'PUT':
        body = request.json
        name = body['name']
        tipo = body['type']
        ability = body['ability']
        h_ability = body['h_ability']
        habitat = body['habitat']
        img = body['img']
        cur = mysql.connection.cursor()
        cur.execute("""
            UPDATE pokemons
            SET name = %s,
                type = %s,
                ability = %s,
                h_ability = %s,
                habitat = %s,
                img = %s
            WHERE id = %s
        """, (name, tipo, ability, h_ability, habitat, img, id))
        mysql.connection.commit()
        return jsonify({'name': body['name']})

if __name__ == '__main__':
    app.run(port = 5000, debug = True)