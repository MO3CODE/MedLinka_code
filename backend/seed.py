"""
MedLinka — Seed Script
Populates the database with realistic sample data for development/testing.
Run: python seed.py
"""

import asyncio
import json
from datetime import datetime, timedelta

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, init_db
from app.models import (
    User, UserRole, Language,
    DoctorProfile, DoctorSpecialty,
    PharmacyProfile, Medicine,
    Appointment, AppointmentStatus, AppointmentType,
    Reminder, ReminderFrequency,
)
from app.utils.security import hash_password


async def seed():
    await init_db()
    async with AsyncSessionLocal() as db:

        print("🌱 Seeding MedLinka database...")

        # ── Patients ──────────────────────────────────────────
        patient_ar = User(
            email="ahmed@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="أحمد محمد الخالد",
            phone="+966501234567",
            role=UserRole.PATIENT,
            preferred_language=Language.AR,
            is_active=True,
            is_verified=True,
        )
        patient_tr = User(
            email="mehmet@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="Mehmet Yılmaz",
            phone="+905301234567",
            role=UserRole.PATIENT,
            preferred_language=Language.TR,
            is_active=True,
            is_verified=True,
        )
        patient_en = User(
            email="john@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="John Smith",
            phone="+447911123456",
            role=UserRole.PATIENT,
            preferred_language=Language.EN,
            is_active=True,
            is_verified=True,
        )

        # ── Doctors ───────────────────────────────────────────
        doctor1_user = User(
            email="dr.sarah@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="د. سارة العمري",
            role=UserRole.DOCTOR,
            preferred_language=Language.AR,
            is_active=True,
            is_verified=True,
        )
        doctor2_user = User(
            email="dr.ali@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="Dr. Ali Hassan",
            role=UserRole.DOCTOR,
            preferred_language=Language.EN,
            is_active=True,
            is_verified=True,
        )
        doctor3_user = User(
            email="dr.ayse@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="Dr. Ayşe Kaya",
            role=UserRole.DOCTOR,
            preferred_language=Language.TR,
            is_active=True,
            is_verified=True,
        )

        # ── Pharmacy ──────────────────────────────────────────
        pharmacy_user = User(
            email="pharmacy@medlinka.com",
            hashed_password=hash_password("Test1234"),
            full_name="صيدلية الشفاء",
            role=UserRole.PHARMACY,
            preferred_language=Language.AR,
            is_active=True,
            is_verified=True,
        )

        db.add_all([
            patient_ar, patient_tr, patient_en,
            doctor1_user, doctor2_user, doctor3_user,
            pharmacy_user,
        ])
        await db.flush()

        # ── Doctor Profiles ───────────────────────────────────
        doc1_profile = DoctorProfile(
            user_id=doctor1_user.id,
            specialty=DoctorSpecialty.CARDIOLOGY,
            bio_ar="طبيبة متخصصة في أمراض القلب والأوعية الدموية، خبرة 12 عاماً.",
            bio_tr="Kardiyoloji uzmanı, 12 yıllık deneyim.",
            bio_en="Cardiologist with 12 years of experience.",
            years_experience=12,
            consultation_fee=150.0,
            rating=4.8,
            total_reviews=236,
            is_available=True,
            available_days="sun,mon,tue,wed,thu",
            available_from="09:00",
            available_to="17:00",
        )
        doc2_profile = DoctorProfile(
            user_id=doctor2_user.id,
            specialty=DoctorSpecialty.GENERAL,
            bio_ar="طبيب عام بخبرة 8 سنوات في الرعاية الصحية الأولية.",
            bio_tr="8 yıllık deneyime sahip genel pratisyen.",
            bio_en="General practitioner with 8 years in primary care.",
            years_experience=8,
            consultation_fee=80.0,
            rating=4.5,
            total_reviews=189,
            is_available=True,
            available_days="mon,tue,wed,thu,fri",
            available_from="08:00",
            available_to="16:00",
        )
        doc3_profile = DoctorProfile(
            user_id=doctor3_user.id,
            specialty=DoctorSpecialty.DERMATOLOGY,
            bio_ar="متخصصة في أمراض الجلد وعلاج حب الشباب.",
            bio_tr="Cilt hastalıkları ve akne tedavisi uzmanı.",
            bio_en="Specialist in dermatology and acne treatment.",
            years_experience=6,
            consultation_fee=120.0,
            rating=4.7,
            total_reviews=142,
            is_available=True,
            available_days="tue,wed,thu",
            available_from="10:00",
            available_to="18:00",
        )

        # ── Pharmacy Profile ──────────────────────────────────
        pharmacy_profile = PharmacyProfile(
            user_id=pharmacy_user.id,
            pharmacy_name_ar="صيدلية الشفاء",
            pharmacy_name_tr="Şifa Eczanesi",
            pharmacy_name_en="Al-Shifa Pharmacy",
            address="شارع الملك فهد، الرياض",
            license_number="PH-2024-00123",
            is_verified=True,
        )

        db.add_all([doc1_profile, doc2_profile, doc3_profile, pharmacy_profile])
        await db.flush()

        # ── Medicines ─────────────────────────────────────────
        medicines = [
            Medicine(
                pharmacy_id=pharmacy_profile.id,
                name_ar="أسبرين 500 مجم",
                name_tr="Aspirin 500 mg",
                name_en="Aspirin 500 mg",
                description_ar="مسكن للألم وخافض للحرارة ومضاد للالتهابات",
                description_tr="Ağrı kesici, ateş düşürücü ve anti-enflamatuar",
                description_en="Pain reliever, fever reducer and anti-inflammatory",
                category="pain_relief",
                price=12.50,
                stock_quantity=500,
                requires_prescription=False,
            ),
            Medicine(
                pharmacy_id=pharmacy_profile.id,
                name_ar="باراسيتامول 1000 مجم",
                name_tr="Parasetamol 1000 mg",
                name_en="Paracetamol 1000 mg",
                description_ar="مسكن للألم وخافض للحرارة للبالغين",
                description_tr="Yetişkinler için ağrı kesici ve ateş düşürücü",
                description_en="Pain reliever and fever reducer for adults",
                category="pain_relief",
                price=8.00,
                stock_quantity=800,
                requires_prescription=False,
            ),
            Medicine(
                pharmacy_id=pharmacy_profile.id,
                name_ar="أموكسيسيلين 500 مجم",
                name_tr="Amoksisilin 500 mg",
                name_en="Amoxicillin 500 mg",
                description_ar="مضاد حيوي واسع الطيف لعلاج الالتهابات البكتيرية",
                description_tr="Bakteriyel enfeksiyonlar için geniş spektrumlu antibiyotik",
                description_en="Broad-spectrum antibiotic for bacterial infections",
                category="antibiotics",
                price=35.00,
                stock_quantity=300,
                requires_prescription=True,
            ),
            Medicine(
                pharmacy_id=pharmacy_profile.id,
                name_ar="ميتفورمين 500 مجم",
                name_tr="Metformin 500 mg",
                name_en="Metformin 500 mg",
                description_ar="لعلاج مرض السكري من النوع الثاني",
                description_tr="Tip 2 diyabet tedavisinde kullanılır",
                description_en="Used for treatment of type 2 diabetes",
                category="diabetes",
                price=22.00,
                stock_quantity=600,
                requires_prescription=True,
            ),
            Medicine(
                pharmacy_id=pharmacy_profile.id,
                name_ar="فيتامين C 1000 مجم",
                name_tr="C Vitamini 1000 mg",
                name_en="Vitamin C 1000 mg",
                description_ar="مكمل غذائي لتعزيز المناعة",
                description_tr="Bağışıklık güçlendirici besin takviyesi",
                description_en="Dietary supplement for immune support",
                category="vitamins",
                price=45.00,
                stock_quantity=400,
                requires_prescription=False,
            ),
        ]
        db.add_all(medicines)
        await db.flush()

        # ── Appointments ──────────────────────────────────────
        appointment = Appointment(
            patient_id=patient_ar.id,
            doctor_id=doc1_profile.id,
            scheduled_at=datetime.utcnow() + timedelta(days=2, hours=10),
            duration_minutes=30,
            type=AppointmentType.VIDEO,
            status=AppointmentStatus.CONFIRMED,
            notes_by_patient="أعاني من ألم في الصدر عند المجهود",
        )
        db.add(appointment)

        # ── Reminders ─────────────────────────────────────────
        reminder = Reminder(
            user_id=patient_ar.id,
            medicine_name="ميتفورمين 500 مجم",
            dosage="قرص واحد",
            frequency=ReminderFrequency.TWICE_DAY,
            times_json=json.dumps(["08:00", "20:00"]),
            start_date=datetime.utcnow(),
            end_date=datetime.utcnow() + timedelta(days=30),
            is_active=True,
        )
        db.add(reminder)

        await db.commit()
        print("✅ Seed complete!")
        print("\n📋 Test accounts:")
        print("  Patient (AR)   → ahmed@medlinka.com      / Test1234")
        print("  Patient (TR)   → mehmet@medlinka.com     / Test1234")
        print("  Patient (EN)   → john@medlinka.com       / Test1234")
        print("  Doctor         → dr.sarah@medlinka.com   / Test1234")
        print("  Doctor         → dr.ali@medlinka.com     / Test1234")
        print("  Doctor         → dr.ayse@medlinka.com    / Test1234")
        print("  Pharmacy       → pharmacy@medlinka.com   / Test1234")
        print("\n🌐 API Docs → http://localhost:8000/docs")


if __name__ == "__main__":
    asyncio.run(seed())
