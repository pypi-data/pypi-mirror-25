import base64

from sendgrid.helpers.mail.mail import Email, Personalization, Mail, Category, Attachment, Content, Substitution

from sendgrid_sdk.client import SendGridException


class MessageBuilder(object):
    """
    Given the necessary information, constructs a SendGrid email message using the library's helper classes. When
    sending emails, subclass this class and call its `get_message()` method to get the JSON content. Override the
    class attributes `category` and `template_id`!

    Has a few overridable methods for customisation. The most important one is the `get_template_substitutions()`,
    used to provide the builder with values that get injected to the SendGrid template.
    """
    category = None
    template_id = None

    def __init__(self, from_address, from_name, to_address, subject):
        if not self.category:
            raise SendGridException('`category` has to be specified.')
        if not self.template_id:
            raise SendGridException('`template_id` has to be specified.')

        self.sender = Email(email=from_address, name=from_name)
        self.receiver = to_address
        self.subject = subject

        self.message = Mail()
        self.personal = Personalization()

    def get_message(self):
        self._set_basic_information()
        self.personal.add_to(Email(self.receiver))
        self._set_attachments()
        self._set_message()
        msg = self.message.get()
        return msg

    def get_attachments(self):
        """
        Override to add attachments to the email message.
        The method should return a list of dictionaries containing a File object, the file name and the MIME type.

        Example:
        f = file_obj.file.read()
        f_name = file_obj.name
        mime_type = 'application/vnd.ms-excel'
        return [
            {
                'file': f,
                'file_name': f_name,
                'mime_type': mime_type
            }
        ]
        """
        return []

    def get_substitutions(self):
        """
        Override this method to provide per-template values that are injected to the SendGrid template.
        The dictionary keys have to match ones in the SendGrid template.

        return {
            'USER_NAME': 'User Name',
            'USER_ID': '666'
        }
        """
        raise NotImplementedError('.get_template_substitutions() has to be implemented in subclass.')

    def set_content(self):
        """
        The JSON blob that gets sent to SendGrid needs to have these fields populated, even if the actual message
        content is populated in their end according to the template ID.

        If you want to add something as a fallback, override this method with something populated as the second
        argument of the Content object.
        """
        self.message.add_content(Content('text/plain', ' '))
        self.message.add_content(Content('text/html', ' '))

    def _set_basic_information(self):
        self.message.from_email = self.sender
        self.message.reply_to = self.sender
        self.message.subject = self.subject
        self.message.template_id = self.template_id
        self.message.add_category(Category(self.category))

    def _set_message(self):
        substitutions = self.get_substitutions()
        self._set_substitutions(substitutions)
        self.message.add_personalization(self.personal)
        self.set_content()

    def _set_attachments(self, encoded=False):
        for a in self.get_attachments():
            attachment = Attachment()
            attachment.content = base64.b64encode(a[0]) if not encoded else a[0]
            attachment.filename = a[1]
            attachment.type = a[2]
            attachment.disposition = 'attachment'
            self.message.add_attachment(attachment)

    def _set_substitutions(self, substitutions):
        for key, value in substitutions.items():
            # Force translation strings
            value = str(value) if isinstance(value, object) else value
            self.personal.add_substitution(Substitution('%%%s%%' % key, value))
