"""
MedLinka — Internationalization (i18n)
Supports: Arabic (ar), Turkish (tr), English (en)
"""

from typing import Optional
from app.config import settings

# ─────────────────────────────────────────────────────────────
# Translation strings
# ─────────────────────────────────────────────────────────────
TRANSLATIONS: dict[str, dict[str, str]] = {

    # ── Auth ────────────────────────────────────────────────
    "auth.login_success": {
        "ar": "تم تسجيل الدخول بنجاح",
        "tr": "Giriş başarılı",
        "en": "Login successful",
    },
    "auth.logout_success": {
        "ar": "تم تسجيل الخروج بنجاح",
        "tr": "Çıkış başarılı",
        "en": "Logout successful",
    },
    "auth.register_success": {
        "ar": "تم إنشاء الحساب بنجاح",
        "tr": "Hesap başarıyla oluşturuldu",
        "en": "Account created successfully",
    },
    "auth.invalid_credentials": {
        "ar": "البريد الإلكتروني أو كلمة المرور غير صحيحة",
        "tr": "Geçersiz e-posta veya şifre",
        "en": "Invalid email or password",
    },
    "auth.email_taken": {
        "ar": "البريد الإلكتروني مستخدم بالفعل",
        "tr": "Bu e-posta zaten kullanımda",
        "en": "Email already in use",
    },
    "auth.token_expired": {
        "ar": "انتهت صلاحية الجلسة، يرجى تسجيل الدخول مجدداً",
        "tr": "Oturum süresi doldu, lütfen tekrar giriş yapın",
        "en": "Session expired, please login again",
    },
    "auth.unauthorized": {
        "ar": "غير مصرح لك بالوصول",
        "tr": "Erişim izniniz yok",
        "en": "Unauthorized access",
    },
    "auth.forbidden": {
        "ar": "ليس لديك صلاحية لهذا الإجراء",
        "tr": "Bu işlem için yetkiniz yok",
        "en": "You do not have permission for this action",
    },

    # ── User ────────────────────────────────────────────────
    "user.not_found": {
        "ar": "المستخدم غير موجود",
        "tr": "Kullanıcı bulunamadı",
        "en": "User not found",
    },
    "user.profile_updated": {
        "ar": "تم تحديث الملف الشخصي بنجاح",
        "tr": "Profil başarıyla güncellendi",
        "en": "Profile updated successfully",
    },
    "user.password_changed": {
        "ar": "تم تغيير كلمة المرور بنجاح",
        "tr": "Şifre başarıyla değiştirildi",
        "en": "Password changed successfully",
    },
    "user.wrong_password": {
        "ar": "كلمة المرور الحالية غير صحيحة",
        "tr": "Mevcut şifre yanlış",
        "en": "Current password is incorrect",
    },

    # ── Appointments ────────────────────────────────────────
    "appointment.booked": {
        "ar": "تم حجز الموعد بنجاح",
        "tr": "Randevu başarıyla alındı",
        "en": "Appointment booked successfully",
    },
    "appointment.cancelled": {
        "ar": "تم إلغاء الموعد",
        "tr": "Randevu iptal edildi",
        "en": "Appointment cancelled",
    },
    "appointment.not_found": {
        "ar": "الموعد غير موجود",
        "tr": "Randevu bulunamadı",
        "en": "Appointment not found",
    },
    "appointment.slot_taken": {
        "ar": "هذا الموعد محجوز بالفعل، يرجى اختيار وقت آخر",
        "tr": "Bu randevu zaten alınmış, lütfen başka bir saat seçin",
        "en": "This slot is already taken, please choose another time",
    },
    "appointment.cannot_cancel_past": {
        "ar": "لا يمكن إلغاء موعد قد مضى",
        "tr": "Geçmiş bir randevu iptal edilemez",
        "en": "Cannot cancel a past appointment",
    },
    "appointment.reminder_set": {
        "ar": "تم ضبط تذكير الموعد",
        "tr": "Randevu hatırlatıcısı ayarlandı",
        "en": "Appointment reminder set",
    },

    # ── Doctor ──────────────────────────────────────────────
    "doctor.not_found": {
        "ar": "الطبيب غير موجود",
        "tr": "Doktor bulunamadı",
        "en": "Doctor not found",
    },
    "doctor.unavailable": {
        "ar": "الطبيب غير متاح في هذا الوقت",
        "tr": "Doktor bu saatte müsait değil",
        "en": "Doctor is not available at this time",
    },

    # ── Pharmacy & Orders ───────────────────────────────────
    "medicine.not_found": {
        "ar": "الدواء غير موجود",
        "tr": "İlaç bulunamadı",
        "en": "Medicine not found",
    },
    "medicine.out_of_stock": {
        "ar": "الدواء غير متوفر حالياً",
        "tr": "İlaç şu anda stokta yok",
        "en": "Medicine is currently out of stock",
    },
    "order.placed": {
        "ar": "تم تقديم الطلب بنجاح",
        "tr": "Sipariş başarıyla verildi",
        "en": "Order placed successfully",
    },
    "order.cancelled": {
        "ar": "تم إلغاء الطلب",
        "tr": "Sipariş iptal edildi",
        "en": "Order cancelled",
    },
    "order.not_found": {
        "ar": "الطلب غير موجود",
        "tr": "Sipariş bulunamadı",
        "en": "Order not found",
    },
    "order.already_shipped": {
        "ar": "لا يمكن الإلغاء، الطلب قيد الشحن بالفعل",
        "tr": "İptal edilemiyor, sipariş zaten kargoya verildi",
        "en": "Cannot cancel, order is already shipped",
    },

    # ── Reminders ───────────────────────────────────────────
    "reminder.created": {
        "ar": "تم إنشاء التذكير بنجاح",
        "tr": "Hatırlatıcı başarıyla oluşturuldu",
        "en": "Reminder created successfully",
    },
    "reminder.deleted": {
        "ar": "تم حذف التذكير",
        "tr": "Hatırlatıcı silindi",
        "en": "Reminder deleted",
    },
    "reminder.not_found": {
        "ar": "التذكير غير موجود",
        "tr": "Hatırlatıcı bulunamadı",
        "en": "Reminder not found",
    },
    "reminder.notification_title": {
        "ar": "💊 وقت الدواء",
        "tr": "💊 İlaç Zamanı",
        "en": "💊 Medication Time",
    },
    "reminder.notification_body": {
        "ar": "حان وقت تناول {medicine_name} — {dosage}",
        "tr": "{medicine_name} alma zamanı — {dosage}",
        "en": "Time to take {medicine_name} — {dosage}",
    },

    # ── AI Chat ─────────────────────────────────────────────
    "ai.processing": {
        "ar": "جارٍ تحليل الأعراض...",
        "tr": "Belirtiler analiz ediliyor...",
        "en": "Analyzing symptoms...",
    },
    "ai.error": {
        "ar": "تعذّر الاتصال بنظام الذكاء الاصطناعي، يرجى المحاولة لاحقاً",
        "tr": "Yapay zeka sistemine bağlanılamadı, lütfen daha sonra tekrar deneyin",
        "en": "Could not reach AI system, please try again later",
    },
    "ai.disclaimer": {
        "ar": "⚠️ هذه المعلومات للاسترشاد فقط وليست بديلاً عن استشارة طبيب متخصص",
        "tr": "⚠️ Bu bilgiler yalnızca rehberlik amaçlıdır ve uzman bir doktora danışmanın yerini tutmaz",
        "en": "⚠️ This information is for guidance only and is not a substitute for professional medical advice",
    },

    # ── General ─────────────────────────────────────────────
    "general.not_found": {
        "ar": "العنصر المطلوب غير موجود",
        "tr": "İstenen öğe bulunamadı",
        "en": "Requested item not found",
    },
    "general.server_error": {
        "ar": "حدث خطأ في الخادم، يرجى المحاولة لاحقاً",
        "tr": "Sunucu hatası oluştu, lütfen daha sonra tekrar deneyin",
        "en": "A server error occurred, please try again later",
    },
    "general.validation_error": {
        "ar": "البيانات المدخلة غير صحيحة",
        "tr": "Girilen veriler geçersiz",
        "en": "Invalid input data",
    },
    "general.success": {
        "ar": "تمت العملية بنجاح",
        "tr": "İşlem başarıyla tamamlandı",
        "en": "Operation completed successfully",
    },
}


