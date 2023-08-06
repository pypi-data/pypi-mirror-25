import numpy as np

class Number(object):
  def __init__(self, intNum):
    self.intNum = intNum

  def float32(self, num):
    return np.float32(num) + self.intNum

  def add(self, a, b):
    return self.float32(a) + self.float32(b)

if __name__ == '__main__':
    number = Number(1)
    print(number.float32(2))