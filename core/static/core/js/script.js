document.addEventListener("DOMContentLoaded", function () {
    // 1. Toggle menu mobile di Navbar
    const mobileBtn = document.getElementById("mobile-menu-btn");
    const mobileMenu = document.getElementById("mobile-menu");
    if (mobileBtn && mobileMenu) {
        mobileBtn.addEventListener("click", function () {
            mobileMenu.classList.toggle("hidden");
        });
    }

    // 2. Tombol tutup notifikasi Django messages
    document.querySelectorAll(".alert-close").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const banner = btn.closest(".alert-banner");
            if (banner) banner.remove();
        });
    });

    // 3. Tombol "Gunakan Tanggal Hari Ini" di Form Laporan
    const todayBtn = document.getElementById("btn-today-date");
    const dateInput = document.getElementById("id_incident_date");
    if (todayBtn && dateInput) {
        todayBtn.addEventListener("click", function () {
            const now = new Date();
            const year = now.getFullYear();
            const month = String(now.getMonth() + 1).padStart(2, "0");
            const day = String(now.getDate()).padStart(2, "0");
            dateInput.value = `${year}-${month}-${day}`;
        });
    }

    // 4. Aturan Privasi: Sembunyikan & nonaktifkan upload foto untuk kategori DOKUMEN
    const categorySelect = document.getElementById("id_category");
    const imageWrapper = document.getElementById("image-field-wrapper");
    const imageInput = document.getElementById("id_image");
    const privacyNotice = document.getElementById("dokumen-privacy-notice");
    const previewBox = document.getElementById("image-preview-box");
    const previewImg = document.getElementById("image-preview");

    function updateImagePrivacyState() {
        if (!categorySelect || !imageWrapper || !privacyNotice) return;

        if (categorySelect.value === "DOKUMEN") {
            imageWrapper.classList.add("hidden");
            privacyNotice.classList.remove("hidden");
            if (imageInput) {
                imageInput.value = "";
                imageInput.disabled = true;
            }
            if (previewBox) previewBox.classList.add("hidden");
        } else {
            imageWrapper.classList.remove("hidden");
            privacyNotice.classList.add("hidden");
            if (imageInput) {
                imageInput.disabled = false;
            }
        }
    }

    if (categorySelect) {
        categorySelect.addEventListener("change", updateImagePrivacyState);
        updateImagePrivacyState(); // Jalankan langsung saat halaman dimuat
    }

    // 5. Pratinjau foto sebelum diunggah di Form Laporan
    if (imageInput && previewBox && previewImg) {
        imageInput.addEventListener("change", function () {
            const file = imageInput.files && imageInput.files[0];
            if (file) {
                const reader = new FileReader();
                reader.onload = function (e) {
                    previewImg.src = e.target.result;
                    previewBox.classList.remove("hidden");
                };
                reader.readAsDataURL(file);
            } else {
                previewBox.classList.add("hidden");
            }
        });
    }

    // 6. Modal "Contact Reporter" di Halaman Detail Barang
    const contactModal = document.getElementById("contact-modal");
    const openContactBtn = document.getElementById("open-contact-modal");
    const closeContactBtns = document.querySelectorAll(".close-contact-modal");

    if (contactModal && openContactBtn) {
        openContactBtn.addEventListener("click", function () {
            contactModal.classList.remove("hidden");
        });

        closeContactBtns.forEach(function (btn) {
            btn.addEventListener("click", function () {
                contactModal.classList.add("hidden");
            });
        });

        contactModal.addEventListener("click", function (e) {
            if (e.target === contactModal) {
                contactModal.classList.add("hidden");
            }
        });
    }

    // 7. Tombol Salin Kontak ke Clipboard
    document.querySelectorAll(".copy-contact-btn").forEach(function (btn) {
        btn.addEventListener("click", function () {
            const value = btn.getAttribute("data-copy");
            if (!value) return;
            navigator.clipboard.writeText(value).then(function () {
                const originalText = btn.textContent;
                btn.textContent = "Tersalin!";
                setTimeout(function () {
                    btn.textContent = originalText;
                }, 1800);
            });
        });
    });
});