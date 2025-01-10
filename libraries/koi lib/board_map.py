import board

__version__ = "1.0.4"

PIN_DICT = {
    "P1": [board.P1,None],
    "P2": [board.P2,None],
    "P3": [board.P3,None],
    "P4": [board.P4,None],
    "NEOPIX": [board.NEOPIX,None],
    "RX":[board.RX,None],
    "TX":[board.TX,None],
    "RX1":[board.RX1,None],
    "TX1":[board.TX1,None],
    "BUZZ":[board.BUZZ,None],
    "M1AN":[board.M1AN,None],
    "M1AP":[board.M1AP,None],
    "M1BN":[board.M1BN,None],
    "M1BP":[board.M1BP,None]
}

def usePin(p):
    if PIN_DICT[p][1]:
        PIN_DICT[p][1].deinit()
    return PIN_DICT[p][0]

def saveObj(p, obj):
    PIN_DICT[p][1] = obj

def checkObj(p):
    return PIN_DICT[p][1]

    
