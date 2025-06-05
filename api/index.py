from flask import Flask
from routes.user_routes import user_bp
from routes.shop_routes import shop_bp
from routes.product_routes import product_bp
from routes.order_routes import order_bp

def create_app():
    app = Flask(__name__)

    # Register blueprints
    app.register_blueprint(user_bp, url_prefix='/api')
    app.register_blueprint(shop_bp, url_prefix='/api')
    app.register_blueprint(product_bp, url_prefix='/api')
    app.register_blueprint(order_bp, url_prefix='/api')

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)