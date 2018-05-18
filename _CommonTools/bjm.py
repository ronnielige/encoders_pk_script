__author__ = 'lr9371'
'''
Implementation of Bjontegaard metric.
Algorithm from VCEG-AE07 and JCTVC-L1100.
'''
from math import *
from copy import *
BD_PSNR = 0
BD_RATE = 1

def get_coeff_polynome_int(x, y):
    '''
    :param x: x array
    :param y: y array
    :return:  return an array containing Polynomial Coefficients
    '''
    E = []
    F = []
    G = []
    H = []
    for i in range(0, 4):
        E.append(x[i])
        F.append(x[i] * x[i])
        G.append(x[i] * x[i] * x[i])
        H.append(y[i])

    DET0 = E[1] * (F[2] * G[3] - F[3] * G[2]) - E[2] * (F[1] * G[3] - F[3] * G[1]) + E[3] * (F[1] * G[2] - F[2] * G[1])
    DET1 = -E[0] * (F[2] * G[3] - F[3] * G[2]) + E[2] * (F[0] * G[3] - F[3] * G[0]) - E[3] * (F[0] * G[2] - F[2] * G[0])
    DET2 = E[0] * (F[1] * G[3] - F[3] * G[1]) - E[1] * (F[0] * G[3] - F[3] * G[0]) + E[3] * (F[0] * G[1] - F[1] * G[0])
    DET3 = -E[0] * (F[1] * G[2] - F[2] * G[1]) + E[1] * (F[0] * G[2] - F[2] * G[0]) - E[2] * (F[0] * G[1] - F[1] * G[0])
    DET = DET0 + DET1 + DET2 + DET3

    D0 = H[0] * DET0 + H[1] * DET1 + H[2] * DET2 + H[3] * DET3

    D1 = H[1] * (F[2] * G[3] - F[3] * G[2]) - H[2] * (F[1] * G[3] - F[3] * G[1]) + H[3] * (F[1] * G[2] - F[2] * G[1])
    D1 = D1 - H[0] * (F[2] * G[3] - F[3] * G[2]) + H[2] * (F[0] * G[3] - F[3] * G[0]) - H[3] * (F[0] * G[2] - F[2] * G[0])
    D1 = D1 + H[0] * (F[1] * G[3] - F[3] * G[1]) - H[1] * (F[0] * G[3] - F[3] * G[0]) + H[3] * (F[0] * G[1] - F[1] * G[0])
    D1 = D1 - H[0] * (F[1] * G[2] - F[2] * G[1]) + H[1] * (F[0] * G[2] - F[2] * G[0]) - H[2] * (F[0] * G[1] - F[1] * G[0])

    D2 = E[1] * (H[2] * G[3] - H[3] * G[2]) - E[2] * (H[1] * G[3] - H[3] * G[1]) + E[3] * (H[1] * G[2] - H[2] * G[1])
    D2 = D2 - E[0] * (H[2] * G[3] - H[3] * G[2]) + E[2] * (H[0] * G[3] - H[3] * G[0]) - E[3] * (H[0] * G[2] - H[2] * G[0])
    D2 = D2 + E[0] * (H[1] * G[3] - H[3] * G[1]) - E[1] * (H[0] * G[3] - H[3] * G[0]) + E[3] * (H[0] * G[1] - H[1] * G[0])
    D2 = D2 - E[0] * (H[1] * G[2] - H[2] * G[1]) + E[1] * (H[0] * G[2] - H[2] * G[0]) - E[2] * (H[0] * G[1] - H[1] * G[0])

    D3 = E[1] * (F[2] * H[3] - F[3] * H[2]) - E[2] * (F[1] * H[3] - F[3] * H[1]) + E[3] * (F[1] * H[2] - F[2] * H[1])
    D3 = D3 - E[0] * (F[2] * H[3] - F[3] * H[2]) + E[2] * (F[0] * H[3] - F[3] * H[0]) - E[3] * (F[0] * H[2] - F[2] * H[0])
    D3 = D3 + E[0] * (F[1] * H[3] - F[3] * H[1]) - E[1] * (F[0] * H[3] - F[3] * H[0]) + E[3] * (F[0] * H[1] - F[1] * H[0])
    D3 = D3 - E[0] * (F[1] * H[2] - F[2] * H[1]) + E[1] * (F[0] * H[2] - F[2] * H[0]) - E[2] * (F[0] * H[1] - F[1] * H[0])

    P=[]
    P.append(D0 / DET)
    P.append(D1 / DET)
    P.append(D2 / DET)
    P.append(D3 / DET)
    return P


