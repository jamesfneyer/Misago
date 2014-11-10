from django.utils.translation import ugettext_lazy as _, ungettext

from misago.conf import settings
from misago.core import forms
from misago.markup import common_flavour

from misago.threads.validators import validate_title


class ReplyForm(forms.Form):
    is_main = True
    legend = _("Reply")
    template = "misago/posting/replyform.html"
    js_template = "misago/posting/replyform_js.html"

    post = forms.CharField(label=_("Message body"), required=False)

    def __init__(self, post=None, request=None, *args, **kwargs):
        self.request = request
        self.post_instance = post
        self.parsing_result = {}

        super(ReplyForm, self).__init__(*args, **kwargs)

    def validate_post(self, post):
        if self.post_instance.original != post:
            self._validate_post(post)
            self.parse_post(post)

    def _validate_post(self, post):
        post_len = len(post)
        if not post_len:
            raise forms.ValidationError(_("Enter message."))

        if post_len < settings.post_length_min:
            message = ungettext(
                "Posted message should be at least %(limit)s character long.",
                "Posted message should be at least %(limit)s characters long.",
                settings.post_length_min)
            message = message % {'limit': settings.post_length_min}
            raise forms.ValidationError(message)

        if settings.post_length_max and post_len > settings.post_length_max:
            message = ungettext(
                "Posted message can't be longer than %(limit)s character.",
                "Posted message can't be longer than %(limit)s characters.",
                settings.post_length_max,)
            message = message % {'limit': settings.post_length_max}
            raise forms.ValidationError(message)

    def parse_post(self, post):
        self.parsing_result = common_flavour(
            self.request, self.post_instance.poster, post)

        self.post_instance.original = self.parsing_result['original_text']
        self.post_instance.parsed = self.parsing_result['parsed_text']

    def validate_data(self, data):
        self.validate_post(data.get('post', ''))

    def clean(self):
        data = super(ReplyForm, self).clean()
        self.validate_data(data)
        return data


class ThreadForm(ReplyForm):
    legend = _("Thread ")

    title = forms.CharField(label=_("Thread title"), required=False)

    def __init__(self, thread=None, *args, **kwargs):
        self.thread_instance = thread
        super(ThreadForm, self).__init__(*args, **kwargs)

    def validate_data(self, data):
        errors = []

        if not data.get('title') and not data.get('post'):
            raise forms.ValidationError(_("Enter thread title and message."))

        try:
            validate_title(data.get('title', ''))
        except forms.ValidationError as e:
            errors.append(e)

        try:
            self.validate_post(data.get('post', ''))
        except forms.ValidationError as e:
            errors.append(e)

        if errors:
            raise forms.ValidationError(errors)


class ThreadLabelFormBase(forms.Form):
    is_supporting = True
    location = 'after_title'
    template = "misago/posting/threadlabelform.html"


def ThreadLabelForm(*args, **kwargs):
    labels = kwargs.pop('labels')

    choices = [(0, _("No label"))]
    choices.extend([(label.pk, label.name ) for label in labels])

    field = forms.TypedChoiceField(
        label=_("Thread label"),
        coerce=int,
        choices=choices)

    FormType = type("ThreadLabelFormFinal",
                    (ThreadLabelFormBase,),
                    {'label': field})

    return FormType(*args, **kwargs)


class ThreadPinForm(forms.Form):
    is_supporting = True
    location = 'lefthand'
    template = "misago/posting/threadpinform.html"

    is_pinned = forms.YesNoSwitch(
        label=_("Pin thread"),
        yes_label=_("Pinned thread"),
        no_label=_("Unpinned thread"))


class ThreadCloseForm(forms.Form):
    is_supporting = True
    location = 'lefthand'
    template = "misago/posting/threadcloseform.html"

    is_closed = forms.YesNoSwitch(
        label=_("Close thread"),
        yes_label=_("Closed thread"),
        no_label=_("Open thread"))