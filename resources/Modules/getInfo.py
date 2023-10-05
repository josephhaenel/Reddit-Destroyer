class InfoExtractor:

    @staticmethod
    def getCommentText(comment):
        commentText = comment.find(id="-post-rtjson-content")
        if commentText is None:
            return ''
        elif isinstance(commentText, str):
            return commentText.strip()
        else:
            return commentText.get_text().strip()

    @staticmethod
    def getCommentLikes(comment):
        commentLikes = comment.get('score')
        if not commentLikes:
            return 0
        return int(commentLikes) if commentLikes else 0

    @staticmethod
    def getCommentUsername(comment):
        commentUsername = comment.find(
            'a', class_="font-bold text-neutral-content-strong text-12 hover:underline")
        return commentUsername.get_text(strip=True) if commentUsername else None

    @staticmethod
    def getCommentDate(comment):
        commentDate = comment.find('time')
        return commentDate['title'] if commentDate and 'title' in commentDate.attrs else None
