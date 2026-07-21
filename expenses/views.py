from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q
from django.http import HttpResponse

import csv

from .forms import TransactionForm
from .models import Transaction



@login_required
def add_transaction(request):

    if request.method == "POST":

        form = TransactionForm(request.POST)

        if form.is_valid():

            transaction = form.save(commit=False)

            transaction.user = request.user

            transaction.save()


            messages.success(
                request,
                "Transaction added successfully!"
            )


            return redirect(
                'transaction_list'
            )


    else:

        form = TransactionForm()



    return render(
        request,
        'add_transaction.html',
        {
            'form': form
        }
    )





@login_required
def transaction_list(request):

    transactions = Transaction.objects.filter(
        user=request.user
    )


    search = request.GET.get(
        'search'
    )


    if search:

        transactions = transactions.filter(
            Q(category__icontains=search) |
            Q(description__icontains=search)
        )



    transaction_type = request.GET.get(
        'type'
    )


    if transaction_type:

        transactions = transactions.filter(
            transaction_type=transaction_type
        )



    date = request.GET.get(
        'date'
    )


    if date:

        transactions = transactions.filter(
            date=date
        )



    transactions = transactions.order_by(
        '-date'
    )



    return render(
        request,
        'transaction_list.html',
        {
            'transactions': transactions
        }
    )







@login_required
def edit_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )



    if request.method == "POST":

        form = TransactionForm(
            request.POST,
            instance=transaction
        )


        if form.is_valid():

            form.save()


            messages.success(
                request,
                "Transaction updated successfully!"
            )


            return redirect(
                'transaction_list'
            )


    else:

        form = TransactionForm(
            instance=transaction
        )



    return render(
        request,
        'edit_transaction.html',
        {
            'form': form
        }
    )







@login_required
def delete_transaction(request, id):

    transaction = get_object_or_404(
        Transaction,
        id=id,
        user=request.user
    )



    if request.method == "POST":

        transaction.delete()


        messages.success(
            request,
            "Transaction deleted successfully!"
        )



    return redirect(
        'transaction_list'
    )









@login_required
def dashboard(request):

    transactions = Transaction.objects.filter(
        user=request.user
    )



    total_income = transactions.filter(
        transaction_type="Income"
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0




    total_expense = transactions.filter(
        transaction_type="Expense"
    ).aggregate(
        Sum('amount')
    )['amount__sum'] or 0




    balance = total_income - total_expense




    expense_data = transactions.filter(
        transaction_type="Expense"
    ).values(
        'category'
    ).annotate(
        total=Sum('amount')
    )




    categories = []

    amounts = []



    for item in expense_data:

        categories.append(
            item['category']
        )

        amounts.append(
            float(item['total'])
        )




    recent_transactions = transactions.order_by(
        '-date'
    )




    context = {

        'total_income': total_income,

        'total_expense': total_expense,

        'balance': balance,

        'categories': categories,

        'amounts': amounts,

        'transactions': recent_transactions,

    }




    return render(
        request,
        'dashboard.html',
        context
    )







@login_required
def export_csv(request):

    transactions = Transaction.objects.filter(
        user=request.user
    ).order_by('-date')



    response = HttpResponse(
        content_type='text/csv'
    )



    response['Content-Disposition'] = (
        'attachment; filename="transactions.csv"'
    )



    writer = csv.writer(response)



    writer.writerow(
        [
            'Date',
            'Type',
            'Category',
            'Amount',
            'Description'
        ]
    )



    for transaction in transactions:

        writer.writerow(
            [
                transaction.date,
                transaction.transaction_type,
                transaction.category,
                transaction.amount,
                transaction.description
            ]
        )



    return response