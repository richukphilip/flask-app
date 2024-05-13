from flask import Flask, render_template, request

app = Flask(__name__)

# Define the calculate_wacc_and_pgr function
def calculate_wacc_and_pgr(risk_level, growth_prospects, market_stability, tech_change):
    # Base values
    wacc_base = 15  # Base WACC percentage
    pgr_base = 2    # Base PGR percentage

    # Adjustments based on risk level and market stability
    if risk_level in ['Much lower', 'Lower'] and market_stability in ['Stable', 'Very stable']:
        wacc_adjustment = -2
    elif risk_level in ['Higher', 'Much higher'] or market_stability in ['Highly unstable', 'Somewhat unstable']:
        wacc_adjustment = 2
    else:
        wacc_adjustment = 0

    # Adjustments based on technological change
    if tech_change in ['Very rapidly', 'Rapidly']:
        wacc_adjustment += 1  # Increasing risk due to rapid change
        pgr_base += 1         # Potential for higher growth if leveraging tech effectively
    elif tech_change in ['Slowly', 'Very slowly']:
        wacc_adjustment -= 1  # Less risk from slow change
        pgr_base -= 1         # Lower growth prospects due to slower innovation

    # Final WACC and PGR calculation
    wacc = wacc_base + wacc_adjustment
    pgr = pgr_base

    # Adjust PGR based on growth prospects
    if growth_prospects in ['Very high growth', 'High growth']:
        pgr += 2
    elif growth_prospects in ['Moderate growth']:
        pgr += 1
    elif growth_prospects in ['Stable, low growth']:
        pgr = max(1, pgr)  # Ensuring not negative or zero
    else:
        pgr = 1  # Declining or negative growth scenario

    return wacc, pgr

# Flask route that uses the function
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Extract data from form
        risk_level = request.form['risk_level']
        growth_prospects = request.form['growth_prospects']
        market_stability = request.form['market_stability']
        tech_change = request.form['tech_change']
        cash_flows = list(map(int, request.form['cash_flows'].split(',')))

        # Calculate WACC and PGR using the function
        wacc, pgr = calculate_wacc_and_pgr(risk_level, growth_prospects, market_stability, tech_change)
        discount_rate = wacc / 100
        growth_rate = pgr / 100

        # Calculate present values of cash flows
        pv_cash_flows = [cf / ((1 + discount_rate) ** (t + 1)) for t, cf in enumerate(cash_flows)]
        terminal_value = cash_flows[-1] * (1 + growth_rate) / (discount_rate - growth_rate)
        pv_terminal_value = terminal_value / ((1 + discount_rate) ** len(cash_flows))
        total_dcf_value = sum(pv_cash_flows) + pv_terminal_value

        # Return results to the template
        return render_template('index.html', wacc=wacc, pgr=pgr, pv_cash_flows=pv_cash_flows, total_dcf_value=total_dcf_value/10)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
