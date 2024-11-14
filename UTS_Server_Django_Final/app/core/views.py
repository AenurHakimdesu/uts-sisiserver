from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Count, Sum, Avg, F, DecimalField, ExpressionWrapper
from django.contrib import messages
from .models import Item, Category, Supplier, Admin
from .forms import ItemForm, CategoryForm, SupplierForm

def dashboard(request):
    total_items = Item.objects.count()
    total_stock_value = Item.objects.aggregate(
        total=Sum(F('price') * F('quantity'))
    )['total'] or 0
    total_categories = Category.objects.count()
    total_suppliers = Supplier.objects.count()
    
    context = {
        'total_items': total_items,
        'total_stock_value': total_stock_value,
        'total_categories': total_categories,
        'total_suppliers': total_suppliers,
    }
    return render(request, '../templates/dashboard.html', context)

def item_list(request):
    items = Item.objects.all()
    stats = Item.objects.aggregate(
        total_stock=Sum('quantity'),
        total_value=Sum(F('price') * F('quantity')),
        avg_price=Avg('price')
    )
    low_stock_items = Item.objects.filter(quantity__lt=5)
    
    for item in items:
        item.total_value = item.price * item.quantity  # Calculate stock value per item
        
    context = {
        'items': items,
        'stats': stats,
        'low_stock_items': low_stock_items,
    }
    return render(request, '../templates/item_list.html', context)

def item_create(request):
    if request.method == 'POST':
        form = ItemForm(request.POST)
        if form.is_valid():
            item = form.save(commit=False)
            try:
                admin = Admin.objects.get(username=request.user.username)
                item.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Admin profile not found for this user. Please contact support.')
                return redirect('item_list')
            item.save()
            messages.success(request, 'Item successfully added.')
            return redirect('item_list')
    else:
        form = ItemForm()
    
    return render(request, '../templates/item_form.html', {'form': form})

def category_list(request):
    categories = Category.objects.annotate(
        item_count=Count('item'),
        total_value=Sum(F('item__price') * F('item__quantity')),
        avg_price=Avg('item__price')
    )
    return render(request, '../templates/category_list.html', {'categories': categories})

def category_create(request):
    if request.method == 'POST':
        form = CategoryForm(request.POST)
        if form.is_valid():
            category = form.save(commit=False)
            try:
                admin = Admin.objects.get(username=request.user.username)
                category.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Admin profile not found for this user. Please contact support.')
                return redirect('category_list')
            category.save()
            messages.success(request, 'Category successfully added.')
            return redirect('category_list')
    else:
        form = CategoryForm()
    
    return render(request, '../templates/category_form.html', {'form': form})

def supplier_list(request):
    suppliers = Supplier.objects.annotate(
        item_count=Count('item'),
        total_value=Sum(F('item__price') * F('item__quantity'))
    )
    return render(request, '../templates/suppliers_list.html', {'suppliers': suppliers})

def supplier_create(request):
    if request.method == 'POST':
        form = SupplierForm(request.POST)
        if form.is_valid():
            supplier = form.save(commit=False)
            try:
                admin = Admin.objects.get(username=request.user.username)
                supplier.created_by = admin
            except Admin.DoesNotExist:
                messages.error(request, 'Admin profile not found for this user. Please contact support.')
                return redirect('supplier_list')
            supplier.save()
            messages.success(request, 'Supplier successfully added.')
            return redirect('supplier_list')
    else:
        form = SupplierForm()
    
    return render(request, '../templates/suppliers_form.html', {'form': form})

def category_items(request, category_id):
    # Ambil kategori dengan kalkulasi tambahan
    category = Category.objects.annotate(
        item_count=Count('item'),
        total_value=ExpressionWrapper(
            Sum(F('item__price') * F('item__quantity')), 
            output_field=DecimalField(max_digits=15, decimal_places=2)
        ),
        avg_price=ExpressionWrapper(
            Avg('item__price'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    ).get(id=category_id)

    # Ambil items dan hitung total value per item
    items = Item.objects.filter(category=category).annotate(
        total_value=ExpressionWrapper(
            F('price') * F('quantity'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    )

    # Hitung total keseluruhan
    totals = items.aggregate(
        total_quantity=Sum('quantity'),
        total_value=Sum(
            F('price') * F('quantity'),
            output_field=DecimalField(max_digits=15, decimal_places=2)
        )
    )

    return render(request, '../templates/category_items.html', {
        'category': category,
        'items': items,
        'total_quantity': totals['total_quantity'] or 0,
        'total_value': totals['total_value'] or 0
    })
