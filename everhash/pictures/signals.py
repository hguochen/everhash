# std lib imports
# django imports
from django.dispatch import receiver, Signal
from django.db.models.signals import pre_save 
from django.core.mail import EmailMessage
from django.contrib.auth.models import User
# 3rd party lib imports
# app imports
from pictures.models import Picture
from albums.models import Album
from everhash.settings.local import EMAIL_HOST_USER

pic_save = Signal()

@receiver(pic_save, sender=Picture)
def picture_save_handler(sender, **kwargs):
	picture_count = Picture.objects.filter(album=kwargs['instance'].album).count()
	album = Album.objects.get(name=kwargs['instance'].album)

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
			album.milestone += 100
			album.save()
			
