
API:

1. To add a new doctor:

curl -H "Content-type: application/json" -X POST https://appointmentsappcedar.herokuapp.com/doctors -d '{"last_name":"Smith","first_name":"Bob"}'

2. To view all doctors:

curl -H "Content-type: application/json" -X GET https://appointmentsappcedar.herokuapp.com/doctors

3. To add a new patient:

curl -H "Content-type: application/json" -X POST https://appointmentsappcedar.herokuapp.com/patients -d '{"last_name":"Doe","first_name":"John","date_of_birth":"04-23-1990","gender":"M","phone_number":"321"}'

4. To view appointments for a date and doctor:

curl -H "Content-type: application/json" -X GET https://appointmentsappcedar.herokuapp.com/appointments -d '{"doctor_id":"0","date":"04-01-2017"}'

5. To make an appointment:

curl -H "Content-type: application/json" -X POST https://appointmentsappcedar.herokuapp.com/appointments -d '{"patient_id":"0","doctor_id":"0","date":"04-01-2017","start_time":"02:59","end_time":"03:00","notes":"hello"}'

_______________________________________________________________________________________

TO-DOs:

1. Make API description more professional
2. Implement front end, with logic for entering doctor id and date and displaying json returned by GET /appointments
3. Split into seperate files, probably grouping APIs and Models in sub directories
4. Add unit tests
5. Add validation logic for trying to add duplicates to any resource or request for resource that isn't there
6. Consolidate queries in can_make_appointment_at_this_time into one, did this because was wasting time on query logic

