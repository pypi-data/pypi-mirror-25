import math
from past.builtins import xrange
from stimulus import round_down_900

#TODO: change all wait_time refs to be threshold instead

def intensity(aht, interval, rate):
    return float(aht) * (float(rate) / float(interval))

def erlang_b(server_count, intensity):
    ib = 1.0
    server_count = int(server_count) # need explicit cast here to prevent range TypeError
    for i in xrange(0, server_count):
        ib = 1.0 + ib * ((float(i) + 1.0) / float(intensity))
    return 1.0 / ib

def erlang_c(server_count, intensity):
    erl_b = erlang_b(server_count=server_count, intensity=intensity)
    return erl_b / (1.0 - float(intensity/server_count) * (1.0 - erl_b))

def occupancy(server_count, intensity):
    return float(intensity) / float(server_count)

def average_queue_time(server_count, rate, interval, aht, **kwargs):
    a = intensity(aht=aht, interval=interval, rate=rate)
    return (erlang_c(float(server_count), a) * float(aht)) / (float(server_count) - a)

def service_level(server_count, rate, interval, aht, wait_time):
    a = intensity(aht=aht, rate=rate, interval=interval)
    return (1.0 - erlang_c(server_count=float(server_count), intensity=a) * math.exp(-(float(server_count) - a) * (float(wait_time) / float(aht))))

def validate_sl_target(t):
    if not 0.0 < t <= 1.0:
        raise ValueError('SL must be between 0 and 1')

    return True

def validate_asa_target(t):
    if t <= 0:
        raise ValueError('ASA must be greater than 0')

    return True

def validate_target(target, target_type):
    validators = {'SL': validate_sl_target,
                  'ASA': validate_asa_target}

    validator = validators[target_type]

    validator(target)

    return True

funcs_to_targets = {'SL': service_level,
                    'ASA': average_queue_time}
def required_server_count(target, rate, interval, aht, wait_time=None, target_type='SL'):

    validate_target(target, target_type)

    a = intensity(aht=aht, rate=rate, interval=interval)
    server_count = max(1, math.ceil(a))

    func = funcs_to_targets[target_type]

    while func(server_count, rate, interval, aht, wait_time) < target:
        server_count += 1
    
    return server_count

def day_to_erlang_dict(day):
    """
    Takes a stimulus.Day object and returns count of calls by 15-minute intervals,
    simplifying the process of running the Erlang C model on that day.
    
    :param day: a stimulus.Day object
    :returns: a dictionary with keys representing 15-min intervals of day, and values
    representing the number of calls received in that interval.
    """
    first_agent_start = round_down_900(day.earliest_arrival)
    calls_by_interval = {}
    day_completed = False
    arrival_times = []

    for call in day.calls:
        arrival_times.append(call.arrival_timestamp)

    for x in xrange(0,86400,900):
        calls_by_interval[x] = sum(1 for i in arrival_times if x <= i < (x + 900))
      
    return calls_by_interval

def vol_dict_to_headcount_dict(vol_dict, aht, interval, rate, target, target_type, wait_time):
    result_dict = {}

    for i in vol_dict:
        if not vol_dict[i] == 0:
            result_dict[i] = required_server_count(aht, interval, rate, target, target_type, wait_time)
        else:
            result_dict[i] = 0

    return result_dict

