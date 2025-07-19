import time

def myFunc():
  yield "Hello"
  time.sleep(2)
  yield 51
  yield "Good Bye"
  
x = myFunc()
  
for z in x:
  print(z)
