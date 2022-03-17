#!/usr/bin/env python
#---------------------------------------------------
# This is free and unencumbered software released into the public domain.
#
# Anyone is free to copy, modify, publish, use, compile, sell, or
# distribute this software, either in source code form or as a compiled
# binary, for any purpose, commercial or non-commercial, and by any
# means.
#
# In jurisdictions that recognize copyright laws, the author or authors
# of this software dedicate any and all copyright interest in the
# software to the public domain. We make this dedication for the benefit
# of the public at large and to the detriment of our heirs and
# successors. We intend this dedication to be an overt act of
# relinquishment in perpetuity of all present and future rights to this
# software under copyright law.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
# IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
# OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
# ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
#
# For more information, please refer to <http://unlicense.org>
#---------------------------------------------------
# 
#		Passive buzzer 			   Pi 
#			VCC ----------------- 3.3V
#			GND ------------------ GND
#			SIG ---------------- Pin Gpio27
#
#		some notes for melodies were taken from:
#		http://www.astlessons.com/pianoforkids1.html
#		http://www.astlessons.com/pianoforkids2.html
#		where you can get more notes
#
#---------------------------------------------------
import RPi.GPIO as GPIO
import time

buzzer_pin = 26

NOTE_B0 = 31
NOTE_C1 =33
NOTE_CS1 =35
NOTE_D1  =37
NOTE_DS1 =39
NOTE_E1  =41
NOTE_F1  =44
NOTE_FS1 =46
NOTE_G1  =49
NOTE_GS1 =52
NOTE_A1  =55
NOTE_AS1 =58
NOTE_B1  =62
NOTE_C2  =65
NOTE_CS2 =69
NOTE_D2  =73
NOTE_DS2 =78
NOTE_E2  =82
NOTE_F2  =87
NOTE_FS2 =93
NOTE_G2  =98
NOTE_GS2 =104
NOTE_A2  =110
NOTE_AS2 =117
NOTE_B2  =123
NOTE_C3  =131
NOTE_CS3 =139
NOTE_D3  =147
NOTE_DS3 =156
NOTE_E3  =165
NOTE_F3  =175
NOTE_FS3 =185
NOTE_G3  =196
NOTE_GS3 =208
NOTE_A3  =220
NOTE_AS3 =233
NOTE_B3  =247
NOTE_C4  =262
NOTE_CS4 =277
NOTE_D4  =294
NOTE_DS4 =311
NOTE_E4  =330
NOTE_F4  =349
NOTE_FS4 =370
NOTE_G4  =392
NOTE_GS4 =415
NOTE_A4  =440
NOTE_AS4 =466
NOTE_B4  =494
NOTE_C5  =523
NOTE_CS5 =554
NOTE_D5  =587
NOTE_DS5 =622
NOTE_E5  =659
NOTE_F5  =698
NOTE_FS5 =740
NOTE_G5  =784
NOTE_GS5 =831
NOTE_A5  =880
NOTE_AS5 =932
NOTE_B5  =988
NOTE_C6  =1047
NOTE_CS6 =1109
NOTE_D6  =1175
NOTE_DS6 =1245
NOTE_E6  =1319
NOTE_F6  =1397
NOTE_FS6 =1480
NOTE_G6  =1568
NOTE_GS6 =1661
NOTE_A6  =1760
NOTE_AS6 =1865
NOTE_B6  =1976
NOTE_C7  =2093
NOTE_CS7 =2217
NOTE_D7  =2349
NOTE_DS7 =2489
NOTE_E7  =2637
NOTE_F7  =2794
NOTE_FS7 =2960
NOTE_G7  =3136
NOTE_GS7 =3322
NOTE_A7  =3520
NOTE_AS7 =3729
NOTE_B7  =3951
NOTE_C8  =4186
NOTE_CS8 =4435
NOTE_D8  =4699
NOTE_DS8 =4978
REST = 0

