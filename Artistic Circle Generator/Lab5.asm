##############################################################################################################
# Created by: 	Kohls, James
# 1		720315
# 3th of June, 	2020
#
# Assignment:	Lab 5, Functions and Graphics
#		CSE 12, Computer Systems and Assembly Language
# 		UCSC Spring Quarter
#
# Description:	This program takes predetermined inputs and will generate a picture using macros and functions
#
# Notes:	This program is designed to be run with the MARS IDE.
################################################################################################################

# Macro that stores the value in %reg on the stack 
#  and moves the stack pointer.
.macro push(%reg)
	subi $sp $sp 4
	sw %reg 0($sp)
.end_macro 

# Macro takes the value on the top of the stack and 
#  loads it into %reg then moves the stack pointer.
.macro pop(%reg)
	lw %reg 0($sp)
	addi $sp $sp 4	
.end_macro 

# %t1 = 0x00120045
# $t1 = 0x12
# $t2 = 0x45

#use and, or, shift to create this macro, bit isolation/ bit masking 


# Macro that takes as input coordinates in the format
# (0x00XX00YY) and returns 0x000000XX in %x and 
# returns 0x000000YY in %y

#------------------------------------------------#
# Get coordinates will take an input with 00xx00yy and break it into two registers of the callers choice
#the xx is done with a simple srl and the yy is done with but masking 

.macro getCoordinates(%input %x %y)

	srl %x, %input, 16		#creates %x just by shifting left 
	addi %y, %input, 0		#adds the values of %y to %input
	and %y, %y, 0x000000ff		#does an and to remove the pointless bits, the output
	
.end_macro

#li $t1 0x00120014
#getCoordinates($t1 $t2 $t3)

# Macro that takes Coordinates in (%x,%y) where
# %x = 0x000000XX and %y= 0x000000YY and
# returns %output = (0x00XX00YY)
.macro formatCoordinates(%output %x %y)

	add %output, %output, %x
	sll %output, %output, 16
	or %output, %output, %y
	
.end_macro 

#li $t3 0x00000012
#li $t4 0x000000ed
#formatCoordinates($t5 $t3 $t4)


.data
originAddress: .word 0xFFFF0000

.text
j done
    
    done: nop
    li $v0 10 
    syscall

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#  Subroutines defined below
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
#*****************************************************
#Clear_bitmap: Given a color, will fill the bitmap display with that color.
#   Inputs:
#    $a0 = Color in format (0x00RRGGBB) 
#   Outputs:
#    No register outputs
#    Side-Effects: 
#    Colors the Bitmap display all the same color
#*****************************************************

# first correct the gp to point at ffff0000
# while number of pixels less then total on screen:
#	increase bit counter by 4
#	replaces the value of that pixel with the color
#	very easy as all pixels are in sequental order, and not an array
clear_bitmap: nop
	
	add $gp, $zero, 0xffff0000
	
	push($t0)
	
	clear_bitmap_while:
		beq $t0, 16384, clear_bitmap_exit	# using t0 as our counter for this function
    		add $gp, $gp, 4        			# goes to the next pixel in the display 
    		sw $a0, -4($gp)        			# makes the pixel the predetermined color 
    		
    		add $t0, $t0, 1
    		j clear_bitmap_while			# repeats the loop
    	clear_bitmap_exit:
    	
    	pop($t0)
	
	jr $ra
	
#*****************************************************
# draw_pixel:
#  Given a coordinate in $a0, sets corresponding value
#  in memory to the color given by $a1	
#-----------------------------------------------------
#   Inputs:
#    $a0 = coordinates of pixel in format (0x00XX00YY)
#    $a1 = color of pixel in format (0x00RRGGBB)
#   Outputs:
#    No register outputs
#*****************************************************
# get coordinate with the macro
#	newValue = y * 128 + x
#	offset = newvalue + ffff #this ensures that the bit is lined up properly 
#	set the pointer to offset
#	pixels(offset) = color

draw_pixel: nop
	
	
	push($t0)				#ensures there is no register overlap
	push($t1)				#		
	push($t2)				#
	push($t3)				#
	
	#add $gp, $zero, 0xffff0000             # sets the counter to the beginning of the stack								     	                     -REGISTER SUMMARY-
	#li $t0 0				# makes sure t0 register are empty													t0 = used by getCoordinates
	#li $t1 0				# makes sure t1 register is empty
	#li $t2 0				# makes sure t1 register is empty	
	#li $t3 0				# makes sure t1 register is empty												 		t1, t2 = x and y coordinates 
						#															 		t3 = position of the gp pointer									
	getCoordinates($a0, $t1 $t2)		# $t1 = x, $t2 = y (we cannot use t0 for out first bit as this is used as masking in get coordinates)
	
	mul $t3, $t2, 128			# t3 = y * 128 to find position                                                 -The equation used was (y x 128 + x) 
	add $t3, $t3, $t1			# t3 = final position of the bit						-then times 4 to allign with the system
	mul $t3, $t3, 4				# alligns the coordinates with the bits
	add $t3, $t3, 0xffff0000		#adds the offset to t3, so t3 is the coordinate of the bit
	add $gp, $zero, $t3			# sets the pointer t3 to the position in the stack we want to edit   
	
	sw $a1, ($gp)     			# makes the pixel the predetermined color 
	
	pop($t3)				# puts back the removed values
	pop($t2)				#
	pop($t1)				#
	pop($t0)				#
	
	jr $ra
	
