unique_sep = '|'    # I posit vertical bar as not appearing in any user name
import datetime

source="pune"
destination='delhi'
arrival_departure="arrival"
terminal_gate_key="terminal_gate"

ls=["pune","delhi","arrival","terminal_gate"]

import uuid
def get_fact_guid(source,destination,terminal_gate_key):
    unique_ID = uuid.uuid5(uuid.NAMESPACE_X500,source + unique_sep + destination+unique_sep+terminal_gate_key)
    return unique_ID

print(get_fact_guid(source,destination,terminal_gate_key))