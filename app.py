from flask import Flask, jsonify, request
from flasgger import Swagger
import requests
from bs4 import BeautifulSoup
from flask_jwt_extended import JWTManager, create_access_token, jwt_required, get_jwt_identity


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = 'pos_ML'  # Change this to a random secret key
jwt = JWTManager(app)

# Custom Swagger configuration to serve at the root URL
app.config['SWAGGER'] = {
    'title': 'API EMBRAPA',
    'specs': [
        {
            'endpoint': 'apispec_1',
            'route': '/apispec_1.json',
            'rule_filter': lambda rule: True,  # all in
            'model_filter': lambda tag: True,  # all in
        }
    ],
    'static_url_path': '/flasgger_static',
    'swagger_ui': True,
    'specs_route': '/'
}

swagger = Swagger(app)


def parse_table(table):
    data = []
    headers = [th.text.strip() for th in table.select('th')]
    for row in table.select('tbody tr'):
        row_data = [td.text.strip() for td in row.find_all('td')]
        data.append(dict(zip(headers, row_data)))
    return data


def html_to_json(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    tables = soup.select('.tb_base')
    json_data = {}
    for i, table in enumerate(tables):
        json_data[f'table_{i+1}'] = parse_table(table)
    return json_data


def return_result(url):
    data = html_to_json(url)
    if data:
        return jsonify(data)
    else:
        return jsonify({"error": "Falha ao obter os dados de processamento"}), 500


@app.route('/producao', methods=['GET'])
def get_producao():
    """
    Endpoint for processing data from Embrapa website
    ---
    tags:
      - Processing
    responses:
      200:
        description: JSON data extracted from the website
        content:
          application/json:
            schema:
              type: object
              properties:
                table_1:
                  type: array
                  items:
                    type: object
                table_2:
                  type: array
                  items:
                    type: object
      500:
        description: Error occurred while processing the data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Falha ao obter os dados de processamento
    """
    return return_result(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_02")


@app.route('/processamento', methods=['GET'])
def get_processamento():
    """
    Endpoint for processing data from Embrapa website
    ---
    tags:
      - Processing
    responses:
      200:
        description: JSON data extracted from the website
        content:
          application/json:
            schema:
              type: object
              properties:
                table_1:
                  type: array
                  items:
                    type: object
                table_2:
                  type: array
                  items:
                    type: object
      500:
        description: Error occurred while processing the data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Falha ao obter os dados de processamento
    """
    return return_result(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_03")


@app.route('/comercializacao', methods=['GET'])
def get_comercializacao():
    """
    Endpoint for processing data from Embrapa website
    ---
    tags:
      - Processing
    responses:
      200:
        description: JSON data extracted from the website
        content:
          application/json:
            schema:
              type: object
              properties:
                table_1:
                  type: array
                  items:
                    type: object
                table_2:
                  type: array
                  items:
                    type: object
      500:
        description: Error occurred while processing the data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Falha ao obter os dados de processamento
    """
    return return_result(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_04")


@app.route('/importacao', methods=['GET'])
def get_importacao():
    """
    Endpoint for processing data from Embrapa website
    ---
    tags:
      - Processing
    responses:
      200:
        description: JSON data extracted from the website
        content:
          application/json:
            schema:
              type: object
              properties:
                table_1:
                  type: array
                  items:
                    type: object
                table_2:
                  type: array
                  items:
                    type: object
      500:
        description: Error occurred while processing the data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Falha ao obter os dados de processamento
    """
    return return_result(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_05")


@app.route('/exportacao', methods=['GET'])
def get_exportacao():
    """
    Endpoint for processing data from Embrapa website
    ---
    tags:
      - Processing
    responses:
      200:
        description: JSON data extracted from the website
        content:
          application/json:
            schema:
              type: object
              properties:
                table_1:
                  type: array
                  items:
                    type: object
                table_2:
                  type: array
                  items:
                    type: object
      500:
        description: Error occurred while processing the data
        content:
          application/json:
            schema:
              type: object
              properties:
                error:
                  type: string
                  example: Falha ao obter os dados de processamento
    """
    return return_result(url="http://vitibrasil.cnpuv.embrapa.br/index.php?opcao=opt_06")


@app.route('/login', methods=['POST'])
def login():
    """
    User login to get a JWT
    ---
    tags:
      - Authentication
    parameters:
      - in: query
        name: username
        required: true
        schema:
          type: string
        example: test
        description: The username of the user
      - in: query
        name: password
        required: true
        schema:
          type: string
        example: test
        description: The password of the user
    responses:
      200:
        description: JWT token
        content:
          application/json:
            schema:
              type: object
              properties:
                access_token:
                  type: string
      401:
        description: Invalid credentials
    """
    username = request.args.get('username', None)
    password = request.args.get('password', None)
    if not password:  # Simple check for demonstration
        return jsonify({"msg": "Bad username or password"}), 401

    access_token = create_access_token(identity=username)
    return jsonify(access_token=access_token), 200


if __name__ == "__main__":
    app.run(debug=True, port=8000)
