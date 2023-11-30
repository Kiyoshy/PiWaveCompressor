# KN: Audio handling

from pydub import AudioSegment
import threading
import pyaudio
import time
import wave


class Recorder(threading.Thread):
	def __init__(self, mode):
		threading.Thread.__init__(self)
		self.flag = False     # Thread control flag
		self.modep = mode  # int number 1: Debug Mode 2:Verbose Mode 3:Normal Mode
		# Audio file properties
		self.chunk = 12288    # Frames in the buffer
		self.format = pyaudio.paInt16
		self.channels = 1     # channels to use
		self.rate = 11025    # Sampling rate
		self.record_seconds = 52   # Recording time
		self.wave_output_filename = "audio.wav"    # ext file (wav, mp3, ogg)
		# Construct audio object
		self.p = pyaudio.PyAudio()

	def run(self) :
		self.flag = True     # Thread enable control flag
		self.start_rec()

	def setStop(self):
		self.flag = False     # Thread disable control flag

	def start_rec(self):
		# Audio configuration
		self.stream = self.p.open(format = self.format,
		        channels = self.channels,
		        rate = self.rate,
		        input = True,
		        frames_per_buffer = self.chunk)
		# Start recording
		self.frames = []
		self.stp_rec = (int(self.rate / self.chunk * self.record_seconds)) - 1
		for i in range(0, int(self.rate / self.chunk * self.record_seconds)):
			if i != self.stp_rec:
				if self.flag == True:
					if (self.modep == 1): print ("Recording...", i)
					if (self.modep == 1): print ("Stp_rec:", self.stp_rec)
					self.data = self.stream.read(self.chunk)
					self.frames.append(self.data)
				else:
					if (self.modep == 1): print ("Stopped by user")
					self.stop_rec()
					break
			else:
				if (self.modep == 1): print ("Stopped by time to record: ", self.stp_rec)
				self.stop_rec()
				break

	def stop_rec(self):
		# Stop recording
		if (self.modep == 1): print ("Stoping...")
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		# Saving audio file
		if (self.modep == 1): print ("Saving...")
		self.wf = wave.open(self.wave_output_filename, 'wb')
		self.wf.setnchannels(self.channels)
		self.wf.setsampwidth(self.p.get_sample_size(self.format))
		self.wf.setframerate(self.rate)
		self.wf.writeframes(b''.join(self.frames))
		self.wf.close()
		if (self.modep == 1): print ("Recording done...")

	def play_audio(self):
		# Playing audio
		self.chunk_pl = 1024
		self.wf = wave.open(self.wave_output_filename, 'rb')  # Open the sound file
		self.p = pyaudio.PyAudio()
		# Open a .Stream object to write the WAV file to
		# 'output = True' indicates that the sound will be played rather than recorded
		self.stream = self.p.open(format = self.p.get_format_from_width(self.wf.getsampwidth()),
		                channels = self.wf.getnchannels(),
		                rate = self.wf.getframerate(),
		                output = True)
		# Read data in chunks
		self.data = self.wf.readframes(self.chunk_pl)
		# Play the sound by writing the audio data to the stream
		if (self.modep == 1): print ("Start playing...")
		while self.data:
			self.stream.write(self.data)
			self.data = self.wf.readframes(self.chunk_pl)
		# Close and terminate the stream
		if (self.modep == 1): print ("Stop playing...")
		self.stream.stop_stream()
		self.stream.close()
		self.p.terminate()
		return 0

	def convert_file(self):
		# Convert .wav file to .mp3 file
		if (self.modep == 1): print ("wav - mp3")
		self.startConvert_time = time.time()
		self.wav_audio = AudioSegment.from_file("audio.wav", format="wav")     # File to compress
		self.wav_audio.export("c_audio.mp3", format="mp3")     # Compressed file
		self.convert_time = (time.time() - self.startConvert_time)
		if (self.modep == 1): print ("Convert Time =  %0.3f" % self.convert_time) 