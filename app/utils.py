from datetime import datetime

from app.twilio_client import client as TwillioClient


def is_past_date(input_date):
    current_date = datetime.now().date()

    if isinstance(input_date, str):
        input_date = datetime.strptime(input_date, "%Y-%m-%d").date()  # Adjust the format as needed

    if input_date < current_date:
        return True
    else:
        return False


def get_phones(data):
    # Create a set with modified phone numbers
    modified_phone_numbers_set = {entry['phone'].replace('0', '+84', 1) for entry in data}
    modified_phone_numbers_list = list(modified_phone_numbers_set)
    # Print the set
    print(modified_phone_numbers_list)
    return modified_phone_numbers_list


def send_SMS(phones, examination_date):
    # send twillio sms
    input_date = datetime.strptime(examination_date, "%Y-%m-%d").date()
    formatted_date_string = input_date.strftime("%d-%m-%Y")
    try:
        for phone in phones:
            message = TwillioClient.messages.create(
                from_='+12184927831',
                to=phone,
                body=f'Đơn khám bệnh của bạn ({phone}) tại Phòng khám mạch tư đã được xác nhận.'
                     f' Hãy nhớ khám bệnh vào ngày {formatted_date_string}',
            )
            print(message.sid)
        return True
    except Exception as e:
        print(e)
        return False


if __name__ == '__main__':

    import datetime
    data = [
        {'user_id': 1, 'fullname': 'Admin', 'phone': '0559110759', 'birthday': datetime.date(2024, 12, 22),
         'examination_date': datetime.date(2024, 22, 29), 'id': 9, 'accepted': False},
    ]
    get_phones(data)
