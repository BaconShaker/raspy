#!/usr/bin/python
import serial,time

# Set screen width in characters
SCREEN_WIDTH = 16

# Initialize serial connection
disp = serial.Serial(port='/dev/ttyAMA0', baudrate=19200)

# Set display to with cursor blink (25 for blinking cursor)
disp.write(chr(22))

# Set backlight to true
disp.write(chr(17))

# Initialize screen
disp.write("Hello,")
disp.write(chr(148))
disp.write("I am the screen")
time.sleep(3)

# Clear screen; we must pause at least 5 ms after this command
disp.write(chr(12))
time.sleep(0.01)


def scrolltext(text):

    # Move cursor to far right of screen, in preparation for scrolling
    cursor_start = 143

    # Initialize window's head and tail
    head = tail = 0

    while tail <= len(text):

        # Actually move the cursor to the far right as set above
        disp.write(chr(cursor_start))

        # Write out text "window"
        disp.write(text[head:tail])

        # Move the start cursor depending on whether or not the text
        # has reached the far left of the screen, as it scrolls to the left
        cursor_start = cursor_start - 1 if not cursor_start <= 128 else 128

        # Updated window  tail
        tail += 1

        # Update window head
        head = head + 1 if tail >= SCREEN_WIDTH else 0
	#disp.write(chr(214))
	#disp.write(chr(223))
        time.sleep(0.4)
        

def disp_bal(balance = "No record" , name = "None"):
	# Make a sound so we know the swipe worked. 
	disp.write(chr(216))
	disp.write(chr(209))
	disp.write(chr(223))
	disp.write(chr(225))
	disp.write(chr(227))
	
	# Clear the screen. 
	disp.write(chr(12))
	time.sleep(.01)
	
	# write some words
	disp.write(str(name))
	
	# Move down a line
	disp.write(chr(13))
	
	# Print the balance and wait
	disp.write("    $" + str(balance))
	time.sleep(5)
	
	# Clear the screen. 
	disp.write(chr(12))
	time.sleep(.01)
	
	
	

# Now scroll some text
#~ scrolltext("Now let's test this thing. What happens now though?")
#~ disp_bal()
