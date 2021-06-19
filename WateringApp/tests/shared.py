class Shared:
    def __init__(self):
        print('Init shared')

    def do_stuff(self, from_mod):
        print('Do stuff from {0}. I am instance {1}'.format(from_mod, self))

shared = Shared()