'''notes = {
	'NOTE_B0' : 31,
	'NOTE_C1' : 33, 'NOTE_CS1' : 35,
	'NOTE_D1' : 37, 'NOTE_DS1' : 39,
	'NOTE_EB1' : 39,
	'NOTE_E1' : 41,
	'NOTE_F1' : 44, 'NOTE_FS1' : 46,
	'NOTE_G1' : 49, 'NOTE_GS1' : 52,
	'NOTE_A1' : 55, 'NOTE_AS1' : 58,
	'NOTE_BB1' : 58,
	'NOTE_B1' : 62,
	'NOTE_C2' : 65, 'NOTE_CS2' : 69,
	'NOTE_D2' : 73, 'NOTE_DS2' : 78,
	'NOTE_EB2' : 78,
	'NOTE_E2' : 82,
	'NOTE_F2' : 87, 'NOTE_FS2' : 93,
	'NOTE_G2' : 98, 'NOTE_GS2' : 104,
	'NOTE_A2' : 110, 'NOTE_AS2' : 117,
	'NOTE_BB2' : 123,
	'NOTE_B2' : 123,
	'NOTE_C3' : 131, 'NOTE_CS3' : 139,
	'NOTE_D3' : 147, 'NOTE_DS3' : 156,
	'NOTE_EB3' : 156,
	'NOTE_E3' : 165,
	'NOTE_F3' : 175, 'NOTE_FS3' : 185,
	'NOTE_G3' : 196, 'NOTE_GS3' : 208,
	'NOTE_A3' : 220, 'NOTE_AS3' : 233,
	'NOTE_BB3' : 233,
	'NOTE_B3' : 247,
	'NOTE_C4' : 262, 'NOTE_CS4' : 277,
	'NOTE_D4' : 294, 'NOTE_DS4' : 311,
	'NOTE_EB4' : 311,
	'NOTE_E4' : 330,
	'NOTE_F4' : 349, 'NOTE_FS4' : 370,
	'NOTE_G4' : 392, 'NOTE_GS4' : 415,
	'NOTE_A4' : 440, 'NOTE_AS4' : 466,
	'NOTE_BB4' : 466,
	'NOTE_B4' : 494,
	'NOTE_C5' : 523, 'NOTE_CS5' : 554,
	'NOTE_D5' : 587, 'NOTE_DS5' : 622,
	'NOTE_EB5' : 622,
	'NOTE_E5' : 659,
	'NOTE_F5' : 698, 'NOTE_FS5' : 740,
	'NOTE_G5' : 784, 'NOTE_GS5' : 831,
	'NOTE_A5' : 880, 'NOTE_AS5' : 932,
	'NOTE_BB5' : 932,
	'NOTE_B5' : 988,
	'NOTE_C6' : 1047, 'NOTE_CS6' : 1109,
	'NOTE_D6' : 1175, 'NOTE_DS6' : 1245,
	'NOTE_EB6' : 1245,
	'NOTE_E6' : 1319,
	'NOTE_F6' : 1397, 'NOTE_FS6' : 1480,
	'NOTE_G6' : 1568, 'NOTE_GS6' : 1661,
	'NOTE_A6' : 1760, 'NOTE_AS6' : 1865,
	'NOTE_BB6' : 1865,
	'NOTE_B6' : 1976,
	'NOTE_C7' : 2093, 'NOTE_CS7' : 2217,
	'NOTE_D7' : 2349, 'NOTE_DS7' : 2489,
	'NOTE_EB7' : 2489,
	'NOTE_E7' : 2637,
	'NOTE_F7' : 2794, 'NOTE_FS7' : 2960,
	'NOTE_G7' : 3136, 'NOTE_GS7' : 3322,
	'NOTE_A7' : 3520, 'NOTE_AS7' : 3729,
	'NOTE_BB7' : 3729,
	'NOTE_B7' : 3951,
	'NOTE_C8' : 4186, 'NOTE_CS8' : 4435,
	'NOTE_D8' : 4699, 'NOTE_DS8' : 4978
}'''

#// change this to make the song slower or faster
#tempo = 200

#// change this to whichever pin you want to use
#buzzer = 11

