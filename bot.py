import praw
import config
from haishoku.haishoku import Haishoku
import haishoku.haillow
import pyimgur
import os

#logs the bot into reddit
def authenticate():
	print("Authenticating...")
	#creates reddit instance
	reddit = praw.Reddit(username = config.username,
		password = config.password,
		client_id = config.client_id,
		client_secret = config.client_secret,
		user_agent = "Joshua's palette_bot")
	print("Successfully Authenticated!!")
	return reddit

def run_bot(reddit):
	print("Obtaining Submissions...")

	for comment in reddit.inbox.mentions(limit=None):
		footer = "\n\n ^I'm&nbsp;a&nbsp;bot.&nbsp;|&nbsp;Creator:&nbsp;[u/JoshuaScript](https://www.reddit.com/u/JoshuaScript).&nbsp;|&nbsp;[Source&nbsp;Code](https://github.com/Joshuascript/Palette_Bot)"
		#checks if the mention is unread, which is only the case if it hasn't been replied to
		if comment.new:
			try:
				#calls the showPalette (which creates and saves the image) method on the image link
				Haishoku.showPalette(comment.submission.url)
				CLIENT_ID = config.imgur_id
				PATH = haishoku.haillow.image_name
				im = pyimgur.Imgur(CLIENT_ID)
				uploaded_image = im.upload_image(PATH, title=f"Color Palette for Reddit Post: {comment.submission.title} ({comment.submission.url})" )
				print(uploaded_image.title)
				print(uploaded_image.link)
				print(uploaded_image.size)
				print(uploaded_image.type)
				comment.reply(f"\n\n Here is the color palette of this image visualized: {uploaded_image.link}. The color sizes are proportionate to their dominance in the image. {footer}")
				#Marks the comment as read so it won't be replied to again
				comment.mark_read()
				print(f"Replied to {comment.submission.title} ({comment.submission.url})")
				#deletes generated palette image from local storage
				os.remove(PATH)
			except OSError as e:
				comment.reply(f"This is most likely a non-image post. Try mentioning me in a new comment and I may be able to get this post's palette if it is an image.{footer}")
				print(f"Comment was most likely on a non-image post ({e}) \n\n Title: {comment.submission.title}, Link: {comment.submission.url}" )
				comment.mark_read()
			except TypeError as e:
				comment.reply(f"I was unable to get the palette of this image, most likely because it's a gif, which is currently unsupported.{footer}")
				print(f"Image was likely a gif ({e}) \n\n Title: {comment.submission.title}, Link: {comment.submission.url}")
				comment.mark_read()
			except Exception as e:
				print(e.__class__.__name__ + e)
		else:
			continue

reddit = authenticate()
run_bot(reddit)