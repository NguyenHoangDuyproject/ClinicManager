from datetime import datetime
import cloudinary.uploader
from flask import Blueprint, render_template, request, redirect, url_for, jsonify, session
from flask_login import logout_user, login_user, current_user
from sqlalchemy.exc import NoResultFound, SQLAlchemyError

from app import login_manager, dao, decorators
from app.models import Gender, Role, User
from app.utils import is_past_date

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('about/index.html')

@main.route('/about-us')
def about_us():
    return render_template('about/about_us.html')

@main.route('/services')
def services():
    return render_template('about/services.html')

@main.route('/news')
def news():
    return render_template('about/news.html')

@main.route('/contact')
def contact():
    return render_template('about/contact_us.html')

@main.route('/login', methods=['GET', 'POST'])
@decorators.anonymous_user
def login_process():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = dao.auth_user(username=username, password=password)
        if user:
            login_user(user=user)
            if user.role == Role.Admin:
                return redirect('/admin')
            if user.role == Role.Doctor or user.role == Role.Nurse:
                return redirect('/nurse')
            url_next = request.args.get('next')
            return redirect(url_next if url_next else '/')
        return redirect(url_for('main.index'))
    return render_template('auth/login.html')

@main.route('/register', methods=['GET', 'POST'])
@decorators.anonymous_user
def register_process():
    if request.method == 'POST':
        form = request.form
        username = form.get('username')
        if dao.get_user_by_username(username):
            return render_template('auth/register.html', err_msg="Tên đăng nhập đã tồn tại")

        fullname = form.get('fullname')
        password = form.get('password')
        birthday = form.get('birthday')
        email = form.get('email')
        phone = form.get('phone')
        avatar_file = request.files.get('avatar_file')

        avatar = ''
        if avatar_file:
            res = cloudinary.uploader.upload(avatar_file)
            avatar = res['secure_url']

        try:
            dao.register_user(username=username,
                              password=password,
                              fullname=fullname,
                              gender=Gender.Male,
                              phone=phone,
                              role=Role.Customer,
                              email=email,
                              birthday=birthday,
                              avatar=avatar)
        except:
            err_msg = 'Đã có lỗi xảy ra! Vui lòng quay lại sau!'
        else:
            return redirect('/login')

    return render_template('auth/register.html')

@main.route('/logout')
@decorators.authenticated_user
def logout():
    logout_user()
    return redirect('/login')

@main.route('/registration-form', methods=['GET', 'POST'])
@decorators.authenticated_user
def registration_form_process():
    if request.method == 'GET':
        return render_template('registration-form.html')

    form = request.form
    examination_date = request.form.get('examination_date')
    print(examination_date)
    examination_date = datetime.strptime(examination_date, '%Y-%m-%d').date()
    user_in_1_day = dao.get_regulation_value('user_in_1_day')
    if dao.count_registration_forms_by_date(examination_date) >= user_in_1_day:
        error_message = f"Đã đạt giới hạn {user_in_1_day} lần đăng ký " \
                        f"trong ngày {examination_date.strftime('%d-%m-%Y')}!!!"
        return render_template('registration-form.html', err_msg=error_message)

    if is_past_date(examination_date):
        error_message = "Ngày đăng ký phải là hôm nay hoặc tương lai!!!"
        return render_template('registration-form.html', err_msg=error_message)

    fullname = form.get('fullname')
    birthday = form.get('birthday')
    phone = form.get('phone')
    user_id = current_user.id
    dao.update_user(user_id=user_id,
                    fullname=fullname,
                    birthday=birthday,
                    phone=phone)
    dao.registration_form(user=current_user,
                          examination_date=examination_date)
    return render_template('registration-form.html', success_msg="Đăng ký lịch hẹn thành công!!!")

@main.route('/delete-exam/<int:exam_id>', methods=['DELETE'])
def delete_exam(exam_id):
    if dao.delete_examination(exam_id):
        return jsonify({"message": f"Examination with ID {exam_id} deleted successfully"}), 200
    else:
        return jsonify({"error:": f"Something wrong"}), 500

@main.route('/history')
@decorators.authenticated_user
def history():
    examination_bills = dao.get_history_examination(current_user.id)
    return render_template('examination-history.html', examination_bills=examination_bills)

@main.route('/api/history/<int:user_id>')
def view_history(user_id):
    bills = dao.get_history_examination(user_id)
    data = []
    for bill in bills:
        data.append({
            'symptom': bill.medical_bill.symptom,
            'prediction': bill.medical_bill.disease_prediction,
            'examination_date': str(bill.examination_date),
        })

    return jsonify(data)

@main.route('/api/medicine', methods=['POST'])
@decorators.authenticated_user
def add_medicine_to_cart():
    """
    session: {
        "bill": {
            "1": {
                "id": "1",
                "quantity": 2
            },
            "2": {
                "id": "2",
                "quantity": 1
            }
        }
    }
    :return:
    """
    data = request.json
    print(data)
    bill = session.get('bill')
    if bill is None:
        bill = {}

    id = str(data.get("id"))
    quantity = int(data.get("quantity"))
    price = data.get("price")
    if id in bill:
        bill[id]['quantity'] += 1
    else:
        bill[id] = {
            "id": int(id),
            "quantity": quantity,
            "price": price,
            "name": data.get("name"),
            "direction": data.get("direction"),
            "unit": data.get("unit")
        }
    session['bill'] = bill

    return jsonify(session['bill'])

@main.route('/api/medicine/delete', methods=['POST'])
@decorators.authenticated_user
def delete_medicine_from_cart():
    data = request.json
    print(data)
    bill = session.get('bill')
    if bill is not None:
        id_to_delete = str(data.get("id"))
        if id_to_delete in bill:
            del bill[id_to_delete]
            session['bill'] = bill
            return jsonify(session['bill'])

    return jsonify({"message": "Fail"})

@main.route('/api/medicine/save', methods=['POST'])
@decorators.authenticated_user
def save_medical_bill():
    bill = session.get('bill')
    data = request.json
    print(data)
    symptom = data.get("symptom")
    disease_prediction = data.get("prediction")
    patient_id = data.get("patient_id")
    form_id = data.get("form_id")

    try:
        medical_bill = dao.create_medical_bill(symptom=symptom, disease_prediction=disease_prediction,
                                               doctor=current_user, patient_id=patient_id)
        total = dao.save_detail(medical_bill, bill)
        dao.save_examination_bill(medicine_money=total,
                                  examination_money=dao.get_regulation_value('examination_price'),
                                  medical_bill=medical_bill, patient_id=patient_id)
        dao.update_used_form(form_id)
        del session['bill']
        return jsonify({"message": "Success"})
    except:
        return jsonify({"message": "Fail"})


@login_manager.user_loader
def load_user(user_id):
    return dao.get_user_by_id(user_id)





