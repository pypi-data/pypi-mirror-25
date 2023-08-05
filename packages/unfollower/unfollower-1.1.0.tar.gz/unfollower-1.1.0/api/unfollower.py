from app import printer


class Unfollower():
    """This class is intended to provide APIs to unfollow all friends ( who unfollowed you ) """

    def __init__(self, api):
        self.api = api

    def _get_friends(self):
        return self.api.GetFriends()

    def destroyAllFriendships(self, only_non_follower=False, friends=None, print_on_delete=False):

        if friends is None:
            friends = self.api.GetFriends()

        if len(friends) == 0:
            printer.print_green("You aren't following anyone already. You are a true leader.")
            return

        for friend in friends:
            if print_on_delete:
                printer.print_yellow("Destroying friendship with user: " + friend.id)
            self.api.DestroyFriendship(user_id=friend.id)
        printer.print_green("You have successfully unfollowed all losers.")
