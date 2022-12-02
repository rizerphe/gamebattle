import sys,time,random,traceback

def main():

    def slowprint(s):
        for c in s + '\n':
            sys.stdout.write(c)
            sys.stdout.flush()
            time.sleep(0.01)

    def board_on():
        a = input('>>> ')
        while a != "skip" and a != "board" :
            print('Please enter correct command')
            a = input()
        return a

    def board_off():
        b = input('>>> ')
        while b != "skip" and b != "go_out"  :
            print('Please enter correct command')
            b = input('>>> ')
        return b

    def after_menu():
        k = input('>>> ')
        while k != "again" and k != "exit"  :
            print('Please enter correct command')
            k = input('>>> ')
        return k

    def pay():
        p = input('>>> ')
        while p != "YES" and p != "NO"  :
            print('Please enter correct command')
            p = input('>>> ')
        return p

    def enter_number():
        while True:
            try: 
                m = int(input('>>> '))
                break
            except:
                print('Please enter suitable number')
        return m

    def enter_number_of_region():
        while True:
            try: 
                num = int(input('>>> '))
                if num == 1 or\
                    num == 2 or\
                    num == 3 or\
                    num == 4 or\
                    num == 5 or\
                    num == 6 or\
                    num == 73 :
                    break
                else:
                    raise Exception('')
            except Exception as e:
                print('Please enter suitable number')
        return num

    list_of_buses = [ 'Syhiv - Luhanska - Tsum - Pivdenniy - Motozavod - Levandivka - Bilohorscha' \
        , 'Arena Lviv - Stryyskyy park - Knyahini Olhy - Piskovi ozera - Skynya - Holovny Vokzal'\
        , 'Psyh likarnya - Horihovyi hai - Podatkova - LNU - Rynok square - Holosko - Epicenter']

    list_of_stops = [ ' Stryyskyy park ', 'Lebedyne ozero', 'Shota Rustaveli', 'Ploscha Rynok']

    slowprint('Disclaimer: some aspects of this game may not be understandable for non-UCU students')


    slowprint('In recent years, Lviv has been actively developing the city with high-rise buildings.')
    slowprint('In some cases, companies try and do well, but many developments destroy the spirit of the city.')
    slowprint('One of these projects wanted to build a complex in the green zone of Lviv. Our citizens,')
    slowprint('have been collecting votes against construction in the park for a month. One hundred thousand')
    slowprint('residents voted against. Your mission, should you choose to accept is to bring the' )
    slowprint('results to the mayor of the city so that he cancels the construction. Hurry up to save')
    slowprint('the city, today is the day of signing the contract in the Lviv City Hall.…')
    slowprint('')
    slowprint('If you enter your name - mission is yours')

    slowprint("Введіть своє ім'я: ")
    player_name = input(">>> ")\

    check_true = 1
    while check_true == 1 :
        try:
            slowprint(' Enter amount of money you want to take with you. Choose wisely.')
            user_money = enter_number()

            slowprint('Please type the number of the region in which you live to launch the appropriate version of the story.')
            slowprint('If you live in UCU type - 73 ')
            region_question = """
                You can choose from this list: 
                1 - Шевченківський район
                2 - Личаківський район
                3 - Сихівський район
                4 - Франківський район
                5 - Залізничний район
                6 - Галицький район
            """
            slowprint(region_question)
        
            region = enter_number_of_region()
            if region != 73:
                slowprint('A real student lives and studies in the UCU day and night')
                slowprint('Game failed')
                slowprint('Try again')
                check = 1/0
            else: 
                slowprint('You are on the bus stop. To board on the bus type - board')
                slowprint('To skip the bus type - skip')
                slowprint('You need a bus that goes through center')
                print('')
                for i in range(3):
                    print(list_of_buses[i])
                    what_to_do = board_on()
                    if i == 2 and what_to_do != 'board':
                        print('You missed your bus')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                    if i == 0 and what_to_do != 'skip':
                        print('You chose wrong bus')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                    if i == 1 and what_to_do != 'skip':
                        print('You chose wrong bus')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0


                slowprint('You can try to ride for free, but there is always chance to be caught')
                slowprint('Would you like to pay 15hrn - print YES or NO')
                print('')
                what_to_do_2 = pay()
                if what_to_do_2 == 'NO':
                    random_thing = random.randint(1 , 2)
                    if random_thing == 2:
                        print('Conductor decided to check you. Do you have modey to pay the fine(500 hrn)?')
                        print('')
                        user_money = user_money - 500
                        if user_money < 0:
                            print(' You dont have enought money')
                            slowprint('Game failed')
                            slowprint('Try again')
                            check = 1/0 
                        else:
                            print('Luckily you had enough money')

                slowprint('Bus is going through some stops. Your destination is Ratusha. Be attentive')    
                slowprint('Choose your stop. There is no stop named - Center')    
                slowprint('To stay in the bus type - skip, to go out type - go_out')
                print('')
                for j in range(4):
                    slowprint(list_of_stops[j])
                    what_to_do_3 = board_off()
                    if j == 3 and what_to_do_3 != 'go_out':
                        print('You missed your stop')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                    if j == 0 and what_to_do_3 != 'skip':
                        print('You got out to early')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                    if j == 1 and what_to_do_3 != 'skip':
                        print('You got out to early')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                    if j == 2 and what_to_do_3 != 'skip':
                        print('You got out to early')
                        slowprint('Game failed')
                        slowprint('Try again')
                        check = 1/0
                print('You are now in center, Ratusha is very close')
                if user_money > 1001:
                    slowprint('You have been robbed,because you had to much money.' )
                    slowprint('Moreover you spent too much time searching your wallet.' )
                    slowprint('Game failed')
                    slowprint('Try again')
                    check = 1/0
                    
                slowprint('- Hello I am guard of the Ratusha. If you are looking for our mayor,')
                slowprint('then you should know that he is in Kryyivka with some clients.')
                slowprint('If you have to tell him something, hurry up.')
                print(                      \
                                            \
                                            )
                slowprint('You ran to the Kryyivka in 30 seconds and there is a guard near it.')
                slowprint('There is almost no time.')
                print(                      \
                                                )
                slowprint('- I am a guard, to get to the mayor solve this equasion correctly')
                slowprint(' |x| = -(x+2)**2 + 2                    enter the sum of the solutions if necessary')
                print('')
            
                user_answer = enter_number()
                if user_answer != -3:
                    slowprint('Wrong answer')
                    slowprint('Game failed')
                    slowprint('Try again')
                    check = 1/0
                else:
                    print( 'Correct, you may enter')
                
                slowprint('Сongratulations, your actions helped save our city')
                slowprint('The only thing left to do is to go on a top of a Ratush')
                slowprint('and see our city from there.    Entrance fee is 50hrn')
                print('')
                if user_money - 50 < 0:
                    slowprint(' You dont have enough money, but stil mission is successful')
                    slowprint('You earned 5 STARS from 10')
                    print('')
                else:
                    slowprint('Congratulations, you are on the top of the Ratusha')
                    slowprint('You earned 10 STARS from 10,        enjoy the view')
                    print('')
                    

                print('If you want to start again type - again , if you want to exit type - exit')
                what_to_do_4 = after_menu()

                if what_to_do_4 == 'again':
                    ZeroDivisionError()
                else:
                    slowprint('Goodbye')
                    check_true = 0

        except Exception: 
            # traceback.print_exc()
            continue
main()
