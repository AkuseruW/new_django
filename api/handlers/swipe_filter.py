from api.models.User import UserPreference

def is_age_within_range(user_age, min_age, max_age):
    return min_age <= user_age <= max_age

def is_gender_and_relationship_match(user_preferences, user_by_distance_preferences):
    return user_preferences.interested_in == user_by_distance_preferences.interested_in and \
           user_preferences.relationship == user_by_distance_preferences.relationship

def filter_profiles(current_user, user_preferences, nearby_users):
    current_user_age = current_user.profile.user_age()
    current_user_age_range = (user_preferences.age_min, user_preferences.age_max)
    current_user_blocked_users = current_user.blocked.all()
    current_user_liked_users = current_user.likes.all()
    
    matching_users = []
    for nearby_user in nearby_users:
        nearby_user_blocked_users = nearby_user.blocked.all()
        
        if nearby_user in current_user_blocked_users or nearby_user in current_user_liked_users:
            continue
        
        if current_user in nearby_user_blocked_users:
            continue        
        
        nearby_user_preferences = UserPreference.objects.get(user=nearby_user)
        nearby_user_age = nearby_user.profile.user_age()
        nearby_user_age_range = (nearby_user_preferences.age_min, nearby_user_preferences.age_max)
        nearby_user_distance_preference = nearby_user_preferences.location_max_distance
        nearby_user_distance = nearby_user.location.distance(current_user.location)
        
        if (is_age_within_range(nearby_user_age, *current_user_age_range) and
            is_age_within_range(current_user_age, *nearby_user_age_range) and
            nearby_user_distance <= nearby_user_distance_preference and
            is_gender_and_relationship_match(user_preferences, nearby_user_preferences)):
            matching_users.append(nearby_user)

    return matching_users