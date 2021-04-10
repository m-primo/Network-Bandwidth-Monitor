import time
import datetime
import psutil
# ================================================================
# Kibibytes = 1024 bytes, Kilobytes = 1000 bytes
# Mebibytes = 1024 kibibytes, Megabytes = 1000 kilobytes
# Gibibytes = 1024 mebibytes, Gigabytes = 1000 megabytes
# ================================================================
# Convert the value to gibi bytes
def convert_to_gb(value):
    return value/1024./1024./1024.

# Convert the value to mebi bytes
def convert_to_mb(value):
    return value/1024./1024.

# Convert the value to kibi bytes
def convert_to_kb(value):
    return value/1024.

# View stats
def send_stat(sent,recv,totl):
    # Unit handler
    def convert_to_unit(value):
        kb_value = convert_to_kb(value)
        kb_unit = 'kiB'
        mb_value = convert_to_mb(value)
        mb_unit = 'MiB'
        gb_value = convert_to_gb(value)
        gb_unit = 'GiB'

        to_unit_name = kb_unit
        to_unit_value = kb_value

        if kb_value >= 1024:
            to_unit_value = mb_value
            to_unit_name = mb_unit
        if mb_value >= 1024:
            to_unit_value = gb_value
            to_unit_name = gb_unit

        return [to_unit_value,to_unit_name]

    # Sent Stats
    sent_stat = convert_to_unit(sent)
    sent_value = sent_stat[0]
    sent_unit = sent_stat[1]

    # Receive Stats
    recv_stat = convert_to_unit(recv)
    recv_value = recv_stat[0]
    recv_unit = recv_stat[1]

    # Total Stats
    totl_stat = convert_to_unit(totl)
    totl_value = totl_stat[0]
    totl_unit = totl_stat[1]

    # Current Time
    now = datetime.datetime.now()
    now_formatted = now.strftime("%Y-%m-%d %I:%M:%S %p")

    # Round
    def to_round(value):
        return str(round(value, 2))

    # View Stats
    time_str = "Time: " + now_formatted
    sent_str = "Sent/Upload: " + to_round(sent_value) + " " + sent_unit
    recv_str = "Receive/Download: " + to_round(recv_value) + " " + recv_unit
    totl_str = "Total: " + to_round(totl_value) + " " + totl_unit

    print(time_str)
    print(sent_str)
    print(recv_str)
    print(totl_str)
    print("")

    # Write Stats to a File
    strs_to_file = time_str+"\n"+sent_str+"\n"+recv_str+"\n"+totl_str+"\n\n"
    with open('stats.log','a+') as file: file.write(strs_to_file)
# ================================================================
def main():
    old_value_sent = 0
    old_value_recv = 0
    old_value_totl = 0

    while True:
        new_value_sent = psutil.net_io_counters().bytes_sent # Bytes Sent
        new_value_recv = psutil.net_io_counters().bytes_recv # Bytes Received
        new_value_totl = new_value_sent + new_value_recv     # Total Bytes

        if old_value_totl:
            sent_stat = new_value_sent - old_value_sent
            recv_stat = new_value_recv - old_value_recv
            totl_stat = new_value_totl - old_value_totl
            send_stat(sent_stat, recv_stat, totl_stat)

        old_value_sent = new_value_sent
        old_value_recv = new_value_recv
        old_value_totl = new_value_totl

        time.sleep(1) # Wait a second
# ================================================================
main()