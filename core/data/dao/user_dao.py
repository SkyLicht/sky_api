from colorama import Fore, Style


class UserDAO:
    def __init__(self, connection):
        self.session = connection
        # logger

    def query_all(self):
        try:
            cursor = self.session.cursor()
            cursor.execute('select * from user')
            result = cursor.fetchall()
            print(f"{Fore.GREEN}Data fetched from user.{Style.RESET_ALL}")
            return result

        except Exception as e:
            print(f"{Style.BRIGHT}{e}{Style.RESET_ALL}")
            return None


    def query_add_user(self, user):
        try:

            self.session.add(user)
            self.session.commit()
            print(f"{Fore.GREEN}User pushed{Style.RESET_ALL}")
            self.session.close()
            print(f"{Fore.GREEN}Session close{Style.RESET_ALL}")
        except Exception as e:
            print(f"{Fore.RED}{e}{Style.RESET_ALL}")



