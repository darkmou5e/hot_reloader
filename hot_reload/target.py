from hot_reload.sub.sub_hello import hello_from_sub_hello

def hello_from_target():
    return hello_from_sub_hello() + "hhhh"
