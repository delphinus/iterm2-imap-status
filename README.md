# iterm2-imap-status

iTerm2 component to show count of messages in IMAP Inbox.

# What's this?

This is a custom status bar component for iTerm2 to show count of messages in IMAP Inbox.

<img width="466" alt="スクリーンショット 0001-08-11 17 56 54" src="https://user-images.githubusercontent.com/1239245/62832158-5b3db400-bc65-11e9-9406-2d8def9fbf78.png">

# Usage

## Prepare scripts

1. Install Python Runtime for iTerm2.
2. Clone this repo.
3. Copy or link `imap_status.py` to `~/Library/ApplicationSupport/iTerm2/Scripts/Autolaunch`

   ```sh
   cp imap_status.py ~/Library/ApplicationSupport/iTerm2/Scripts/Autolaunch
   ```

## Setup IMAP auth info

1. Restart iTerm2.
2. Configure Status Bar.

<img width="658" alt="スクリーンショット 0001-08-11 18 02 33" src="https://user-images.githubusercontent.com/1239245/62832166-65f84900-bc65-11e9-89fb-28d64366f348.png">

Example setting.

* Gmail
  - Server: imap.gmail.com
  - Port: 993
  - Username: your_mail@example.com
* iCloud
  - Server: imap.mail.me.com
  - Port: 993
  - Username: your_account

## Store your password in keychain

This component reads your passwords from the keychain service. So you should prepare them.

Today IMAP services (Gmail, iCloud, ... etc.) have the two-factor authentication feature. It is **strongly** recommended that you use it and prepare own “App Passwords” only for this component.

* Google: [Sign in using App Passwords - Google Account Help](https://support.google.com/accounts/answer/185833)
* Apple: [Using app-specific passwords - Apple Support](https://support.apple.com/en-us/HT204397)

After you get passwords, you should store them in keychain. You can use the GUI, or the `security` command in CLI.

```sh
# for Google
security add-internet-password -a foo@gmail.com -s imap.gmail.com -P 993 -w 'your_password'
# for Apple
security add-internet-password -a foo -s imap.mail.me.com -P 993 -w 'your_password'
```

# Trouble Shooting

## I see only a ladybug in status bar!

<img width="466" alt="スクリーンショット 0001-08-11 18 20 53" src="https://user-images.githubusercontent.com/1239245/62832168-6c86c080-bc65-11e9-88fe-c28b66122962.png">

* Your Mac has no connection to the Internet.
* Or some unknown bugs in the script occur. See the Script Console (type ⌥⌘J) and report an issue with the log.
