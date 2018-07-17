class Test(object):
    @staticmethod
    def a():
        print "a ..."

    @staticmethod
    def b():
        print "b ..."


class CallFunc():
    def __init__(self):
        self.list = []
        self.add()

    def add(self):
        self.list.append(Test.a)
        self.list.append(Test.b)

    def run(self):
        for f in self.list: f()



CallFunc().run()

class PipPackage():
    name = ''
    version = 'xxxx'
    package_name = ''

p = PipPackage
p.package_name = 'ga'
print p.package_name
print p.version

t = PipPackage
print t.package_name
