from django import forms
from .models import Entry

class EntryForm(forms.ModelForm):
    class Meta:
        model=Entry
        fields=['text']
        labels={'text':''}
        widgets={'text':forms.Textarea(attrs={'cols':80})}#widget小部件，可设置属性更改部件类型，如单行文本框、多行、下拉列表