from modelos import user

'''

Main app

'''
class CLIApp:
    def __init__(self, service, profile_service=None, nutrition_service=None):
        self.service = service
        #self.profile_service = profile_service
        #self.nutrition_service = nutrition_service


    def execute(self, user : user):
        print(f"Bem-vindo! {user.email}!")

