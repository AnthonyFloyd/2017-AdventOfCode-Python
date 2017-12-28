counter = 0

b = 106700
c = 123700
step = 17

for target in range(b, c + step, step):
   flag = False
   d = 2
   while d != target:
      e = target // d
      if e < d:
         break
      if target % d == 0:
         flag = True
         #print("d: {0:d} e: {1:d} b: {2:d}".format(d, e, target))
         break
      d += 1
   if flag:
      counter += 1
   else:
      print("Prime: {0:d}".format(target))

print("{0:d}".format(counter))

#905 is correct
