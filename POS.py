class POS():
    def __init__(self):
        menu = open('menu.txt', 'w')
        menu.write('자장면:5000,짬뽕:6000,볶음밥:6000,탕수육:10000')
        menu.close()
        
        list_pay = open('list_pay.txt', 'w')
        list_pay.close()
        
        passw = input('POS 작동 시작합니다!\n비밀번호를 뭐로 설정할까요? : ')
        self.password = passw
        self.pay_stack = []
        
    def choose_mode(self):
        mod = -1
        while not mod in [0,1,2]:
            mod = int(input('무슨 모드로 접속하나요?(0:관리자, 1:메뉴 주문, 2:결제)\n:'))
        self.mode = mod
    
    def run(self):
        if self.mode == 0:
            key = input('비밀번호를 입력하세요! : ')
            if self.is_password(key):
                self.edit_menu()
            else: 
                print('비밀번호가 틀렸습니다!!!!!')
                return
        elif self.mode == 1:
            key = self.choose_menu() # [테이블 번호, ['자장면', 3, '탕수육', 4, ~]] 이런 식으로 넘길 생각
            self.stack_pay(key)
        
        elif self.mode == 2:
            key = int(input('테이블 번호를 입력하세요!! : '))
            if self.is_pay(key):
                self.pay(key)
            else:
                print('해당 테이블에는 주문이 없습니다!!')
        
    def is_password(self, key): #action : key와 패스워드 같은지 확인 / return : Bool 형 자료 반환
        return key == self.password
    
    def edit_menu(self):
        mod = -1
        menus = self.print_menu()
        
        while not mod in [0, 1]:
            mod = int(input('[0] : 메뉴 추가/가격 수정 [1] 메뉴 삭제 '))
        
        if mod == 0:
            name = input('메뉴명 : ')
            price = input('가격 : ')
            menus[name] = price
            print(f'[{name} : {price}] 추가!')
        elif mod == 1:
            name = input('메뉴명 : ')
            if name in menus.keys():
                del menus[name]
            else:
                print('해당 메뉴가 없습니다!')
        
        menu_f = open('menu.txt', 'w')
        text = ""
        for key in menus.keys():
            text += key + ':' + str(menus[key]) + ','
        text = text [:-1] # '자장면:5000,짬뽕:6000,볶음밥:6000,탕수육:10000' 처럼 끝에는 ,가 없도록 마지막 글자를 짤라냄
        menu_f.write(text)
        menu_f.close()
        self.menus = menus
            
        
    def print_menu(self): #action : 메뉴 출력 / return : 메뉴 목록 딕셔너리로 반환 
        print('\n메뉴 출력\n========================')
        menus = {}
        menu_file = open('menu.txt', 'r')
        temp = (menu_file.readlines()[0]).split(',')
        for t in temp:
            temp2 = t.split(':')
            menus[temp2[0]] = int(temp2[1])
            name = temp2[0]; price = int(temp2[1])
            print(f'{name}\t:{price}원')
        print('========================')
        menu_file.close()
        self.menus = menus
        return menus
    
    
    def choose_menu(self):
        orders = []
        while 1:
            order = -1
            menus = self.print_menu()

            while not order in menus.keys():
                order = input('메뉴 선택 : ')

            menu_no = int(input(f'{order}를 몇 개 시키실 건가요? : ' ))
            if order in orders:
                orders[orders.index(order) + 1] += menu_no
            else:
                orders.append(order)
                orders.append(menu_no)

            continue_or_not = -1
            while not continue_or_not in ['y','n','Y','N']:
                continue_or_not = input('더 주문하실 게 있으신가요? (y/n) : ')

            if continue_or_not in ['n', 'N']:
                break
        
        print('================================')
        for i in range(0, len(orders), 2):
            print(f'{orders[i]}\t: {orders[i+1]}\t : {self.menus[orders[i]] * orders[i+1]}원')
        print('================================\n')
        table_no = int(input('테이블 번호를 입력하세요! : '))
        
        return [table_no, orders]
        
        
        

    def stack_pay(self, key):
        table_no = key[0]
        orders = key[1]
        if len(orders)%2 != 0: #정상적인 경우 결제해야 하는 목록은 짝수여야 함
            print(f'결제 대기 목록에 이상이 있습니다 \n {orders}')
            return
        
        tot_price = 0
        for i in range(0, len(orders), 2):
            tot_price += self.menus[orders[i]] * orders[i+1]
        
        self.pay_stack.append([table_no, tot_price])
    
    def is_pay(self, key):
        for table_no_in_pay_stack in self.pay_stack:
            if key == table_no_in_pay_stack[0]:
                return True
            
        return False
    
    def pay(self, key):
        for table_no_in_pay_stack in self.pay_stack:
            if key == table_no_in_pay_stack[0]:
                # 카드인지 아닌지 묻기
                card_or_not = -1
                print(f'\n 총 금액 : {table_no_in_pay_stack[1]}')
                while not card_or_not in [0,1]:
                    card_or_not = int(input('어떤 방식으로 결제하시겠습니까? (0 : 현금, 1: 카드)\n :'))
                
                if card_or_not == 0:
                    cash = -1
                    while cash < table_no_in_pay_stack[1]:
                        cash = int(input('현금을 투입하세요 : '))
                    rest = cash - table_no_in_pay_stack[1]
                    print(f'거스름돈 반환 : {rest}')
                    list_pay = open('list_pay.txt', 'a')
                    list_pay.write(f'{table_no_in_pay_stack[0]} : {table_no_in_pay_stack[1]} 현금 결제\n')
                    
                    del self.pay_stack[self.pay_stack.index(table_no_in_pay_stack)]
                    list_pay.close()
                
                elif card_or_not == 1:
                    print('IC카드를 투입하세요!')
                    self.loading()
                    list_pay = open('list_pay.txt', 'a')
                    list_pay.write(f'{table_no_in_pay_stack[0]} : {table_no_in_pay_stack[1]} 카드 결제\n')
                    
                    del self.pay_stack[self.pay_stack.index(table_no_in_pay_stack)]
                    list_pay.close()
    
    
    
    def loading(self):
        import time
        i = 0
        time.sleep(.5)
        print('IC 카드를 뽑지 마세요!')
        animation = "|/-\\"
        idx = 0
        while i < 20:
            print(animation[idx % len(animation)], end="\r")
            idx += 1
            time.sleep(0.2)
            i += 1

        print('결제가 완료되었습니다!')
            

POS= POS()
while 1:
    POS.choose_mode()
    POS.run()