#*****************************************************
# get_pixel:
#  Given a coordinate, returns the color of that pixel	
#-----------------------------------------------------
#   Inputs:
#    $a0 = coordinates of pixel in format (0x00XX00YY)
#   Outputs:
#    Returns pixel color in $v0 in format (0x00RRGGBB)
#*****************************************************
# get coordinate with the macro, same as draw pixel but getting a value rather then saving it
#	newValue = y * 128 + x
#	offset = newvalue + ffff #this ensures that the bit is lined up properly 
#	set the pointer to offset
#	pixelColor = pixels(offset)
get_pixel: nop
	
	push($t0)
	push($t1)
	push($t2)
	push($t3)
	
	#add $gp, $zero, 0xffff0000             # sets the counter to the beginning of the stack								     	                     -REGISTER SUMMARY-
	#li $t0 0				# makes sure t0 register are empty													t0 = used by getCoordinates
	#li $t1 0				# makes sure t1 register is empty
	#li $t2 0				# makes sure t1 register is empty	
	#li $t3 0				# makes sure t1 register is empty												 		t1, t2 = x and y coordinates 
						#															 		t3 = position of the gp pointer									
	getCoordinates($a0, $t1 $t2)		# $t1 = x, $t2 = y (we cannot use t0 for out first bit as this is used as masking in get coordinates)
	
	mul $t3, $t2, 128			# t3 = y * 128 to find position                                                 -The equation used was (y x 128 + x) 
	add $t3, $t3, $t1			# t3 = final position of the bit						-then times 4 to allign with the system
	mul $t3, $t3, 4				# alligns the coordinates with the bits
	add $t3, $t3, 0xffff0000		#adds the offset to t3, so t3 is the coordinate of the bit
	add $gp, $zero, $t3			# sets the pointer t3 to the position in the stack we want to edit   
	
	lw $v0, ($gp)     			# makes the pixel the predetermined color 
	
	pop($t3)
	pop($t2)
	pop($t1)
	pop($t0)
	
	jr $ra

#***********************************************
# draw_solid_circle:
#  Considering a square arround the circle to be drawn  
#  iterate through the square points and if the point 
#  lies inside the circle (x - xc)^2 + (y - yc)^2 = r^2
#  then plot it.
#-----------------------------------------------------
# draw_solid_circle(int xc, int yc, int r) 
#    xmin = xc-r
#    xmax = xc+r
#    ymin = yc-r
#    ymax = yc+r
#    for (i = xmin; i <= xmax; i++) 
#        for (j = ymin; j <= ymax; j++) 
#            a = (i - xc)*(i - xc) + (j - yc)*(j - yc)	 
#            if (a < r*r ) 
#                draw_pixel(x,y) 	
#-----------------------------------------------------
#   Inputs:
#    $a0 = coordinates of circle center in format (0x00XX00YY)
#    $a1 = radius of the circle
#    $a2 = color in format (0x00RRGGBB)
#   Outputs:
#    No register outputs
#***************************************************
draw_solid_circle: nop

	push($ra)					# pushes all the registers to the stack to ensure their safety
	push($s0)					#
	push($s1)					#
	push($s2)					#
	push($s3)					#
	push($s4)					#
	push($s5)					#
	push($s6)					#
	push($s7)					#

	getCoordinates($a0, $t1 $t2)			# $t1 = x, $t2 = y (we cannot use t0 for out first bit as this is used as masking in get coordinates)					t0 = used by getCoordinates, t1 = xc, t2 = yc
	sub $s0, $t1, $a1				# s0 = xmin																t3 used by drawpixel
	add $s1, $t1, $a1				# s1 = xmax
	sub $s2, $t2, $a1				# s2 = ymin
	add $s3, $t2, $a1				# s3 = ymax
	
	#s0, s1  s2, s3 = min and max
	#s4 s5 = math
	
	
	circle_loop_one:
		bge $s0, $s1, exit_circle_loop_one		#s0 == xmin, s1 == xmax
		add $s0, $s0, 1
		circle_loop_two:
			bge $s2, $s3, exit_circle_loop_two	#s2 == ymin   s3 == ymax
			add $s2, $s2, 1
			
			sub $s4, $s0, $t1 			#calculates first part of equation ((i - xc))
			mul $s4, $s4, $s4			#doubles the value of $t7
			
			sub $s5, $s2, $t2 			#calculates second part of equation ((j - yc))
			mul $s5, $s5, $s5			#doubles the value of $t8 from the equation
			
			add $s4, $s4, $s5  			#t7 becomes a	#adds them together to complete the equation 
			mul $s5, $a1, $a1			#t8 becomes r
			
			
			blt $s4, $s5, print_the_pixel_please
			return_here:
			
			
			j circle_loop_two
		exit_circle_loop_two:
		sub $s2, $t2, $a1			# t5 = ymin
		
		j circle_loop_one
	exit_circle_loop_one:
		
	
	pop($s7)					# Pop the register values back 
	pop($s6)					#
	pop($s5)					#
	pop($s4)					#
	pop($s3)					#
	pop($s2)					#
	pop($s1)					#
	pop($s0)					#
	pop($ra)					#
	
	jr $ra
	
