# -*- coding: utf-8 -*-
"""根据js修改生成"""
import random

from .compat import bytes


def random_byte():
    """返回一个 0 <= x < 256 的integer"""
    return random.randint(0, 0xff)


class TEA(object):
    def __init__(self, key):
        """128-bit key"""
        assert isinstance(key, bytes)
        assert len(key) == 16
        self.key = key

    MAX_UINT = 0xffffffff
    DELTA = 2654435769

    @staticmethod
    def put_uint_to_bytes(arr, from_index, uint):
        arr[from_index + 3] = uint >> 0 & 0xff
        arr[from_index + 2] = uint >> 8 & 0xff
        arr[from_index + 1] = uint >> 16 & 0xff
        arr[from_index + 0] = uint >> 24 & 0xff

    def encipher(self, v):
        o = int(v[0:4].hex(), 16)
        r = int(v[4:8].hex(), 16)
        p = int(self.key[0:4].hex(), 16)
        a = int(self.key[4:8].hex(), 16)
        s = int(self.key[8:12].hex(), 16)
        l = int(self.key[12:16].hex(), 16)
        c = 0
        for _ in range(16):
            c += self.DELTA
            c = self.MAX_UINT & c
            o += (r << 4) + p ^ r + c ^ (r >> 5) + a
            o = self.MAX_UINT & o
            r += (o << 4) + s ^ o + c ^ (o >> 5) + l
            r = self.MAX_UINT & r
        g = bytearray(8)
        self.put_uint_to_bytes(g, 0, o)
        self.put_uint_to_bytes(g, 4, r)
        return g

    def set_encrypt_result(self):
        for i in range(8):
            if self.is_first_xor:
                self.xor_a[i] ^= self.xor_b[i]
            else:
                self.xor_a[i] ^= self.result[self.result_pre_last_index + i]
        e = self.encipher(self.xor_a)
        for i in range(8):
            self.result[self.result_last_index + i] = e[i] ^ self.xor_b[i]
            self.xor_b[i] = self.xor_a[i]
        self.result_pre_last_index = self.result_last_index
        self.result_last_index += 8
        self.xor_index = 0
        self.is_first_xor = False

    def encrypt(self, v):
        self.xor_a = bytearray(8)
        self.xor_b = bytearray(8)
        self.result_last_index = self.result_pre_last_index = 0
        self.is_first_xor = True
        self.xor_index = 0

        v_len = len(v)
        self.xor_index = (v_len + 10) % 8
        if self.xor_index != 0:
            self.xor_index = 8 - self.xor_index
        # 结果的最终长度是 v_len + self.xor_index + 10
        self.result = bytearray(v_len + self.xor_index + 10)
        # 第0个元素 0xff & ( 0xf8 & random_byte() | self.xor_index)
        # 实际上就是把self.xor_index放到后三个bit里面
        self.xor_a[0] = 0xf8 & random_byte() | self.xor_index
        # 接下来的n位填充随机byte
        for i in range(1, self.xor_index+1):
            self.xor_a[i] = random_byte()
        self.xor_index += 1
        # 初始化tr
        for i in range(8):
            self.xor_b[i] = 0

        for _ in range(2):
            if self.xor_index < 8:
                self.xor_a[self.xor_index] = random_byte()
                self.xor_index += 1
            if self.xor_index == 8:
                self.set_encrypt_result()

        # 加密v
        for b in v:
            if self.xor_index < 8:
                self.xor_a[self.xor_index] = b
                self.xor_index += 1
            if self.xor_index == 8:
                self.set_encrypt_result()
        # 补齐后面的数
        for _ in range(7):
            if self.xor_index < 8:
                self.xor_a[self.xor_index] = 0
                self.xor_index += 1
            if self.xor_index == 8:
                self.set_encrypt_result()
        return self.result

    def decipher(self, v):
        o = int(v[0:4].hex(), 16)
        r = int(v[4:8].hex(), 16)
        p = int(self.key[0:4].hex(), 16)
        a = int(self.key[4:8].hex(), 16)
        s = int(self.key[8:12].hex(), 16)
        l = int(self.key[12:16].hex(), 16)
        c = 3816266640
        for _ in range(16):
            r -= (o << 4) + s ^ o + c ^ (o >> 5) + l
            r = self.MAX_UINT & r
            o -= (r << 4) + p ^ r + c ^ (r >> 5) + a
            o = self.MAX_UINT & o
            c -= self.DELTA
            c = self.MAX_UINT & c
        g = bytearray(8)
        self.put_uint_to_bytes(g, 0, o)
        self.put_uint_to_bytes(g, 4, r)
        return g

    def decipher_wrapper(self):
        for t in range(8):
            try:
                self.xor_b[t] ^= self.k_arr[self.result_last_index + t]
            except IndexError:
                pass
        self.xor_b = self.decipher(self.xor_b)
        self.result_last_index += 8
        self.xor_index = 0
        return True

    def decrypt(self, v):
        e = 0
        i = bytearray(8)
        n = len(v)

        self.k_arr = v
        if n % 8 != 0 or n < 16:
            return
        self.xor_b = self.decipher(v)
        self.xor_index = 7 & self.xor_b[0]
        e = n - self.xor_index - 10
        if e < 0:
            return
        for o in range(len(i)):
            i[o] = 0
        self.result = bytearray(e)
        self.result_pre_last_index = 0
        self.result_last_index = 8
        self.xor_index += 1

        for r in range(1, 3):
            if self.xor_index < 8:
                self.xor_index += 1
                r += 1
            if self.xor_index == 8:
                i = v
                if not self.decipher_wrapper():
                    return
        o = 0
        while e != 0:
            if self.xor_index < 8:
                self.result[o] = 0xff & (i[self.result_pre_last_index +
                                         self.xor_index] ^
                                         self.xor_b[self.xor_index])
                o += 1
                e -= 1
                self.xor_index += 1
            if self.xor_index == 8:
                i = v
                self.result_pre_last_index = self.result_last_index - 8
                if not self.decipher_wrapper():
                    return
        for r in range(1, 8):
            if self.xor_index < 8:
                if (
                    i[self.result_pre_last_index + self.xor_index] ^
                    self.xor_b[self.xor_index]
                   ) != 0:
                    return
                self.xor_index += 1
            if self.xor_index == 8:
                i = v
                self.result_pre_last_index = self.result_last_index
                if not self.decipher_wrapper():
                    return
        return self.result
