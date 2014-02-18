#__author__ = 'seyren'
#coding=utf-8


class Operation(object):
    #抽象化所有计算器运算
    def __init__(self):
        #两个输入参数
        self.numa = 0
        self.numb = 0

    def setnumba(self, value):
        self.numa = value

    def setnumbb(self, value):
        self.numb = value

    def getresult(self):
        pass


class OperationAdd(Operation):
    #+的具体实现
    def getresult(self):
        #重写父类的getresult方法
        return self.numa + self.numb


class OperationSub(Operation):
    #-的具体实现
    def getresult(self):
        return self.numa - self.numb


class OperFactory(object):
    #工厂类用来创建合适对橡
    def __init__(self):
        #用list来储存创建+ - 类
        self.opers = {
            "+": OperationAdd(),
            "-": OperationSub()
        }

    def getopers(self, oper):
        return self.opers[oper]

    def createropers(self, oper):
        me = self.getopers(oper)
        return me


#
if __name__ == "__main__":
    factory = OperFactory()
    oper = factory.createropers("+")
    oper.setnumba(10)
    oper.setnumbb(20)
    print oper.getresult()





