import sys

INF = sys.maxsize


def coin_change_modified(d, n):
  k = len(d) - 1
  M = [0]*(n+1)
  S = [0]*(n+1)

  for j in range(1, n+1):
    minimum = INF
    coin = 0
    for i in range(1, k+1):
      if(j >= d[i]):
        minimum = min(minimum, 1+M[j-d[i]])
        coin = i
    M[j] = minimum
    S[j] = coin

  l = n
  solutions = []
  while(l>0):
    solutions.append((d[S[l]]))
    l = l-d[S[l]]
  print(f"M: {M}")
  print(f"S: {S}")
  return solutions


d = [1, 2, 5, 25, 100]
n = 6
print(f"To change amount ${n} with {d}, the best we can do is: "
      f"{coin_change_modified(d, n)}")
