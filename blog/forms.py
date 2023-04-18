from .models import Comment
from django import forms


# 댓글 form
# View 안에 form 을 넣을꺼임 ->forms.ModelForm
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        # 어떤 값들을 받아낼 것인지
        fields = ('content',)
