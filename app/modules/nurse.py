import sys
import os
from datetime import datetime, date
from flask import redirect, request, render_template
from flask_admin import Admin, BaseView, expose, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from app.models import db, User, Role,  Medicine, RegistrationForm, MedicineTag, Regulation
from flask_login import logout_user, current_user
from .. import dao
from .. import utils
class AuthenticatedUser(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated


class NurseView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == Role.Nurse


class DoctorView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role == Role.Doctor


class EmployeeView(BaseView):
    def is_accessible(self):
        return current_user.is_authenticated and (current_user.role == Role.Doctor or current_user.role == Role.Nurse)


class MyNurseView(AdminIndexView):

    def __init__(self, name=None, **kwargs):
        super(MyNurseView, self).__init__(name=name, **kwargs)

    @expose('/')
    def index(self):
        return self.render('admin/nurses/index.html')


class NurseRegisterView(EmployeeView):
    @expose('/', methods=['GET', 'POST'])
    def nurse_register(self):
        template_str = 'admin/nurses/medical-appointment.html'
        if request.method == 'GET':
            return self.render(template_str)

        form = request.form
        examination_date = form.get('appointmentDate')
        examination_date = datetime.strptime(examination_date, '%Y-%m-%d').date()
        user_in_1_day = dao.get_regulation_value('user_in_1_day')
        if dao.count_registration_forms_by_date(examination_date) >= user_in_1_day:
            error_message = f"Đã đạt giới hạn {user_in_1_day} lần đăng ký " \
                            f"trong ngày {examination_date.strftime('%d-%m-%Y')}!!!"
            return self.render(template_str,
                               err_msg=error_message,
                               form_data=form)

        if utils.is_past_date(examination_date):
            error_message = "Ngày đăng ký phải là hôm nay hoặc tương lai!!!"
            return self.render('admin/nurses/medical-appointment.html',
                               err_msg=error_message,
                               form_data=form)

        fullname = form.get('fullname')
        birthday = form.get('birthday')
        phone = form.get('phone')
        email = form.get('email')
        gender = form.get('gioiTinh')

        if not fullname:
            error_message = "Chưa nhập họ tên bệnh nhân!!!"
            return self.render(template_str,
                               err_msg=error_message,
                               is_fullname_error=True,
                               form_data=form)
        if not birthday or not utils.is_past_date(birthday):
            error_message = "Ngày sinh phải là quá khứ!!!"
            return self.render(template_str,
                               err_msg=error_message,
                               is_birthday_error=True,
                               form_data=form)
        if not phone or len(phone) != 10:
            error_message = "Chưa nhập số điện thoại bệnh nhân hoặc số điện thoại không hợp lệ!!!"
            return self.render(template_str,
                               err_msg=error_message,
                               is_phone_error=True,
                               form_data=form)

        patient = dao.register_user(fullname=fullname,
                                    username=phone,
                                    birthday=birthday,
                                    phone=phone,
                                    gender=gender,
                                    email=email,
                                    password="123456"
                                    )
        dao.registration_form(user=patient,
                              examination_date=examination_date)
        return self.render(template_str, success_msg="Đăng ký lịch hẹn thành công!!!")


class NurseCompleteView(EmployeeView):
    @expose('/', methods=['GET', 'POST'])
    def nurse_complete(self):
        today = datetime.today().date()
        examination_date = request.args.get('examination-date')
        if examination_date is None:
            examination_date = today
        else:
            examination_date = datetime.strptime(examination_date, "%Y-%m-%d").date()
        if request.method == 'GET':
            registration_data = dao.get_registration_form(examination_date=examination_date)
            all_confirmed = all(record['accepted'] for record in registration_data)
            return self.render('admin/nurses/complete-view.html',
                               registration_data=registration_data,
                               examination_date=examination_date,
                               today=today,
                               all_confirmed=all_confirmed)
        complete_date = request.form.get('complete-date')
        data = dao.update_complete_form(complete_date)
        all_confirmed = all(record['accepted'] for record in data)

        # send SMS
        utils.send_SMS(utils.get_phones(data), complete_date)
        return self.render('admin/nurses/complete-view.html',
                           registration_data=data,
                           examination_date=examination_date,
                           today=today,
                           accepted=True,
                           all_confirmed=all_confirmed)


class NurseCompletePayment(EmployeeView):
    @expose('/', methods=['GET', 'POST'])
    def complete_payment(self):
        phone_to_search = request.args.get('phone')
        if request.method == 'GET':
            examination_bills = dao.get_complete_payment(phone_to_search)
            return self.render('admin/nurses/complete-payment.html',
                               examination_bills=examination_bills,
                               )
        ex_id = request.form.get('complete-payment')
        dao.update_complete_payment(ex_id)
        examination_bills = dao.get_complete_payment(phone_to_search)
        return self.render('admin/nurses/complete-payment.html',
                           examination_bills=examination_bills,
                           )

    @expose('/<int:medical_bill_id>', methods=['GET', 'POST'])
    def detail_payment(self, medical_bill_id):
        # medical_bill_id = request.args.get('medical_bill_id')
        medicine_details, total_amount = dao.get_medicine_details(medical_bill_id)
        return self.render('admin/nurses/detail-payment.html',
                           medicine_details=medicine_details,
                           total_amount=total_amount)


class DoctorExaminationList(DoctorView):
    @expose('/', methods=['GET', 'POST'])
    def examination_list(self):
        today = datetime.today().date()
        examination_data = dao.get_registration_form(examination_date=today, used=False)
        return self.render('admin/doctor/examination_list.html',
                           examination_data=examination_data
                           )

    @expose('/<int:registration_id>', methods=['GET', 'POST'])
    def create_medical_bill(self, registration_id):
        registration_form = dao.get_registration_form(id=registration_id)
        medicines = dao.get_medicines()

        return self.render('admin/doctor/medical_bill.html',
                           registration_form=registration_form,
                           medicines=medicines)


class NurseLogoutView(AuthenticatedUser):
    @expose("/")
    def index(self):
        logout_user()
        return redirect('/')



def init_nurse(app):
    employee = Admin(app=app,
                    name="Nhân viên hệ thống Phòng mạch",
                    template_mode='bootstrap4',
                    url='/nurse',
                    endpoint='nurse',
                    index_view=MyNurseView(name="Trang chủ", endpoint="nurse", url="/nurse"))
    employee.add_view(NurseRegisterView(name="Đăng ký khám", endpoint="register"))
    employee.add_view(NurseCompleteView(name="Hoàn tất lịch khám", endpoint="complete"))
    employee.add_view(NurseCompletePayment(name="Thanh toán hóa đơn", endpoint="payment"))
    employee.add_view(DoctorExaminationList(name="Lập phiếu khám", endpoint="examination"))
    employee.add_view(NurseLogoutView(name="Đăng xuất"))
