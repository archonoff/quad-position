# coding=utf-8

"""
The MIT License (MIT)
Copyright (c) 2017 Zaitsev Oleg
"""

import asyncore
import socket
import math
from gyro_data_server import mpu6050

mpu = mpu6050.MPU6050()
mpu.dmpInitialize()
mpu.setDMPEnabled(True)
packet_size = mpu.dmpGetFIFOPacketSize()


class GyroHandler(asyncore.dispatcher_with_send):
    def get_gyro_value(self, packet):
        if packet[16] > 127:
            packet[16] -= 256

        if packet[20] > 127:
            packet[20] -= 256

        if packet[24] > 127:
            packet[24] -= 256

        data = {
            'x': (packet[16] << 8) + packet[17],
            'y': (packet[20] << 8) + packet[21],
            'z': (packet[24] << 8) + packet[25]
        }

        return data

    def handle_read(self):
        data = self.recv(1024)

        if not data:
            return

        mpu_int_status = mpu.getIntStatus()
        if mpu_int_status >= 2: # check for DMP data ready interrupt (this should happen frequently)
            # Чтение из буфера датчика
            mpu.resetFIFO()
            fifo_count = mpu.getFIFOCount()
            while fifo_count < packet_size:
                fifo_count = mpu.getFIFOCount()

            # Получение и преобразование данных
            result = mpu.getFIFOBytes(packet_size)
            q = mpu.dmpGetQuaternion(result)
            gyro = self.get_gyro_value(result)
            # g = mpu.dmpGetGravity(q)
            # ypr = mpu.dmpGetYawPitchRoll(q, g)

            # Углы в градусах
            # pitch = ypr['pitch'] * 180 / math.pi
            # roll = ypr['roll'] * 180 / math.pi
            # yaw = ypr['yaw'] * 180 / math.pi

            w = q.get('w')
            qx = q.get('x')
            qy = q.get('y')
            qz = q.get('z')

            gx = gyro.get('x')
            gy = gyro.get('y')
            gz = gyro.get('z')

            # self.send('{}:{}:{}\0'.format(pitch, roll, yaw).encode('ascii'))
            self.send('{}:{}:{}:{}:{}:{}:{}\0'.format(w, qx, qy, qz, gx, gy, gz).encode('ascii'))
        else:
            self.send(b'error\0')


class GyroServer(asyncore.dispatcher):
    def __init__(self, host, port):
        asyncore.dispatcher.__init__(self)
        self.create_socket(socket.AF_INET, socket.SOCK_STREAM)
        self.set_reuse_addr()
        self.bind((host, port))
        self.listen(1)

    def handle_accept(self):
        pair = self.accept()
        if pair is not None:
            sock, addr = pair
            GyroHandler(sock)


if __name__ == '__main__':
    HOST, PORT = 'localhost', 31337
    server = GyroServer(HOST, PORT)
    asyncore.loop()
