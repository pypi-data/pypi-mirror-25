# Example handler. Used in tests

from django.contrib.auth.models import User


def appodeal_reward_create_handler(output, rewards):
    # Validate amount and currency
    # ...
    # Check impression_id for uniqueness
    # ...
    # Check if rewards exists
    if rewards.count() == 0:
        # User hasn't been rewarded
        profile = None
        try:
            profile = User.objects.get(user=output['user_id'])
            profile.reward(100)
            result = 'Rewarded with 100'
        except Profile.DoesNotExist:
            result = 'User does not exist'
    else:
        result = 'Already rewarded'
    return result
