# encoding=windows-1252

"""
Disclaimer : y'a pas tout qui marche des fois ça bug
gentil créateur : Nephty :)
"""

from math import fabs


hexToBinDct = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}


def hexToBin(s):
    line1 = ""
    line2 = ""
    for char in s:
        line1 += "  " + char + "   "
        line2 += hexToBinDct[char] + "  "
    print(line1)
    print(line2)
    return "".join(hexToBinDct[char] for char in s)


def binToHex(s):
    line1 = ""
    couples = []
    line2 = ""
    oldpos = 0
    for cnt in range(len(s)):
        if cnt % 4 == 0 and cnt != 0:
            line1 += s[oldpos:cnt] + "  "
            couples.append(s[oldpos:cnt])
            oldpos = cnt
        cnt += 1
    line1 += s[oldpos:]
    couples.append(s[oldpos:])
    for i in range(4 - len(couples[-1])):
        couples[-1] = "0" + couples[-1]

    dct = dict(zip(hexToBinDct.values(), hexToBinDct.keys()))
    for char in couples:
        line2 += "  " + dct[char] + "   "
    line3 = ""
    for i in couples:
        line3 += i + "  "
    print(line3)
    print(line2)
    return "".join(dct[char] for char in couples)


def binToDec(s):
    return int(s, 2)


def binAddNat(x, y):
    print(" " * (len(y) - len(x)) + x)
    print(" " * (len(x) - len(y)) + y)
    ln = len(x) if len(x) > len(y) else len(y)
    print("-" * ln)
    # res = int(x + y, 2)


def LTZtoBinary(x, M):
    w = ""
    bits = 0
    while x > 0 and bits < M:
        print(f"{x} > 0 et le nombre de bits < {M} (nombre max de bits demandés)")
        print(f"--> on multiplie {x} par 2, il devient {x * 2}")
        x *= 2
        bits += 1
        if int(x) > 0:
            print(f"{x} > 0")
            print(f"--> on soustrait 1 à {x} et on ajoute '1' au mot")
            x -= 1
            w += "1"
        else:
            print(f"{x} > 0")
            print(f"--> on ajoute '0' au mot")
            w += "0"
        print("[---------]")
    print(f"{x} <= 0 ou le nombre max de bits demandé < {M}")
    print(f"{x} <= 0 : {x <= 0}, nbr max de bits < {M} : {bits < M}")
    return w


def normalizeFloatingPoint(x):
    m = x
    e = 0
    while m < 1:
        m *= 2
        e -= 1
    while m >= 2:
        m /= 2
        e += 1
    print(f"{x} = {m} * 2^{e}")
    return f"{m}.{x}"


def valueFromNormalizedIEEE754(s, m, b):
    signBit = int(s[0])
    exp = binToDec(s[1:len(s) - m])
    mantisse = binToDec(s[len(s) - m:])
    x = ((-1) ** signBit) * (1 + (mantisse / (2 ** m))) * (2 ** (exp - b))
    return x


def valueFromDeNormalizedIEEE754(s, m, b):
    signBit = int(s[0])
    mantisse = binToDec(s[len(s) - m:])
    x = ((-1) ** signBit) * (mantisse / (2 ** m)) * (2 ** (1 - b))
    return x


def IEEE754toDec(s):
    if len(s) == 32:
        if "0" not in s[1:9]:
            if "1" not in s[len(s) - 23:]:
                return "-inf" if s[0] == "1" else "+inf"
            if s[len(s) - 23:] != "0" * 23:
                return "NaN"
        if s[1:9] == "00000000":
            return valueFromDeNormalizedIEEE754(s, 23, 127)
        return valueFromNormalizedIEEE754(s, 23, 127)
    elif len(s) == 64:
        if "0" not in s[1:12]:
            if "1" not in s[len(s) - 52:]:
                return "-inf" if s[0] == "1" else "+inf"
            if s[len(s) - 52:] != "0" * 52:
                return "NaN"
        if s[1:9] == "00000000":
            return valueFromDeNormalizedIEEE754(s, 52, 1023)
        return valueFromNormalizedIEEE754(s, 52, 1023)
    print("len is not 32 or 64")


def smallestNormalizedIEEE754(B):
    return 2 ** (1 - B)


def highestNormalizedIEEE754(M, E, B):
    highestM = 0
    for i in range(M):
        highestM += 2 ** i
    highestE = -1
    for i in range(E):
        highestE += 2 ** i
    return (1 + highestM / (2 ** M)) * (2 ** (highestE - B))


def smallestDenormalizedIEEE754(M, B):
    return (1 / (2 ** M)) * (2 ** (1 - B))


def highestDenormalizedIEEE754(M, B):
    highestM = 0
    for i in range(M):
        highestM += 2 ** i
    return (highestM / (2 ** M)) * (2 ** (1 - B))


def decToIEEE754(x, M, E, B):
    signBit = 1 if x < 0 else 0
    x = fabs(x)
    power = 0
    if x < 1:
        y = x
        while not 1 <= y < 2:
            y *= 2
            power -= 1
    else:
        y = x
        while not 1 <= y < 2:
            y /= 2
            power += 1
    e = power + B
    normalized = False
    denormalized = False
    if 0 < e < (2 ** E) - 1:
        normalized = True
    elif e <= 0:
        denormalized = True

    if normalized:
        m = int(round((x - 1) * (2 ** M), 0))
        bine = str(bin(e)[2:])
        binm = str(bin(m)[2:])
    elif denormalized:
        m = int(round(x * (2 ** (M - (1 - B))), 0))
        bine = "0" * E
        binm = str(bin(m)[2:])
    else:
        return "Le nombre n'est pas représentable"
    while len(bine) < E:
        bine = "0" + bine
    while len(binm) < M:
        binm = "0" + binm
    return f"{signBit} {bine} {binm} "


