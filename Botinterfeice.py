import vk_api
from vk_api.longpoll import VkLongPoll, VkEventType
from vk_api.utils import get_random_id
from VkTools import VKTools
from token import access_token, community_token
from Viewed import add_user(), check_user()


class BotInterface():
    def __init__(self, access_token, community_token):
        self.bot = vk_api.VkApi(token=community_token)
        self.api = VKTools(access_token)
        self.params = None
        self.worksheets = []
    
    def message_send(self, user_id, message, attachment=None):
        self.bot.method('messages.send', {
                        'user_id': user_id,
                        'message': message,
                        'random_id': get_random_id(),
                        'attachment': attachment, }
                        )

    def handler(self):
        longpull = VkLongPoll(self.bot)

        for event in longpull.listen():
            if event.type == VkEventType.MESSAGE_NEW and event.to_me:
                messages = event.text.lower()
                context = ''
                if cotext == '':
                    if messages == 'привет':
                        self.params = self.api.get_profile_info(event.user_id)
                        self.message_send(event.user_id, f'привет {self.params["name"]}')
                        
                        if self.params['age'] == "None":
                            context += str("age")
                        if self.params['city'] == "None":
                            context += str("city")
                        if context == 'age':
                            self.message_send(event.user_id, f'У вас не достаточно информации на странице, напишите пожалуйста возраст, например: 40')
                        if context == 'city':
                            self.message_send(event.user_id, f'У вас не достаточно информации на странице, напишите пожалуйста город, например: Москва')
                        if context == 'agecity':
                            self.message_send(event.user_id, f'У вас не достаточно информации на странице, напишите пожалуйста возраст и город через пробел, например: 40 Москва')
                    elif messages == 'поиск':
                        self.message_send(event.user_id, f'Начинаем поиск')
                        if self.worksheets:
                            worksheet = self.worksheets.pop()
                        else:
                            self.worksheets = self.api.serch_users(self.params)
                            worksheet = self.worksheets.pop()
                            # проверка базы данных
                        saved_profiles = check_user()
                        while saved_profiles == "True":
                            if self.worksheets:
                                worksheet = self.worksheets.pop()
                            else:
                                self.worksheets = self.api.serch_users(self.params)
                                worksheet = self.worksheets.pop()    

                        photos_user = self.api.get_photos(worksheet['id'])

                        attachment = ' '
                        for num, photo in enumerate(photos_user):
                            attachment += f'photo{photo["owner_id"]}_{photo["id"]}'
                            if num == 2:
                                break
                        self.message_send(event.user_id, f'Встречайте {worksheet["name"]} ссылка:vk.com/{worksheet["id"]}', attachment=attachment)
                    # запись в базу данных
                        add_user()
                    elif messages == 'пока':
                        self.message_send(event.user_id, f'всего доброго')
                    else:
                        self.message_send(event.user_id, f'неизвестная команда')
                else:   
                    if context == 'age':
                        self.params['age'] = messages
                    elif context == 'city':
                        self.params['city'] = messages
                    elif context == 'agecity':
                        age_city = messages.split(' ')[0]
                        if age_city.isdigit() == "True":
                            self.params['age'] = age_city
                        else:
                            self.params['city'] = age_city
                        age_city_params = messages.split(' ')[1]
                        if age_city_params.isdigit() == "True":
                            self.params['age'] = age_city_params
                        else:
                            self.params['city'] = age_city_params
                    del context

if __name__ == '__main__':
    bot = BotInterface(community_token, access_token)
    bot.handler()
    
                
