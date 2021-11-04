import json
import time
import datetime

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view

from app.models import Products, Orders, Payments, OrderProducts


@api_view(['POST'])
def put_order(request):
    rtype = "/order"
    status = False
    message = "General Failure"
    data = []

    if request.method == 'POST':
        if request.body:
            payloads = json.loads(request.body)

            product_ids = payloads.get('product_ids', [])
            product_amounts = payloads.get('product_amounts', [])
            user = request.user
            method = payloads.get('method', None)

            if len(product_ids) > 0 and len(product_amounts) \
                    and len(product_ids) == len(product_amounts) \
                    and user and method:
                products = Products.objects.filter(id__in=product_ids)

                is_out_of_stock = False
                is_less_stock = False
                sub_total = 0

                index = 0
                for product in products:
                    if product.stock < 1:
                        is_out_of_stock = True
                    elif product.stock < product_amounts[index]:
                        is_less_stock = True

                    sub_total += product.price * product_amounts[index]
                    index += 1

                if is_out_of_stock:
                    message = "One or more product(s) are out of stock"
                elif is_less_stock:
                    message = "One or more product(s) stock are less than what you order"
                else:
                    # Create payment
                    payment = Payments()
                    payment.method = method
                    payment.payment_identifier = str(round(time.time_ns()))  # Generate random payment number
                    payment.sub_total = sub_total
                    payment.tax = sub_total * 0.1
                    payment.total = payment.sub_total + payment.tax
                    payment.expired_at = datetime.datetime.now() + datetime.timedelta(days=1)
                    payment.save()

                    # Create order
                    order = Orders()
                    order.user = user
                    order.payment = payment
                    order.save()

                    # Create order products
                    index = 0
                    for product in products:
                        order_product = OrderProducts()
                        order_product.order = order
                        order_product.product = product
                        order_product.amount = product_amounts[index]
                        order_product.total_price = product_amounts[index] * product.price
                        order_product.save()

                        index += 1

                    data = generate_order_object(order)
                    status = True
                    message = "Order created"
            else:
                message = "No products"
        else:
            message = "Empty parameters"
    else:
        message = "Method not allowed"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


@api_view(['GET'])
def get_order_info(request, order_id):
    rtype = "/order/" + str(order_id)
    status = False
    message = "General Failure"
    data = []

    if order_id:
        order = Orders.objects.filter(id=order_id).first()

        if order:
            data = generate_order_object(order)

            status = True
            message = "Order info found"
        else:
            message = "Order not found"
    else:
        message = "Order ID not found"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message,
        'data': data,
    })


@csrf_exempt
def confirm_payment(request, order_id):
    rtype = "/order/confirm/" + str(order_id)
    status = False
    message = "General Failure"
    data = []

    if order_id:
        order = Orders.objects.filter(id=order_id).first()

        if order:
            if order.payment.status == 0:
                # Reduce the stock
                order_products = OrderProducts.objects.filter(order=order)
                for order_product in order_products:
                    order_product.product.stock -= order_product.amount
                    order_product.product.save()

                order.payment.status = 1
                order.payment.paid_at = datetime.datetime.now()
                order.payment.save()

                status = True
                message = "Payment confirmed"
            elif order.payment.status == 1:
                message = "Order already paid"
            elif order.payment.status == 2:
                message = "Payment is expired"
            else:
                message = "Unknown status"
        else:
            message = "Order not found"
    else:
        message = "Order ID not found"

    return JsonResponse({
        'type': rtype,
        'status': status,
        'message': message
    })


def generate_order_object(order):
    order_object = {
        'id': order.id,
        'status': order.payment.get_status_display(),
        'method': order.payment.method,
        'payment_identifier': order.payment.payment_identifier,
        'total': order.payment.total,
        'sub_total': order.payment.total,
        'tax': order.payment.tax,
        'expired_at': order.payment.expired_at.strftime('%d %b %Y %H:%M:%S'),
    }

    return order_object
