from time import sleep

class   MyTest:
    def __init__(self):
        self.cnt = 0

class RecHolder:
    mylist = []
    def myrectest(self, mycnt):
        t = MyTest()
        t.cnt += 1
        print(t.cnt)
        cnt = 0
        mycnt += 1
        if mycnt >= 5:
            return mycnt
        self.mylist.append(self.myrectest(mycnt))
        cnt += 1
        print(cnt)

mycnt = 0
r = RecHolder()
r.myrectest(mycnt)

for c in r.mylist:
    print (c)