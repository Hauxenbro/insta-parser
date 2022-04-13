import instaloader
import json
import re

my_login = input('Введите свой логин или введите STANDART:\n')
user_name = input('Введите username профиля, пример в фигурных скобках (https://www.instagram.com/{kendalljenner}):\n')
my_password = input('Введите пароль от вашего аккаунта:\n')

load = instaloader.Instaloader()
load.login(my_login, my_password)

profile = instaloader.Profile.from_username(load.context, user_name)
photos = {}
answer = {user_name : photos}
likers = {}
commenters = {}
cnt = 0
pattern = r"<Profile (.+) "
for post in profile.get_posts():
    cnt += 1
    print(f'POST number {cnt} loading...')
    answer[user_name][cnt] = {'url' : '', 'likes' : '','comments' : {'profile' : '', 'text' : ''}}
    answer[user_name][cnt]['url'] = post.url + '\n'
    answer[user_name][cnt]['likes'] = post.likes
    for i in post.get_comments():
        profile_comm = re.findall(pattern, str(i.owner))[0]
        answer[user_name][cnt]['comments']['profile'] = profile_comm
        if profile_comm not in commenters.keys():
            commenters[profile_comm] = 1
        else:
            commenters[profile_comm] += 1
        answer[user_name][cnt]['comments']['text'] = str(i.text)
    for j in post.get_likes():
        like_prof = re.findall(pattern, str(j))[0]
        if like_prof not in likers.keys():
            likers[like_prof] = 1
        else:
            likers[like_prof] += 1
with open('answer_info.json', 'w') as ans_info:
    json.dump(answer, ans_info, indent = 1, sort_keys=True)

def get_maximas(info):
    max1, max2, max3, max4, max5 = (0,''),(0,''),(0,''),(0,''),(0,'')
    for i in info.keys():
        if info[i] >= max1[0]:
            max1, max2, max3, max4, max5 = (info[i], i), max1, max2, max3, max4
        elif info[i] >= max2[0]:
            max2, max3, max4, max5 = (info[i], i), max2, max3, max4
        elif info[i] >= max3[0]:
            max3, max4, max5 = (info[i], i), max3, max4
        elif info[i] >= max4[0]:
            max4, max5 = (info[i], i), max4
        elif info[i] >= max5[0]:
            max5 = (info[i], i)
    if info == likers:
        print('____ВАС БОЛЬШЕ ВСЕГО ЛАЙКАЮТ:____')
    else:
        print('____ВАС БОЛЬШЕ ВСЕГО КОММЕНТИРУЮТ:____')
    print(str(max1[1]) + ' likes: ' + str(max1[0]))
    print(str(max2[1]) + ' likes: ' + str(max2[0]))
    print(str(max3[1]) + ' likes: ' + str(max3[0]))
    print(str(max4[1]) + ' likes: ' + str(max4[0]))
    print(str(max5[1]) + ' likes: ' + str(max5[0]))
get_maximas(likers)
get_maximas(commenters)
final = input('Type something and press RETURN\n')
if final:
    print('Good Luck')

