from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from .forms import ItemForm
from .models import Item


def home(request):
    recent_items = Item.objects.select_related("reporter").filter(
        status=Item.Status.ACTIVE
    )[:6]
    return render(request, "core/home.html", {"recent_items": recent_items})


def item_list(request):
    items = Item.objects.select_related("reporter").all()

    q = request.GET.get("q", "").strip()
    report_type = request.GET.get("report_type", "").strip()
    category = request.GET.get("category", "").strip()
    location = request.GET.get("location", "").strip()
    status = request.GET.get("status", "").strip()

    if q:
        items = items.filter(
            Q(name__icontains=q) | Q(location_detail__icontains=q)
        )
    if report_type:
        items = items.filter(report_type=report_type)
    if category:
        items = items.filter(category=category)
    if location:
        items = items.filter(location=location)
    if status:
        items = items.filter(status=status)

    context = {
        "items": items,
        "report_types": Item.ReportType.choices,
        "categories": Item.Category.choices,
        "locations": Item.Location.choices,
        "statuses": Item.Status.choices,
        "selected_q": q,
        "selected_report_type": report_type,
        "selected_category": category,
        "selected_location": location,
        "selected_status": status,
    }
    return render(request, "core/item_list.html", context)


def item_detail(request, pk):
    item = get_object_or_404(Item.objects.select_related("reporter"), pk=pk)
    can_manage = request.user.is_authenticated and (
        item.reporter == request.user or request.user.is_staff
    )
    return render(
        request,
        "core/item_detail.html",
        {"item": item, "can_manage": can_manage},
    )

def _handle_item_create(request, report_type, form_title):
    if request.method == "POST":
        item = Item(report_type=report_type)
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            item = form.save(commit=False)
            item.report_type = report_type
            item.reporter = request.user
            item.save()
            messages.success(request, "Laporan barang berhasil dipublikasikan.")
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm()

    return render(
        request,
        "core/item_form.html",
        {"form": form, "form_title": form_title},
    )

@login_required
def item_create_lost(request):
    return _handle_item_create(
        request,
        Item.ReportType.LOST,
        "Lapor Barang Saya yang Hilang",
    )


@login_required
def item_create_found(request):
    return _handle_item_create(
        request,
        Item.ReportType.FOUND,
        "Lapor Penemuan Barang Hilang",
    )


@login_required
def item_update(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.reporter != request.user and not request.user.is_staff:
        raise PermissionDenied("Anda tidak memiliki izin untuk mengedit laporan ini.")

    if request.method == "POST":
        form = ItemForm(request.POST, request.FILES, instance=item)
        if form.is_valid():
            form.save()
            messages.success(request, "Laporan barang berhasil diperbarui.")
            return redirect("item_detail", pk=item.pk)
    else:
        form = ItemForm(instance=item)

    return render(
        request,
        "core/item_form.html",
        {"form": form, "item": item, "form_title": "Edit Laporan Barang"},
    )


@login_required
def item_delete(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.reporter != request.user and not request.user.is_staff:
        raise PermissionDenied("Anda tidak memiliki izin untuk menghapus laporan ini.")

    if request.method == "POST":
        item.delete()
        messages.success(request, "Laporan barang berhasil dihapus.")
        return redirect("item_list")

    return render(request, "core/item_confirm_delete.html", {"item": item})


@login_required
@require_POST
def item_toggle_status(request, pk):
    item = get_object_or_404(Item, pk=pk)
    if item.reporter != request.user and not request.user.is_staff:
        raise PermissionDenied("Anda tidak memiliki izin mengubah status laporan ini.")

    if item.status == Item.Status.ACTIVE:
        item.status = Item.Status.RETURNED
        messages.success(request, "Status barang diubah menjadi Returned.")
    else:
        item.status = Item.Status.ACTIVE
        messages.success(request, "Status barang diubah kembali menjadi Active.")

    item.save(update_fields=["status", "updated_at"])
    return redirect("item_detail", pk=item.pk)