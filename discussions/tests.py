from django.test import TestCase
from users.models import User, Address, Friendship, Status, Status_Comment
from discussions.models import Discussion, Discussion_Comment


# Create your tests here.


class DiscussionTestCase(TestCase):
    def setUp(self):
        adam = User.objects.create_user(username='adam',
                                        email='adam@web.de',
                                        password='adamweb',
                                        )
        eva = User.objects.create_user(username='eva',
                                       email='eva@web.de',
                                       password='evaweb',
                                       )
        discussion = Discussion.objects.create(owner=adam,
                                               title='discussion_title',
                                               message='discussion_message',
                                               )
        discussion.participants.add(eva)
        discussion.save()

    def test_discussion_is_setup(self):
        discussion = Discussion.objects.get(title="discussion_title")
        adam = User.objects.get(username="adam")
        self.assertEqual(discussion.owner, adam)
        self.assertEqual(discussion.message, "discussion_message")
        print(discussion.participants)


class Discussion_CommentTestCase(TestCase):
    def setUp(self):
        DiscussionTestCase.setUp(self)
        eva = User.objects.get(username="eva")
        discussion = Discussion.objects.get(title="discussion_title")
        Discussion_Comment.objects.create(message="comment",
                                          user=eva,
                                          discussion=discussion)

    def test_discussion_comment_is_setup(self):
        comment = Discussion_Comment.objects.get(message="comment")
        eva = User.objects.get(username="eva")
        discussion = Discussion.objects.get(title="discussion_title")
        self.assertEqual(comment.message, "comment")
        self.assertEqual(comment.user, eva)
        self.assertEqual(comment.discussion, discussion)
