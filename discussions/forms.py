from django import forms


class DiscussionForm(forms.Form):
    discussion_title = forms.CharField(label='Title', max_length=254,
                                       widget=forms.TextInput(
                                           attrs={'class': 'form-control', 'placeholder': 'Enter title'}))
    discussion_message = forms.CharField(label='Message', max_length=254,
                                         widget=forms.Textarea(
                                             attrs={'class': 'form-control', 'placeholder': 'Enter message',
                                                    'rows': 2}))

    def clean_title(self):
        title = self.cleaned_data['discussion_title']
        return title

    def clean_message(self):
        message = self.cleaned_data['discussion_message']
        return message


class DiscussionCommentForm(forms.Form):
    discussion_comment_message = forms.CharField(label='Message', max_length=254, widget=forms.Textarea(
        attrs={'class': 'form-control', 'placeholder': 'Enter message', 'rows': 2}))

    def clean_discussion_comment(self):
        discussion_comment_message = self.cleaned_data['discussion_comment_message']
        return discussion_comment_message
