import random

position = str(random.randint(0,100)) + " " + str(random.randint(0,100))
position2 = str(random.randint(0,100)) + " " + str(random.randint(0,100))

print(position+','+position2)
receive = (position+','+position2)


def read_pos(str):
    str = str.split(",")
    for st in str:
        str2 = st.split(" ")
        print(int(str2[0]), int(str2[1]))

read_pos(receive)