def bjm(ref_rate_a=[], ref_psnr_a=[], rate_a=[], psnr_a=[], bjm_mode = BD_RATE):
    '''
    :param ref_rate_a: reference rate array, must have 4 items
    :param ref_psnr_a: reference psnr array, must have 4 items
    :param rate_a:     rate array
    :param psnr_a:     psnr array
    :param bjm_mode:   mode: 0,calculate bd_psnr; 1, calculate bd_rate
    :return: bd_rate or bd_psnr
    '''
    if len(ref_rate_a) != 4 or len(ref_psnr_a) != 4 or len(rate_a) != 4 or len(psnr_a) != 4:
        print "Param Error: length of rate and psnr array must be 4!!!"
        return 0.0

    x0 = []
    y0 = []
    x1 = []
    y1 = []

    if bjm_mode == BD_PSNR:
        for r in ref_rate_a:
            x0.append(log10(r))
        for r in rate_a:
            x1.append(log10(r))
        for p in ref_psnr_a:
            if p < 0 or p > 99:
                print "Param Error: psnr out of range[0, 99]!!!"
                return 0.0
            y0.append(p)
        for p in psnr_a:
            y1.append(p)
            if p < 0 or p > 99:
                print "Param Error: psnr out of range[0, 99]!!!"
                return 0.0
    elif bjm_mode == BD_RATE:
        for r in ref_rate_a:
            y0.append(log10(r))
        for r in rate_a:
            y1.append(log10(r))
        for p in ref_psnr_a:
            x0.append(p)
            if p < 0 or p > 99:
                print "Param Error: psnr out of range[0, 99]!!!"
                return 0.0
        for p in psnr_a:
            x1.append(p)
            if p < 0 or p > 99:
                print "Param Error: psnr out of range[0, 99]!!!"
                return 0.0
    else:
        print "Param Error: bjm_mode out of range[0, 1]!"
        return 0.0

    min_x0 = min(x0)
    min_x1 = min(x1)
    xl = max(min_x0, min_x1)
    max_x0 = max(x0)
    max_x1 = max(x1)
    xh = min(max_x0, max_x1)

    P = get_coeff_polynome_int(x0, y0)
    sum0 = P[0] * (xh - xl) + P[1] * (xh * xh - xl *xl) / 2 + P[2] * (xh * xh *xh -xl * xl * xl) / 3 + P[3] * (xh * xh * xh * xh - xl * xl * xl *xl) / 4
    P = get_coeff_polynome_int(x1, y1)
    sum1 = P[0] * (xh - xl) + P[1] * (xh * xh - xl *xl) / 2 + P[2] * (xh * xh *xh -xl * xl * xl) / 3 + P[3] * (xh * xh * xh * xh - xl * xl * xl *xl) / 4

    diff = (sum1 - sum0) / (xh - xl)
    if bjm_mode == BD_RATE:
        diff = (pow(10, diff) - 1)

    return diff


def pchipend(h1, h2, del1, del2):
    d = ((2 * h1 + h2) * del1 - h1 * del2) / (h1 + h2)
    if d * del1 < 0:
        d = 0
    elif del1 * del2 < 0 and abs(d) > abs(3 * del1):
        d = 3 * del1
    return d

def bdrint(c_rate=[], c_dist=[], low=0, high=0):
    rate = copy(c_rate)
    dist = copy(c_dist)
    rate.sort(reverse=False)
    dist.sort(reverse=False)
    log_rate = []
    for i in range(0, 4):
        log_rate.append(log10(rate[i]))

    H = []
    delta = []
    for i in range(0, 3):
        H.append(dist[i + 1] - dist[i])
        delta.append((log_rate[i + 1] - log_rate[i]) / H[i])

    d = []
    d.append(pchipend(H[0], H[1], delta[0], delta[1]))
    for i in range(1, 3):
        d.append((3 * H[i - 1] + 3 * H[i]) / ((2 * H[i] + H[i - 1]) / delta[i - 1] + (H[i] + 2 * H[i - 1]) / delta[i]))
    d.append(pchipend(H[2], H[1], delta[2], delta[1]))

    c = []
    b = []
    for i in range(0, 3):
        c.append((3 * delta[i] - 2 * d[i] - d[i + 1]) / H[i])
        b.append((d[i] - 2 * delta[i] + d[i + 1]) / (H[i] * H[i]))

    result = 0
    for i in range(0, 3):
        s0 = dist[i]
        s1 = dist[i + 1]
        s0 = min(high, max(s0, low))
        s1 = min(high, max(s1, low))
        s0 = s0 - dist[i]
        s1 = s1 - dist[i]
        if s1 > s0:
            result = result + (s1 - s0) * log_rate[i]
            result = result + (s1 * s1 - s0 * s0) * d[i] / 2
            result = result + (s1 * s1 * s1 - s0 * s0 * s0) * c[i] / 3
            result = result + (s1 * s1 * s1 * s1 - s0 * s0 * s0 * s0) * b[i] / 4

    return result


def bdrate(ref_rate_a=[], ref_psnr_a=[], rate_a=[], psnr_a=[]):
    minPSNR = max(min(ref_psnr_a), min(psnr_a))
    maxPSNR = min(max(ref_psnr_a), max(psnr_a))

    vA = bdrint(ref_rate_a, ref_psnr_a, minPSNR, maxPSNR)
    vB = bdrint(rate_a,     psnr_a,     minPSNR, maxPSNR)

    avg = (vB - vA) / (maxPSNR - minPSNR)
    bdrate = pow(10, avg) - 1
    return bdrate


if __name__ == "__main__":
    ref_rate = [2077.71, 2065.17, 1665.06, 1634.52 ]
    ref_psnr = [44.85, 43.03, 41.08, 39.18 ]
    rate =     [2336.76, 2190.63, 1839.24, 1495.20 ]
    psnr =     [44.80, 43.02, 41.05, 39.20]

    print r"bdrate1 = %5.3f" %(100 * bjm   (ref_rate, ref_psnr, rate, psnr, BD_RATE)) + "%"
    print r"bdrate2 = %5.3f" %(100 * bdrate(ref_rate, ref_psnr, rate, psnr)) + "%"
    print r"%5.3f dB"%bjm(ref_rate, ref_psnr, rate, psnr, BD_PSNR)