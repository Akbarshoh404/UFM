from flask import Flask, Response
from flask_cors import CORS
from routes.shop_routes import shop_bp
from routes.user_routes import user_bp
from routes.product_routes import product_bp

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend compatibility

# Register Blueprints
app.register_blueprint(shop_bp, url_prefix='/api')
app.register_blueprint(user_bp, url_prefix='/api')
app.register_blueprint(product_bp, url_prefix='/api')

@app.route('/favicon.ico')
@app.route('/favicon.png')
def favicon():
    return Response(status=204)  # Return empty response for favicon requests

if __name__ == '__main__':
    app.run(debug=True)