def create_three(username, function):
    try:
        root_object = Person.objects.get(full_name=instagram_username)
    except:
        root_object = Person.objects.create(full_name=instagram_username)
    friends = inst.get_friends_list_by_instagram_username(instagram_username)
    for root_friend in friends:
        try:
            root_friend_object = Person.objects.create(full_name=root_friend, parent=root_object)

            for friend_lvl_2 in inst.get_friends_list_by_instagram_username(root_friend):
                try:
                    friend_lvl_2_object = Person.objects.create(full_name=friend_lvl_2, parent=root_friend_object)
                except:
                    continue
        except:
            continue