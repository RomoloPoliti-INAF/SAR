import smtplib
from SAR.config import conf
import rich_click as click
from email.headerregistry import Address
from email.message import EmailMessage
from MyCommonLib import debug_help_text


def page(item):
    text = f"""<html >
    <body >
    {item}
    </body>
    </html>
    """
    return text


def builtAdr(debug) -> tuple:
    out = []
    for item in conf.distribution:
        if debug:
            conf.console.log(item)
        parts = item .split(' ')
        name = ' '.join(parts[:-1])
        seg = parts[-1].split('@')

        out.append(Address(display_name=name, username=seg[0], domain=seg[1]))
    if debug:
        conf.console.log(out)
    return tuple(out)


def mail(subject, text: str = None, html: str = None, debug: bool = False):
    if debug:
        conf.console.log(conf.distribution)

    message = EmailMessage()
    message["Subject"] = f"[SAR] {subject}"
    message["From"] = Address(display_name='SAR bot',
                              username='sarbot', domain='localhost')  # sender_email
    message["To"] = builtAdr(debug)  # ', '.join(conf.distribution)
    # Create the plain-text and HTML version of your message
    if text is None:
        text = """\
    Hi,
    How are you?
    Real Python has many great tutorials:
    www.realpython.com"""
        html = None

    if html is None:
        html = """\
    <html>
    <body>
        <p>Hi,<br>
        How are you?<br>
        <a href="http://www.realpython.com">Real Python</a> 
        has many great tutorials.
        </p>
    </body>
    </html>
    """

    message.set_content(text)

    message.add_alternative(html, subtype='html')
    if debug:
        conf.console.print(text)
        conf.console.print(html)

    with smtplib.SMTP('localhost') as s:
        s.send_message(message)


@click.command()
@click.option('-d', '--debug', is_flag=True, help=debug_help_text, default=False)
def action(debug):
    txt = "Test mail"
    mail(subject="Test", text=txt, html=page(
        f"<strong>{txt}</strong><br/>"), debug=debug)


if __name__ == "__main__":
    action()
