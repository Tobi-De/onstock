from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.template.response import TemplateResponse
from django.views.decorators.http import require_http_methods
from onstock.core.types import HttpRequest
from onstock.core.utils import for_htmx
from onstock.core.utils import paginate_queryset

from .forms import SupplierForm
from .models import Supplier


@for_htmx(use_partial="table")
def index(request: HttpRequest):
    suppliers = Supplier.objects.order_by("id")
    return TemplateResponse(
        request,
        "suppliers/index.html",
        context={"suppliers_page": paginate_queryset(request, suppliers)},
    )


def detail(request: HttpRequest, pk: int):
    supplier = get_object_or_404(Supplier.objects, pk=pk)
    return TemplateResponse(
        request,
        "suppliers/detail.html",
        context={"supplier": supplier},
    )


def create(request: HttpRequest):
    form = SupplierForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("suppliers:index")
    return TemplateResponse(
        request,
        "suppliers/create.html",
        context={"form": form},
    )


def update(request: HttpRequest, pk: int):
    supplier = get_object_or_404(Supplier.objects, pk=pk)
    form = SupplierForm(request.POST or None, instance=supplier)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("suppliers:detail", pk=pk)
    return TemplateResponse(
        request,
        "suppliers/update.html",
        context={"supplier": supplier, "form": form},
    )


@require_http_methods(["DELETE"])
def delete(_: HttpRequest, pk: int):
    Supplier.objects.filter(pk=pk).delete()
    return HttpResponse("")
