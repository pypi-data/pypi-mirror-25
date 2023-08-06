from django.test import TestCase

# Create your tests here.
from slxauth.utils import get_user_from_token


class ParseTokenTestCast(TestCase):
    def test_token_can_be_decoded(self):
        """Sample Authentication access_token can be correctly decoded"""

        token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJsYXN0TmFtZSI6IkRvdyIsImxhbmd1YWdlIjoiZW4iLCJpc0N1c3RvbWVyQWRtaW4iOnRydWUsImN1c3RvbWVyTnVtYmVyIjoiMTIzNDUiLCJ0aXRsZSI6Ik1SIiwiY3VzdG9tZXJOYW1lIjoiTGluYXJhIiwiYXV0aG9yaXRpZXMiOlsiUk9MRV9TT0xBUkxVWF9JTlNJREUiLCJST0xFX05FV1NfQVBQIiwiUk9MRV9URUNITklDQUxfRE9DUyIsIlJPTEVfVklERU9TIiwiUk9MRV9TUEFDRVMiLCJST0xFX0dFTkVSQUxfTkVXUyJdLCJjbGllbnRfaWQiOiJteS1jbGllbnQtd2l0aC1yZWdpc3RlcmVkLXJlZGlyZWN0IiwiZmlyc3ROYW1lIjoiSm9obiIsInNjb3BlIjpbInJlYWQiLCJ0cnVzdCJdLCJleHAiOjE1MTM1NjA3NzcsImNybUNvbnRhY3RJZCI6bnVsbCwiZW1haWwiOiJqb2huLmRvZUBzb2xhcmx1eC5kZSIsImp0aSI6IjZmYTBmMDg0LWJkYWUtNGI2Zi05ODU5LWNhMGNlNWI2YWFiNSJ9.cLjdauBKUb7wUnS2GiSEa9l2eia51Pt1YTXbWNVngveVsuJJRKp5cb7PJ55Icm5nXuccbDE5IxpdxaLLOrJ_seXpQUUjQR7M2-HwXaZIMp3VsEahudyumOECPCdqV0EYwlmlgKGHpxudw7XCG0buGcT7rtnF5iK7WadAzIenLPMenGqLEmoGosIayPxczlAiFK2_YmLaw6_Qd3g8PWYdBt7p3srewcAcNqzD9fATzIA4FG1FWGBcfWjJ53bz9YTTqQhTGglUx5bR5BEQ9kzwd6O98TohaJ0lnYFAyVSpeBR8OZOv8y17K24cKSZ2L5jIFGRnTc-QIl8yH2gTow3lbg'

        user = get_user_from_token(token)

        self.assertEqual(user.email, 'john.doe@solarlux.de')
        self.assertEqual(user.customer_no, '12345')
        self.assertEqual(user.first_name, 'John')
        self.assertEqual(user.last_name, 'Dow')
        self.assertEqual(user.customer_name, 'Linara')
        self.assertEqual(user.title, 'MR')
        self.assertEqual(user.is_customer_admin, True)
        self.assertEqual(user.crm_contact_id, None)
        self.assertEqual(user.language, 'en')
