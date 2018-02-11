from django import forms


class LikertWidget(forms.RadioSelect):
    template_name = 'widgets/likert.html'


    def get_context(self, *args, **kwargs):
        context = super().get_context(*args, **kwargs)
        context.update({'choices': self.choices,
                        })
        return context
