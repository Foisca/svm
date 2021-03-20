from DataType import *
import re
import math


# Add a Server type
# (Type, CPU, Memory, HW_Cost, Daily_Cost)
# (str, int, int, int, int)
def Add_Server_Type(cmd_str) -> Server:
    global Highest_Server_Type
    global Lowest_Server_Type
    global Highest_Price
    global Lowest_Price
    p = re.findall(r'[a-zA-Z0-9.]+', cmd_str)
    tmp_arr = np.array([int(p[1]), int(p[2])])
    ns = Server(Standard=tmp_arr)
    ns.Type = p[0]
    ns.HW_Cost = int(p[3])
    ns.Daily_Cost = int(p[4])
    if ns.HW_Cost > Highest_Price:
        # print(ns.Type, ns.HW_Cost)
        Highest_Price = ns.HW_Cost
        Highest_Server_Type = ns.Type

    if ns.HW_Cost < Lowest_Price:
        Lowest_Price = ns.HW_Cost
        Lowest_Server_Type = ns.Type
    return ns


# Add a Virtual_Machine type
# (Type, CPU, Memory, Deploy)
# (str, int, int, int)
def Add_Virtual_Machine_Type(cmd_str) -> Virtual_Machine:
    p = re.findall(r'[a-zA-Z0-9.]+', cmd_str)
    nvm = Virtual_Machine()
    nvm.Type = p[0]
    nvm.Standard = np.array([int(p[1]), int(p[2])])
    nvm.Deploy = int(p[3])
    return nvm


# Add Virtual_Machine
# (add, type, vm_id)
def Add_Virtual_Machine(vm_type, vm_id):
    global vmid_queue
    vmid_queue.append(vm_id)
    tmp = Types_VMs[vm_type]
    tmp.ID = vm_id
    Dict_VMs[vm_id] = tmp


def Decide(cmd_str):
    p = re.findall(r'[a-zA-Z0-9.]+', cmd_str)
    if len(p) == 3: # add(add, type, vm_id)
        Add_Virtual_Machine(p[1], int(p[2]))
    else: # del(del, vm_id)
        del Dict_VMs[p[1]]


def Potential_Load(): # return np.array([])
    global Dict_VMs
    total_A = np.array([0, 0])
    esti_max = np.array([0, 0])
    cache = [] # contains all requestion Standard singled node
    for vm_id in Dict_VMs:
        tmp_vm = Dict_VMs[vm_id]
        if tmp_vm.Deploy == 1: # double node
            total_A += (tmp_vm.Standard // 2)
        else: # single node
            cache.append(tmp_vm.Standard)
    list_cpu = []
    list_memory = []
    for arr in cache:
        list_cpu.append(arr[0])
        list_memory.append(arr[1])
    # the two lists are random, but picked the biggest sum
    list_cpu.sort(reverse=True)
    list_memory.sort(reverse=True)
    for i in range(math.ceil(len(list_cpu) / 2)):
        esti_max += np.array([list_cpu[i], list_memory[i]])
    Dict_VMs = {}
    return (total_A + esti_max)


def Determine_Type(load):
    global Highest_Server_Type
    global Lowest_Server_Type
    if load.all() < Types_Server[Lowest_Server_Type].Standard.all():
        return [Lowest_Server_Type]
    elif load.all() > Types_Server[Highest_Server_Type].Standard.all():
        load -= Types_Server[Highest_Server_Type].Standard
        return [Highest_Server_Type, Determine_Type(load)]
    else:
        dict_remains = {}
        for s in Types_Server:
            tmp = Types_Server[s]
            remain = tmp.Standard - load
            if remain.all() > 0:
                key = remain[0] + remain[1]
                if key in dict_remains:
                    if s.HW_Cost < dict_remains[key].HW_Cost:
                        dict_remains[key] = tmp.Type
                else:
                    dict_remains[key] = tmp.Type
        list = sorted(dict_remains.keys(), reverse=True)
        return [dict_remains[list[0]]]

    # half_load = Potential_Load()


# (purchase, Q) Q: types to purchase
# (server_type, quantity)
sid = 0


def Purchase_Server(server_type, quantity):
    global sid
    for _ in range(quantity):
        Dict_Servers[sid] = Types_Server[server_type]
        sid += 1


# (migration, W) W: quantity to migrate
# (vm_id, destination server_id, destination server_node)
def Migration_Server():
    print('(migration, 0)')


def fit(a, b):
    return (a > b).all()


cur_serid = 0


# Deploy VMs in the sequence of users' requestions
# (Server_ID) or (Server_ID, Server_node)
def Deploy_Virtual_Machine():
    global cur_serid
    global vmid_queue
    cs = Dict_Servers[cur_serid] #current server
    for id in vmid_queue:
        cvm = Dict_VMs[id] #current vm
        if Dict_VMs[id].Deploy == 1:
            while (True):
                a1 = cs.Remain_A
                a2 = cs.Remain_B
                b = cvm.Standard
                if fit(a1, b) and fit(a2, b):
                    print('(%d)' % cur_serid)
                    cs.VM.append(cvm.Type)
                    cs.Remain_A -= cvm.Standard // 2
                    cs.Remain_B -= cvm.Standard // 2
                    cs.On = True
                    break
                else:
                    print('add1')
                    cur_serid += 1
                    cs = Dict_Servers[cur_serid] #current server
        else:
            while (True):
                a1 = cs.Remain_A
                a2 = cs.Remain_B
                b = cvm.Standard
                if fit(a1, b):
                    print('(%d, A)' % cur_serid)
                    cs.VM.append(cvm.Type)
                    cs.Remain_A -= cvm.Standard
                    break
                elif fit(a2, b):
                    print('(%d, B)' % cur_serid)
                    cs.VM.append(cvm.Type)
                    cs.Remain_B -= cvm.Standard
                    break
                else:
                    print('add1')
                    cur_serid += 1
                    cs = Dict_Servers[cur_serid] #current server


def Days():
    global Highest_Server_Type
    global vmid_queue
    global Dict_VMs
    load = Potential_Load() * 2
    typelist = Determine_Type(load)
    hn = typelist.count(Highest_Server_Type)
    types = len(typelist) - hn
    print('(purchase, %d)' % len(typelist))
    print('(%s, %d)' % (typelist[0], hn))
    Purchase_Server(typelist[0], hn)
    if types > hn:
        for i in range(hn, types):
            print('(%s, %d)' % (typelist[i], 1))
            Purchase_Server(typelist[i], 1)
    Migration_Server()
    # deploy servers
    Deploy_Virtual_Machine()
    vmid_queue = []
    Dict_VMs = {}


def showinfo():
    print()
    print('##Types_Servers')
    for v in Types_Server:
        Types_Server[v].exp()

    print()
    print('##Types_VMs')
    for v in Types_VMs:
        Types_VMs[v].exp()

    print()
    print('##Dict_VMs')
    for v in Dict_VMs:
        Dict_VMs[v].exp()

    print('Potential_max_single_node_load:', Potential_Load())

    print()
    print('##Dict_Servers')
    for v in Dict_Servers:
        Dict_Servers[v].exp()
    print()

    print('Highest_Serer_Type:', Highest_Server_Type)
    Types_Server[Highest_Server_Type].exp()

    print('Lowest_Serer_Type:', Lowest_Server_Type)
    Types_Server[Lowest_Server_Type].exp()
