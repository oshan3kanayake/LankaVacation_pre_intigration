from flask import Flask, render_template, url_for
from extensions import db, migrate, login_manager
from models import *

def create_app():
    app = Flask(__name__, static_folder="static", template_folder="templates")

    # Configuration
    app.config['SECRET_KEY'] = 'your-secret-key-here-change-it'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:oshan%401234@localhost/lankavacation_db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    login_manager.login_view = 'auth.login'

    # Register blueprints
    from auth.routes import auth_bp
    app.register_blueprint(auth_bp, url_prefix='/auth')

    from bookings.routes import bookings_bp
    app.register_blueprint(bookings_bp, url_prefix='/bookings')

    from packages.routes import packages_bp
    app.register_blueprint(packages_bp, url_prefix='/packages')

    from reviews.routes import reviews_bp
    app.register_blueprint(reviews_bp, url_prefix='/reviews')

    from tickets.routes import tickets_bp
    app.register_blueprint(tickets_bp, url_prefix='/tickets')

    from hotel_bookings.routes import hotel_bp
    app.register_blueprint(hotel_bp, url_prefix='/hotel')

    from hotels.routes import hotels_bp
    app.register_blueprint(hotels_bp, url_prefix='/hotels')

    from admin.routes import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    # Home route
    @app.route("/")
    def home():
        featured_packages = Package.query.all()
        if not featured_packages:
            featured_packages = [
                {"id": 1, "title": "Sigiriya & Ancient Cities", "location": "Sigiriya • Polonnaruwa", "days": "3 Days", "price": "USD 180", "image": url_for('static', filename='images/sigiriya.jpg')},
                {"id": 2, "title": "Tea-Country Retreat", "location": "Nuwara Eliya • Ella", "days": "2 Nights", "price": "USD 140", "image": url_for('static', filename='images/nuwara_ella.jpg')},
                {"id": 3, "title": "Southern Coast Escape", "location": "Galle • Mirissa", "days": "4 Days", "price": "USD 220", "image": url_for('static', filename='images/galle.jpg')}
            ]
        popular_destinations = [
            {"name": "Sigiriya", "image": url_for('static', filename='images/sigiriya_thumb.jpg')},
            {"name": "Ella", "image": url_for('static', filename='images/ella_thumb.jpg')},
            {"name": "Galle", "image": url_for('static', filename='images/galle_thumb.jpg')},
            {"name": "Yala", "image": url_for('static', filename='images/yala.jpg')},
            {"name": "Nuwara Eliya", "image": url_for('static', filename='images/nuwara_ella.jpg')}
        ]
        testimonials = [
            {"name": "S. Perera", "text": "Amazing Sri Lanka tour. Well organized and fantastic guide."},
            {"name": "L. Fernando", "text": "The beach trip to Mirissa was perfect!"},
            {"name": "A. Silva", "text": "Sigiriya sunrise was unforgettable."}
        ]
        counters = [
            {"label": "Tours", "value": 128},
            {"label": "Happy Travelers", "value": 4520},
            {"label": "Destinations", "value": 38},
            {"label": "Bookings", "value": 930}
        ]

        return render_template("home.html",
                               featured_packages=featured_packages,
                               popular_destinations=popular_destinations,
                               testimonials=testimonials,
                               counters=counters)

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)