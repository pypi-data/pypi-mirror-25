
from SpirentSLC import SLC

with SLC.init(host='localhost:9005') as slc:
    print('============== Prolects list ==============')
    print(slc.list())

    print('============== NativePyLib project resources ==============')
    proj = slc.open('NativePyLib')
    print(proj.list(parameter_file=True, response_map=True))

    print('============== Topology ==============')
    with proj['Server+PC_tbml'].server1.cmd.open() as cmd_session:
        print(cmd_session.command('help'))
