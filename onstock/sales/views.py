from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from onstock.core.types import HttpRequest
from onstock.core.utils import for_htmx
from onstock.core.utils import paginate_queryset

from .forms import SaleForm
from .models import Sale


@for_htmx(use_partial="table")
def index(request: HttpRequest):
    sales = Sale.objects.order_by("id")
    return TemplateResponse(
        request,
        "sales/index.html",
        context={"sales_page": paginate_queryset(request, sales)},
    )


def detail(request: HttpRequest, pk: int):
    sale = get_object_or_404(Sale.objects, pk=pk)
    return TemplateResponse(
        request,
        "sales/detail.html",
        context={"sale": sale},
    )


def create(request: HttpRequest):
    form = SaleForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("sales:index")
    return TemplateResponse(
        request,
        "sales/create.html",
        context={"form": form},
    )


def update(request: HttpRequest, pk: int):
    sale = get_object_or_404(Sale.objects, pk=pk)
    form = SaleForm(request.POST or None, instance=sale)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("sales:detail", pk=pk)
    return TemplateResponse(
        request,
        "sales/update.html",
        context={"sale": sale, "form": form},
    )


@require_http_methods(["DELETE"])
def delete(_: HttpRequest, pk: int):
    Sale.objects.filter(pk=pk).delete()
    return HttpResponse("")
