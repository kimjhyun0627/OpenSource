#!/usr/bin/python3

import HW06
while(1):
    num = input("Select menu: 1)b2h 2)integerUnionIntersection 3)fibo 4)exit ? ")
    if num == "exit": 
        quit()
    else:
        if num == '1':
            #import HW06.b2h
            print("b2h")

        elif num == '2':
            import HW06.integerUnionIntersection

        elif num == '3':
            import HW06.fibo
        
        elif num == '4':
            print("exit the program...")
            quit()
        
        else:
            print("you choose wrong number ")
            
        