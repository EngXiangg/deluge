import snap7

IP_ADDRESS = '192.168.0.5'
RACK = 0
SLOT = 1

class PLC_Python():
    def __init__(self, ip, rack, slot):
        self.ip = ip
        self.rack = rack
        self.slot = slot
        self.connected = False
        self.plc = snap7.client.Client()

        self.bit_list = []
        self.bit_list2 = []
        self.sum_list = []
        self.sum_list2 = []

    def connect(self, ip=None):
        if ip is None:
            ip = self.ip

        try:
            self.plc.connect(ip, self.rack, self.slot)
            self.connected = True
            print('connected')

        except Exception as e:
            print(f"Error: {e}")

    def disconnect(self):
        self.plc.disconnect()
        self.connected = False

    def get_bool(self, offset: int, bit: int):
        '''
        offset : refers PLC DB offset number
        bit : refers PLC DB bit number (eg. offset = 2.1  , bit = 1)
        db : refers PLC DB number (eg. DB2  = 2)
        max_byte : refers PLC DB Max Offset numbers
        '''

        db = 4
        max_byte = 2
        read = self.plc.db_read(db, 0, max_byte)
        bool = snap7.util.get_bool(read, offset, bit)
        print(f'bool = {bool}')

    def write_bool(self, offset: int, bit: int, value: bool):
        '''
        offset : refers PLC DB offset number
        bit : refers PLC DB bit number (eg. offset = 2.1  , bit = 1)
        value : True or False / 1 or 0
        db : refers PLC DB number (eg. DB2  = 2)
        max_byte : refers PLC DB Max Offset numbers
        '''

        db = 4
        max_byte = 2
        array = self.plc.db_read(db, 0, max_byte)
        snap7.util.set_bool(array, offset, bit, value)
        self.plc.db_write(db, 0, array)

    def get_int(self,db: int ,offset: int):
        max_byte = 11
        read = self.plc.db_read(db, 0, max_byte)
        data = snap7.util.get_int(read, offset)
        return data

    def write_int(self,db: int, max_byte : int, offset: int, value: int):
        array = self.plc.db_read(db, 0, max_byte)
        snap7.util.set_int(array, offset, value)
        self.plc.db_write(db, 0, array)

    def get_real(self,offset: int):
        db = 4
        max_byte = 144
        array = self.plc.db_read(db, 104, max_byte)
        data = snap7.util.get_real(array, offset)
        print(f'real = {round(data,3)}')

    def write_real(self, offset: int, value: float):
        '''
        value = float number (eg.  value =1.2123)
        '''
        db = 4
        max_byte = 144
        array = self.plc.db_read(db, 0, max_byte)
        snap7.util.set_real(array, offset, value)
        self.plc.db_write(db, 0, array)

    # CONVERT INT TO USINT , THEN WRITE TO PLC
    def get_bit(self,input,first=True):
        num = [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768]

        for i in range(15):
            if num[i] >= input:

                if first:
                    a = i-1
                elif num[i-1] < input < num[i] and not first:
                    a = i-1
                else:
                    a = i
                print(a)
                if num[a] < 256:
                    self.bit_list.append(num[a])
                else:
                    new_bit = 2**(a - 8)
                    print(new_bit)
                    self.bit_list2.append(new_bit)
                remain = input - num[a]
                print(f'number = {remain}')
                if remain == 0:
                    print(f'bit list = {self.bit_list}')
                    print(f'sum = {sum(self.bit_list)}')
                    print(f'bit list2 = {self.bit_list2}')
                    print(f'sum2 = {sum(self.bit_list2)}')

                    return sum(self.bit_list),sum(self.bit_list2)
                else:
                    return self.get_bit(remain,first=False)

    def reset(self):
        self.bit_list = []
        self.bit_list2 = []

    # READ USINT DATA FROM PLC , THEN CONVERT TO INT
    def read_usint_data(self,input1, input2, first=True):
        num = [1, 2, 4, 8, 16, 32, 64, 128, 256]
        if input1 <= 255:
            self.sum_list = input1
        if input2 < 256 and input2 != 0:
            for i in range(7):
                if num[i] >= input2:
                    if first and input2 > 1:
                        a = i - 1
                    elif num[i - 1] < input2 < num[i] and not first:
                        a = i - 1
                    else:
                        a = i
                    remain = input2 - num[a]
                    b = 2 ** (8 + a)
                    self.sum_list2.append(b)
                    if remain == 0:
                        self.sum_list2.append(remain)
                        # print(sum(self.sum_list2))
                        # print(sum(self.sum_list2, self.sum_list))
                        return sum(self.sum_list2,self.sum_list)
                    else:
                        return self.read_usint_data(input1,remain, False)
        # print(input1)
        return input1

if __name__ == '__main__':
    commu = PLC_Python(IP_ADDRESS,RACK,SLOT)

    commu.connect(IP_ADDRESS)
    # commu.get_bool(2,0)
    # while True:
        # commu.write_bool(1,3,0)
        # commu.get_bool(2,0)
        # time.sleep(0.5)
        # commu.write_bool(1,3,True)
        # time.sleep(0.5)

    # commu.write_int(2,11)
    # commu.write_bool(1,1,True)
    # commu.write_bool(1,2,True)
    # commu.write_real(24,-1.231)
    # commu.get_int(2)
    # commu.get_bit(647)

    # commu.read_usint_data(12,1)





