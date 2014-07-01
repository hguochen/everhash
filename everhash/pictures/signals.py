# std lib imports
# django imports
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_save 
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
# 3rd party lib imports
# app imports
from .models import Picture
from albums.models import Album
from everhash.settings.local import EMAIL_HOST_USER

send_email = Signal()

@receiver(send_email, sender=Picture)
def picture_save_handler(sender, **kwargs):
	"""
	Handle the action when send_email() signal is fired. This handler retrieves album and 
	pictures data from database and send album owner a notification email for every successive 
	100 pictures in album until a maximum of 500 pictures in a album.
	"""
	# retrieve latest picture count and album milestone
	picture_count = Picture.objects.filter(album=kwargs['instance'].album).count()
	album = Album.objects.get(name=kwargs['instance'].album)

	# if picture count is less than 500 in album and less than current milestone, send a
	# notification email
	if picture_count <= 500:
		if picture_count >= album.milestone:
			# set email contents
			from_email = EMAIL_HOST_USER
			album = Album.objects.get(name=kwargs['instance'].album)
			to_email = []
			to_email.append(album.user.email)
			bcc = []
			bcc.append(EMAIL_HOST_USER)	
			subject="#" + str(kwargs['instance'].album) + " has " + str(picture_count) + " photos"
			message_body = "I'm awesome!"
			
			#send the email
			email = EmailMessage(
				subject,
				message_body,
				from_email,
				to_email,
				bcc,
				)
			email.send()
			# milestone reached. update to new milestone.
			album.milestone += 100
			album.save()
	return
			
