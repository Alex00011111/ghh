import vk_api
from datetime import datetime
from vk_api.exceptions import ApiError
from token import access_token


class VKTools():
    def __init__(self, access_token):
        self.api = vk_api.VkApi(token=access_token)

    def get_profile_info(self, user_id):
        try:
            info, = self.api.method('users.get',
                                    {'user_id': user_id,
                                     'fields': 'city, bdate, sex, relation,'
                                     })
        except ApiError:
            return
        if 'bdate' in info:
            curent_year = datetime.now().year
            user_year = int(info['bdate'].split('.')[2])
            your_age = curent_year - user_year
        else:
            your_age = None
        user_info = {'name': info['first_name'] + ' ' + info['last_name'],
                     'id': info['id'],
                     'age': your_age,
                     'relation': info['relation'],
                     'sex': info['sex'],
                     'city': info['city']['id']
                     }

        return user_info

    def serch_users(self, params):

        sex = 1 if params['sex'] == 2 else 2
        city = params['city']
        age = params['age']
        age_from = age - 3
        age_to = age + 3
        relation = params['relation']

        users = self.api.method('users.search',
                                {'count': 50,
                                 'offset': 50,
                                 'age_from': age_from,
                                 'age_to': age_to,
                                 'sex': sex,
                                 'city': city,
                                 'relation': relation,
                                 'is_closed': False
                                 })
        try:
            users = users['items']
        except KeyError:
            return []

        res = []

        for user in users:
            if user['is_closed'] == "False":
                res.append({'id': user['id'],
                            'name': user['first_name'] + ' ' + user['last_name']
                            }
                           )
        return res

    def questionnaires(self):
        worksheets = []
        if worksheets:
            worksheet = worksheets.pop()
        else:
            worksheets = self.api.serch_users(self.params, self.offset)
            worksheet = worksheets.pop()
        return worksheet


    def get_photos(self, user_id):
        photos = self.api.method('photos.get',
                                 {'user_id': user_id,
                                  'album_id': 'profile',
                                  'extended': 1
                                  })
        try:
            photos = photos['items']
        except ApiError:
            return []

        res = []

        for photo in photos:
            res.append({'owner_id': photo['owner_id'],
                        'id': photo['id'],
                        'likes': photo['likes']['count'],
                        'comments': photo['comments']['count'],
                        })

        res.sort(key=lambda x: x['likes'] + x['comments'] * 10, reverse=True)

        return res