def bestBiaisFromELength(E):
    return 2 ** (E - 1) - 1


def getEpsilonMachine(M):
    return 2 ** (-(M + 1))


def roundToNearestEven(s, R, isPositive):
    keep = s[:len(s) - R]
    drop = s[len(s) - R:]
    if drop[0] == "0":
        # Round to zero
        return keep
    elif drop[0] == "1" and "1" in drop[1:]:
        return roundToInfinite(keep, isPositive)
    else:
        if keep[-1] == "0":
            # Round to zero
            return keep
        else:
            return roundToInfinite(keep, isPositive)


def roundToInfinite(keep, isPositive):
    if isPositive:
        return bin(binToDec(keep) + 1)[2:]
    else:
        return keep


def erreurVraie(x, dx):
    return x - dx


def erreurAbsolue(x, dx):
    return abs(erreurVraie(x, dx))


def erreurRelative(x, dx):
    return erreurAbsolue(x, dx) / abs(x)


def binAddFloats(s1, s2, E):
    exp1 = s1[0:E]
    exp2 = s2[0:E]
    mant1 = s1[E:]
    mant2 = s2[E:]

    if binToDec(exp1) > binToDec(exp2):
        mant1 = "1" + mant1
        mant2 = "1" + mant2
        diff = binToDec(exp1) - binToDec(exp2)
        expfinal = exp1
        for i in range(diff):
            mant2 = "0" + mant2
            mant1 = mant1 + "0"
        print(f"{expfinal} ({mant1[0]}) {mant1[1:]}")
        print(f"{expfinal} ({mant2[0]}) {mant2[1:]}")
        print(f"{'-' * len(expfinal)}----{'-' * len(mant1)}")
        somme = bin(int(binToDec(mant1)) + int(binToDec(mant2)))[2:]
        for i in range(E - len(somme)):
            somme = "0" + somme
        print(f"{expfinal} ({somme[0:len(somme) - E - 2]}) {somme[len(somme) - E - 2:]}")

    elif binToDec(exp1) < binToDec(exp2):
        mant1 = "1" + mant1
        mant2 = "1" + mant2
        diff = binToDec(exp2) - binToDec(exp1)
        expfinal = exp2
        for i in range(diff):
            mant1 = "0" + mant1
            mant2 = mant2 + "0"
        print(f"{expfinal} ({mant1[0]}) {mant1[1:]}")
        print(f"{expfinal} ({mant2[0]}) {mant1[1:]}")
        print(f"{'-' * len(expfinal)}----{'-' * len(mant1)}")
        somme = bin(int(binToDec(mant1)) + int(binToDec(mant2)))[2:]
        for i in range(E - len(somme)):
            somme = "0" + somme
        print(f"{expfinal} ({somme[0:len(somme) - E - 2]}) {somme[len(somme) - E - 2:]}")

    else:
        mant1 = "1" + mant1
        mant2 = "1" + mant2
        expfinal = exp1
        print(f"{expfinal} ({mant1[0]}) {mant1[1:]}")
        print(f"{expfinal} ({mant2[0]}) {mant1[1:]}")
        print(f"{'-' * len(expfinal)}----{'-' * len(mant1)}")
        somme = bin(int(binToDec(mant1)) + int(binToDec(mant2)))[2:]
        for i in range(E - len(somme)):
            somme = "0" + somme
        print(f"{expfinal} ({somme[0:len(somme) - E - 2]}) {somme[len(somme) - E - 2:]}")
    print("Attention, si le nombre entre () est plus long que 1 bit, il faut normaliser :"
          "\nIl faut décaler vers la droite (passer de (10) à (1) 0 par exemple) et augmenter de 1 l'exposant. Ne pas "
          "oublier de supprimer les bits qui \"dépassent\" à droite. "
          "\n\nSi l'exposant est de la forme 111...10, que la mantisse est de la forme 000...00 et que le nombre "
          "entre () est plus long que 1 bit, "
          "\nIl n'est pas représentable, car il faut alors décaler et incrémenter l'exposant,"
          "\nCe qui implique que l'exposant vaut 111....11 et la mantisse 0000...00 ce qui vaut l'infini (pas -inf "
          "car somme)"
          "\nSi le nombre entre () est long de 3 4 bits, il faut faire attention car en décalant il faudra"
          "faire un report à l'arrondi."
          "\n(Ouais jsp trop cque je fais mais ça marche 3x sur 4)")


# EXAMPLES :

# LTZtoBinary(0.441566, 64)
# hexToBin("F3AD")
# binToHex("0000111100001")
# binAddNat("110", "100101")
# normalizeFloatingPoint(17.33)
# print(IEEE754toDec("00000000000000000000000000000000"))
# print(IEEE754toDec("01000000000000000000000000000000"))
# print(IEEE754toDec("01000000011000000000000000000000"))
# print(IEEE754toDec("01111111101111111111111111111111"))
# print(IEEE754toDec("10000000010000000000000000000000") == (-2) ** (-127))
# print(smallestDenormalizedIEEE754(4, 4))
# print(highestDenormalizedIEEE754(8, 8))
# print(decToIEEE754(-0.015625, 4, 3, 4))
# print(roundToNearestEven("100100000", 6, True))
# print(binAddFloats("1010110000", "1000000110", 4))
