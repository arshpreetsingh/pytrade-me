from django import forms

class MainForm(forms.Form):
	
    CHOICES=[('BTC/USD','btcusd'),('ETH/USD','ethusd')]
    trading_size=forms.FloatField(required=True, max_value=100000)
    time = forms.FloatField(required=True, max_value=100000)
    currency = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    
    #Choose 1 of the following currency pairs on bitfinex btc/usd or eth/usd
