from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Avg
from django.db.models.functions import TruncMonth
from django.http import HttpResponse

from reportlab.pdfgen import canvas

from expenses.models import Transaction

from .ai_engine import generate_insights



@login_required
def insights_page(request):

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



    average_expense = transactions.filter(
        transaction_type="Expense"
    ).aggregate(
        Avg('amount')
    )['amount__avg'] or 0



    category_data = transactions.filter(
        transaction_type="Expense"
    ).values(
        'category'
    ).annotate(
        total=Sum('amount')
    ).order_by(
        '-total'
    )


    highest_category = "No Data"


    if category_data:
        highest_category = category_data[0]['category']



    monthly_savings = balance



    messages = generate_insights(
        transactions
    )



    monthly_expenses = transactions.filter(
        transaction_type="Expense"
    ).annotate(
        month=TruncMonth('date')
    ).values(
        'month'
    ).annotate(
        total=Sum('amount')
    ).order_by(
        'month'
    )



    months = []

    monthly_amounts = []


    for item in monthly_expenses:

        months.append(
            item['month'].strftime('%b')
        )

        monthly_amounts.append(
            float(item['total'])
        )



    context = {

        "messages": messages,

        "total_income": total_income,

        "total_expense": total_expense,

        "balance": balance,

        "average_expense": round(
            average_expense,
            2
        ),

        "highest_category": highest_category,

        "monthly_savings": monthly_savings,

        "expense_data": category_data,

        "months": months,

        "monthly_amounts": monthly_amounts,

    }



    return render(
        request,
        "insights.html",
        context
    )





@login_required
def download_report(request):

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



    messages = generate_insights(
        transactions
    )



    response = HttpResponse(
        content_type="application/pdf"
    )


    response["Content-Disposition"] = (
        'attachment; filename="Smart_Expense_Report.pdf"'
    )



    pdf = canvas.Canvas(response)



    pdf.setFont(
        "Helvetica-Bold",
        16
    )


    pdf.drawString(
        50,
        800,
        "Smart Expense Tracker Report"
    )



    pdf.setFont(
        "Helvetica",
        12
    )


    y = 760


    data = [

        f"Total Income: Rs.{total_income}",

        f"Total Expense: Rs.{total_expense}",

        f"Balance: Rs.{balance}",

    ]



    for line in data:

        pdf.drawString(
            50,
            y,
            line
        )

        y -= 30



    y -= 20


    pdf.drawString(
        50,
        y,
        "Smart Advice:"
    )


    y -= 30



    for message in messages:

        pdf.drawString(
            50,
            y,
            message[:90]
        )

        y -= 25



    pdf.save()


    return response