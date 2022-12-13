from flask import Blueprint, render_template, request
from src.models import ArtImages, Products


art = Blueprint('art', __name__)

@art.route("/cart")
def cart():
    """
        Cart route
    """
    return render_template('cart.html', title="Cart")

@art.route("/gallery")
def gallery():
    """
        Gallery route
    """
    page = request.args.get('page', 1, type=int)
    images = ArtImages.query.paginate(page=page, per_page=6)
    return render_template('gallery.html', title="Gallery", images=images)

@art.route("/image<int:image_id>")
def view_image(image_id):
    """
        View selected image route
    """
    image = ArtImages.query.get_or_404(image_id)
    return render_template('viewimage.html', image=image)

@art.route("/shop")
def shop():
    """
        Shop route
    """
    page = request.args.get('page', 1, type=int)
    products = Products.query.paginate(page=page, per_page=6)
    return render_template('shop.html', title="Shop", products=products)

@art.route("/product<int:product_id>")
def view_product(product_id):
    """
        View selected product
    """
    product = Products.query.get_or_404(product_id)
    return render_template('viewproduct.html', product=product)