melody = [
  
  
  NOTE_E5,8, NOTE_E5,8, REST,8, NOTE_E5,8, REST,8, NOTE_C5,8, NOTE_E5,8, #//1
  NOTE_G5,4, REST,4, NOTE_G4,8, REST,4, 
  NOTE_C5,-4, NOTE_G4,8, REST,4, NOTE_E4,-4, #// 3
  NOTE_A4,4, NOTE_B4,4, NOTE_AS4,8, NOTE_A4,4,
  NOTE_G4,-8, NOTE_E5,-8, NOTE_G5,-8, NOTE_A5,4, NOTE_F5,8, NOTE_G5,8,
  REST,8, NOTE_E5,4,NOTE_C5,8, NOTE_D5,8, NOTE_B4,-4,
  NOTE_C5,-4, NOTE_G4,8, REST,4, NOTE_E4,-4, #// repeats from 3
  NOTE_A4,4, NOTE_B4,4, NOTE_AS4,8, NOTE_A4,4,
  NOTE_G4,-8, NOTE_E5,-8, NOTE_G5,-8, NOTE_A5,4, NOTE_F5,8, NOTE_G5,8,
  REST,8, NOTE_E5,4,NOTE_C5,8, NOTE_D5,8, NOTE_B4,-4,

  
  REST,4, NOTE_G5,8, NOTE_FS5,8, NOTE_F5,8, NOTE_DS5,4, NOTE_E5,8,#//7
  REST,8, NOTE_GS4,8, NOTE_A4,8, NOTE_C4,8, REST,8, NOTE_A4,8, NOTE_C5,8, NOTE_D5,8,
  REST,4, NOTE_DS5,4, REST,8, NOTE_D5,-4,
  NOTE_C5,2, REST,2,

  REST,4, NOTE_G5,8, NOTE_FS5,8, NOTE_F5,8, NOTE_DS5,4, NOTE_E5,8,#//repeats from 7
  REST,8, NOTE_GS4,8, NOTE_A4,8, NOTE_C4,8, REST,8, NOTE_A4,8, NOTE_C5,8, NOTE_D5,8,
  REST,4, NOTE_DS5,4, REST,8, NOTE_D5,-4,
  NOTE_C5,2, REST,2,

  NOTE_C5,8, NOTE_C5,4, NOTE_C5,8, REST,8, NOTE_C5,8, NOTE_D5,4,#//11
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2,

  NOTE_C5,8, NOTE_C5,4, NOTE_C5,8, REST,8, NOTE_C5,8, NOTE_D5,8, NOTE_E5,8,#//13
  REST,1, 
  NOTE_C5,8, NOTE_C5,4, NOTE_C5,8, REST,8, NOTE_C5,8, NOTE_D5,4,
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2,
  NOTE_E5,8, NOTE_E5,8, REST,8, NOTE_E5,8, REST,8, NOTE_C5,8, NOTE_E5,4,
  NOTE_G5,4, REST,4, NOTE_G4,4, REST,4, 
  NOTE_C5,-4, NOTE_G4,8, REST,4, NOTE_E4,-4, #// 19
  
  NOTE_A4,4, NOTE_B4,4, NOTE_AS4,8, NOTE_A4,4,
  NOTE_G4,-8, NOTE_E5,-8, NOTE_G5,-8, NOTE_A5,4, NOTE_F5,8, NOTE_G5,8,
  REST,8, NOTE_E5,4, NOTE_C5,8, NOTE_D5,8, NOTE_B4,-4,

  NOTE_C5,-4, NOTE_G4,8, REST,4, NOTE_E4,-4, #// repeats from 19
  NOTE_A4,4, NOTE_B4,4, NOTE_AS4,8, NOTE_A4,4,
  NOTE_G4,-8, NOTE_E5,-8, NOTE_G5,-8, NOTE_A5,4, NOTE_F5,8, NOTE_G5,8,
  REST,8, NOTE_E5,4, NOTE_C5,8, NOTE_D5,8, NOTE_B4,-4,

  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,#//23
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_D5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_G5,-8, NOTE_F5,-8,
  
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2, #//26
  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_B4,8, NOTE_F5,4, NOTE_F5,8, NOTE_F5,-8, NOTE_E5,-8, NOTE_D5,-8,
  NOTE_C5,8, NOTE_E4,4, NOTE_E4,8, NOTE_C4,2,

  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,#//repeats from 23
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_D5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_G5,-8, NOTE_F5,-8,
  
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2, #//26
  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_B4,8, NOTE_F5,4, NOTE_F5,8, NOTE_F5,-8, NOTE_E5,-8, NOTE_D5,-8,
  NOTE_C5,8, NOTE_E4,4, NOTE_E4,8, NOTE_C4,2,
  NOTE_C5,8, NOTE_C5,4, NOTE_C5,8, REST,8, NOTE_C5,8, NOTE_D5,8, NOTE_E5,8,
  REST,1,

  NOTE_C5,8, NOTE_C5,4, NOTE_C5,8, REST,8, NOTE_C5,8, NOTE_D5,4, #//33
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2,
  NOTE_E5,8, NOTE_E5,8, REST,8, NOTE_E5,8, REST,8, NOTE_C5,8, NOTE_E5,4,
  NOTE_G5,4, REST,4, NOTE_G4,4, REST,4, 
  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_D5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_A5,-8, NOTE_G5,-8, NOTE_F5,-8,
  
  NOTE_E5,8, NOTE_C5,4, NOTE_A4,8, NOTE_G4,2, #//40
  NOTE_E5,8, NOTE_C5,4, NOTE_G4,8, REST,4, NOTE_GS4,4,
  NOTE_A4,8, NOTE_F5,4, NOTE_F5,8, NOTE_A4,2,
  NOTE_B4,8, NOTE_F5,4, NOTE_F5,8, NOTE_F5,-8, NOTE_E5,-8, NOTE_D5,-8,
  NOTE_C5,8, NOTE_E4,4, NOTE_E4,8, NOTE_C4,2,
  
  #//game over sound
  NOTE_C5,-4, NOTE_G4,-4, NOTE_E4,4, #//45
  NOTE_A4,-8, NOTE_B4,-8, NOTE_A4,-8, NOTE_GS4,-8, NOTE_AS4,-8, NOTE_GS4,-8,
  NOTE_G4,8, NOTE_D4,8, NOTE_E4,-2,  

]

tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
]

'''melody = [
  notes['E5'], notes['E5'], 0, notes['E5'],
  0, notes['C5'], notes['E5'], 0,
  notes['G5'], 0, 0,  0,
  notes['G4'], 0, 0, 0,
 
  notes['C5'], 0, 0, notes['G4'],
  0, 0, notes['E4'], 0,
  0, notes['A4'], 0, notes['B4'],
  0, notes['AS4'], notes['A4'], 0,
 
  notes['G4'], notes['E5'], notes['G5'],
  notes['A5'], 0, notes['F5'], notes['G5'],
  0, notes['E5'], 0, notes['C5'],
  notes['D5'], notes['B4'], 0, 0,
 
  notes['C5'], 0, 0, notes['G4'],
  0, 0, notes['E4'], 0,
  0, notes['A4'], 0, notes['B4'],
  0, notes['AS4'], notes['A4'], 0,
 
  notes['G4'], notes['E5'], notes['G5'],
  notes['A5'], 0, notes['F5'], notes['G5'],
  0, notes['E5'], 0, notes['C5'],
  notes['D5'], notes['B4'], 0, 0


]

tempo = [
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
 
  9, 9, 9,
  12, 12, 12, 12,
  12, 12, 12, 12,
  12, 12, 12, 12,
]
'''
'''
underworld_melody = [
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['C4'], notes['C5'], notes['A3'], notes['A4'],
  notes['AS3'], notes['AS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0,
  notes['F3'], notes['F4'], notes['D3'], notes['D4'],
  notes['DS3'], notes['DS4'], 0,
  0, notes['DS4'], notes['CS4'], notes['D4'],
  notes['CS4'], notes['DS4'],
  notes['DS4'], notes['GS3'],
  notes['G3'], notes['CS4'],
  notes['C4'], notes['FS4'], notes['F4'], notes['E3'], notes['AS4'], notes['A4'],
  notes['GS4'], notes['DS4'], notes['B3'],
  notes['AS3'], notes['A3'], notes['GS3'],
  0, 0, 0
]

underworld_tempo = [
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  3,
  12, 12, 12, 12,
  12, 12, 6,
  6, 18, 18, 18,
  6, 6,
  6, 6,
  6, 6,
  18, 18, 18, 18, 18, 18,
  10, 10, 10,
  10, 10, 10,
  3, 3, 3
]

adventure_time_melody = [
    notes['D5'], 
    notes['G5'], notes['G5'], notes['G5'], notes['G5'], notes['FS5'],
    notes['FS5'], notes['E5'], notes['D5'], notes['E5'], notes['D5'], notes['D5'],
    notes['C5'], notes['B5'], notes['A5'], notes['G4'],  
    0, notes['C5'], notes['B5'], notes['A5'], notes['G4'], 0,  
    notes['G5'], 0, notes['G5'], notes['G5'], 0, notes['G5'], 
    notes['FS5'], 0, notes['E5'], notes['E5'], notes['D5'], notes['D5'], 
    notes['C5'], notes['C5'], notes['C5'], notes['D5'], 
    notes['D5'], notes['A5'], notes['B5'], notes['A5'], notes['G4'], 
    notes['G5']
  ]
adventure_time_tempo = [
    24,
    24, 12, 12, 12, 24,
    12, 24, 24, 24, 12, 24,
    12, 12, 12, 12,
    24, 12, 24, 24, 12, 24,  
    24, 24, 24, 12, 24, 12, 
    24, 24, 24, 12, 12, 24, 
    8, 24, 24, 8, 
    8, 24, 12, 24, 24, 
    12 
  ]


star_wars_melody = [ 
					notes['G4'], notes['G4'], notes['G4'], 
					notes['EB4'], 0, notes['BB4'], notes['G4'], 
					notes['EB4'], 0, notes['BB4'], notes['G4'], 0,
					
					notes['D4'], notes['D4'], notes['D4'], 
					notes['EB4'], 0, notes['BB3'], notes['FS3'],
					notes['EB3'], 0, notes['BB3'], notes['G3'], 0,
					
					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'], 
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0, 
					
					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,
					notes['EB3'], notes['FS3'], notes['EB3'], notes['FS3'], 
					notes['BB3'], 0, notes['G3'], notes['BB3'], notes['D4'], 0,
					
					
					notes['G4'], 0, notes['G3'], notes['G3'], 0,
					notes['G4'], 0, notes['FS4'], notes['F4'], 
					notes['E4'], notes['EB4'], notes['E4'], 0,
					notes['GS3'], notes['CS3'], 0, 
					
					notes['C3'], notes['B3'], notes['BB3'], notes['A3'], notes['BB3'], 0,
					
					notes['EB3'], notes['FS3'], notes['EB3'],  
					notes['BB3'], notes['G3'], notes['EB3'], 0, notes['BB3'], notes['G3'],
					]


star_wars_tempo = [
					2, 2, 2, 
					4, 8, 6, 2, 
					4, 8, 6, 2, 8,
					
					2, 2, 2,
					4, 8, 6, 2,
					4, 8, 6, 2, 8,
					
					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8, 
					4, 4, 6, 4, 2, 8,
					4, 2, 4, 4, 
					2, 8, 4, 6, 2, 8,
					
					2, 16, 4, 4, 8,
					2, 8, 4, 6,
					6, 4, 4, 8,
					4, 2, 8, 
					4, 4, 6, 4, 2, 8,
					4, 2, 2, 
					4, 2, 4, 8, 4, 2,
					]

popcorn_melody = [
	
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'], 
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'], 
	
	notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'], notes['G4'], 
	notes['A4'], notes['G4'],notes['A4'], notes['F4'], notes['A4'],
	
	
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'], 
	notes['A4'], notes['G4'], notes['A4'], notes['E4'], notes['C4'], notes['E4'], notes['A3'], 
	
	notes['A4'], notes['B4'], notes['C5'], notes['B4'], notes['C5'], notes['A4'], notes['B4'], notes['A4'], notes['B4'], notes['G4'], 
	notes['A4'], notes['G4'],notes['A4'], notes['B4'], notes['C5'],
	
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'], 
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'], 
	
	notes['E5'], notes['FS5'], notes['G5'], notes['FS5'], notes['G5'], notes['E5'], notes['FS5'], notes['E5'], notes['FS5'], notes['D5'], 
	notes['E5'], notes['D5'],notes['E5'], notes['C5'], notes['E5'],
	
	###
	
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'], 
	notes['E5'], notes['D5'], notes['E5'], notes['C5'], notes['G4'], notes['C5'], notes['E4'], 
	
	notes['E5'], notes['FS5'], notes['G5'], notes['FS5'], notes['G5'], notes['E5'], notes['FS5'], notes['E5'], notes['FS5'], notes['D5'], 
	notes['E5'], notes['D5'],notes['B4'], notes['D5'], notes['E5'],
]
popcorn_tempo = [
	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,
	
	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,
	
	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,
	
	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,
	
	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,
	
	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,
	
	8,8,8,8,8,8,4,
	8,8,8,8,8,8,4,
	
	8,8,8,8,8,8,8,8,8,8,
	8,8,8,8,4,
]

twinkle_twinkle_melody = [
	notes['C4'], notes['C4'], notes['G4'], notes['G4'], notes['A4'], notes['A4'], notes['G4'],
	notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'], notes['D4'], notes['C4'],
	
	notes['G4'], notes['G4'], notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'],
	notes['G4'], notes['G4'], notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'],
	
	notes['C4'], notes['C4'], notes['G4'], notes['G4'], notes['A4'], notes['A4'], notes['G4'],
	notes['F4'], notes['F4'], notes['E4'], notes['E4'], notes['D4'], notes['D4'], notes['C4'],
]

twinkle_twinkle_tempo = [
	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,
	
	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,
	
	4,4,4,4,4,4,2,
	4,4,4,4,4,4,2,
]

crazy_frog_melody = [
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],0,
	
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],0,
	
	
	notes['A3'], notes['G3'], notes['E3'], notes['D3'],
	
	notes['A4'], notes['C5'], notes['A4'], notes['A4'], notes['D5'], notes['A4'], notes['G4'], 
	notes['A4'], notes['E5'], notes['A4'], notes['A4'], notes['F5'], notes['E5'], notes['C5'],
	notes['A4'], notes['E5'], notes['A5'], notes['A4'], notes['G4'], notes['G4'], notes['E4'], notes['B4'], 
	notes['A4'],
]

crazy_frog_tempo = [
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,
	
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,4,
	
	8,4,4,4,
	
	2,4,4,8,4,4,4,
	2,4,4,8,4,4,4,
	4,4,4,8,4,8,4,4,
	1,
]

deck_the_halls_melody = [
	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,
	
	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,
	
	notes['D5'], notes['E5'], notes['F5'], notes['D5'],
	notes['E5'], notes['F5'], notes['G5'], notes['D5'],
	notes['E5'], notes['F5'], notes['G5'], notes['A5'], notes['B5'], notes['C6'],
	notes['B5'], notes['A5'], notes['G5'], 0,
	
	notes['G5'], notes['F5'], notes['E5'], notes['D5'],
	notes['C5'], notes['D5'], notes['E5'], notes['C5'],
	notes['D5'], notes['E5'], notes['F5'], notes['D5'], notes['E5'], notes['D5'],
	notes['C5'], notes['B4'], notes['C5'], 0,
]

deck_the_halls_tempo = [
	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,
	
	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,
	
	2,4,2,2,
	2,4,2,2,
	4,4,2,4,4,2,
	2,2,2,2,
	
	2, 4, 2, 2,
	2, 2, 2, 2,
	4, 4, 4, 4, 2, 4,
	2, 2, 2, 2,
]

manaderna_melody = [
	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['E4'],0,notes['D4'],notes['D4'],0,
	
	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['D4'],0,notes['C4'],notes['C4'],0,
	
	notes['D4'],notes['D4'],notes['E4'],notes['C4'],
	notes['D4'],notes['E4'],notes['F4'],notes['E4'],notes['C4'],
	notes['D4'],notes['E4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['D4'],notes['G3'],0,
	
	notes['E4'],notes['E4'],notes['F4'],notes['G4'],
	notes['G4'],notes['F4'],notes['E4'],notes['D4'],
	notes['C4'],notes['C4'],notes['D4'],notes['E4'],
	notes['D4'],0,notes['C4'],notes['C4'],
]

manaderna_tempo = [
	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,4,
	
	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,4,
	
	2,2,2,2,
	2,4,4,2,2,
	2,4,4,2,2,
	2,2,1,4,
	
	2,2,2,2,
	2,2,2,2,
	2,2,2,2,
	2,4,4,2,
]

bonnagard_melody = [
	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,notes['G4'],
	
	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,notes['G4'],notes['G4'],
	
	notes['C5'],notes['C5'],notes['C5'],notes['G4'],notes['G4'],
	notes['C5'],notes['C5'],notes['G4'],
	notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],
	notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],notes['C5'],0,
	
	notes['C5'],notes['C5'],notes['C5'],notes['G4'],
	notes['A4'],notes['A4'],notes['G4'],
	notes['E5'],notes['E5'],notes['D5'],notes['D5'],
	notes['C5'],0,
]

bonnagard_tempo = [
	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,2,2,
	
	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,2,4,4,
	
	2,2,2,4,4,
	2,2,1,
	4,4,2,4,4,2,
	4,4,4,4,2,2,4,
	
	2,2,2,2,
	2,2,1,
	2,2,2,2,
	1,1,
]

final_countdown_melody = [
	notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['A3'],notes['E5'],notes['D5'],notes['E5'],notes['A4'],
	notes['F3'],notes['F5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['D3'],notes['F5'],notes['E5'],notes['F5'],notes['A4'],
	notes['G3'],0,notes['D5'],notes['C5'],notes['D5'],notes['C5'],notes['B4'],notes['D5'],
	notes['C5'],notes['B4'],notes['C5'],notes['D5'],notes['C5'],notes['D5'],
	notes['E5'],notes['D5'],notes['C5'],notes['B4'],notes['A4'],notes['F5'],
	notes['E5'],notes['E5'],notes['F5'],notes['E5'],notes['D5'],
	notes['E5'],
]

final_countdown_tempo = [
	1,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,4,16,16,4,4,
	1,16,16,8,8,4,
	1,16,16,4,4,
	2,4,16,16,8,8,8,8,
	4,16,16,4,16,16,
	8,8,8,8,4,4,
	2,8,4,16,16,
	1,
]
'''


