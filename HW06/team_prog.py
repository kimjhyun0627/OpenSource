#!/usr/bin/python3

import mypkg
while(1):
    num = input("Select menu: 1)b2h 2)integerUnionIntersection 3)fibo 4)exit ? ")
    if num == "exit": 
        quit()
    else:
        if num == '1':
            import mypkg.b2h
            print("b2h")

        elif num == '2':
            import mypkg.integerUnionIntersection

        elif num == '3':
            import mypkg.fibo
        
        elif num == '4':
            print("exit the program...")
            quit()
        
        else:
            print("you choose wrong number ")
            
        