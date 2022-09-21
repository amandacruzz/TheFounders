#from private import Private
from access import Private, Public           # change to test different modules
from formats import money


@Private('name', 'pay')                      # onDecorator, bound to privates
class Person:                                # onInstance, bound to aClass
    def __init__(self, name, job, pay):      # Person = onDecorator(Person)
        self.name = name
        self.job  = job                      # access work here in class
        self.pay  = pay                      # onInstance catches outside access
    def giveRaise(self):
        self.pay *= 1.10
    def getName(self): return self.name          # accessors can be used
    def getPay(self):  return money(self.pay)    # but their attrs cannot
    def setPay(self, new): self.pay = new


"""
@Public('job', 'giveRaise', 'getName', 'getPay', 'setPay')
class Person:
    def __init__(self, name, job, pay):      # Person = onDecorator(Person)
        self.name = name
        self.job  = job                      # access work here in class
        self.pay  = pay                      # onInstance catches outside access
    def giveRaise(self):
        self.pay *= 1.10
    def getName(self): return self.name              # accessors can be used
    def getPay(self):  return '$%.2f' % self.pay     # but their attrs cannot
    def setPay(self, new): self.pay = new
"""


if __name__ == '__main__':

    # onInstance embeds a Person:
    # outside class, bob is really an onInstance
    # but within Person class, self is still a Person

    bob = Person('Bob', 'dev', pay=100000)       # bob = onInstance(args)
    bob.giveRaise()                              # bob is a onInstance
    print bob.getName()                          # onInstance embeds a Person
    print bob.job
    print bob.getPay()
    print bob.job

    ##print bob.pay         # fails!
    print bob._onInstance__wrapped.pay   # works, if you insist!*******

    bob.job = 'Mgr'
    print bob.job
    bob.setPay(9999)
    print bob.getPay()
    ##bob.pay = 99         # fails!
    ##bob.name = 'Loretta' # fails!

    print
    sue = Person('Sue', 'mgr', 50000)
    print sue.getName(), sue.job, sue.getPay()
    print bob.getName(), bob.job, bob.getPay()
    sue.giveRaise(); bob.giveRaise()
    for person in (sue, bob):
        print person.getName(), person.job, person.getPay()
