from django import forms


class CustomerResisterForm(forms.Form):
    name = forms.CharField(
        label='名前',
        max_length=50,
        required=True,
        widget=forms.TextInput()
    )
    hurigana = forms.CharField(
        max_length=100,
        label='ふりがな',
        required=True,
        widget=forms.TextInput()
    )
    mail_address = forms.EmailField()
    address = forms.CharField(
        max_length=256,
        label='住所',
        required=True,
        widget=forms.TextInput()
    )
    telephone_number = forms.CharField(
        max_length=15,
        label='電話番号',
        required=True,
        widget=forms.TextInput()
    )
    password = forms.CharField(
        max_length=128,
        min_length=8,
        required=True,
        label='パスワード',
        widget=forms.TextInput()
    )
    gender = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(),
        label="性別(任意)"
    )



