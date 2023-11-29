from django import forms

class ChannelForm(forms.Form):
    channel_id = forms.CharField(label='YouTube Channel ID', max_length=50)
