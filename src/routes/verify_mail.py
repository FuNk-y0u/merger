from src.inc import *
from src.model import *
from src.defines import *


def send_mail(recipient_mail: str, subject: str, html: str):
	username = os.getenv("EMAIL_CLIENT_USERNAME")
	password = os.getenv("EMAIL_CLIENT_PASSWORD")
	sender   = os.getenv("EMAIL_SENDER")

	msg = MIMEMultipart('mixed')
	msg['Subject'] = subject
	msg['From']    = sender
	msg['To']      = recipient_mail

	html_message = MIMEText(html, 'html')
	msg.attach(html_message)

	mailServer = smtplib.SMTP('mail.smtp2go.com', 587)
	mailServer.ehlo()
	mailServer.starttls()
	mailServer.ehlo()
	mailServer.login(username, password)
	mailServer.sendmail(sender, recipient_mail, msg.as_string())
	mailServer.close()


def verify_mail(token: str) -> Response:
	try:
		object = jwt.decode(jwt=token, key=os.getenv('SECRET_KEY'), algorithms=["HS256"])
	except jwt.exceptions.ExpiredSignatureError as e:
		return MResponse(
			TOKEN_EXIPRED,
			"Token has been expired.",
			[]
		).as_json()
	except Exception as e:
		return MResponse(
			FAILED,
			"Token is invalid",
			[]
		).as_json()

	query = User.query.filter_by(email = object["email"]).first()
	query.is_verified = True

	pdb.session.add(query)
	pdb.session.commit()

	return MResponse(
		SUCESS,
		"Sucessfully Verified Email",
		[]
	).as_json()
