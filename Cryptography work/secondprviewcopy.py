
#main
key = input("Enter key: ").lower()
message = input("Enter message: ").lower()
cipher = input("Enter cipher: ").upper()

def encryptShift(k, m):
    result = ""
    for x in range(len(m)):
        shift = ord(k[(x%len(k))]) - ord('a')
        fixer = (ord(m[x]) + shift - ord('a')) % 26 + ord('a')
        result += chr(fixer)
    return result

def decryptShift(k, c):
    result = ""
    c = c.strip()
    for x in range(len(c)):
        shift = ord(c[x]) - ord('A')
        fixer = chr((shift - (ord(k[x % len(k)]) - ord('a')) + 26) % 26 + ord('a'))
        result += fixer
    return result

def cipherFreqFinder(c):
    freqs = int[26]
    c = c.strip()
    for x in range(len(c)):
        freqs[ord(c[x]) - ord('A')] += 1
    for a in freqs:
        a/len(c)
    return freqs

def indexOfCoincidence(freq):
    ioc = 0
    for i in freq:
        ioc += i^2
    return ioc

def bruteForceShift():
    for a in range(26):
        print(decryptShift((chr)(a + ord('a')), message) + "\n")

def multTable(n):
    for i in range(n):
        print((str)(i) + ":", end= " ")
        for j in range(n):
            print((i * j) % n, end= " ")
        print("\n", end= "")

def affineCipherEncrypt(m : str, a : int, b : int):
    a = ""
    for i in range(len(m)):
        a += (chr)(((((ord(m[i]) - ord('a')) * a) + b) % 26) + ord('A'))
    return a

def affineCipherDecrypt(c : str, a : int, b :int):
    a = ""
    for i in range(26):
        for j in range(len(c)):
            a += (chr)((((((ord(c[j]) - ord('A')) - a + 26) % 26) * i) % 26) + ord('a'))
        a += ", "
    return a



#print(indexOfCoincidence(cipherFreqFinder(cipher)))



multTable(23)