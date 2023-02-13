from calculation_functions import saving_plan
import numpy as np

def main():
    end_price = 3_000_000               # förväntad slutpris
    cash = end_price * 0.15             # kontantinsats
    monthly_cost = 4_000                # månadsavgift
    operating_costs = 1000              # driftkostnad per månad
    living_costs = 20_000               # levnadskostnader på alla låntagare

    loan_amount = end_price - cash      # Lånebelopp
    loan_grade = 1 - cash / end_price   # Belåningsgrad
    payment_time = 50                   # Återbetalningstid
    payments_number = payment_time * 12 # Antal avbetalningar

    net_salary = 60000                  # Nettolön på alla låntagare
    money_available = net_salary - monthly_cost - operating_costs - living_costs

    assert money_available >= 0, f"Not enough money available, net amount: {money_available}"

    stock_yearly_interest = 2 / 100     # Förväntad börstillväxt %
    nominal_interest = 4 / 100          # bolåneränta %
    effective_interest = np.power((1 + nominal_interest / 12), 12) - 1

    # Extra
    stop_after_years = False    # Set to False or an integer > 0 for number of years

    best_results = -np.inf
    saved_results = []
    step = 1
    search_range = range(0, money_available+step, step) if money_available != 0 else [0]
    for mortgage_payment in search_range:
        results, saving_plan_months, invested_per_month = saving_plan(
            loan_amount,
            payments_number,
            nominal_interest=nominal_interest,
            saving_amount=money_available,
            mortgage_payment=mortgage_payment,
            interest_rate=stock_yearly_interest,
            early_stopping=stop_after_years
        )

        if results > best_results:
            best_results = results
            best_fixed_mortgage = mortgage_payment
            best_saving_plan_months = saving_plan_months
            best_invested_per_month = invested_per_month

        saved_results.append(results)
    
    assert best_results != -np.inf, f"\n\
    Cannot afford the interest and mortgage payments, with {money_available} SEK per month\n\
    Minimum required: {int(np.round(loan_amount / 12 * nominal_interest + loan_amount / payments_number))} SEK\n\
    Interest cost starting at: {int(np.round(loan_amount / 12 * nominal_interest))} SEK\n\
    Mortgage at: {int(np.round(loan_amount / payments_number))} SEK\n"
    
    print('--'*20)
    print(f"Purchase for end price: {end_price:,} SEK with an interest rate of {nominal_interest*100} %")
    print(f"Minimum mortgage payment required {int(np.round(loan_amount / payments_number))} SEK")
    print(f"Months available to pay off loan: {payments_number}")
    print(f"Estimated stock market yearly interest: {stock_yearly_interest * 100} %")

    print(f"\nBest end results: {best_results:,} SEK with {money_available:,} SEK available per month")
    print(f"Saving for {best_saving_plan_months} months, or {best_saving_plan_months/12:.1f} years")
    print(f"Mortgage payment (fixed): {best_fixed_mortgage:,} SEK per month")
    print(f"Additional mortgage from minimum required: {int(np.round(best_fixed_mortgage - loan_amount / payments_number))} SEK")
    if money_available > 0:
        print(f"Average stock market investment per month: {best_invested_per_month:,} SEK")
    else:
        print(f"Stock market investment per month: {0} SEK")
    # print(f"Results per fixed mortgage cost: {saved_results}")
    print('--'*20)

if __name__ == "__main__":
    main()