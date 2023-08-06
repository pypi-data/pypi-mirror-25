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
            user = User.objects.get(username=output['user_id'])
            # reward(user, 100)
            result = 'Rewarded with 100'
        except User.DoesNotExist:
            result = 'User does not exist'
    else:
        result = 'Already rewarded'
    return result
