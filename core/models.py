from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError

# Create your models here.
class Item(models.Model):
    class ReportType(models.TextChoices):  # models.TextChoices menjabarkan pilihan nilai teks
        LOST = "LOST", "Lost (Barang Hilang)"
        FOUND = "FOUND", "Found (Barang telah Ditemukan)"

    class Category(models.TextChoices):
        DOKUMEN = "DOKUMEN", "Dokumen / Identitas (KTP, KTM, SIM, dan sejenisnya)"
        KUNCI_KENDARAAN = "KUNCI_KENDARAAN", "Kunci Kendaraan"
        ELEKTRONIK = "ELEKTRONIK", "Elektronik & Gadget"
        AKSESORIS = "AKSESORIS", "Aksesoris & Barang Pribadi (Dompet, Kunci, Kacamata)"
        ALAT_TULIS = "ALAT_TULIS", "Alat Tulis & Buku"
        PERLENGKAPAN_MAKAN = "PERLENGKAPAN_MAKAN", "Alat Makan, Air, Botol Minum/Tumbler, dan sejenisnya"
        LAINNYA = "LAINNYA", "Lainnya"

    class Location(models.TextChoices):
        GEDLAM = "GEDLAM", "Gedung Lama"
        GEDBAR_DAN_GEDBARBAR = "GEDBAR_DAN_GEDBARBAR", "Gedung Baru dan Gedung Baru Baru"

    class Status(models.TextChoices):
        ACTIVE = "ACTIVE", "Active"
        RETURNED = "RETURNED", "Returned"

    # Membuat relasi Many-to-One di database
    reporter = models.ForeignKey(
        settings.AUTH_USER_MODEL,  # merujuk ke tabel User yang aktif
        on_delete=models.CASCADE,  # jika akun user dihapus, barang yang pernah ia lapor juga terhapus
        related_name="reported_items",  # bisa mengambil semua barang yang pernah dilaporkan oleh seorang user
    )

    report_type = models.CharField(
        max_length=18,
        choices=ReportType.choices,
    )

    name = models.CharField(max_length=150)

    category = models.CharField(
        max_length=20,
        choices=Category.choices,
    )

    description = models.TextField(blank=True)

    location = models.CharField(
        max_length=30,
        choices=Location.choices,
        verbose_name="Gedung",
    )

    location_detail = models.CharField(
        max_length=150,
        verbose_name="Detail Lokasi / Ruangan",
        help_text="Contoh: A6.07, Lab A1.02, atau yang lainnya",
    )

    # Input manual waktu oleh user, terlepas dari date yang di bawah
    incident_date = models.DateField(verbose_name="Tanggal Kejadian")
    incident_time = models.TimeField(
        blank=True,
        null=True,
        verbose_name="Waktu Kejadian (Opsional)",
    )

    image = models.ImageField(
        upload_to="items/",
        blank=True,
        null=True,
    )

    status = models.CharField(
        max_length=10,
        choices=Status.choices,
        default=Status.ACTIVE,
    )

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    # Metadata, mengatur perilaku tabel secara keseluruhan
    class Meta:
        ordering = ["-created_at"]


    # Validasi formulir sebelum data masuk database
    def clean(self):
        super().clean()
        if self.category == self.Category.DOKUMEN and self.image:
            raise ValidationError(
                {
                    "image": "Demi menjaga privasi, kategori Dokumen/Identitas tidak perlu mengunggah gambar."
                }
            )

    def save(self, *args, **kwargs):
        if self.category == self.Category.DOKUMEN:
            self.image = None
        # Save yang di bawah ini adalah save asli miliki models.Model
        # inilah yang mengeksekusi perintah SQL untuk menulis data ke database
        super().save(*args, **kwargs)

    def __str__(self):
        # get_<nama_field>_display() untuk menampilkan teks label mudah dibaca milik ReportType
        return f"[{self.get_report_type_display()}] {self.name} - {self.get_location_display()} ({self.location_detail})"