from itoolkit import *
from itoolkit.transport import DatabaseTransport
import ibm_db_dbi


itool = iToolKit()

conn = ibm_db_dbi.connect()
itransport = DatabaseTransport(conn)

itool.add(iCmd('addlible', 'ADDLIBLE PGPROGS'))
itool.add(iCmd('addlible', 'ADDLIBLE PGFILES'))
itool.add(iCmd('addlible', 'ADDLIBLE PGCO#00004'))

itool.add(
iPgm('chgedtupcl', 'CHGEDTUPCL')
    .addParm(iData('BATCH#', '8a', '01153092'))
    .addParm(iData('BATCHU', '10a', 'MVICK'))
)

itool.call(itransport)

chgedtupcl = itool.dict_out('chgedtupcl')

if 'success' in chgedtupcl:
    print(chgedtupcl['success'])
    # print("Return parameter values:")
    # print("BATCH#: " + chgedtupcl['BATCH#'])
    # print("BATCHU: " + chgedtupcl['BATCHU'])
else:
    raise Exception("Program call error:" + chgedtupcl['error'])
