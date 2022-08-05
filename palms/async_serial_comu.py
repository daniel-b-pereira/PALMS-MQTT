import asyncio
import serial_asyncio
import datetime



async def start(loop,port):
        reader, _ = await serial_asyncio.open_serial_connection(url=port, baudrate=9600)
        received = recv(reader)
        return await asyncio.wait([received])

async def recv(r):
    while True:
        try:
            msg = await r.readuntil(b'\n')
            timer = datetime.datetime.utcnow
            msg = msg.decode().rstrip()
            tag = dict()
            if msg != '':
                    _temp = msg.split('-')
                    if len(_temp) ==7:
                        for e in _temp:
                            if e.startswith('I'): # TAG ID
                                tag['id']       = e[1:]
                            elif e.startswith('A'): # Antena
                                tag['ant']      = e[1:]
                            elif e.startswith('R'): # Reader
                                tag['readerId'] = e[1:]
                            elif e.startswith('P'):
                                tag['pnrd']     = e[1:]
                            elif e.startswith('T'):
                                string_token    = e[2:-1]
                                tag['token']     = string_token.split(',')
                                tag['token'] = list(map(int, tag['token']))
                            elif e.startswith('F'):
                                tag['fire']     = int(e[1:])
                        tag['time'] = timer
                        #if_saved = pnrd_db(tag)
                        #print(if_saved)
                    if tag == {}:
                        pass
                    else:
                        # print (tag)
                        return tag

        except:
            return "ERROR ON READ"
                    
