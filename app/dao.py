from datetime import datetime, date

from sqlalchemy import func

from app.models import db, User, Role, MedicalBill, MedicalBillDetail, ExaminationBill, Medicine, RegistrationForm, \
    MedicineTag, Regulation, Gender, Unit
# Các hàm và logic của bạn ở đây
import hashlib


def get_user_by_id(user_id):
    return User.query.get(user_id)

def get_user_by_username(username):
    return User.query.filter(User.username.ilike(f"%{username}%")).first()
def auth_user(username, password):
    password = str(hashlib.md5(password.strip().encode('utf-8')).hexdigest())

    return User.query.filter(User.username.__eq__(username.strip()),
                             User.password.__eq__(password)).first()


def register_user(**kwargs):
    new_user = User(**kwargs)
    db.session.add(new_user)
    db.session.commit()
    db.session.flush()
    return new_user


def update_user(user_id, **kwargs):
    user = get_user_by_id(user_id)
    for key, value in kwargs.items():
        setattr(user, key, value)
    db.session.commit()


def get_units():
    return Unit.query.all()


# name, description, direction
def get_medicines(**kwargs):
    query = Medicine.query
    for key, value in kwargs.items():
        if hasattr(Medicine, key):
            query = query.filter(getattr(Medicine, key).ilike(f"%{value}%"))

    medicines = query.all()
    return medicines


def get_medical_bill(patient_id=None, phone=None):
    query = MedicalBill.query
    if patient_id is not None:
        query = query.filter(MedicalBill.patient_id == patient_id)
    if phone is not None:
        query = query.join(User).filter(User.phone == phone)
    medical_bills = query.all()
    return medical_bills


def get_examination_bill(medical_bill_id, examination_date):
    query = ExaminationBill.query
    if examination_date:
        query = query.filter(examination_date=examination_date)
    if medical_bill_id:
        return query.filter_by(medical_bill_id=medical_bill_id).first()
    return query.all()


def get_medical_bill_detail(medical_bill_id):
    return MedicalBillDetail.query.filter_by(medical_bill_id=medical_bill_id).all()


def count_registration_forms_by_date(examination_date=None):
    if examination_date is None:
        return 0
    start_of_day = datetime.combine(examination_date, datetime.min.time())
    end_of_day = datetime.combine(examination_date, datetime.max.time())
    return (
        RegistrationForm.query
        .filter(RegistrationForm.examination_date >= start_of_day, RegistrationForm.examination_date <= end_of_day)
        .count()
    )


def registration_form(**kwargs):
    form = RegistrationForm(**kwargs)
    db.session.add(form)
    db.session.commit()


def get_regulation_value(key):
    regulation = Regulation.query.filter_by(key=key).first()
    if regulation:
        return regulation.value
    return 0


def get_history_examination(user_id):
    return ExaminationBill.query.filter(ExaminationBill.patient_id == user_id)


def get_registration_form(**kwargs):
    print(kwargs)
    registration_forms = RegistrationForm.query
    id = kwargs.get("id")
    if id:
        return registration_forms.get(id)
    examination_date = kwargs.get("examination_date")
    registration_forms = registration_forms.filter(
        RegistrationForm.examination_date == examination_date,
    )
    if kwargs.get("used") is not None:
        registration_forms = registration_forms.filter(RegistrationForm.used == False)
    return map_form_to_data(registration_forms)


def delete_examination(examination_id):
    form = RegistrationForm.query.get(examination_id)
    if form:
        try:
            db.session.delete(form)
            db.session.commit()
            return True
        except:
            return False
    return False


def update_used_form(form_id):
    if form_id is not None:
        print(form_id)
        form = RegistrationForm.query.get(form_id)
        form.used = True
        db.session.commit()
        print(form_id)
        return True
    else:
        return False


def update_complete_form(complete_date):
    try:
        forms_to_update = RegistrationForm.query \
            .filter(RegistrationForm.examination_date == complete_date).all()
        if forms_to_update:
            for form in forms_to_update:
                form.accepted = True
            db.session.commit()
            return map_form_to_data(forms_to_update)
        return []
    except:
        return []


def map_form_to_data(forms):
    registration_data = []
    for form in forms:
        user = form.user
        registration_info = {
            "user_id": user.id,
            "fullname": user.fullname,
            "phone": user.phone,
            "birthday": user.birthday,
            "examination_date": form.examination_date,
            "id": form.id,
            "accepted": form.accepted
        }
        registration_data.append(registration_info)
    return registration_data


def get_complete_payment(phone_to_search=None):
    query = ExaminationBill.query.join(
        User, ExaminationBill.patient_id == User.id
    ).add_columns(
        User.fullname,
        User.phone,
        ExaminationBill.paid,
        ExaminationBill.id,
        ExaminationBill.medicine_money,
        ExaminationBill.examination_date,
        ExaminationBill.examination_money,
        (ExaminationBill.medicine_money + ExaminationBill.examination_money).label('total_cost'),
        ExaminationBill.medical_bill_id
    ).filter(ExaminationBill.paid == 0)
    if phone_to_search:
        query = query.filter(User.phone.ilike(f'%{phone_to_search}%'))
    results = query.all()
    payments = []
    for result in results:
        payment = {
            'examination_date': result.examination_date,
            'patient_name': result.fullname,
            'phone': result.phone,
            'medicine_cost': result.medicine_money,
            'examination_cost': result.examination_money,
            'total_cost': result.total_cost,
            'medical_bill_id': result.medical_bill_id,
            'paid': result.paid,
            'id': result.id,
        }
        payments.append(payment)
    return payments


