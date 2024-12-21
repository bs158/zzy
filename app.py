from flask import Flask, jsonify
from flask_cors import CORS
import psycopg2

app = Flask(__name__)
CORS(app)

# 数据库连接设置
DB_SETTINGS = {
    'dbname': 'TransportationDB',
    'user': 'postgres',
    'password': 'yourpassword',
    'host': 'localhost',
    'port': 5432
}

# 获取数据库连接
def get_db_connection():
    conn = psycopg2.connect(**DB_SETTINGS)
    return conn

@app.route('/roads', methods=['GET'])
def get_roads():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Name, ST_AsGeoJSON(Geometry) FROM Roads;")
    roads = [{'name': row[0], 'geometry': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(roads)

@app.route('/trafficlights', methods=['GET'])
def get_trafficlights():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT Status, ST_AsGeoJSON(Coordinates) FROM TrafficLights;")
    lights = [{'status': row[0], 'coordinates': row[1]} for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return jsonify(lights)

if __name__ == '__main__':
    app.run(debug=True)
