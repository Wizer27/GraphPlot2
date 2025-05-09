def hide(password):
    pwd= list(password)    
    for i in range(len(pwd)):
        if pwd[i].upper() == pwd[i]:
            pwd[i] = '##'
        else:
            pwd[i] = '&^'    
    res = ''
    for i in pwd:
        res += i
    return res              
p = "NIIghbdtn"
#print(hide(p)) 
def hide2(password):
    pwd = list(password)
    res = ''
    for i in sorted(pwd):
        res += i
    return res    
print(hide2(p))          