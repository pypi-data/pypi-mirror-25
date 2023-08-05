#!/usr/bin/python
# -*- coding: utf-8 -*-
import wave
import pyaudio


class WaveHelper(object):

    @staticmethod
    def save_base64_file(data, file_name):
        store_file = open(file_name, "wb")
        store_file.write(data)
        store_file.close()

    @staticmethod
    def play(file_name):
        chunk = 1024
        file_handler = wave.open(file_name, "rb")
        player = pyaudio.PyAudio()

        stream = player.open(format=player.get_format_from_width(file_handler.getsampwidth()),
                             channels=file_handler.getnchannels(), rate=file_handler.getframerate(), output=True)
        data = file_handler.readframes(chunk)
        while data != "":
            stream.write(data)
            data = file_handler.readframes(chunk)
        stream.stop_stream()
        stream.close()
        player.terminate()

    @staticmethod
    def reverse_wave(old_file, new_file):
        old_wave = wave.open(old_file, 'rb')
        new_wave = wave.open(new_file, 'wb')
        new_wave.setparams(old_wave.getparams())
        for i in range(old_wave.getnframes()):
            new_wave.writeframes(old_wave.readframes(i)[::-1])
        new_wave.close()
        old_wave.close()