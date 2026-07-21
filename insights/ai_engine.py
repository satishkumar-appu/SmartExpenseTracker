from django.db.models import Sum


def generate_insights(transactions):

    insights = []


    expenses = transactions.filter(
        transaction_type="Expense"
    )


    income = transactions.filter(
        transaction_type="Income"
    ).aggregate(
        total=Sum('amount')
    )['total'] or 0



    expense_total = expenses.aggregate(
        total=Sum('amount')
    )['total'] or 0



    # Saving analysis

    savings = income - expense_total


    if expense_total > income:

        insights.append(
            "⚠️ Your expenses are higher than your income. Try reducing unnecessary spending."
        )

    else:

        insights.append(
            f"💰 Good job! You saved ₹{savings}. Keep maintaining this habit."
        )



    # Highest expense category

    category = expenses.values(
        'category'
    ).annotate(
        total=Sum('amount')
    ).order_by(
        '-total'
    ).first()



    if category:

        insights.append(
            f"📌 Your highest spending category is {category['category']} (₹{category['total']})."
        )



        # Category specific advice

        if category['category'] == "Food":

            insights.append(
                "🍔 Food spending is high. Try cooking more at home to save money."
            )


        elif category['category'] == "Travel":

            insights.append(
                "🚗 Transport expenses are high. Consider cheaper travel options."
            )


        elif category['category'] == "Shopping":

            insights.append(
                "🛒 Shopping expenses are high. Avoid unnecessary purchases."
            )


        elif category['category'] == "Bills":

            insights.append(
                "💡 Review your bills and check for unnecessary subscriptions."
            )



    # Expense control advice

    if expense_total > 5000:

        insights.append(
            "📊 Your spending is increasing. Setting a monthly budget can help control expenses."
        )


    elif expense_total == 0:

        insights.append(
            "📝 Add some expenses to receive personalized financial advice."
        )


    else:

        insights.append(
            "✅ Your expenses are under control. Continue tracking regularly."
        )


    return insights