from django.shortcuts import render, redirect, reverse, HttpResponse, get_object_or_404
from django.contrib import messages

from products.models import Product

# Create your views here.

def view_bag(request):
    """ A view that renders the bag contents page """

    return render(request, 'bag/bag.html')

def add_to_bag(request, item_id):
    """ Add a quantity of the specific product to the shopping bag """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    redirect_url = request.POST.get('redirect_url')
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if item_id in list(bag.keys()):
            if size in bag[item_id]['items_by_size'].keys():
                bag[item_id]['items_by_size'][size] += quantity
                messages.success(request, f'Se actualizo la cantidad de {size.upper()} {product.name} a {bag[item_id]["items_by_size"][size]} en su carrito de compra')
            else:
                bag[item_id]['items_by_size'][size] = quantity
                messages.success(request, f'Se agrego {size.upper()} a {product.name} en su carrito de compra')
        else:
            bag[item_id] = {'items_by_size': {size: quantity}}
            messages.success(request, f'Se agrego {size.upper()} a {product.name} en su carrito de compra')
    else:
        if item_id in list(bag.keys()):
            bag[item_id] += quantity
            messages.success(request, f'Se actualizo la cantidad de {product.name} a {bag[item_id]} en su carrito de compra')
        else:
            bag[item_id] = quantity
            messages.success(request, f'Se agrego {product.name} a su carrito de compra')

    request.session['bag'] = bag

    # print(request.session['bag'])
    
    return redirect(redirect_url)


def adjust_bag(request, item_id):
    """ Adjust the quantity of the specific product to the specified amount """

    product = get_object_or_404(Product, pk=item_id)
    quantity = int(request.POST.get('quantity'))
    size = None
    if 'product_size' in request.POST:
        size = request.POST['product_size']
    bag = request.session.get('bag', {})

    if size:
        if quantity > 0:
            bag[item_id]['items_by_size'][size] = quantity
            messages.success(request, f'Se actualizo la cantidad de {size.upper()} {product.name} a {bag[item_id]["items_by_size"][size]} en su carrito de compra')
        else:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Se elimino {size.upper()} de {product.name} en su carrito de compra')
    else:
        if quantity > 0:
            bag[item_id] = quantity
            messages.success(request, f'Se actualizo la cantidad de {product.name} a {bag[item_id]} en su carrito de compra')
        else:
            bag.pop(item_id)
            messages.success(request, f'Se elimino {product.name} de su carrito de compra')

    request.session['bag'] = bag
    return redirect(reverse('view_bag'))


def remove_from_bag(request, item_id):
    """ Remove the item from the shopping bag """

    try:
        product = get_object_or_404(Product, pk=item_id)
        size = None
        if 'product_size' in request.POST:
            size = request.POST['product_size']
        bag = request.session.get('bag', {})

        if size:
            del bag[item_id]['items_by_size'][size]
            if not bag[item_id]['items_by_size']:
                bag.pop(item_id)
            messages.success(request, f'Se elimino {size.upper()} de {product.name} en su carrito de compra')
        else:
            bag.pop(item_id)
            messages.success(request, f'Se elimino {product.name} de su carrito de compra')

        request.session['bag'] = bag
        return HttpResponse(status=200)

    except Exception as e:
        messages.error(request, f'error al intentar eliminar el item: {e}')
        return HttpResponse(status=500)