#// this calculates the duration of a whole note in ms
#wholenote = (60000 * 4) / tempo

#divider = 0, 
#noteDuration = 0

def buzz(frequency, length):	 #create the function "buzz" and feed it the pitch and duration)

	if(frequency==0):
		time.sleep(length)
		return
	period = 1.0 / frequency 		 #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
	delayValue = period / 2		 #calcuate the time for half of the wave
	numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
	for i in range(numCycles):		#start a loop from 0 to the variable "cycles" calculated above
		GPIO.output(buzzer_pin, True)	 #set pin 27 to high
		time.sleep(delayValue)		#wait with pin 27 high
		GPIO.output(buzzer_pin, False)		#set pin 27 to low
		time.sleep(delayValue)		#wait with pin 27 low
	


def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(buzzer_pin, GPIO.IN)
	GPIO.setup(buzzer_pin, GPIO.OUT)
	
def destroy():
	GPIO.cleanup()				# Release resource
	

def play(melody,tempo,pause,pace=0.800):
	
	for i in range(0, len(melody)):		# Play song
		
		noteDuration = pace/tempo[i]
		buzz(melody[i],noteDuration)	# Change the frequency along the song note
		
		pauseBetweenNotes = noteDuration * pause
		time.sleep(pauseBetweenNotes)
	
	
