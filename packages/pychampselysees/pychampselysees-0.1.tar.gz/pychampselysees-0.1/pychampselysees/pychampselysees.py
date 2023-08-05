# just a random function
def printIfTrue(m, prefix = ''):
  import sys
  if m:
    print(prefix + m)
    sys.stdout.flush()
  return m

if __name__ == '__main__':
  printIfTrue(False, 'tool test:')
  printIfTrue('True', 'tool test:')
