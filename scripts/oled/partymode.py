#!/usr/bin/python

import ledfun as oled
from time import sleep

oled.init_display()
oled.display_off()
oled.display_on(show_cursor=False)
oled.lib_credits()


def main():
    oled.clear_display()
    sch=2
    for col in range(16):
        oled.set_pos(1,col)
        
        if sch == 2 or sch == 3:
            oled.write_raw_data(sch)
        else:
            oled.write_string(sch)

        if sch == 2:
            sch = 3
        elif sch == 3:
            sch = " "
        else:
            sch = 2
    for count in range(20):
        oled.set_pos(0,0)
        oled.write_raw_data(5)
        oled.set_pos(0,3)
        oled.write_raw_data(4)
        oled.set_pos(0,6)
        oled.write_raw_data(5)
        oled.set_pos(0,10)
        oled.write_raw_data(4)
        oled.set_pos(0,14)
        oled.write_raw_data(5)
        sleep(0.5)
        oled.set_pos(0,0)
        oled.write_raw_data(4)
        oled.set_pos(0,3)
        oled.write_raw_data(5)
        oled.set_pos(0,6)
        oled.write_raw_data(4)
        oled.set_pos(0,10)
        oled.write_raw_data(5)
        oled.set_pos(0,14)
        oled.write_raw_data(4)
        sleep(0.5)


    
    for col in range(16):
        oled.set_pos(0,col)
        oled.write_string(" ")

    for col in [10,3,6,4,8,9,12,4,13,3,15,8]:
        oled.set_pos(0,col)
        oled.write_raw_data(5)
        sleep(0.5)
        oled.set_pos(0,col)
        oled.write_raw_data(4)
        sleep(0.5)
        oled.set_pos(0,col)
        oled.write_string(" ")

    for col in range(16):
        oled.set_pos(0,col)
        oled.write_string(" ")

    oled.set_pos(0,0)    
    display = "D E R B Y  C O N"
    oled.write_string(display.center(16), typeomatic_delay=1)


if __name__ == '__main__':
    main()


