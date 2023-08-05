# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

from SpirentSLC import SLC

with SLC.init(host='localhost:9005', itar_path='itars/') as slc:
    print(slc.list())

    proj = slc.open('my_project')
    print(proj.list(parameter_file=True, response_map=True))

    # -------------------- Python session ---------------------------
    # with proj.slc_test_ffsp.open() as s1:
    #     print('==== agent ====')
    #     print(s1.agent)

    #     print('==== command ====')
    #     print(s1.command('print(1)', test_param=True))

    #     print(s1.my_quickcall(param1=123, param2=True))

    print("check telnet")
    # -------------------- Telnet session (somewhat broken atm) -----
    # with proj.telnet_ffsp.open(ipAddress='40.76.76.181', port=80) as s1:
    #     print('==== agent ====')
    #     print(s1.agent)

    print("check HTTP")
    # -------------------- HTTP session -----------------------------
    with proj.http_ffsp.open() as s1:
        resp = s1.command('get page http://xored.com')
        print(resp.text)

    # -------------------- REST session -----------------------------
    # with proj.REST_ffsp.open(url='https://jsonplaceholder.typicode.com/') as s1:
    #     print(s1.GET('/posts/1'))
