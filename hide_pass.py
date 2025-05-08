def hide(password):
    pwd= list(password)    
    for i in range(len(pwd)):
        if pwd[i].upper() == pwd[i]:
            pwd[i] = '##'
    return pwd           
p = "NIIghbdtn"
print(hide(p))            