# ---------- For profile completion progressbar -------------- 
def calculate_profile_completion(user_profile):
    checks = [
        (user_profile.profile_picture, "adding profile picture", 20),
        (user_profile.bio and len(user_profile.bio) > 9, "adding your bio (atleast 10 characters)", 20),
        (user_profile.department and user_profile.year, "adding both department and year of study", 20),
        (user_profile.location, "adding your place", 10),
        (user_profile.interests, "adding your interests", 20),
    ]
    
    missing = []
    percentage = 10  # base
    
    for has_field, message, points in checks:
        if has_field:
            percentage += points
        else:
            missing.append(message)
    
    return {
        "percentage": min(100, percentage),  # Cap at 100%
        "missing": missing
    }
