import rsa, subprocess, os

os.system("cd /home/elie/pythonprojects/Chiffrement")

subprocess.run("")
key = rsa.newkeys(1024)
prkey = key[1]
pukey = key[0]


def block(total, maxrange, ins=False):
    result = []
    for i in range(0, maxrange):
        result.append(
            total[i * int(len(total) / maxrange) : (i + 1) * int(len(total) / maxrange)]
        )
    result.append(total[maxrange * int(len(total) / maxrange) : len(total)])
    if ins:
        return result
    if len(result[-1]) > int(len(total) / maxrange):
        ii = result[-1]
        result.pop(-1)
        ii = block(ii, int(maxrange / 10), True)
        for i in ii:
            result.append(i)
    return result
