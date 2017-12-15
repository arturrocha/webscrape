def set_max_min():
    set_max = input("Set your max price in euros or leave blank for no MAX (example: >800): >")
    set_min = input("Set your min price in euros or leave blank for no MIN (example: >200): >")
    if set_max == "":
        max = 9999999
    else:
        max = int(set_max)

    if set_min == "":
        min = 0
    else:
        min = int(set_min)
    return (max, min)

def tst_print():
    return "thnao untdhtoadeuntedoauthd"