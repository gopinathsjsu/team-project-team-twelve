import json
import psycopg2
from psycopg2.extras import RealDictCursor
import requests
import datetime
import time
import pytz

host="team12.ck2larrolbdg.us-east-2.rds.amazonaws.com"
username="postgres"
password="teamtwelve12" 
database="postgres"
conn=psycopg2.connect(
    host=host,
    database=database,
    user=username,
    password=password
)

# host="http://127.0.0.1"
# host="http://ec2-3-141-169-170.us-east-2.compute.amazonaws.com"
host="http://ec2-18-116-238-148.us-east-2.compute.amazonaws.com"

def cron_gate_allocate(event,context):
    current_time_start=datetime.datetime.now(pytz.timezone('US/Pacific')).time()
    current_time_end=(datetime.datetime.now(pytz.timezone('US/Pacific'))+datetime.timedelta(minutes=15)).time()
    current_date=datetime.datetime.now(pytz.timezone('US/Pacific')).date().strftime("%Y-%m-%d")

    print("current_time_start - ",current_time_start)
    print("current_time_end - ",current_time_end)

    # daily flight schedule
    url=f"{host}:8000/auth_urls/flight-schedule-list/?time__gte={current_time_start}&time__lte={current_time_end}&date__gte={current_date}&date__lte={current_date}"
    sd=requests.get(url=url)

    gate_status="open"
    terminal_gate=""
    td=requests.get(url=f"{host}:8000/auth_urls/terminal-gate-list/?gate_status={gate_status}&terminal_gate={terminal_gate}")

    fdd1=json.loads(sd.text)
    tdd=json.loads(td.text)
    # print('flights before: ', fdd)
    # for flight in fdd:
    #     if flight['terminal_gate_key'] != None :
    #         fdd.remove(flight)
    # # print('flights after: ', fdd)

    fdd=[]
    for flight in fdd1:
        # flight_gate_open_time=flight['gate_open_time']
        if flight['terminal_gate_key'] ==None:
            fdd.append(flight)


    # print('tdd : ', tdd)
    if len(fdd) == 0:
        print('msg: All flights are assigned gates')
        # return {'msg':'All flights are assigned gates'}

    if len(tdd) == 0:
        print('msg: All gates occupied')
        # return {'msg':'All gates occupied'}
    

    mn=min(len(fdd),len(tdd))

    for i in range(mn):
        update_flight_schedule_data={}
        flight_data=fdd[i]
        terminal_gate=tdd[i]['terminal_gate']
        
        tmp = datetime.datetime.strptime(flight_data['date']+" "+flight_data["time"],'%Y-%m-%d %H:%M:%S')
        gate_close_time=tmp+datetime.timedelta(minutes=-5)
        gate_open_time=tmp+datetime.timedelta(minutes=5)
        fact_guid=flight_data['fact_guid']
        update_flight_schedule_data['terminal_gate_key']=terminal_gate
        update_flight_schedule_data['gate_close_time']=gate_close_time.strftime('%H:%M:%S')
        update_flight_schedule_data['gate_open_time']=gate_open_time.strftime('%H:%M:%S')

        flight_url = f'{host}:8000/auth_urls/flight-schedule-rud/{fact_guid}'
        payload = update_flight_schedule_data
        r = requests.patch(flight_url, payload)
        print('updated flight schedule api')
        # sending the req to close the gate:
        gate_url = f'{host}:8000/auth_urls/terminal-gate-rud/{terminal_gate}/'
        payload ={'gate_status' : 'close'}
        r = requests.patch(gate_url, payload,timeout=30)
        print(f"in alloction - updated gate status {terminal_gate}")




# def cron_gate_deallocate(event,context):
    # sending the req to open the gate:
    current_time=datetime.datetime.now(pytz.timezone('US/Pacific')).time()
    gate_status="close"
    terminal_gate=""
    current_date=datetime.datetime.now(pytz.timezone('US/Pacific')).date().strftime("%Y-%m-%d")
    sd1=requests.get(url=f"{host}:8000/auth_urls/flight-schedule-list/?date__gte={current_date}&date__lte={current_date}")

    cdd1=json.loads(sd1.text)
    cdd=[]
    for flight in cdd1:
        # flight_gate_open_time=flight['gate_open_time']
        if flight['terminal_gate_key'] !=None:
            cdd.append(flight)


    
    print('dellocation -flights after: ', cdd)
    for flight in cdd:
        tt=datetime.datetime.strptime(flight['gate_open_time'],"%H:%M:%S").time()
        print(tt, "-" ,current_time)
        if tt<current_time:
            # flight schedule update req;
            update_flight_schedule_data={}
            fact_guid=flight['fact_guid']
            update_flight_schedule_data['terminal_gate_key']=""
            # update_flight_schedule_data['gate_close_time']=None
            # update_flight_schedule_data['gate_open_time']=""
            flight_url = f'{host}:8000/auth_urls/flight-schedule-rud/{fact_guid}'
            payload = update_flight_schedule_data
            r = requests.patch(flight_url, payload)
            print(f"updated flight schedule api - {fact_guid}  - gate deallocated {flight['terminal_gate_key']}")
            
            payload ={'gate_status' : 'open'}
            td=f"{host}:8000/auth_urls/terminal-gate-rud/{flight['terminal_gate_key']}/"
            r = requests.patch(td, payload)
            print(f"updated gate status {flight['terminal_gate_key']} - open ")
