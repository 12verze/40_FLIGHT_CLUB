from flight_search import FlightSearch
from data_manager import DataManager
from mail_sender import MailSender


city_data = DataManager()
data = city_data.get_data()


for n in data["formResponses1"]:
    if n["destCode"] == '' or n["originCode"] == '':
        dcode = FlightSearch().get_iata(n['destination'].strip())
        ocode = FlightSearch().get_iata(n['origin'].strip())

        city_data.update_data(d_iata=dcode,o_iata=ocode,row_id=n["id"])

for n in data["formResponses1"]:
    if n['mailsent'] == '':
        dest_code = n['destCode']
        origin_code = n['originCode']
        name = n['name']
        mail = n['mail']
        price = 100000
        date = n['timestamp'].split(" ")[0]

        message = FlightSearch().cheapest_flight(dest_code,origin_code, price,name,date)

        if message is not None:
            MailSender().send_mail(mail,message)
        else:
            message = "Oops we couldn't find any flight, your luck must be really bad :(("
            MailSender().send_mail(mail, message)
        city_data.update_state(row_id=n["id"])












