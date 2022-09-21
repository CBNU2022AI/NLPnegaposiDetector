
"""

@author 최제현
@date 2022/09/21

댓글 객체

userID 유저 ID
content 댓글 내용

대댓글 포함

"""
class Reply:

    @property
    def userID(self):
        return self._userID

    @userID.setter
    def userID(self, userID):
        self._userID = userID

    @property
    def content(self):
        return self._content


    @content.setter
    def content(self, content):
        self._content = content

    @property
    def date(self):
        return self._date

    @date.setter
    def date(self, date):
        self._date = date