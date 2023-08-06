import json
import email

from django import forms
from django.forms import widgets
from django.contrib.postgres import forms as pg_forms

from wapipelines.models import Pipeline, Step


class HTTPHeaderField(forms.Field):

    def clean(self, data):
        if data and ':' not in data:
            raise forms.ValidationError(
                'Headers must be in Key: Value format.')
        message = email.message_from_string(data)
        return dict([
            (key, message.get(key))
            for key in message.keys()])


class HTTPHeaderWidget(forms.Textarea):

    def format_value(self, raw_value):
        if not raw_value:
            return ''
        if isinstance(raw_value, basestring):
            return raw_value

        return '\n'.join([
            '%s: %s' % (key, value)
            for key, value in raw_value.items()
        ])


class CreatePipelineForm(forms.ModelForm):
    name = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}))
    endpoint = forms.URLField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = Pipeline
        fields = (
            'name',
            'active',
            'endpoint',
        )


class CreateStepForm(forms.ModelForm):
    name = forms.CharField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}))
    url = forms.URLField(
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        help_text=('Specify a URL to request outputs from, leave blank if '
                   'this step is only going to be used for waiting for '
                   'outputs from preceding steps'),
        required=False)
    timeout = forms.CharField(
        widget=widgets.Select(attrs={'class': 'form-control'},
                              choices=Step.TIMEOUT_CHOICES))
    inputs = pg_forms.SimpleArrayField(
        forms.CharField(),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)
    outputs = pg_forms.SimpleArrayField(
        forms.CharField(),
        widget=widgets.TextInput(attrs={'class': 'form-control'}),
        required=False)
    headers = HTTPHeaderField(
        widget=HTTPHeaderWidget(attrs={'class': 'form-control'}),
        required=False)

    class Meta:
        model = Step
        fields = (
            'name',
            'url',
            'timeout',
            'inputs',
            'outputs',
            'headers',
        )


class PipelineRunForm(forms.Form):
    data = forms.CharField(
        widget=forms.Textarea(attrs={'class': 'form-control'}),
        required=True)

    def clean_data(self):
        raw_data = self.cleaned_data['data']
        if not raw_data:
            raise forms.ValidationError('A JSON value is required')
        try:
            return json.loads(raw_data)
        except (ValueError,):
            raise forms.ValidationError('Invalid JSON')
