import random
import time
from utils import secs_to_time
from pprint import pprint


class Agent(object):
    _ID = 0
    def __init__(self, schedule):
        self.id = self._ID; self.__class__._ID += 1
        self.schedule = schedule
        self.status = 'logged_off'
        self.last_status = 'initialized'
        self.time_in_status = 0
        self.active_call = False
        self.previously_active = False
        self.handling_call = None
        self.outbound_reserved = False
        self.previously_outbound = False

    def reset(self):
        self.status = 'logged_off'
        self.last_status = 'initialized'
        self.time_in_status = 0
        self.active_call = False
        self.previously_active = False
        self.handling_call = None
        self.outbound_reserved = False
        self.previously_outbound = False

class AgentSchedule(object):
    _ID = 0
    def __init__(self, regular_start=28800, regular_end=(3600*16.5), regular_lunch=(3600*12), lunch_duration=1800, tz='America/Chicago', work_days=[1,2,3,4,5]):
        self.id = self._ID; self.__class__._ID += 1
        self.regular_start = regular_start
        self.regular_end = regular_end
        self.regular_lunch = regular_lunch
        self.lunch_duration = lunch_duration
        self.tz = tz
        self.work_days = work_days

class Day(object):
    _ID = 0
    def __init__(self, agents, calls, outbound_list=[], outbound_reservation=0.0, dials_per_reservation=0.0, reservation_length=0.0):
        self.id = self._ID; self.__class__._ID += 1
        self.agents = agents
        self.calls = calls
        self.outbound_list = outbound_list
        self.outbound_reservation = outbound_reservation
        self.dials_per_reservation = dials_per_reservation
        self.reservation_length = reservation_length
        self.INITIAL_OUTBOUND_LIST_COUNT = len(outbound_list)
        self.sl_threshold = 20
        self.sl_target = 0.90
        self.interval = 15 * 60 # 15 minutes

        self.sl_interval_dict = {}

        earliest_arrival = 99999

        for call in self.calls:
            if call.arrival_timestamp < earliest_arrival:
                earliest_arrival = call.arrival_timestamp

        self.earliest_arrival = earliest_arrival

    def agents_currently_available(self):
        return sum(agent.status=='logged_on' and agent.active_call==False and agent.outbound_reserved==False for agent in self.agents)

    def agents_currently_logged_on(self):
        return sum(agent.status=='logged_on' for agent in self.agents)

    def percent_agents_available(self):
        try:
            return self.agents_currently_available() / self.agents_currently_logged_on()
        except ZeroDivisionError:
            return 0.0

    def offered_calls(self):
        return sum(call.status!='pre-call' for call in self.calls)

    def completed_calls(self):
        return sum(call.status=='completed' for call in self.calls)

    def dials_made(self):
        return self.INITIAL_OUTBOUND_LIST_COUNT - len(self.outbound_list)

    def dials_remaining(self):
        return len(self.outbound_list)

    def active_calls(self):
        return sum(call.status=='active' for call in self.calls)

    def queued_calls(self):
        return sum(call.status=='queued' for call in self.calls)

    def abandoned_calls(self):
        return sum(call.status=='abandoned' for call in self.calls)

    def calls_within_sl(self):
        return sum(call.met_sl for call in self.calls)

    def service_level(self):
        try:
            return 1.0 * self.calls_within_sl() / self.offered_calls()
        except ZeroDivisionError:
            return 1.0

    def print_status_line(self):
        return (' offered: ' + str(self.offered_calls()) + ' queued: ' + str(self.queued_calls()) + ' active: ' + str(self.active_calls()) +
                ' completed: ' + str(self.completed_calls()) + ' abandoned: ' + str(self.abandoned_calls()) +
                ' SL: ' + "{0:.2f}%".format(100*self.service_level()) +
                ' aht: ' + str(self.aht()) +
                ' dials: ' + str(self.dials_made()) +
                ' dials left: ' + str(self.dials_remaining())
               )

    def list_of_completed_calls(self):
        return [call for call in self.calls if call.status=='completed']

    def aht(self):
        try:
            return sum([call.duration for call in self.list_of_completed_calls()]) / len(self.list_of_completed_calls())
        except ZeroDivisionError:
            return '--'

    def reset(self):
        for call in self.calls:
            call.reset()
        for agent in self.agents:
            agent.reset()

