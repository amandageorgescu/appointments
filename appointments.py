import flask
import flask_sqlalchemy
from flask import request, json, render_template

import datetime

app = flask.Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////tmp/appointments.db'
db = flask_sqlalchemy.SQLAlchemy(app)

#Model
class Doctor(db.Model):
	__tablename__ = 'doctors'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	last_name = db.Column(db.String(64))
	first_name = db.Column(db.String(64))

	def __init__(self, last_name=None, first_name=None):
		self.last_name = last_name
		self.first_name = first_name

class Patient(db.Model):
	__tablename__ = 'patients'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	last_name = db.Column(db.String(64))
	first_name = db.Column(db.String(64))
	date_of_birth = db.Column(db.Date)
	gender = db.Column(db.String(1))
	phone_number = db.Column(db.String(16))

	def __init__(self, last_name=None, first_name=None, date_of_birth=None, gender=None, phone_number=None):
		self.last_name = last_name
		self.first_name = first_name
		self.date_of_birth = date_of_birth
		self.gender = gender
		self.phone_number = phone_number

class Appointment(db.Model):
	__tablename__ = 'appointments'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	patient_id = db.Column(db.Integer, db.ForeignKey('patients.id'))
	doctor_id = db.Column(db.Integer, db.ForeignKey('doctors.id'))
	date = db.Column(db.Date)
	start_time = db.Column(db.Time)
	end_time = db.Column(db.Time)
	notes = db.Column(db.String(256))

	def __init__(self, patient_id=None, doctor_id=None, date=None, start_time=None, end_time=None, notes=None):
		self.patient_id = patient_id
		self.doctor_id = doctor_id
		self.date = date
		self.start_time = start_time
		self.end_time = end_time
		self.notes = notes

#API/Routes
@app.route('/doctors', methods = ['POST', 'GET'])
def api_doctors():
	if request.method == 'POST':
		return add_new_doctor(request)
	if request.method == 'GET':
		return get_all_doctors()

@app.route('/patients', methods = ['POST'])
def api_patients():
	return add_new_patient(request)

@app.route('/appointments', methods = ['POST', 'GET'])
def api_appointments():
	if request.method == 'POST':
		return make_appointment(request)
	if request.method == 'GET':
		return get_appointments_by_doctor(request)

#Controller Logic
def add_new_doctor(request):
	doctor = Doctor(request.json["last_name"], request.json["first_name"])
	db.session.add(doctor)
	db.session.commit()
	return json.dumps({'success':True}), 201, {'ContentType':'application/json'} 

def get_all_doctors():
	doctors = Doctor.query.all()
	doctors_json = []
	for doctor in doctors:
		doctor_json = {"id":doctor.id,"last_name":doctor.last_name,"first_name":doctor.first_name}
		doctors_json.append(doctor_json)
	return json.dumps({"doctors":doctors_json})

def add_new_patient(request):
	patient = Patient(request.json["last_name"], request.json["first_name"], datetime.datetime.strptime(request.json["date_of_birth"], '%m-%d-%Y').date(), request.json["gender"], request.json["phone_number"])
	db.session.add(patient)
	db.session.commit()
	return json.dumps({'success':True,"patient_id":patient.id}), 201, {'ContentType':'application/json'} 

def get_appointments_by_doctor(request):
	appointments = Appointment.query.filter(Appointment.doctor_id == request.json["doctor_id"] and Appointment.date == datetime.datetime.strptime(request.json["date"], '%m-%d-%Y').date())
	appointments_json = []
	for appt in appointments:
		appt_json = {"patient_id":appt.patient_id,"start_time":appt.start_time.strftime('%H:%M'),"end_time":appt.end_time.strftime('%H:%M'),"notes":appt.notes}
		appointments_json.append(appt_json)
	return json.dumps({"appointments":appointments_json})

def can_make_appointment_at_this_time(doctor_id, date, start, end):
	conflicting_start = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date == date, Appointment.start_time >= start, Appointment.start_time < end).all()
	conflicting_end = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date == date, Appointment.end_time > start, Appointment.end_time <= end).all()
	conflicting_longer = Appointment.query.filter(Appointment.doctor_id == doctor_id, Appointment.date == date, Appointment.start_time <= start, Appointment.end_time >= end).all()

	num_conflicts = len(conflicting_start) + len(conflicting_end) + len(conflicting_longer)
	print(num_conflicts)
	if num_conflicts > 0:
		return False
	else:
		return True

def make_appointment(request):
	start = datetime.datetime.strptime(request.json["start_time"], '%H:%M').time()
	end = datetime.datetime.strptime(request.json["end_time"], '%H:%M').time()
	date = datetime.datetime.strptime(request.json["date"], '%m-%d-%Y').date()

	if can_make_appointment_at_this_time(request.json["doctor_id"], date, start, end):
		appointment = Appointment(request.json["patient_id"], request.json["doctor_id"], date, start, end, request.json["notes"])
		db.session.add(appointment)
		db.session.commit()
		return json.dumps({'success':True}), 200, {'ContentType':'application/json'} 
	else:
		return json.dumps({'success':False}), 400, {'ContentType':'application/json'}

if __name__ == '__main__':
	db.create_all()
	#port = int(os.environ.get("PORT", 5000))
	#app.run(host='0.0.0.0', port=port)
	app.run()




