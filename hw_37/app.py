from flask import Flask
from models import DB, Master, Appointment
from blueprints.masters.routes import masters_bp
from blueprints.appointments.routes import appointments_bp
import auth

print("=== DEBUG ===")
print("auth.py loaded from:", auth.__file__)
print("USERS =", auth.USERS)
print("=== END DEBUG ===")

app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
app.url_map.strict_slashes = False

app.register_blueprint(masters_bp)
app.register_blueprint(appointments_bp)


@app.before_request
def create_tables():
    DB.connect()
    DB.create_tables([Master, Appointment], safe=True)


@app.teardown_request
def close_db(_):
    if not DB.is_closed():
        DB.close()


if __name__ == "__main__":
    app.run(debug=True, host="127.0.0.1", port=5000)
