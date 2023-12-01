class InfoExtractor:
    '''
    The InfoExtractor class provides utility methods to extract specific pieces of information
    from a given Reddit comment object, which is presumably a BeautifulSoup element.

    The class contains static methods to retrieve:
    - Comment text
    - Comment likes (score)
    - Comment username
    - Comment date
    '''
    
    @staticmethod
    def getCommentText(comment):
        '''
        Extracts the text content of a given comment.

        Parameters:
        - comment (BeautifulSoup element): The comment element to extract text from.

        Returns:
        - str: The extracted text or an empty string if not found.
        '''
        commentText = comment.find(id="-post-rtjson-content")
        if commentText is None:
            return ''
        elif isinstance(commentText, str):
            return commentText.strip()
        else:
            return commentText.get_text().strip()

    @staticmethod
    def getCommentLikes(comment):
        '''
        Extracts the like count (score) of a given comment.

        Parameters:
        - comment (BeautifulSoup element): The comment element to extract likes from.

        Returns:
        - int: The like count or 0 if not found.
        '''
        commentLikes = comment.get('score')
        if not commentLikes:
            return 0
        return int(commentLikes) if commentLikes else 0
    
    @staticmethod
    def getCommentUsername(comment): # No Longer Working
        '''
        Extracts the username associated with a given comment.

        Parameters:
        - comment (BeautifulSoup element): The comment element to extract the username from.

        Returns:
        - str: The extracted username or None if not found.
        '''
        commentUsername = comment.find(
            'a', class_="font-bold text-neutral-content-strong text-12 hover:underline")
        return commentUsername.get_text(strip=True) if commentUsername else None

    @staticmethod
    def getCommentDate(comment):
        '''
        Extracts the date associated with a given comment.

        Parameters:
        - comment (BeautifulSoup element): The comment element to extract the date from.

        Returns:
        - str: The extracted date or None if not found.
        '''
        commentDate = comment.find('time')
        return commentDate['title'] if commentDate and 'title' in commentDate.attrs else None
