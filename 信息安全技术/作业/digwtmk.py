import binascii
import time
import cv2
import numpy as np
import matplotlib.pyplot as plt
import math


# 数字水印生成，返回扩频水印和噪声序列
def gen_digwtmk(ID, length):
    m = bin(ID)[2:]
    print("原始信息:", m)

    s = ""  # 原始信息扩频
    for i in range(len(m)):
        for _ in range((length // len(m)) + 1):
            s += m[i]
    s = s[:length]
    print(f"按片率 {length // len(m)} 扩展后:", s)

    p = ""  # 伪随机噪声序列
    for i in range(length):
        p += str(np.random.randint(0, 2))
    print("伪随机噪声序列:", p)

    w = ""  # 扩频水印
    for i in range(length):
        w += str(int(s[i]) ^ int(p[i]))
    print("扩频水印:", w, "\n")

    return w, p


# 数字水印嵌入，返回嵌入水印的图像
def emb_digwtmk(img, wtmk, length, alpha=5):
    img = img.astype(np.float)
    dct = cv2.dct(img)
    n, m = len(dct), len(dct[0])
    x = zhi(dct)
    for i in range(length):
        x[i + 1] += alpha * (-1 if wtmk[i] == '0' else 1)
    dct_wtmk = np.array(izhi(x, n, m))
    idct = cv2.idct(dct_wtmk)
    img_wtmk = idct.astype(np.uint8)
    return img_wtmk


# 块数字水印嵌入，返回嵌入水印的图像
def emb_digwtmk_blk(img, wtmk, length, alpha=1):
    img = img.astype(np.float)
    n, m = len(img), len(img[0])
    if n < 320 or m < 320:
        raise Exception("The Image is too small to embed block digital watermark")
    if length > 1600:
        raise Exception("The version is to embed digital watermark which length less than 1600")

    ctr = (n // 2, m // 2)
    left_upper = (ctr[0] - 20 * 8, ctr[1] - 20 * 8)
    count = 0
    for i in range(40):
        for j in range(40):
            blk_left_upper = (left_upper[0] + 8 * i, left_upper[1] + 8 * j)
            blk_img = img[blk_left_upper[0]:blk_left_upper[0] + 8, blk_left_upper[1]:blk_left_upper[1] + 8]
            blk_dct = cv2.dct(blk_img)
            blk_zhi = zhi(blk_dct)
            # 取第一个交流分量嵌入
            blk_zhi[11] += alpha * (-1 if wtmk[count] == '0' else 1)
            blk_izhi = np.array(izhi(blk_zhi, 8, 8))
            blk_idct = cv2.idct(blk_izhi)
            blk_wtmk = blk_idct.astype(np.uint8)
            img[blk_left_upper[0]:blk_left_upper[0] + 8, blk_left_upper[1]:blk_left_upper[1] + 8] = blk_wtmk

            count += 1
            if count == length:
                break
        if count == length:
            break
    return img.astype(np.uint8)


# 三通道数字水印嵌入，返回嵌入水印的图像（全图水印嵌入和分块水印嵌入）
def emb_digwtmk_3chn(img_3chn, wtmk, length, method="whole", alpha=5):
    bgr_wtmk = []
    for img in cv2.split(img_3chn):
        if method == "whole":
            img_wtmk = emb_digwtmk(img, wtmk, length, alpha=alpha)
        elif method == "block":
            img_wtmk = emb_digwtmk_blk(img, wtmk, length, alpha=alpha)
        else:
            raise Exception("Unknown Method")
        bgr_wtmk.append(img_wtmk)
    img_wtmk = cv2.merge(bgr_wtmk)
    return img_wtmk


# 数字水印检测
def detect_digwtmk(img, img_dtmk):
    # 原图
    ori_float = img.astype(np.float)
    ori_dct = cv2.dct(ori_float)
    ori_zhi = zhi(ori_dct)

    # 水印图
    res_float = img_dtmk.astype(np.float)
    res_dct = cv2.dct(res_float)
    res_zhi = zhi(res_dct)

    # ID 的复原
    w_recovered = ""
    for i in range(length):
        if res_zhi[i + 1] - ori_zhi[i + 1] > 0:
            w_recovered += '1'
        else:
            w_recovered += '0'
    return w_recovered


# 数字水印检测
def detect_digwtmk_blk(img, img_dtmk):
    # 原图
    ori_float = img.astype(np.float)
    res_float = img_dtmk.astype(np.float)

    n, m = len(img), len(img[0])
    ctr = (n // 2, m // 2)
    left_upper = (ctr[0] - 20 * 8, ctr[1] - 20 * 8)
    count = 0
    ori_l = []
    res_l = []
    for i in range(40):
        for j in range(40):
            blk_left_upper = (left_upper[0] + 8 * i, left_upper[1] + 8 * j)

            blk_img = ori_float[blk_left_upper[0]:blk_left_upper[0] + 8, blk_left_upper[1]:blk_left_upper[1] + 8]
            blk_dct = cv2.dct(blk_img)
            blk_zhi = zhi(blk_dct)
            ori_l.append(blk_zhi[11])

            blk_img = res_float[blk_left_upper[0]:blk_left_upper[0] + 8, blk_left_upper[1]:blk_left_upper[1] + 8]
            blk_dct = cv2.dct(blk_img)
            blk_zhi = zhi(blk_dct)
            res_l.append(blk_zhi[11])

            count += 1
            if count == length:
                break
        if count == length:
            break

    # ID 的复原
    w_recovered = ""
    for i in range(length):
        if res_l[i] - ori_l[i] > 0:
            w_recovered += '1'
        else:
            w_recovered += '0'
    return w_recovered


# 三通道数字水印检测
def detect_digwtmk_3chn(img_3chn, img_wtmk_3chn, method="whole"):
    img_3chn = cv2.split(img_3chn)
    img_wtmk_3chn = cv2.split(img_wtmk_3chn)
    w_recovered_3chn = []
    for i in range(3):
        img = img_3chn[i]
        img_wtmk = img_wtmk_3chn[i]
        if method == "whole":
            w_recovered = detect_digwtmk(img, img_wtmk)
        elif method == "block":
            w_recovered = detect_digwtmk_blk(img, img_wtmk)
        else:
            raise Exception("Unknown Method")
        w_recovered_3chn.append(w_recovered)
    return w_recovered_3chn


# 数字水印验证
def val_digwtmk(ID, w, p, threshold=0.95):
    length = len(p)
    m = bin(ID)[2:]
    # print("原始信息:", m)

    s = ""  # 原始信息扩频
    for i in range(len(m)):
        for _ in range((length // len(m)) + 1):
            s += m[i]
    s = s[:length]
    # print(f"按片率 {length // len(m)} 扩展后:", s)

    o = ""  # 破译的扩频信息
    for i in range(length):
        o += str(int(w[i]) ^ int(p[i]))
    print("破译的扩频信息:", o)

    a = 0
    for i in range(length):
        if s[i] == o[i]:
            a += 1
    a = a / length
    print("匹配率:", a, "\n")
    if a > threshold:
        return True
    else:
        return False


# 三通道数字水印验证
def val_digwtmk_3chn(ID, w_3chn, p, threshold=0.95):
    i = 1
    res = False
    for w in w_3chn:
        print("Channel", i)
        i += 1
        tmp = val_digwtmk(ID, w, p, threshold=threshold)
        if tmp:
            res = tmp
    return res


# 之字形展开
def zhi(mat):
    l = []
    n = len(mat)
    m = len(mat[0])
    d = 1
    for i in range(m + n - 1):
        if d == 1:
            for j in range(i + 1):
                if 0 <= j < m and 0 <= i - j < n:
                    l.append(mat[i - j][j])
        else:
            for j in range(i + 1):
                if 0 <= j < n and 0 <= i - j < m:
                    l.append(mat[j][i - j])
        d *= -1
    return l


# 之字形折叠
def izhi(li, n, m):
    d = 1
    idx = 0
    mat = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(m + n - 1):
        if d == 1:
            for j in range(i + 1):
                if 0 <= j < m and 0 <= i - j < n:
                    mat[i - j][j] = li[idx]
                    idx += 1
        else:
            for j in range(i + 1):
                if 0 <= j < n and 0 <= i - j < m:
                    mat[j][i - j] = li[idx]
                    idx += 1
        d *= -1
    return mat


# 水印攻击: 将图片缩小为原来的 1/n
def digwtmk_attack_v1(img_dtmk, n=3):
    h, w = img_dtmk.shape[:2]
    img_dtmk = cv2.resize(img_dtmk, (w // n, h // n))
    img_dtmk = cv2.resize(img_dtmk, (w, h))
    return img_dtmk


# 水印攻击: 遮挡图片的一部分
def digwtmk_attack_v2(img_dtmk, r=100, ctr=False):
    h, w = img_dtmk.shape[:2]
    if ctr:
        img_dtmk[h//2-r//2:h//2+r//2, w//2-r//2:w//2+r//2] = 0
    else:
        img_dtmk[-r:, -r:] = 0
    return img_dtmk


# 水印攻击: 椒盐噪声
def digwtmk_attack_v3(img_dtmk, prob=0.01):
    output = np.zeros(img_dtmk.shape, np.uint8)
    thres = 1 - prob
    for i in range(img_dtmk.shape[0]):
        for j in range(img_dtmk.shape[1]):
            rdn = np.random.random()
            if rdn < prob:
                output[i][j] = 0
            elif rdn > thres:
                output[i][j] = 255
            else:
                output[i][j] = img_dtmk[i][j]
    return output


# DCT 可视化
def dct_visual(image_path, name, length=1000):
    img = cv2.imread(image_path, 0)
    img = img[: img.shape[0] // 2 * 2, : img.shape[1] // 2 * 2].astype(np.float)
    dct = cv2.dct(img)
    x = zhi(dct)
    dct = np.log(abs(dct))

    plt.subplot(121)
    plt.plot(x[1:1 + length])
    plt.title(f'Linear DCT from 1 to {1 + length}'), plt.xticks([]), plt.yticks([])
    plt.subplot(122)
    plt.imshow(dct)
    plt.title('DCT Image (Log Version)'), plt.xticks([]), plt.yticks([])
    plt.savefig("./Image/" + name + "_dct.jpg")
    plt.show()


# 计算 PSNR
def psnr(img1, img2):
    mse = np.mean((img1 - img2) ** 2)
    if mse == 0:
        return 100
    return 20 * math.log10(255.0 / math.sqrt(mse))


if __name__ == "__main__":
    ID = 19335286
    length = 1000
    name = "cat"
    image_path = "./Test/" + name + ".jpg"
    alpha = 10
    print("ID:", ID)

    # DCT 可视化
    # dct_visual(image_path, name)

    # 数字水印生成
    start = time.time()
    wtmk, noise = gen_digwtmk(ID, length)
    end = time.time()
    print("数字水印生成用时: %.2f\n" % (end - start))

    img = cv2.imread(image_path, 1)
    img = img[: img.shape[0] // 2 * 2, : img.shape[1] // 2 * 2]

    # 数字水印嵌入
    start = time.time()
    img_dtmk = emb_digwtmk_3chn(img, wtmk, length, method="whole", alpha=5)
    end = time.time()
    print("数字水印嵌入用时（全局DCT）: %.2f" % (end - start))
    psnr_dtmk = psnr(img, img_dtmk)
    print("数字水印嵌入（全局DCT）后与原图的 PSNR:", psnr_dtmk, "\n")
    # cv2.imwrite("./Image/" + name + "_dtmk.jpg", img_dtmk)

    start = time.time()
    img_dtmk_blk = emb_digwtmk_3chn(img, wtmk, length, method="block", alpha=5)
    end = time.time()
    print("数字水印嵌入用时（分块DCT）: %.2f" % (end - start))
    psnr_dtmk_blk = psnr(img, img_dtmk_blk)
    print("数字水印嵌入（分块DCT）后与原图的 PSNR:", psnr_dtmk_blk, "\n")
    # cv2.imwrite("./Image/" + name + "_dtmk_blk.jpg", img_dtmk_blk)

    # 模拟水印攻击
    attack = "IpsNoise"
    if attack == "Fuzzy":
        print("模糊攻击\n")
        img_dtmk = digwtmk_attack_v1(img_dtmk)
        img_dtmk_blk = digwtmk_attack_v1(img_dtmk_blk)
        cv2.imwrite("./Image/" + name + "_dtmk_noise_v1.jpg", img_dtmk)
        cv2.imwrite("./Image/" + name + "_dtmk_blk_noise_v1.jpg", img_dtmk_blk)
    elif attack == "EdgeShade":
        print("边缘遮挡攻击\n")
        img_dtmk = digwtmk_attack_v2(img_dtmk)
        img_dtmk_blk = digwtmk_attack_v2(img_dtmk_blk)
        cv2.imwrite("./Image/" + name + "_dtmk_noise_v21.jpg", img_dtmk)
        cv2.imwrite("./Image/" + name + "_dtmk_blk_noise_v21.jpg", img_dtmk_blk)
    elif attack == "CtrShade":
        print("中心遮挡攻击\n")
        img_dtmk = digwtmk_attack_v2(img_dtmk, ctr=True)
        img_dtmk_blk = digwtmk_attack_v2(img_dtmk_blk, ctr=True)
        cv2.imwrite("./Image/" + name + "_dtmk_noise_v22.jpg", img_dtmk)
        cv2.imwrite("./Image/" + name + "_dtmk_blk_noise_v22.jpg", img_dtmk_blk)
    elif attack == "IpsNoise":
        print("椒盐噪声攻击\n")
        img_dtmk = digwtmk_attack_v3(img_dtmk)
        img_dtmk_blk = digwtmk_attack_v3(img_dtmk_blk)
        cv2.imwrite("./Image/" + name + "_dtmk_noise_v3.jpg", img_dtmk)
        cv2.imwrite("./Image/" + name + "_dtmk_blk_noise_v3.jpg", img_dtmk_blk)


    # 基于原图的检测
    w_recovered = detect_digwtmk_3chn(img, img_dtmk, method="whole")
    w_recovered_blk = detect_digwtmk_3chn(img, img_dtmk_blk, method="block")

    # 数字水印验证
    print("--全局DCT验证------------------------------------------------------------------------------------------------")
    val = val_digwtmk_3chn(ID, w_recovered, noise, threshold=0.65)
    print("是否检测到水印:", val)

    print("--分块DCT验证------------------------------------------------------------------------------------------------")
    val_blk = val_digwtmk_3chn(ID, w_recovered_blk, noise, threshold=0.65)
    print("是否检测到水印:", val_blk)

    plt.subplot(131)
    plt.imshow(img[..., ::-1].copy())
    plt.title('Original Image'), plt.xticks([]), plt.yticks([])
    plt.subplot(132)
    plt.imshow(img_dtmk[..., ::-1].copy())
    plt.title('Digital Watermark Image(Whole DCT)'), plt.xticks([]), plt.yticks([])
    plt.subplot(133)
    plt.imshow(img_dtmk_blk[..., ::-1].copy())
    plt.title('Digital Watermark Image(Block DCT)'), plt.xticks([]), plt.yticks([])
    plt.show()
