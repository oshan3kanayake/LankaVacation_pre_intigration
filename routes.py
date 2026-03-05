from flask import render_template
from models import Package
from . import packages_bp

@packages_bp.route('/')
def all_packages():
    packages = Package.query.all()
    return render_template('all_packages.html', packages=packages)

@packages_bp.route('/<int:package_id>')
def package_detail(package_id):
    package = Package.query.get_or_404(package_id)
    return render_template('package_detail.html', package=package)

    @bookings_bp.route('/add-more-packages')
    def add_more_packages():
        from models import Package
    if Package.query.count() < 6:  # Only add if we have fewer than 6
        more_packages = [
            Package(
                title="Kandy Cultural Tour",
                location="Kandy • Peradeniya",
                days="2 Days",
                price="USD 150",
                image="images/kandy.jpg",
                description="Explore the sacred Temple of the Tooth, stroll through Royal Botanical Gardens, and experience traditional Kandyan dance."
            ),
            Package(
                title="Yala Wildlife Safari",
                location="Yala • Tissamaharama",
                days="3 Days",
                price="USD 280",
                image="images/yala_safari.jpg",
                description="Embark on jeep safaris to spot leopards, elephants, and exotic birds. Stay at a wildlife lodge."
            ),
            Package(
                title="Ella Hiking Adventure",
                location="Ella • Bandarawela",
                days="2 Nights",
                price="USD 160",
                image="images/ella.jpg",
                description="Hike Little Adam's Peak, visit Nine Arches Bridge, and enjoy breathtaking mountain views."
            )
        ]
        for p in more_packages:
            db.session.add(p)
        db.session.commit()
        return "6 packages now available!"
    else:
        return "Packages already exist."