def update_complete_payment(ex_id):
    try:
        exam = ExaminationBill.query.get(ex_id)
        if exam:
            exam.paid = True
            db.session.commit()
            return exam.paid
        return []
    except Exception as e:
        print(e)
        return []


def get_medicine_details(medical_bill_id):
    results = MedicalBillDetail.query.join(
        Medicine, Medicine.id == MedicalBillDetail.medicine_id
    ).filter(
        MedicalBillDetail.medical_bill_id == medical_bill_id
    ).with_entities(
        Medicine.name,
        MedicalBillDetail.quantity,
        Medicine.direction,
        Medicine.price
    ).all()
    medicine_details = []
    total_amount = 0
    for result in results:
        total_cost = result.price * result.quantity
        total_amount += total_cost
        detail = {
            'name': result.name,
            'quantity': result.quantity,
            'direction': result.direction,
            'price': result.price,
            'total_cost': total_cost,

        }
        medicine_details.append(detail)
    return medicine_details, total_amount


def create_medical_bill(**kwargs):
    print('create_medical_bill')
    new_medical_bill = MedicalBill(**kwargs)
    db.session.add(new_medical_bill)
    db.session.commit()
    db.session.flush()
    return new_medical_bill


def save_detail(bill, details):
    print('save_detail')
    try:
        total = 0
        for item_id, item_data in details.items():
            total = total + item_data['price'] * item_data['quantity']
            detail = MedicalBillDetail(quantity=item_data['quantity'], medicine_id=item_data['id'], medical_bill=bill)
            db.session.add(detail)
        db.session.commit()
        db.session.flush()
        return total
    except Exception as e:
        print(e)
        return -1


def save_examination_bill(**kwargs):
    print('save_examination_bill')
    new_examination_bill = ExaminationBill(**kwargs)
    db.session.add(new_examination_bill)
    db.session.commit()
    db.session.flush()
    return new_examination_bill


def stats_revenue(kw=None):
    # Thống kê doanh thu
    revenue_stats_query = (
        db.session.query(
            func.extract('month', MedicalBill.examination_date).label('month'),
            func.sum(ExaminationBill.medicine_money + ExaminationBill.examination_money).label('total_revenue')
        )
        .join(ExaminationBill, MedicalBill.id == ExaminationBill.medical_bill_id)
    )
    if kw:
        year = int(kw)
        revenue_stats_query = revenue_stats_query.filter(func.extract('year', MedicalBill.examination_date) == year)
    revenue_stats = revenue_stats_query.group_by(func.extract('month', MedicalBill.examination_date)).all()
    # Thống kê tần suất khám
    examination_frequency = (
        db.session.query(
            func.extract('month', MedicalBill.examination_date).label('month'),
            func.count(MedicalBill.id).label('examination_count')
        )
        .join(ExaminationBill, MedicalBill.id == ExaminationBill.medical_bill_id)
    )
    if kw:
        year = int(kw)
        examination_frequency = examination_frequency.filter(func.extract('year', MedicalBill.examination_date) == year)
    examination_frequency = examination_frequency.group_by(func.extract('month', MedicalBill.examination_date)).all()
    return revenue_stats, examination_frequency


def stats_medicine(selected_month, selected_year=2024):
    return db.session.query(Medicine.name,
                            func.count(MedicalBillDetail.medicine_id),
                            func.sum(MedicalBillDetail.quantity)) \
        .join(MedicalBillDetail, Medicine.id == MedicalBillDetail.medicine_id) \
        .join(MedicalBill, MedicalBill.id == MedicalBillDetail.medical_bill_id) \
        .filter(func.extract('year', MedicalBill.examination_date) == selected_year) \
        .filter(func.extract('month', MedicalBill.examination_date) == selected_month) \
        .group_by(Medicine.name).all()


if __name__ == '__main__':
    with app.app_context():
        new_date = date(2024, 1, 3)
        # today = datetime.today().date()
        # bill = get_regulation_value('user_in_1_day')
        # print(today)
        # # registration_data = get_registration_form(today)
        # # print(registration_data)
        # # payment = get_medicine_details(1)
        # # print(payment)
        # new_medical_bill = create_medical_bill(examination_date=datetime.now(), symptom="Ho nhiều",
        #                                        patient_id=1, doctor_id=2)
        # print(new_medical_bill)
        month = 1
        year = 2024  # Năm cần thống kê
        revenue_stats, examination_frequency = stats_revenue(year)
        print("Thống kê doanh thu và tần suất khám cho tháng: {}".format(revenue_stats))
        print("Tần suất khám cho tháng: {}".format(examination_frequency))

        # Gọi hàm stats_medicine_usage_by_month
        medicine_usage_stats = stats_medicine(month, year)
        print("Thống kê tần suất sử dụng thuốc cho tháng {}: {}".format(month, medicine_usage_stats))
