from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from django.urls import reverse
from onstock.core.types import HttpRequest
from onstock.core.utils import for_htmx, paginate_queryset

from .forms import ProductForm
from .models import Product


@for_htmx(use_partial="table")
def index(request: HttpRequest):
    products = Product.objects.order_by("id")
    return TemplateResponse(
        request,
        "products/index.html",
        context={"products_page": paginate_queryset(request, products)},
    )


def detail(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    return TemplateResponse(
        request,
        "products/detail.html",
        context={"product": product},
    )


def create(request: HttpRequest):
    form = ProductForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:index")
    return TemplateResponse(
        request,
        "products/create.html",
        context={"form": form},
    )


def update(request: HttpRequest, pk: int):
    product = get_object_or_404(Product.objects, pk=pk)
    form = ProductForm(request.POST or None, instance=product)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("products:detail", pk=pk)
    return TemplateResponse(
        request,
        "products/update.html",
        context={"product": product, "form": form},
    )


@require_http_methods(["DELETE"])
def delete(_: HttpRequest, pk: int):
    Product.objects.filter(pk=pk).delete()
    return HttpResponse("")
