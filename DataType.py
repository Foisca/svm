import numpy as np
# key = Type
Types_Server = {}
Types_VMs = {}

Highest_Server_Type = None
Lowest_Server_Type = None
Highest_Price = 0
Lowest_Price = 100000

# key = ID
Dict_VMs = {}
Dict_Servers = {}

# vm queue
vmid_queue = []


class Server:
    ID = -1

    def __init__(self,
                 Type=None,
                 Standard=np.array([0, 0]),
                 HW_Cost=0,
                 Daily_Cost=0,
                 VM=[]):
        self.Type = Type
        self.Standard = Standard
        self.HW_Cost = HW_Cost
        self.Daily_Cost = Daily_Cost
        self.Remain_A = Standard // 2
        self.Remain_B = Standard // 2
        self.VM = VM
        self.On = False # On or not

    def exp(self):
        print(
            self.Type,
            self.Standard,
            self.HW_Cost,
            self.Daily_Cost,
            self.Remain_A,
            self.Remain_B,
            self.VM,
            self.ID,
        )


class Virtual_Machine:
    def __init__(self, Type=None, Standard=np.array([0, 0]), Deploy=0, ID=0):
        self.Type = Type
        self.Standard = Standard
        self.Deploy = Deploy
        self.ID = ID
        self.Host_ID = 0

    def exp(self):
        print(
            self.Type,
            self.Standard,
            self.Deploy,
            self.ID,
        )
