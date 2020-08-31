from flask import Flask, render_template, request, redirect
import pandas as pd

# Must be named "application" for AWS deployment to work properly
app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config['TEMPLATES_AUTO_RELOAD'] = True

# Declare coins dict and initialize counts to zero (0)
coins = {'Coins': ['Silver Dollar', 'Half Dollar', 'Quarter', 'Dime', 'Nickel', 'Penny'],
         'Values': [1.00, .50, .25, .10, .05, .01],
         'Count': [0, 0, 0, 0, 0, 0]}


@app.route('/')
def index():
    
    # Reset count of coins to be zero
    coins['Count'][0] = 0
    coins['Count'][1] = 0
    coins['Count'][2] = 0
    coins['Count'][3] = 0
    coins['Count'][4] = 0
    coins['Count'][5] = 0
    
    # Convert updated dict to dataframe
    coins_df = pd.DataFrame.from_dict(coins, orient='columns')
    
    # Convert the dataframe to HTML table with centered text
    coins_html = coins_df.to_html(index=False, classes='table table-striped', columns=['Coins', 'Count']).replace('<tr style="text-align: right;">', '<tr style="text-align: center;">').replace('<tbody>', '<tbody style="text-align: center;">')

    # Display index.html page and coins table with values set to zero (0)
    return render_template('index.html', table=coins_html)


@app.route('/count_coins', methods=['GET', 'POST'])
def count_coins():
    
    # Ensure the form was submitted via the "Submit" button
    if request.method == 'POST' and 'submit' in request.form:
        
        # Get dollar amount from user
        cents_dec = request.form.get('amount')
        
        # Build the output string displaying the entered amount
        cents_str = 'Amount: $' + cents_dec
        
        # Convert decimal amount to whole number for calculations below
        cents = int(float(cents_dec) * 100)

        # Calculate and update the count for each coin
        coins['Count'][0] = cents // 100  # Silver Dollar
        coins['Count'][1] = (cents % 100) // 50  # Half Dollar
        coins['Count'][2] = ((cents % 100) % 50) // 25  # Quarter
        coins['Count'][3] = (((cents % 100) % 50) % 25) // 10  # Dime
        coins['Count'][4] = ((((cents % 100) % 50) % 25) % 10) // 5  # Nickel
        coins['Count'][5] = (((((cents % 100) % 50) % 25) % 10) % 5)  # Penny
        
        # Convert updated dict to dataframe
        coins_df = pd.DataFrame.from_dict(coins, orient='columns')
        
        # Convert the dataframe to HTML table with centered text
        coins_html = coins_df.to_html(index=False, classes='table table-striped', columns=['Coins', 'Count']).replace('<tr style="text-align: right;">', '<tr style="text-align: center;">').replace('<tbody>', '<tbody style="text-align: center;">')
        
        # Display index.html page and updated coins table
        return render_template('index.html', cents_str=cents_str, table=coins_html)
    
    # If form submitted via the "Reset" button redirect to index method which resets the counts.
    elif request.method == 'POST' and 'reset' in request.form:
        
        return redirect('/')