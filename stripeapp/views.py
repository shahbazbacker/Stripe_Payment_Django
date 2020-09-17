from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import TemplateView
from .models import Product
from django.conf import settings
from django.http.response import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt 
import stripe




class ProductListView(ListView):
    queryset = Product.objects.all()
    context_object_name = 'product_list'
    template_name = 'stripeapp/product_list.html'


def ProductDetailView(request, pk):
    qs = get_object_or_404(Product, pk=pk)
    request.session['productId'] = qs.id
    

    return render(request, 'stripeapp/product_detail.html', context= {'product': qs})
    
    
    

@csrf_exempt
def stripe_config(request):
    if request.method == 'GET':
        stripe_config = {'publicKey': settings.STRIPE_PUBLISHABLE_KEY}
        return JsonResponse(stripe_config, safe=False)


@csrf_exempt
def create_checkout_session(request):
    productid = request.session.get("productId", None)
    print(productid)
    product = Product.objects.get(id=productid)
    print(product)
    price = product.price * 100
    
    if request.method == 'GET':
        domain_url = 'http://localhost:8000/'
        stripe.api_key = settings.STRIPE_SECRET_KEY
        try:
            checkout_session = stripe.checkout.Session.create(
                success_url=domain_url + 'success?session_id={CHECKOUT_SESSION_ID}',
                cancel_url=domain_url + 'cancelled/',
                payment_method_types=['card'],
                mode='payment',
                line_items=[
                    {
                        'name': product.name,
                        'quantity': 1,
                        'currency': 'inr',
                        'amount': price,
                    }
                ]
            )
            return JsonResponse({'sessionId': checkout_session['id']})
        except Exception as e:
            return JsonResponse({'error': str(e)})


class SuccessView(TemplateView):
    template_name = 'stripeapp/success.html'



class CancelledView(TemplateView):
    template_name = 'stripeapp/cancelled.html'