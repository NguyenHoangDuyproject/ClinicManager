import hashlib
from sqlalchemy.orm import relationship, backref
from sqlalchemy import Column, Integer, String, Float, Enum, DateTime, Boolean, ForeignKey, Text, Date
from datetime import datetime
from flask_login import UserMixin
from enum import Enum as ModelEnum
from app import db

class BaseModel(db.Model):
    __abstract__ = True
    id = Column(Integer, primary_key=True, autoincrement=True)

class Gender(ModelEnum):
    Male = 1
    Female = 2

class Role(ModelEnum):
    Admin = 1
    Customer = 2
    Nurse = 3
    Doctor = 4

class User(BaseModel, UserMixin):
    __tablename__ = 'user'
    __table_args__ = {'extend_existing': True}
    fullname = Column(String(255), nullable=False)
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    avatar = Column(String(255), nullable=True)
    gender = Column(Enum(Gender), default=Gender.Male)
    birthday = Column(Date, default=datetime.now())
    email = Column(String(255), nullable=True)
    phone = Column(String(11), nullable=False)
    active = Column(Boolean, default=True)
    created_date = Column(DateTime, default=datetime.now())
    role = Column(Enum(Role), default=Role.Customer)

    registration_forms = relationship('RegistrationForm', back_populates='user', lazy=True)
    examination_bills = relationship('ExaminationBill', back_populates='patient', lazy=True, uselist=True)
    regulations = relationship('Regulation', back_populates='user', lazy=True)
    medical_bills = relationship('MedicalBill', back_populates='patient', lazy=True,
                                 foreign_keys='[MedicalBill.patient_id]', uselist=True)
    doctor_bills = relationship('MedicalBill', back_populates='doctor', lazy=True,
                                foreign_keys='[MedicalBill.doctor_id]', uselist=True)

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.password = str(hashlib.md5(kwargs.get('password').strip().encode('utf-8')).hexdigest())

    def __str__(self):
        return self.fullname

    def __repr__(self):
        return '<User: {}>'.format(self.fullname)

class Unit(BaseModel):
    __tablename__ = 'unit'
    __table_args__ = {'extend_existing': True}
    name = Column(String(50), nullable=False)
    medicines = relationship('Medicine', back_populates='unit', lazy=True)

    def __str__(self):
        return self.name

class Tag(BaseModel):
    __tablename__ = 'tag'
    __table_args__ = {'extend_existing': True}
    name = Column(String(255), nullable=False)
    medicine_tags = relationship('MedicineTag', backref='tags', lazy=False)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Tag: {}>'.format(self.name)

class Medicine(BaseModel):
    __tablename__ = 'medicine'
    __table_args__ = {'extend_existing': True}
    name = Column(String(255), nullable=False)
    price = Column(Float, default=0)
    description = Column(Text, nullable=True)
    direction = Column(Text, nullable=True)
    unit_in_stock = Column(Integer, default=0)
    unit_id = Column(Integer, ForeignKey(Unit.id), nullable=False)
    unit = relationship('Unit', back_populates='medicines', lazy=False)
    medicine_tags = relationship('MedicineTag', backref='medicines', lazy=True)
    medical_bill_details = relationship('MedicalBillDetail', back_populates='medicine', lazy=True)

    def __str__(self):
        return self.name

    def __repr__(self):
        return '<Medicine: {}>'.format(self.name)

class MedicineTag(BaseModel):
    __tablename__ = 'medicine_tag'
    __table_args__ = {'extend_existing': True}
    tag_id = Column(Integer, ForeignKey(Tag.id), nullable=False)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)

    def __str__(self):
        return self.medicine.name + self.tag.name

class RegistrationForm(BaseModel):
    __tablename__ = 'registration_form'
    __table_args__ = {'extend_existing': True}
    user_id = Column(Integer, ForeignKey(User.id), nullable=False)
    examination_date = Column(Date, nullable=False)
    accepted = Column(Boolean, default=False)
    used = Column(Boolean, default=False)
    user = relationship('User', back_populates='registration_forms', lazy=True)

    def __str__(self):
        return self.user_id

    def __repr__(self):
        return '<RegistrationForm: {}>'.format(self.user_id)

class MedicalBill(BaseModel):   #Phieu kham
    __tablename__ = 'medical_bill'
    __table_args__ = {'extend_existing': True}
    examination_date = Column(Date, default=datetime.now())
    symptom = Column(Text, nullable=False)  # Trieu chung
    disease_prediction = Column(Text, nullable=True)    # du doan benh
    patient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    doctor_id = Column(Integer, ForeignKey(User.id), nullable=False)
    patient = relationship('User', back_populates='medical_bills', lazy=False, foreign_keys=[patient_id])
    doctor = relationship('User', back_populates='doctor_bills', lazy=False, foreign_keys=[doctor_id])
    examination_bill = relationship('ExaminationBill', back_populates='medical_bill', lazy=False, uselist=False)
    medical_bill_details = relationship('MedicalBillDetail', back_populates='medical_bill', lazy=True, uselist=True)

    def __str__(self):
        return f'Medical Bill: {self.examination_date} - {self.id}'

    def __repr__(self):
        return f'Medical Bill: {self.examination_date} - {self.id}'

class MedicalBillDetail(BaseModel):
    __tablename__ = 'medical_bill_detail'
    __table_args__ = {'extend_existing': True}
    quantity = Column(Integer, default=1)
    medicine_id = Column(Integer, ForeignKey(Medicine.id), nullable=False)
    medical_bill_id = Column(Integer, ForeignKey(MedicalBill.id), nullable=False)
    medicine = relationship('Medicine', back_populates='medical_bill_details', lazy=False, uselist=False)
    medical_bill = relationship('MedicalBill', back_populates='medical_bill_details', lazy=False, uselist=False)

    def __str__(self):
        return f'MedicalBillDetail'

class ExaminationBill(BaseModel):
    __tablename__ = 'examination_bill'
    __table_args__ = {'extend_existing': True}
    examination_date = Column(Date, default=datetime.now())
    medicine_money = Column(Float, default=0)
    examination_money = Column(Float, default=0)
    medical_bill_id = Column(Integer, ForeignKey(MedicalBill.id), nullable=False, unique=True)
    patient_id = Column(Integer, ForeignKey(User.id), nullable=False)
    paid = Column(Boolean, default=False)
    medical_bill = relationship('MedicalBill', back_populates='examination_bill', lazy=False, uselist=False)
    patient = relationship('User', back_populates='examination_bills', lazy=False, foreign_keys=[patient_id])

class Regulation(BaseModel):
    __tablename__ = 'regulation'
    __table_args__ = {'extend_existing': True}
    key = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    value = Column(Integer, nullable=False)
    user_id = Column(Integer, ForeignKey(User.id), nullable=True)
    user = relationship('User', back_populates='regulations', lazy=False)

    def __str__(self):
        return f'Regulation {self.regulation}: {self.value}'

    def __repr__(self):
        return f'Regulation {self.regulation}: {self.value}'
