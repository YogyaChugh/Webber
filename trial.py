import traceback
import sys

def main():
    a = "Hello brother"
    try:
      b = a.maggi
    except Exception as e:
      exc_type, exc_value, exc_tb = sys.exc_info()
      exc_type = None
      if exc_type and exc_value:
          tb = traceback.TracebackException(exc_type, exc_value, exc_tb)
          print("new")
          exception_string = ''.join(tb.format())
      else:
          exception_string = f"Error: {e.args[0]} \nExtra: Couldn't traceback"
      print(exception_string)

main()