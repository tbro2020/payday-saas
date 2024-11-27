from django.forms import EmailField, ValidationError
from django.contrib.auth import get_user_model
from django.contrib.auth import forms


class UserCreationForm(forms.UserCreationForm):
    
    def clean_email(self):
        """Reject email that differ only in case."""
        email = self.cleaned_data.get("email")
        if (
            email
            and self._meta.model.objects.filter(email__iexact=email).exists()
        ):
            self._update_errors(
                ValidationError(
                    {
                        "email": self.instance.unique_error_message(
                            self._meta.model, ["email"]
                        )
                    }
                )
            )
        else:
            return email

    class Meta:
        fields = ("email",)
        model = get_user_model()
        field_classes = {"email": EmailField}