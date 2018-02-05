import re

def clear_long_text(var):
    var=''.join(var).strip()
    var=re.split('\s{2,}',var)
    var=''.join(var)
    return var

def find_fee(var):
    fee=re.findall('£\d+,\d+',var)
    fee='-'.join(fee).replace(',','').replace('£','')
    fee=fee.split('-')
    try:
        fee=list(map(int,fee))
        fee=max(fee)
    except:
        return fee
    return fee

def find_fee_s(var):
    var=''.join(var)
    fee=re.findall('£\d+,?\d+',var)
    fee='-'.join(fee).replace(',','').replace('£','')
    fee=fee.split('-')
    try:
        fee=list(map(int,fee))
        fee=max(fee)
    except:
        return fee
    return fee
def find_title(var,longvar):
    try:
        return longvar[longvar.index(var):]
    except:
        return ''

def index_1(var,text,num):
    try:
        cout=text.index(var)+num
        cout=text[cout]
        return cout
    except:
        return ''

def get_index(title,var):
    try:
        index=title.index(var)
        return index
    except:
        index=-1
        return index

