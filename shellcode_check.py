#!/usr/bin/python
#paste shellcode continous in quotes i.e. "\xfc\x6a\xeb\x47\xe8\xf9\xff\xff\xff\x60\........"

import sys
import pylibemu


shellcode = input("Enter shellcode : " )

emulator = pylibemu.Emulator()
offset = emulator.shellcode_getpc_test(shellcode)

emulator.prepare(shellcode, offset)
emulator.test()

if offset >= 0:

    print "Shellcode detected. "
    print emulator.emu_profile_output

else:
    print "No shellcode was detected. "
