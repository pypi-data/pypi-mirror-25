# ****************       BEGIN-STANDARD-COPYRIGHT      ***************
#
# Copyright (c) 2017, Spirent Communications.
#
# All rights reserved. Proprietary and confidential information of Spirent Communications.
#
#  ***************        END-STANDARD-COPYRIGHT       ***************

from xml.etree import ElementTree
from SpirentSLC import SLC

##
with SLC.init(host='localhost:9005', itar_path='itars') as slc:

    ## Openin a response map projecy
    proj = slc.open('response_map_test_prj')

    proj2 = slc.open('my_project')
    with proj2.slc_test_ffsp.open() as s2:
        # for i in range(1, 1000):
        # resp = s2.command('print(1)')
        resp = s2.eval('puts(1)')
        print(resp.text)

    # -------------------- HTTP session -----------------------------
    with proj.http_ffsp.open() as s1:

        for i in range(1, 1000):
            resp = s1.command('get page http://download.xored.com/q7/cd_catalog.xml', response_map="xml_catalog.ffrm")
            # print(resp.queries())

            ## Query for titles
            if resp.xml != None:
                print([x.text for x in resp.xml.findall('.//TITLE')])

            ## Do same with response map defined query
            # print(resp.titles())

    # -------------------- SSH session -----------------------------
    with proj.ssh_ffsp.open() as s1:
        resp = s1.command('ls -la', response_map="la_la.ffrm")
        print(resp.text)
        print(resp.queries())
        print(ElementTree.tostring(resp.xml))

    # -------------------- REST session -----------------------------
    with proj.REST_ffsp.open(url='https://jsonplaceholder.typicode.com/') as s1:
        print(s1.GET('/posts/1'))
