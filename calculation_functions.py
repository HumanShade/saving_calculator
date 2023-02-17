import numpy as np

def total_interest_cost(loan_amount, payments_number, nominal_interest=0, added_mortgage=0, fixed_mortage_cost=0):
        remaining_loan = loan_amount
        total_interest = 0
        months_taken = 0
        months_remaining = payments_number
        while remaining_loan > 0:
            interest_payment = remaining_loan / 12 * nominal_interest
            if fixed_mortage_cost == 0:
                mortgage_payment = remaining_loan / months_remaining + added_mortgage
            else:
                if fixed_mortage_cost < remaining_loan / months_remaining:
                    mortgage_payment = remaining_loan / months_remaining
                else:
                    mortgage_payment = fixed_mortage_cost

            total_interest += interest_payment
            remaining_loan -= mortgage_payment
            months_taken += 1
            months_remaining = payments_number - months_taken

        return int(np.round(total_interest)), months_taken

def stock_growth(monthly_deposit, interest_rate, months_saving):
        total_saved = 0
        monthly_interest_rate = np.power(1+interest_rate, 1/12)

        for _ in range(months_saving):
            total_saved *= monthly_interest_rate
            total_saved += monthly_deposit
        
        return  int(np.round(total_saved))

# TODO: Add belåningsgrad, 2 % amortering when above 70 % belåningsgrad, 1 % when above 50 %, 0 % otherwise
# TODO: Add monthly cost as return value: list of (interest payment + mortgage) per month
# TODO: Add ränteavdrag
# TODO: Break down the function into smaller functions for readability
# TODO: Add increased house valuation (Separate function)
# TODO: Add starting month instead of assuming that it starts in January (affects ränteavdrag)
# TODO: Add average yearly pay increase
def saving_plan(loan_amount, payments_number, nominal_interest=0, saving_amount=0, start_saving=0, mortgage_payment=0, interest_rate=0, early_stopping=False, yearly_pay_raise=0):
    # Housing
    remaining_loan = loan_amount
    loan_interest_paid = 0
    yearly_interest_paid = 0
    months_taken = 0
    first_month = 0
    last_month = 0
    interest_payment = 0

    # Stock market
    total_invested = 0 + start_saving
    stock_valuation = 0 + start_saving
    monthly_interest_rate = np.power(1 + interest_rate, 1/12)
    stock_interest_earned = 0
    monthly_saving = 0

    if mortgage_payment < loan_amount / payments_number:
        return -np.inf, np.inf, 0, 0, 0, 0, 0

    while remaining_loan > 0:
        interest_payment = remaining_loan / 12 * nominal_interest
        loan_interest_paid += interest_payment
        yearly_interest_paid += interest_payment
        remaining_loan -= mortgage_payment
        months_taken += 1

        if first_month == 0:
            first_month = mortgage_payment + interest_payment

        if saving_amount != 0:
            monthly_saving = saving_amount - mortgage_payment - interest_payment
            if monthly_saving >= 0:
                total_invested += monthly_saving
                stock_valuation += monthly_saving
                stock_valuation *= monthly_interest_rate
            else:
                return -np.inf, np.inf, 0, 0, 0, 0, 0

        # Yearly changes 
        if months_taken % 12 == 0:

            # Ränteavdrag
            if yearly_interest_paid <= 100_000:
                interest_deduction = yearly_interest_paid * 0.3
            else:
                # yearly_interest_paid > 100_000
                interest_deduction = 30_000 + (yearly_interest_paid - 100_000) * 0.21
            
            # For simplicity, it goes to the stocks?
            stock_valuation += interest_deduction
            total_invested += interest_deduction

            # Pay raises
            saving_amount += yearly_pay_raise


        if early_stopping and months_taken / 12 == early_stopping:
            break
    
    if last_month == 0:
        last_month = mortgage_payment + interest_payment

    stock_interest_earned = stock_valuation - total_invested
    results = stock_interest_earned - loan_interest_paid

    return int(np.round(results)), months_taken, int(round(total_invested / months_taken)), stock_valuation, remaining_loan, first_month, last_month