j continue_please
print_the_pixel_please: 			#This is the function that draws the pixel, we need to swap the a registres around so they line up properly with the other functions
		
			add $t5, $t5, 1		#just a counter variable
			
			li $t4, 0		#ensures that t4 is not pollouted
			formatCoordinates($t4, $s0, $s2)
			
			add $t6, $a0, $zero 	#saves a0 in t6
			add $a0, $t4, $zero	#puts t4 in a0
			
			add $t7, $a1, $zero 	#saves r to t7
			add $a1, $a2, $zero	#puts RGB data into a1
			
			#push($a1)
			#add $a1, $a2, $zero
			
			jal draw_pixel		#runs the draw pixel with the coordinates and color info
			
			add $a1, $t7, $zero	#puts back the radius value
			
			#pop($a2)
			
			add $a0, $t6, $zero 	#returns t6 to a0 
			
j return_here
continue_please:
#***********************************************
# draw_circle:
#  Given the coordinates of the center of the circle
#  plot the circle using the Bresenham's circle 
#  drawing algorithm 	
#-----------------------------------------------------
# draw_circle(xc, yc, r) 
#    x = 0 
#    y = r 
#    d = 3 - 2 * r 
#    draw_circle_pixels(xc, yc, x, y) 
#    while (y >= x) 
#        x=x+1 
#        if (d > 0) 
#            y=y-1  
#            d = d + 4 * (x - y) + 10 
#        else
#            d = d + 4 * x + 6 
#        draw_circle_pixels(xc, yc, x, y) 	
#-----------------------------------------------------
#   Inputs:
#    $a0 = coordinates of the circle center in format (0x00XX00YY)
#    $a1 = radius of the circle
#    $a2 = color of line in format (0x00RRGGBB)
#   Outputs:
#    No register outputs
#***************************************************
draw_circle: nop

	push($ra)
	push($s0)
	push($s1)
	push($s2)
	push($s3)
	push($s4)
	push($s5)
	push($s6)
	push($s7)
	
	li $s0, 0		# x			s0 = x
	add $s1, $a1, $zero	# y = r			s1 = y
	#add $s1, $s1, 1	# y = r			s1 = y
	mul $s2, $a1, 2		# 2 * r
	li $s5, 3
	sub $s2, $s5, $s2		# d = 3 - r * 2   	s2 = d
	
	
	push($a1)		# draw_circle_pixels(xc, yc, x, y) 
	add $a1, $a2, $zero	#
	add $a2, $s0, $zero	#
	add $a3, $s1, $zero	#
		push($a3)
		push($a2)
		push($a1)
		push($a0)
		push($s0)
		push($s1)
		push($s2)
		push($s3)
		push($s4)
	jal draw_circle_pixels	#
		pop($s4)
		pop($s3)
		pop($s2)
		pop($s1)
		pop($s0)
		pop($a0)
		pop($a1)
		pop($a2)
		pop($a3)
	add $a2, $a1, $zero	#
	pop($a1)		#
	

	draw_circle_loop:
	
		blt $s1, $s0, exit_draw_circle_loop
		add $s0, $s0, 1
		bgez $s2, condition_one # if d > 0
					
		# -ELSE- # d = d + 4 * x + 6
		
		mul $s3, $s0, 4		# 4 * x
		add $s3, $s3, 6		# 4 * x + 6
		add $s2, $s2, $s3 	# d = d + 4 * x + 6
		
		
			
		add $t9, $t9, 1		# a counter variable for counting how many times the else statement runs
		
		j skip_condition_one
		
		condition_one:		# IF 
		
		sub $s1, $s1, 1
		
		sub $s3, $s0, $s1	# (x - y)
		mul $s3, $s3, 4		# 4 * (x - y)
		add $s3, $s3, 10	# 4 * (x - y) + 10  
		add $s2, $s2, $s3	# d = d + 4 * (x - y) + 10  
		
		
		
		
		
		
		add $t8, $t8, 1	# a counter variable for counting how many times the if statement runs
			
		skip_condition_one:
		
		
					# draw_circle_pixels(xc, yc, x, y) 
		push($a1)		# saves the r to the stack
		add $a1, $a2, $zero	# moves the color to the a1 position
		add $a2, $s0, $zero	# moves x to the a2
		add $a3, $s1, $zero	# moves y to the a1
			push($a3)
			push($a2)
			push($a1)
			push($a0)
			push($s0)
			push($s1)
			push($s2)
			push($s3)
			push($s4)
		jal draw_circle_pixels	#
			pop($s4)
			pop($s3)
			pop($s2)
			pop($s1)
			pop($s0)
			pop($a0)
			pop($a1)
			pop($a2)
			pop($a3)
		add $a2, $a1, $zero	#
		pop($a1)		#
		
		
		
		j draw_circle_loop
	exit_draw_circle_loop:
	
	
	#getCoordinates($a0, $t1 $t2)		# $t1 = x, $t2 = y 				t0 = used by getCoordinates, t1 = xc, t2 = yc
	#jal draw_circle_pixels
	
	
	pop($s7)
	pop($s6)
	pop($s5)
	pop($s4)
	pop($s3)
	pop($s2)
	pop($s1)
	pop($s0)
	pop($ra)
	
	jr $ra
	
