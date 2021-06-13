class Version:
    def __init__(self, vers):
        self.version: str = vers
        self.iter_stg_1: str = vers[:1]
        self.iter_stg_2: str = vers[2:4]
        self.iter_stg_3: str = vers[5]

    def increment(self, iteration: str = "iter_stg_1", iter_range: int = 1):
        if iteration.lower() == 'iter_stg_1':
            self.iter_stg_1 = iter_range + int(self.iter_stg_1)
            self.version = str(self.iter_stg_1) + self.version[1:]
        elif iteration.lower() == 'iter_stg_2':
            self.iter_stg_2 = iter_range + int(self.iter_stg_2)
            if self.iter_stg_2 > 99 and iter_range >= 1:
                self.increment('iter_stg_1', 1)
                self.iter_stg_2 = '00'
                self.version = str(self.iter_stg_1) + "." + str(self.iter_stg_2) + "." + str(self.iter_stg_3)
            else:
                self.version = str(self.iter_stg_1) + "." + str(self.iter_stg_2) + "." + str(self.iter_stg_3)
        elif iteration.lower() == 'iter_stg_3':
            self.iter_stg_3 = iter_range + int(self.iter_stg_3)
            if self.iter_stg_3 > 9 and iter_range >= 1:
                self.increment("iter_stg_2", 1)
                self.iter_stg_3 = '0'
                self.version = self.version[:5] + str(self.iter_stg_3)
            else:
                self.version = self.version[:5] + str(self.iter_stg_3)


"""Used in C:/Users/Shlok/J.A.R.V.I.SV2021/Classified_J.A.R.V.I.S.py"""
ver = Version("2.70.0")
version = ver.version
