from django.http import JsonResponse
from rest_framework.decorators import api_view

from app.models import Merchants, Products
from app.api.lib import pagination


@api_view(['GET'])
def get_merchants(request, merchant_id=None):
    rtype = "/merchants"
    status = False
    message = "General Failure"
    data = []

    # Pagination
    n = request.GET.get('n', 10)
    page = request.GET.get('page', 1)

    # Search Keyword
    search = request.GET.get('search', None)

    if merchant_id:
        rtype = "/merchants/" + str(merchant_id)

        merchant = Merchants.objects.filter(id=merchant_id).first()

        if merchant:
            data = generate_merchant_object(merchant)

            status = True
            message = "Merchant found"
    else:
        merchants = Merchants.objects.all()

        if search:
            merchants = merchants.filter(name__icontains=search)

        merchants = pagination(merchants, int(n), int(page)-1)

        if len(merchants) > 0:
            for merchant in merchants:
                data.append(generate_merchant_object(merchant))

            status = True
            message = "Merchants found"
        else:
            message = "Merchants not found"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


@api_view(['GET'])
def get_products(request):
    rtype = "/merchants/products"
    status = False
    message = "General Failure"
    data = []

    # Pagination
    n = request.GET.get('n', 10)
    page = request.GET.get('page', 1)

    # Search Keyword
    search = request.GET.get('search', None)
    merchant_id = request.GET.get('merchant_id', None)

    if merchant_id:
        products = Products.objects.filter(merchant_id=merchant_id)
    else:
        products = Products.objects.all()

    if search:
        products = products.filter(name__icontains=search)

    products = pagination(products, int(n), int(page)-1)

    if len(products) > 0:
        for product in products:
            data.append(generate_product_object(product))

            status = True
            message = "Products found"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


@api_view(['GET'])
def get_detail_product(request, product_id):
    rtype = "/merchants/products"
    status = False
    message = "General Failure"
    data = []

    if product_id:
        product = Products.objects.filter(id=product_id).first()

        if product:
            data = generate_product_object(product, is_detailed=True)

            status = True
            message = "Product detail found"
        else:
            message = "Product not found"
    else:
        message = "Product ID not found"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


def generate_merchant_object(merchant):
    return {
        "id": merchant.id,
        "name": merchant.name,
    }


def generate_product_object(product, is_detailed=False):
    product_object = {
        "id": product.id,
        "name": product.name,
        "price": product.price,
        "merchant_name": product.merchant.name,
    }

    if is_detailed:
        product_object['description'] = product.description
        product_object['stock'] = product.stock

    return product_object