def t(key: str, lang: Optional[str] = None, **kwargs) -> str:
    """
    Translate a key into the requested language.

    Usage:
        t("auth.login_success", lang="ar")
        t("reminder.notification_body", lang="tr", medicine_name="Aspirin", dosage="500mg")
    """
    lang = lang or settings.DEFAULT_LANGUAGE

    # Fallback chain: requested lang → default lang → English → key itself
    entry = TRANSLATIONS.get(key, {})
    text = entry.get(lang) or entry.get(settings.DEFAULT_LANGUAGE) or entry.get("en") or key

    # Interpolate named placeholders e.g. {medicine_name}
    if kwargs:
        try:
            text = text.format(**kwargs)
        except KeyError:
            pass

    return text


def get_language_from_header(accept_language: Optional[str]) -> str:
    """
    Parse Accept-Language header and return best matching supported language.
    Example header: "ar-SA,ar;q=0.9,tr;q=0.8,en;q=0.7"
    """
    if not accept_language:
        return settings.DEFAULT_LANGUAGE

    supported = settings.supported_languages_list

    for segment in accept_language.split(","):
        lang_code = segment.strip().split(";")[0].strip().split("-")[0].lower()
        if lang_code in supported:
            return lang_code

    return settings.DEFAULT_LANGUAGE
