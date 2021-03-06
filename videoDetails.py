import os
from googleapiclient.http import MediaFileUpload

class Video:
    description = "test description"
    category = "20"
    keywords = "vtubers"
    privacyStatus = "private"

    # makeOutputFileName()

    def getFileName(self, type):
        for file in os.listdir("E:\\Videos\\Youtube\\Upload"):
            if type == "video" and file.split(".", 1)[1] != "jpg":
                return file
                break
            elif type == "thumbnail" and file.split(".", 1)[1] != "mp4":
                return file
                break

    def insertThumbnail(self, youtube, videoId):
        thumnailPath = "E:\\Videos\\Youtube\\Upload\%s" % (self.getFileName("thumbnail"))

        request = youtube.thumbnails().set(
            videoId=videoId,
            media_body=MediaFileUpload(thumnailPath)
        )
        response = request.execute()
        print(response)