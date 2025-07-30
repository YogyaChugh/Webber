import subprocess, sys, asyncio, threading, time

# Subprocess A: Sends a success bit
proc_a = subprocess.Popen(
    ['python', '-c', 'import sys,time; time.sleep(2); sys.stdout.write("12"); sys.stdout.flush(); time.sleep(2); sys.stdout.write("23")'],
    stdout=subprocess.PIPE
)

# Subprocess B: Receives the bit and prints it
# proc_b = subprocess.Popen(
#     ['python', '-c', 'import sys; data = sys.stdin.read(); print("Subprocess B got:", data)'],
#     stdin=proc_a.stdout
# )
toto = None
def dothat():
    global toto
    toto = proc_a.stdout.read1()

print('gg')
man = threading.Thread(target=dothat)
man.start()
print('maggi')
pasta = True
while pasta:
    print('hi')
    time.sleep(5)
    if toto:
        print(toto)
        man.join()
        man = threading.Thread(target=dothat)
        man.start()