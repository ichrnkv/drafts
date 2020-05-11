from time import sleep

for i in range(10):
    print('current iteration is %s' %i, end='\r')
    sleep(.2)