class Call(object):
    _ID = 0
    def __init__(self, arrival_timestamp, duration, direction='in'):
        self.id = self._ID; self.__class__._ID += 1
        self.arrival_timestamp = arrival_timestamp
        self.duration = duration
        self.status = 'pre-call'
        self.queued_at = None
        self.answered_at = None
        self.abandoned_at = None
        self.queue_elapsed = None
        self.handled_by = None
        self.met_sl = False

    def reset(self):
        self.status = 'pre-call'
        self.queued_at = None
        self.answered_at = None
        self.queue_elapsed = None
        self.handled_by = None
        self.met_sl = False

def simulate_one_step(timestamp, day, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    i = timestamp
    day.agents = agent_logons(day.agents, i)
    day.agents = agent_logoffs(day.agents, i)
    day.calls = queue_calls(day.calls, i)
    day = answer_calls(day, i)
    day = hangup_calls(day, i)
    day.calls = update_queued_call_stats(day.calls, i)
    day = abandon_calls(day, i, abandon_dist)
    day = reserve_outbound(day, i)
    day = cancel_reservation(day, i)
    day.agents = update_agent_status_stats(day.agents, i)

    c = 0
    pc = 0

    for call in day.calls:
        if call.status == 'completed':
            c += 1
        elif call.status == 'pre-call':
            pc += 1
    
    if pc == len(day.calls) or c == len(day.calls):
        fast_mode = True # enters fast mode when all calls are pre-call or done

    if not skip_sleep:
        if fast_mode:
            time.sleep(0.00001)
        else:
            time.sleep(0.05)
    
    if verbose_mode:
        print(secs_to_time(i) + day.print_status_line())

    return day

def simulate_day(day, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    for i in range(3600*24):
        day = simulate_one_step(timestamp=i, day=day, abandon_dist=abandon_dist, skip_sleep=skip_sleep, fast_mode=fast_mode, verbose_mode=verbose_mode)
    return day

def simulate_days(day_list, abandon_dist, skip_sleep=True, fast_mode=True, verbose_mode=False):
    for day in day_list:
        day = simulate_day(day, abandon_dist, skip_sleep, fast_mode, verbose_mode)
    return day_list

def simulate_days_alt(projected_volume_df, vol_dim, day_of_week_dist, start_time, handles_base, 
                      agent_list, abandon_dist, outbound_list=[], outbound_reservation=0.0,
                      dials_per_reservation=0.0, reservation_length=0,
                      skip_sleep=True, fast_mode=True, verbose_mode=False):
    
    simulated_days = []
    
    for i, day in projected_volume_df.iterrows():
        count_calls = day[vol_dim]
        arrival_rates = count_calls * day_of_week_dist
        arrival_times = []

        for x in arrival_rates:
            for xx in range(start_time, start_time + 900):
                threshold = x / 900
                if random.random() < threshold:
                    arrival_times.append(xx)
            start_time += 900

        calls_list = []
        actual_num_calls = len(arrival_times)
        call_durations = handles_base.sample(actual_num_calls)

        for arr, dur in zip(arrival_times, call_durations):
            calls_list.append(Call(arr,dur))

        day_object = Day(agent_list, calls_list, outbound_list=outbound_list, 
                         outbound_reservation=outbound_reservation,
                         dials_per_reservation=dials_per_reservation,
                         reservation_length=reservation_length)

        simulated_day = simulate_day(day_obj, abandon_dist)
        simulated_days.append(simulated_day)
    
    return simulated_days


def agent_logons(agents, timestamp):
    for agent in agents:
        if agent.schedule.regular_start == timestamp and agent.status == 'logged_off':
            agent.status = 'logged_on'
    return agents

def agent_logoffs(agents, timestamp):
    for agent in agents:
        if agent.active_call == False and agent.status == 'logged_on' and agent.schedule.regular_end <= timestamp and agent.outbound_reserved == False:
            agent.status = 'logged_off'
    return agents

def update_agent_status_stats(agents, timestamp):
    for agent in agents:
        if agent.last_status != agent.status or agent.previously_active != agent.active_call or agent.previously_outbound != agent.outbound_reserved:
            agent.last_status = agent.status
            agent.previously_active = agent.active_call
            agent.previously_outbound = agent.outbound_reserved
            agent.time_in_status = 0
        else:
            agent.time_in_status += 1
    return agents

def queue_calls(calls_list, timestamp):
    for call in calls_list:
        if call.arrival_timestamp == timestamp:
            call.status = 'queued'
            call.queued_at = timestamp
    return calls_list

def update_queued_call_stats(calls_list, timestamp):
    for call in calls_list:
        if call.status == 'queued':
            call.queue_elapsed = timestamp - call.queued_at
    return calls_list

def answer_calls(day, timestamp):
    for call in day.calls:
        if call.status == 'queued':
            for agent in day.agents:
                if agent.status == 'logged_on' and agent.active_call == False and agent.outbound_reserved == False:
                    agent.active_call = True
                    agent.handling_call = call.id
                    call.handled_by = agent
                    call.answered_at = timestamp
                    call.queue_elapsed = timestamp - call.queued_at
                    call.met_sl = (call.queue_elapsed <= day.sl_threshold)
                    call.status = 'active'
                    break
    return day

def hangup_calls(day, timestamp):
    for call in day.calls:
        if call.status == 'active' and (call.duration + call.answered_at) <= timestamp:
            call.status = 'completed'
            call.completed_at = timestamp
            call.handled_by.active_call = False
            call.handled_by.handling_call = None 
    return day

def abandon_calls(day, timestamp, abandon_distribution):
    abandon_distribution = sorted(abandon_distribution)
    for call in day.calls:
        if call.status == 'queued':
            for aban_tuple in abandon_distribution:
                if aban_tuple[0] >= call.queue_elapsed:
                    if random.random() >= aban_tuple[1]:
                        call.status = 'abandoned'
                        call.abandoned_at = timestamp  
                        break
    return day

def reserve_outbound(day, timestamp):
    if not day.outbound_list == [] and day.percent_agents_available() < day.outbound_reservation and day.agents_currently_available() >= 2:
        longest_available_time = 0 
        reservation_candidate = None
        for agent in day.agents:
            if agent.status == 'logged_on' and agent.active_call == False and agent.outbound_reserved == False:
                if agent.time_in_status > longest_available_time:
                    reservation_candidate = agent
                    longest_available_time = agent.time_in_status
        if reservation_candidate is not None:
            reservation_candidate.outbound_reserved = True
    return day

def cancel_reservation(day, timestamp):
    for agent in day.agents:
        if agent.outbound_reserved == True:
            if agent.time_in_status == day.reservation_length:
                agent.outbound_reserved = False
                # strike dials_per_reservation from front of list
                day.outbound_list = day.outbound_list[day.dials_per_reservation:]
    return day

def round_down_900(stamp):
    return stamp - (stamp % 900)

def calculate_required_headcount(day, abandon_dist, agent_counts={}, skip_sleep=True, fast_mode=True, verbose_mode=False):
    
    first_agent_start = round_down_900(day.earliest_arrival)

    day_completed = False

    while not day_completed:
        
        day.reset()
        
        agent_list = []

        for i in agent_counts.keys():
            for ii in range(0, int(agent_counts[i])):
                agent_list.append(Agent(AgentSchedule(regular_start=i, regular_end=i+900, regular_lunch=3600*24)))

        day.agents = agent_list
        
        for stamp in range(first_agent_start,3600*24):
            day = simulate_one_step(timestamp=stamp, day=day, abandon_dist=abandon_dist, skip_sleep=skip_sleep, fast_mode=fast_mode, verbose_mode=verbose_mode)
            if stamp % 900 == 0:
                if day.service_level() < day.sl_target:
                    agent_counts[stamp-900] += 1
                    #pprint(agent_counts)
                    print agent_counts[stamp-900]
                    break
            if stamp == 86399:
                day_completed = True

    pprint(agent_counts)
    return agent_counts

