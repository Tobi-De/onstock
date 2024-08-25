from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods, require_POST
from django.urls import reverse

from onstock.core.types import HttpRequest, AuthenticatedHttpRequest
from onstock.core.utils import for_htmx, paginate_queryset

from .forms import PurchaseForm, ItemForm
from .models import Purchase


@for_htmx(use_partial="table")
def index(request: AuthenticatedHttpRequest):
    purchases = Purchase.objects.order_by("id").prefetch_related("items")
    return TemplateResponse(
        request,
        "purchases/index.html",
        context={"purchases_page": paginate_queryset(request, purchases)},
    )


def detail(request: AuthenticatedHttpRequest, pk: int):
    purchase = get_object_or_404(Purchase.objects, pk=pk)
    return TemplateResponse(
        request,
        "purchases/detail.html",
        context={"purchase": purchase},
    )


def create(request: AuthenticatedHttpRequest):
    form = PurchaseForm(request.POST or None)
    item_form = ItemForm()
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("purchases:index")
    return TemplateResponse(
        request,
        "purchases/create.html",
        context={"form": form, "item_form": item_form},
    )


@require_POST
def add_item(request: AuthenticatedHttpRequest):
    pass


def update(request: AuthenticatedHttpRequest, pk: int):
    purchase = get_object_or_404(Purchase.objects, pk=pk)
    form = PurchaseForm(request.POST or None, instance=purchase)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("purchases:detail", pk=pk)
    return TemplateResponse(
        request,
        "purchases/update.html",
        context={"purchase": purchase, "form": form},
    )


@require_http_methods(["DELETE"])
def delete(_: AuthenticatedHttpRequest, pk: int):
    Purchase.objects.filter(pk=pk).delete()
    return HttpResponse("")
