import json
from hashlib import sha256
import binascii
class tx:
    def __init__(self) -> None:
        pass

    def str2int(self,s):
        n = len(s)
        res = 0
        for i in range(n,0,-2):
            res = (res<<8) + int(s[i-2:i],16)
        return res
    
    def getSize(self,data,offset):
        size = data[offset:offset+2]
        if size == 'fd':
            len = 4; buf = 2
        elif size == 'fe':
            len = 8; buf = 2
        elif size == 'ff':
            len = 16; buf = 2
        else:
            len = 2; buf = 0
        return self.str2int(data[offset+buf:offset+buf+len]),offset+buf+len
    def little_endian(self, data):
        n = len(data)
        res = ''
        for i in range(n,0,-2):
            res = res + data[i-2:i]
        return res

    def tx_in_Parser(self,data,offset):
        tx_in = {}
        step = 2

        previous_output_hash = self.little_endian(data[offset:offset+32*step])
        offset += 32*step
        tx_in["prev_hash"] = previous_output_hash
        previous_output_index = self.str2int(data[offset:offset+4*step])
        offset += 4*step
        tx_in["output_index"] = previous_output_index

        script_length, offset = self.getSize(data, offset)
        signature_script = data[offset:offset+script_length*step]
        offset += script_length*step
        if script_length != 0:
            tx_in["script"] = signature_script

        sequence = self.str2int(data[offset:offset+4*step])
        offset+= 4*step
        tx_in["sequence"] = sequence

        return tx_in,offset

    def tx_out_Parser(self,data,offset):
        tx_out = {}
        step = 2

        value = self.str2int(data[offset:offset+8*step])
        offset += 8*step
        tx_out["value"] = value

        pk_script_length, offset = self.getSize(data, offset)
        pk_script= data[offset:offset+pk_script_length*step]
        offset += pk_script_length*step
        if pk_script_length*step != 0:
            tx_out["script"] = pk_script

        return tx_out,offset
    
    def tx_witness_Parser(self,data,offset):
        tx_witness = []
        step = 2
        txid0 = data[0:8]+data[12:offset]

        tx_witness_count, offset = self.getSize(data, offset)
        for _ in range(tx_witness_count):
            witness_len, offset = self.getSize(data, offset)
            tx_witness.append(data[offset:offset+witness_len*step])
            offset = offset+witness_len*step
        txid = txid0 + data[offset:]

        return txid, tx_witness, offset

    def tx_Parser(self,data):
        tx = {}

        offset = 0
        step = 2

        version = self.str2int(data[offset:offset+4*step])
        tx["ver"] = hex(version)[2:]
        offset += step*4

        if data[offset:offset+2*step]=='0001':
            flag = 1
            offset += step*2
            tx["flag"] = hex(flag)[2:]

        tx_in_count, offset = self.getSize(data,offset)
        tx["vin_sz"] = tx_in_count
        tx_in = []
        for _ in range(tx_in_count):
            tmp,offset = self.tx_in_Parser(data,offset)
            tx_in.append(tmp)
        tx["input"] = tx_in

        tx_out_count, offset = self.getSize(data,offset)
        tx["vout_sz"] = tx_out_count
        tx_out = []
        for _ in range(tx_out_count):
            tmp,offset = self.tx_out_Parser(data,offset)
            tx_out.append(tmp)
        tx["out"] = tx_out

        if "flag" in tx:
            txid,tx_witness,offset = self.tx_witness_Parser(data, offset)
            tx["input"][0]["witness"] = tx_witness
        else:    
            txid = data
        
        lock_time = self.str2int(data[offset:offset+4*step])
        tx["lock_time"] = lock_time
        offset += step*4

        hash = sha256(sha256(bytes.fromhex(txid)).digest()).digest()
        hash = binascii.hexlify(hash[::-1]).decode()
        tx["hash"] = hash

        tx_json = json.dumps(tx,indent=2)
        print(tx_json)

        


tmp = tx()
data = '02000000000101f53249f1d1890738d602a8c946afb2607ed7c785f9b69f8f374f995bcc747c7e0000000000feffffff0265db0f0000000000160014c0d335aedf1ca12077fa8145bf443fd983177b4ae8030000000000001600147dbd2d6e1f0d941d837aa91b0b70f9dab394d2a80247304402204f80c2c6d848374bbc5d385a9005910d02ec9f86c396fd9b932291a6c138789f02206ccacba092506210fad7791a0b0d814da8e6ca2153aae8e7b43b9707b04386d20121035e0b29ff08002919afde207d4fdccc4d9a29e24a9504953625f1c3fdfc33c64d00432500'
data = "02000000017068681de49f874b5f9b0ecf4b65137acedf3e18b1332471a64ace1d12bc78a1000000006a473044022038575d0d58b17398e20ce98e8de0ac4a2bb6a595fe73a817e8775d5a6c58716002204e3295b967ef26bc5495d4001c713b8273f5956454d0167670b7ed14ddf71bfe012103bc7ec78e3d829980100d7309dde86eeae21c7d26ce77799d4e1cb63aa1ddadd0fdffffff02072f971400000000160014089366df20a7597915600aa2ab8e6edbb7f4147c28921000000000001600147dbd2d6e1f0d941d837aa91b0b70f9dab394d2a8ff422500"
tmp.tx_Parser(data)
print()