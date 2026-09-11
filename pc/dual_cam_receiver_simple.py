#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
双目摄像头UDP接收程序（简化版）
用于快速测试和调试
"""

import socket
import struct
import numpy as np
import cv2

# 配置
UDP_IP = "0.0.0.0"
UDP_PORT = 6003
IMG_WIDTH = 640
IMG_HEIGHT = 480

def rgb565_to_bgr(rgb565_data):
    """RGB565转BGR888（OpenCV格式）"""
    r = ((rgb565_data >> 11) & 0x1F) << 3
    g = ((rgb565_data >> 5) & 0x3F) << 2
    b = (rgb565_data & 0x1F) << 3
    return np.stack([b, g, r], axis=-1).astype(np.uint8)

def main():
    # 创建UDP socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.bind((UDP_IP, UDP_PORT))
    print(f"监听 {UDP_IP}:{UDP_PORT}...")

    # 帧缓存
    frame_data = bytearray(IMG_WIDTH * IMG_HEIGHT * 4)
    received_packets = set()
    current_pic = -1

    while True:
        try:
            # 接收数据
            data, addr = sock.recvfrom(65536)

            # 解析包头（32字节，小端序）
            if len(data) < 32:
                continue

            header = struct.unpack('<8I', data[:32])
            img_header, img_width, img_height, img_total, img_offset, \
            img_picseq, img_framseq, img_framsize = header

            # 验证包头
            if img_header != 0xAA0055FF:
                print(f"包头错误: 0x{img_header:08X}")
                continue

            # 新的一帧
            if img_picseq != current_pic:
                if current_pic != -1 and len(received_packets) > 0:
                    print(f"\n帧#{current_pic} 接收完成，包数:{len(received_packets)}")

                    # 解析图像
                    try:
                        pixels = np.frombuffer(frame_data, dtype=np.uint8).reshape((-1, 4))
                        left_565 = (pixels[:, 0].astype(np.uint16) << 8) | pixels[:, 1]
                        right_565 = (pixels[:, 2].astype(np.uint16) << 8) | pixels[:, 3]

                        left_img = rgb565_to_bgr(left_565.reshape((IMG_HEIGHT, IMG_WIDTH)))
                        right_img = rgb565_to_bgr(right_565.reshape((IMG_HEIGHT, IMG_WIDTH)))

                        # 显示
                        combined = np.hstack([left_img, right_img])
                        cv2.imshow('Left | Right', combined)

                        if cv2.waitKey(1) & 0xFF == ord('q'):
                            break

                    except Exception as e:
                        print(f"解析错误: {e}")

                # 重置
                current_pic = img_picseq
                received_packets.clear()
                frame_data = bytearray(IMG_WIDTH * IMG_HEIGHT * 4)

            # 存储数据
            payload = data[32:32+img_framsize]
            frame_data[img_offset:img_offset+len(payload)] = payload
            received_packets.add(img_framseq)

            print(f"\r帧#{img_picseq} 包#{img_framseq} 进度:{len(received_packets)}", end='')

        except KeyboardInterrupt:
            print("\n退出")
            break
        except Exception as e:
            print(f"\n错误: {e}")

    sock.close()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
