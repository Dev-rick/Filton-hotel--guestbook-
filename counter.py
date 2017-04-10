from models import Message

def save_to_data(value):
    result = 0.0
    if value == "bad":
        result += 1.0
    elif value == "not_special":
        result += 2.0
    elif value == "good":
        result += 3.0
    elif value == "very good":
        result += 4.0
    elif value == "excellent":
        result += 5.0
    return result


def get_average_rating():
    list_of_ratings = []
    messages = Message.query().fetch()
    for message in messages:
        list_of_ratings.append(message.ratings)
    float_in_list_of_ratings = [num for num in list_of_ratings if isinstance(num, (int, float))]
    if len(float_in_list_of_ratings) > 0:
        average = sum(float_in_list_of_ratings) / float(len(float_in_list_of_ratings))
        if average < 1.5:
            average = "bad"
        elif average < 2.5:
            average = "not special"
        elif average < 3.5:
            average = "good"
        elif average < 4.5:
            average = "very good"
        elif average > 4.5 or average == 4.5:
            average = "excellent"
    else:
        average = None

    return average

