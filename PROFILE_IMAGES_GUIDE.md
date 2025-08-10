# Profile Images System Guide

## Overview

The Profile Images system allows users to submit custom Avatar Realms account screenshots to be displayed on their global profiles. All submissions require owner approval to ensure authenticity and appropriateness.

## Commands

### `/setprofile`
Submit your Avatar Realms profile image for approval.

**Usage:**
```
/setprofile image:[screenshot]
```

**Requirements:**
- Must be an image file (PNG, JPG, etc.)
- File size must be under 10MB
- Image should show a valid Avatar Realms account screenshot

**Process:**
1. Upload your Avatar Realms account screenshot
2. Bot owner receives approval request via DM
3. Owner reviews the image and approves/rejects it
4. You receive a DM notification of the result
5. If approved, your image appears on your profile

### `/profile`
View your or another user's profile with custom image (if approved).

**Usage:**
```
/profile [user:@username] [scope:global/server]
```

**Features:**
- Shows custom profile image if approved, otherwise uses Discord avatar
- Displays global statistics and achievements
- Shows global ranking and performance metrics
- Includes account creation and activity information

### `/pendingapprovals` (Owner Only)
View all pending profile image approval requests.

**Usage:**
```
/pendingapprovals
```

**Features:**
- Lists all users waiting for approval
- Shows submission details (user, server, timestamp)
- Only accessible to the bot owner (ID: 1051142172130422884)

## Approval Workflow

### For Users:
1. **Submit Image**: Use `/setprofile` with your Avatar Realms screenshot
2. **Wait for Review**: Bot owner will review your submission
3. **Receive Notification**: Get DM when approved or rejected
4. **View Profile**: Use `/profile` to see your image once approved

### For Owner:
1. **Receive Request**: Get DM with image and approval buttons
2. **Review Image**: Check if it's a valid Avatar Realms screenshot
3. **Approve/Reject**: Click buttons to approve or reject with reason
4. **User Notified**: User automatically receives result notification

## File Storage

- **Temporary Files**: `data/users/profile_images/temp_[user_id].png`
- **Approved Files**: `data/users/profile_images/[user_id].png`
- **Automatic Cleanup**: Rejected images are automatically deleted

## Data Structure

Profile images are stored in the global profile preferences:

```json
{
  "preferences": {
    "profile_image_path": "data/users/profile_images/123456789.png",
    "profile_image_approved_at": "2024-01-01T12:00:00Z"
  }
}
```

## Security Features

- **Owner Approval**: Only the bot owner can approve/reject images
- **File Validation**: Checks file type and size before processing
- **Automatic Cleanup**: Rejected images are immediately deleted
- **Privacy Protection**: Images are stored locally and not shared publicly

## Error Handling

- **Invalid File Type**: Rejects non-image files
- **File Too Large**: Rejects files over 10MB
- **Download Failures**: Handles network errors gracefully
- **Storage Errors**: Logs and reports file system issues

## Integration

The profile images system integrates with:
- **Global Profiles**: Images appear on global profile embeds
- **Leaderboards**: Custom images shown in profile displays
- **Achievement System**: Images enhance achievement showcases
- **Cross-Server**: Images work across all servers

## Best Practices

### For Users:
- Use clear, high-quality screenshots
- Ensure the image shows your Avatar Realms account clearly
- Avoid uploading inappropriate or off-topic images
- Be patient during the approval process

### For Owner:
- Review images promptly
- Provide clear rejection reasons when needed
- Ensure images are actually Avatar Realms screenshots
- Maintain consistent approval standards

## Technical Details

- **Supported Formats**: PNG, JPG, JPEG, GIF, WebP
- **Max File Size**: 10MB
- **Storage Location**: `data/users/profile_images/`
- **Owner ID**: 1051142172130422884
- **Dependencies**: aiohttp (for image downloading)

## Troubleshooting

### Common Issues:

**"Invalid file type"**
- Ensure you're uploading an image file
- Check file extension (.png, .jpg, etc.)

**"File too large"**
- Compress your image to under 10MB
- Use image editing software to reduce size

**"No approval notification"**
- Check your DMs are open to the bot
- Wait for owner review (may take time)

**"Image not showing on profile"**
- Ensure your image was approved
- Check if you have an approved profile image

### Support:
For issues with the profile images system, contact the bot owner or check the bot logs for error details.
