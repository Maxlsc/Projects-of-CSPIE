from const import OPCODE
class script:
    def __init__(self) -> None:
        pass
    
    def script_Parser(self, data):
        n = len(data)
        step = 2
        offset = 0
        script = []
        while offset < n:
            opcode = int(data[offset:offset+step],16)
            offset = offset + step
            if opcode in OPCODE:
                script.append(OPCODE[opcode])
            else:
                datalen = opcode
                script.append(data[offset:offset+step*datalen])
                offset = offset + step*datalen
        print(script)

data = '00147dbd2d6e1f0d941d837aa91b0b70f9dab394d2a8'
data = '76A91489ABCDEFABBAABBAABBAABBAABBAABBAABBAABBA88AC'
tmp = script()
tmp.script_Parser(data)