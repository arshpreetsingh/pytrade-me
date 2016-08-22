from django import forms

class MainForm(forms.Form):
	
    CHOICES=[('btcusd','BTC/USD'),('ethusd','ETH/USD')]
    CHOICES2 = [('bitfinex','Bitfinex'),('poloniex','POLONIEX')]
    trading_size=forms.FloatField(required=True, max_value=100000)
    amount = forms.FloatField(required=True, max_value=100000)
    currency = forms.ChoiceField(choices=CHOICES, widget=forms.RadioSelect())
    market = forms.ChoiceField(choices=CHOICES2, widget=forms.RadioSelect())
    #Choose 1 of the following currency pairs on bitfinex btc/usd or eth/usd