def main():
	while True:
		setup()
		#print("Popcorn Melody")
		#play(popcorn_melody, popcorn_tempo, 0.50, 1.000)
		#time.sleep(2)
		#print("Manaderna (Symphony No. 9) Melody")
		#play(manaderna_melody, manaderna_tempo, 0.30, 0.800)
		#time.sleep(2)
		print("Super Mario Theme")
		play(melody, tempo, 1.3, 0.800)
		time.sleep(2)
        #print("The Final Countdown")
        #play(final_countdown_melody, final_countdown_tempo, 0.30, 1.2000)
        #time.sleep(2)
        #print("Per Olssons Bonnagard (Old MacDonald Had A Farm) Melody")
        #play(bonnagard_melody, bonnagard_tempo, 0.30, 0.800)
        #time.sleep(2)
        #print("Manaderna (Symphony No. 9) Melody")
        #play(manaderna_melody, manaderna_tempo, 0.30, 0.800)
        #time.sleep(2)
        #print("Deck The Halls Melody")
        #play(deck_the_halls_melody, deck_the_halls_tempo, 0.30, 0.800)
        #time.sleep(2)
        #print("Crazy Frog (Axel F) Theme")
        #play(crazy_frog_melody, crazy_frog_tempo, 0.30, 0.900)
        #time.sleep(2)
        #print("Twinkle, Twinkle, Little Star Melody")
        #play(twinkle_twinkle_melody, twinkle_twinkle_tempo, 0.50, 1.000)
        #time.sleep(2)
        #print("Popcorn Melody")
        #play(popcorn_melody, popcorn_tempo, 0.50, 1.000)
        #time.sleep(2)
        #print("Star Wars Theme")
        #play(star_wars_melody, star_wars_tempo, 0.50, 1.000)
        #time.sleep(2)
		#print("Super Mario Theme")
		#play(melody, tempo, 1.3, 0.800)
		#time.sleep(2)
        #print("Super Mario Underworld Theme")
        #play(underworld_melody, underworld_tempo, 1.3, 0.800)
        #time.sleep(2)
        #print("Adventure Time Theme")
        #play(adventure_time_melody, adventure_time_tempo, 1.3, 1.500)
        

if __name__ == '__main__':		# Program start from here
	main()