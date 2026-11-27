from django import forms
from .models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = [
            "name",
            "category",
            "location",
            "location_detail",
            "incident_date",
            "description",
            "image",
        ]
        help_texts = {
            "location_detail": None,
        }
        widgets = {
            "incident_date": forms.DateInput(attrs={"type": "date"}),
            "incident_time": forms.TimeInput(
                format="%H:%M",
                attrs={"type": "time"},
            ),
            "location_detail": forms.TextInput(
                attrs={"placeholder": "Contoh: A6.07, Lab A1.02, Kantin"}
            ),
            "description": forms.Textarea(
                attrs={
                    "rows": 4,
                    "placeholder": "Ciri-ciri spesifik barang, warna, merek, atau kronologi singkat (opsional)",
                }
            ),
            "image": forms.ClearableFileInput(
                attrs={
                    "accept": "image/*",
                }
            ),
        }

    def clean(self):
        cleaned_data = super().clean()
        category = cleaned_data.get("category")
        image = cleaned_data.get("image")

        if category == Item.Category.DOKUMEN and image:
            self.add_error(
                "image",
                "Demi menjaga privasi, kategori Dokumen / Identitas tidak diperbolehkan mengunggah gambar.",
            )

        return cleaned_data