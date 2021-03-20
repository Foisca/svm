from Utils import *


def main():

    N = int(input()) # N servers to add
    for _ in range(N):
        cmd_str = input()
        # (Type, CPU, Memory, HW_Cost, Daily_Cost)
        tmp = Add_Server_Type(cmd_str)
        Types_Server[tmp.Type] = tmp

    M = int(input()) # M VMs to add
    for _ in range(M):
        cmd_str = input()
        # (Type, CPU, Memory, Deploy)
        tmp = Add_Virtual_Machine_Type(cmd_str)
        Types_VMs[tmp.Type] = tmp

    T = int(input()) # T days to receive user requestions
    for _ in range(T):
        # Daily input
        R = int(input()) # R requestions a day
        for _ in range(R):
            cmd_str = input()
            Decide(cmd_str)
        # print(vmid_queue)
        Days() # Daily output

    print('----------End Input----------')
    showinfo()

    # to read standard input
    # process
    # to write standard output
    # sys.stdout.flush()

    # pass


if __name__ == "__main__":
    main()
