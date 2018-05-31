import random
def get_photos(vk_session, id_group,vk):
    try:
        attachment = ''
        for i in range(5):
            max_num = vk.photos.get(owner_id=id_group, album_id='wall', count=0)['count']
            num = random.randint(1, max_num)
            pictures = vk.photos.get(owner_id=str(id_group), album_id='wall', count=1, offset=num)['items'][0]['id']
            if len(attachment)<4:
                attachment ='photo' + str(id_group) + '_' + str(pictures)
            else:
                attachment =attachment +',' + 'photo' + str(id_group) + '_' + str(pictures)
            del max_num
            del num
            del pictures
        print(attachment)
        return attachment
    except:
        get_photos(vk_session, id_group, vk)