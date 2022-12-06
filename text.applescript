# https://stackoverflow.com/questions/11812184/how-to-send-an-imessage-text-with-applescript-only-in-provided-service

on run {targetMessage, targetBuddyPhone}
    tell application "Messages"
        set targetService to 1st service whose service type = SMS
        set targetBuddy to buddy targetBuddyPhone of targetService
        send targetMessage to targetBuddy
    end tell
end run