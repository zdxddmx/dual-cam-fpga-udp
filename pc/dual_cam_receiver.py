#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双目摄像头UDP接收与解包程序
接收格式：4字节/像素（左目RGB565 + 右目RGB565）
"""

import socket
import struct
import numpy as np
import cv2
from collections import defaultdict
import time

# ============================================================================
# 配置参数
# ============================================================================
UDP_IP = "0.0.0.0"          # 监听所有网卡
UDP_PORT = 6003             # 目标端口（对应FPGA的DST_UDP_PORT）
IMG_WIDTH = 640
IMG_HEIGHT = 480
IMG_HEADER = 0xAA0055FF
BYTES_PER_PIXEL = 4         # 4字节/像素（左右目各2字节）

# ============================================================================
# RGB565转RGB888函数
# ============================================================================
def rgb565_to_rgb888(data_565):
    """
    将RGB565格式转换为RGB888格式
    输入：16位RGB565数据（numpy array）
    输出：(H, W, 3) RGB888图像
    """
    # 提取RGB565的各个分量
    r5 = (data_565 >> 11) & 0x1F  # 高5位：R
    g6 = (data_565 >> 5) & 0x3F   # 中6位：G
    b5 = data_565 & 0x1F          # 低5位：B

    # 扩展到8位
    r8 = (r5 << 3) | (r5 >> 2)    # 5位->8位
    g8 = (g6 << 2) | (g6 >> 4)    # 6位->8位
    b8 = (b5 << 3) | (b5 >> 2)    # 5位->8位

    # 组合成RGB888 (OpenCV使用BGR顺序)
    img = np.stack([b8, g8, r8], axis=-1).astype(np.uint8)
    return img

# ============================================================================
# UDP包解析类
# ============================================================================
class DualCamReceiver:
    def __init__(self, ip, port):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind((ip, port))
        self.sock.settimeout(5.0)  # 5秒超时

        # 帧缓存
        self.frame_buffers = defaultdict(lambda: {
            'data': bytearray(IMG_WIDTH * IMG_HEIGHT * BYTES_PER_PIXEL),
            'received_packets': set(),
            'total_packets': 0,
            'start_time': 0
        })

        print(f"[INFO] UDP服务器启动，监听 {ip}:{port}")
        print(f"[INFO] 图像尺寸：{IMG_WIDTH}x{IMG_HEIGHT}")
        print(f"[INFO] 数据格式：左目RGB565(16bit) + 右目RGB565(16bit)")

    def parse_header(self, data):
        """
        解析UDP包头（32字节）
        返回：(header, frame_seq, pic_seq, offset, total, height, width, frame_size)
        """
        if len(data) < 32:
            return None

        # 小端序解析（FPGA端使用的字节序）
        header_data = struct.unpack('<8I', data[:32])

        img_header = header_data[0]
        img_width = header_data[1]
        img_height = header_data[2]
        img_total = header_data[3]
        img_offset = header_data[4]
        img_picseq = header_data[5]
        img_framseq = header_data[6]
        img_framsize = header_data[7]

        # 验证包头
        if img_header != IMG_HEADER:
            print(f"[WARN] 包头错误：0x{img_header:08X}，期望：0x{IMG_HEADER:08X}")
            return None

        return {
            'header': img_header,
            'width': img_width,
            'height': img_height,
            'total': img_total,
            'offset': img_offset,
            'pic_seq': img_picseq,
            'frame_seq': img_framseq,
            'frame_size': img_framsize
        }

    def process_packet(self, data):
        """处理接收到的UDP包"""
        # 解析包头
        header_info = self.parse_header(data)
        if header_info is None:
            return None

        pic_seq = header_info['pic_seq']
        frame_seq = header_info['frame_seq']
        offset = header_info['offset']
        frame_size = header_info['frame_size']

        # 提取数据部分（跳过32字节包头）
        payload = data[32:32+frame_size]

        # 初始化帧缓存
        fb = self.frame_buffers[pic_seq]
        if fb['start_time'] == 0:
            fb['start_time'] = time.time()

        # 存储数据到对应偏移位置
        fb['data'][offset:offset+len(payload)] = payload
        fb['received_packets'].add(frame_seq)
        fb['total_packets'] = max(fb['total_packets'], frame_seq + 1)

        # 调试信息
        print(f"[RECV] 图片#{pic_seq} 包#{frame_seq}/{fb['total_packets']} "
              f"偏移:{offset} 大小:{len(payload)} "
              f"进度:{len(fb['received_packets'])}/{fb['total_packets']}",
              end='\r')

        # 检查是否接收完整
        if len(fb['received_packets']) >= fb['total_packets']:
            elapsed = time.time() - fb['start_time']
            print(f"\n[INFO] 图片#{pic_seq} 接收完成！"
                  f"用时:{elapsed:.2f}s "
                  f"速度:{len(fb['data'])/elapsed/1024:.1f}KB/s")

            # 解析图像
            return self.parse_image(fb['data'], pic_seq)

        return None

    def parse_image(self, data, pic_seq):
        """
        解析双目图像数据
        数据格式：每4字节一个像素
        - byte0: 左目RGB565高8位
        - byte1: 左目RGB565低8位
        - byte2: 右目RGB565高8位
        - byte3: 右目RGB565低8位
        """
        try:
            # 转换为numpy数组
            pixel_count = IMG_WIDTH * IMG_HEIGHT
            raw_data = np.frombuffer(data[:pixel_count*4], dtype=np.uint8)

            # 重组为 (H*W, 4) 的数组
            pixels = raw_data.reshape((pixel_count, 4))

            # 提取左右目数据
            left_rgb565 = (pixels[:, 0].astype(np.uint16) << 8) | pixels[:, 1]
            right_rgb565 = (pixels[:, 2].astype(np.uint16) << 8) | pixels[:, 3]

            # 重塑为图像尺寸
            left_rgb565 = left_rgb565.reshape((IMG_HEIGHT, IMG_WIDTH))
            right_rgb565 = right_rgb565.reshape((IMG_HEIGHT, IMG_WIDTH))

            # 转换为RGB888
            left_img = rgb565_to_rgb888(left_rgb565)
            right_img = rgb565_to_rgb888(right_rgb565)

            print(f"[INFO] 图片#{pic_seq} 解析成功")
            print(f"       左目：{left_img.shape} {left_img.dtype}")
            print(f"       右目：{right_img.shape} {right_img.dtype}")

            return {
                'pic_seq': pic_seq,
                'left': left_img,
                'right': right_img
            }

        except Exception as e:
            print(f"[ERROR] 图片#{pic_seq} 解析失败：{e}")
            return None

    def run(self):
        """主循环"""
        print("[INFO] 开始接收数据...")

        frame_count = 0

        while True:
            try:
                # 接收UDP包
                data, addr = self.sock.recvfrom(65536)

                # 处理包
                result = self.process_packet(data)

                # 如果接收到完整图像
                if result is not None:
                    pic_seq = result['pic_seq']
                    left_img = result['left']
                    right_img = result['right']

                    # 显示图像
                    combined = np.hstack([left_img, right_img])
                    cv2.imshow('Dual Camera (Left | Right)', combined)

                    # 保存图像
                    frame_count += 1
                    if frame_count % 10 == 0:  # 每10帧保存一次
                        cv2.imwrite(f'frame_{pic_seq:06d}_left.jpg', left_img)
                        cv2.imwrite(f'frame_{pic_seq:06d}_right.jpg', right_img)
                        print(f"[SAVE] 已保存第{frame_count}帧")

                    # 清理缓存
                    if pic_seq in self.frame_buffers:
                        del self.frame_buffers[pic_seq]

                    # 按'q'退出
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        print("\n[INFO] 用户退出")
                        break

            except socket.timeout:
                print("\n[WARN] 接收超时，等待数据...")
                continue
            except KeyboardInterrupt:
                print("\n[INFO] 程序中断")
                break
            except Exception as e:
                print(f"\n[ERROR] {e}")
                continue

        self.sock.close()
        cv2.destroyAllWindows()
        print("[INFO] 程序结束")

# ============================================================================
# 主程序
# ============================================================================
if __name__ == "__main__":
    receiver = DualCamReceiver(UDP_IP, UDP_PORT)
    receiver.run()