#*****************************************************
# draw_circle_pixels:
#  Function to draw the circle pixels 
#  using the octans' symmetry
#-----------------------------------------------------
# draw_circle_pixels(xc, yc, x, y)  
#    draw_pixel(xc+x, yc+y) 
#    draw_pixel(xc-x, yc+y)
#    draw_pixel(xc+x, yc-y)
#    draw_pixel(xc-x, yc-y)

#    draw_pixel(xc+y, yc+x)
#    draw_pixel(xc-y, yc+x)
#    draw_pixel(xc+y, yc-x)
#    draw_pixel(xc-y, yc-x)
#-----------------------------------------------------
#   Inputs:
#    $a0 = coordinates of circle center in format (0x00XX00YY)
#    $a1 = color of pixel in format (0x00RRGGBB)
#    $a2 = current x value from the Bresenham's circle algorithm
#    $a3 = current y value from the Bresenham's circle algorithm
#   Outputs:
#    No register outputs	
#*****************************************************
draw_circle_pixels: nop
	
	push($ra)
	push($s0)
	push($s1)
	push($s2)
	push($s3)
	push($s4)
	push($s5)
	push($s6)
	push($s7)
	

	
	getCoordinates($a0, $s0 $s1)		# $s0 = xc, $s1 = yc, $a2 = x, $a3 = y
	
	
	add $s2, $s0, $a2			# xc+x
	add $s3, $s1, $a3			# yc+y
	add $s4, $a0, $zero
	li $a0, 0
	formatCoordinates($a0, $s2, $s3)		#writes the new coordinate in a0
	jal draw_pixel
	add $a0, $s4, $zero				#puts a0 back
	
	#j skipphere
	
	sub $s2, $s0, $a2			# xc-x 
	add $s3, $s1, $a3			# yc+y
	push($a0)			#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s2, $s3)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	add $s2, $s0, $a2			# xc+x
	sub $s3, $s1, $a3			# yc-y
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s2, $s3)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	sub $s2, $s0, $a2			# xc-x
	sub $s3, $s1, $a3			# yc-y
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s2, $s3)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	#---------------------------------------#
	
	
	add $s2, $s1, $a2			# xc+y
	add $s3, $s0, $a3			# yc+x
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s3, $s2)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	sub $s2, $s1, $a2			# xc-x 
	add $s3, $s0, $a3			# yc+y
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s3, $s2)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	add $s2, $s1, $a2			# xc+x
	sub $s3, $s0, $a3			# yc-y
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s3, $s2)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	sub $s2, $s1, $a2			# xc-x
	sub $s3, $s0, $a3			# yc-y
	push($a0)				#saves the original a0 in the stack
	li $a0, 0
	formatCoordinates($a0, $s3, $s2)		#writes the new coordinate in a0
	jal draw_pixel
	pop($a0)				#puts a0 back
	
	
	skipphere:
	
	pop($s7)
	pop($s6)
	pop($s5)
	pop($s4)
	pop($s3)
	pop($s2)
	pop($s1)
	pop($s0)
	pop($ra)
	
	jr $ra
