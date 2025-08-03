# run_demo.py

import os
import django
from typing import Optional

# Setup Django environment
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'signals.settings')
django.setup()

# Import models
from django.contrib.auth.models import User
from messaging.models import Message, MessageHistory

# -----------------------------------------------------------------
# SERVICE FUNCTION: The single, correct way to edit a message
# -----------------------------------------------------------------
def edit_message(editor: User, message: Message, new_content: str) -> Message:
    """
    Edits a message's content and ensures the editor is recorded.

    This function is the single source of truth for this business logic.
    """
    print(f"--- SERVICE: User '{editor.username}' is attempting to edit message {message.id}.")
    
    # Attach the editor to the instance so the signal handler can access it.
    message.editor = editor
    
    # Update the content
    message.content = new_content
    
    # Save the message. The pre_save signal will now fire correctly.
    message.save()
    
    print(f"--- SERVICE: Message {message.id} saved successfully.")
    return message

# -----------------------------------------------------------------
# DEMONSTRATION SCRIPT
# -----------------------------------------------------------------
def run():
    """Demonstrates the robust message editing workflow."""
    print("Step 1: Preparing users...")
    user1, _ = User.objects.get_or_create(username='alice')
    user2, _ = User.objects.get_or_create(username='bob')
    print(f"Users '{user1.username}' and '{user2.username}' are ready.\n")

    print("Step 2: Creating a new message from Alice to Bob...")
    msg = Message.objects.create(
        sender=user1,
        receiver=user2,
        content="Project Alpha is on schedule."
    )
    print(f"Message (ID: {msg.id}) created.\n")

    print("Step 3: Alice edits her message using the robust service function...")
    # This is the correct way: call the dedicated function.
    # We pass the user performing the action and the new content.
    edit_message(
        editor=user1,
        message=msg,
        new_content="Project Alpha is slightly behind schedule. Need to discuss."
    )
    print("Message edit process complete.\n")

    print("Step 4: Viewing the final message and its history...")
    # Fetch the final state of the message from the database
    final_message = Message.objects.get(id=msg.id)

    print("\n--- Final Message Details ---")
    print(f"  Content: '{final_message.content}'")
    status = f"Edited by {final_message.last_edited_by.username}" if final_message.edited else "Original"
    print(f"  Status: {status}")

    # Display the history, which was created by the signal
    history_entries = final_message.history.all()
    print("\n--- Edit History ---")
    if history_entries.exists():
        for version in history_entries:
            editor_name = version.edited_by.username if version.edited_by else "Unknown"
            print(f"  - Version saved at {version.edited_at.strftime('%Y-%m-%d %H:%M')}")
            print(f"    Edited By: {editor_name}")
            print(f"    Old Content: '{version.old_content}'")
    else:
        print("  No edit history found.")

if __name__ == '__main__':
    # Clean up DB for a fresh demonstration
    Message.objects.all().delete()
    run()