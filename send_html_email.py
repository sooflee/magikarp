#!/usr/bin/env python3
"""Send an HTML test email via Gmail SMTP.

Usage:
    export GMAIL_APP_PASSWORD="your-16-char-app-password"
    python3 send_html_email.py

The App Password is NOT your normal Gmail password. Create one at:
    https://myaccount.google.com/apppasswords
(Requires 2-Step Verification to be enabled on the account.)
"""

import os
import smtplib
import ssl
import sys
from email.message import EmailMessage

SENDER = "bensonw.dev@gmail.com"
RECIPIENT = "bensonw.dev@gmail.com"
SUBJECT = "Test HTML email from Claude Code"

PLAIN_BODY = """\
Hello, world!

This is a sample HTML email sent from Claude Code via Gmail. It uses inline
styles and a table-based layout so it renders consistently across email clients.

Learn more: https://claude.com/claude-code

-- Sent with Claude Code
"""

HTML_BODY = """\
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Hello from Claude Code</title>
</head>
<body style="margin:0; padding:0; background-color:#f4f4f7; font-family:Arial, Helvetica, sans-serif;">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0" style="background-color:#f4f4f7;">
    <tr>
      <td align="center" style="padding:24px 12px;">
        <table role="presentation" width="600" cellpadding="0" cellspacing="0" style="max-width:600px; width:100%; background-color:#ffffff; border-radius:8px; overflow:hidden; box-shadow:0 1px 3px rgba(0,0,0,0.08);">
          <tr>
            <td style="background-color:#4f46e5; padding:32px 40px; text-align:center;">
              <h1 style="margin:0; color:#ffffff; font-size:24px; font-weight:700;">Hello, world &#128075;</h1>
            </td>
          </tr>
          <tr>
            <td style="padding:40px;">
              <p style="margin:0 0 16px; color:#333333; font-size:16px; line-height:1.6;">
                This is a sample <strong>HTML email</strong> sent from Claude Code via Gmail.
              </p>
              <p style="margin:0 0 24px; color:#333333; font-size:16px; line-height:1.6;">
                It uses inline styles and a table-based layout so it renders consistently across email clients.
              </p>
              <table role="presentation" cellpadding="0" cellspacing="0">
                <tr>
                  <td style="border-radius:6px; background-color:#4f46e5;">
                    <a href="https://claude.com/claude-code" target="_blank" style="display:inline-block; padding:12px 28px; color:#ffffff; font-size:16px; font-weight:600; text-decoration:none;">Learn more</a>
                  </td>
                </tr>
              </table>
            </td>
          </tr>
          <tr>
            <td style="background-color:#fafafa; padding:24px 40px; text-align:center; border-top:1px solid #eeeeee;">
              <p style="margin:0; color:#999999; font-size:12px; line-height:1.5;">
                Sent with Claude Code &middot; You received this because you requested a test.
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>
"""


def main() -> int:
    app_password = os.environ.get("GMAIL_APP_PASSWORD")
    if not app_password:
        print(
            "ERROR: set GMAIL_APP_PASSWORD first, e.g.\n"
            '    export GMAIL_APP_PASSWORD="abcd efgh ijkl mnop"',
            file=sys.stderr,
        )
        return 1

    msg = EmailMessage()
    msg["From"] = SENDER
    msg["To"] = RECIPIENT
    msg["Subject"] = SUBJECT
    msg.set_content(PLAIN_BODY)
    msg.add_alternative(HTML_BODY, subtype="html")

    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
        server.login(SENDER, app_password)
        server.send_message(msg)

    print(f"Sent HTML email to {RECIPIENT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
