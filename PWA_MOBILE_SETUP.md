# 📱 PWA Mobile Setup Instructions

## Fixing PWA Icon, Notifications & Sound on Mobile

### ✅ Changes Made:

1. **Fixed Icon Paths in `manifest.json`**
   - Updated all icon paths to use `/app/static/assets/pwa/` (Streamlit Cloud format)
   - Icons now properly display on home screen when installed

2. **Enhanced Service Worker (`sw.js`)**
   - Updated notification icons to use PWA icons
   - Added sound support in notifications
   - Increased vibration pattern for better feedback

3. **Added Notification Support (`streamlit_app.py`)**
   - Auto-requests notification permissions after 3 seconds
   - Includes `window.playNotificationSound()` function
   - Includes `window.testNotification()` function for testing

4. **Added Test Buttons (`pages/0_Landing.py`)**
   - 🔔 Test Notification & Sound button
   - 🔊 Test Sound Only button

---

## 🔧 How to Update PWA on Your Phone:

### For iOS (Safari):
1. Delete the old PWA from home screen (long press > Remove App)
2. Open Safari and go to your deployed app URL
3. Tap the **Share** button (square with arrow pointing up)
4. Tap **"Add to Home Screen"**
5. Name it "Insaka" and tap **Add**
6. Open the newly installed app
7. When prompted, tap **Allow** for notifications

### For Android (Chrome):
1. Uninstall the old PWA from home screen
2. Open Chrome and go to your deployed app URL
3. Tap the **3-dot menu** > **Add to Home screen**
4. Name it "Insaka" and tap **Add**
5. Open the newly installed app
6. When prompted, tap **Allow** for notifications

---

## 🧪 Testing Notifications & Sound:

1. Open the app (either in browser or as PWA)
2. Scroll to the bottom of the landing page
3. Click **"🔔 Test Notification & Sound"**
4. You should:
   - See a notification banner
   - Hear a notification sound
   - Feel vibration (on mobile)

### If notifications don't work:
- Check device notification settings
- Make sure "Do Not Disturb" is off
- Ensure the app has notification permissions
- Try the **"🔊 Test Sound Only"** button first

### If sound doesn't play:
- Make sure device volume is up
- Check that sound is not muted
- iOS requires user interaction first - tap the sound test button
- Some browsers block autoplay - this is normal

---

## 📝 Console Testing:

You can also test directly in browser console (F12):

```javascript
// Test notification
window.testNotification();

// Test sound only
window.playNotificationSound();

// Check notification permission
console.log('Notification permission:', Notification.permission);
```

---

## 🔍 Troubleshooting:

### Icons still showing Streamlit logo:
1. **Clear browser cache** and reload
2. **Uninstall and reinstall** the PWA
3. Check that icon files exist in `assets/pwa/` folder
4. Verify manifest.json is accessible at `/manifest.json`

### Notifications not working:
1. Check browser console for errors (F12)
2. Verify notification permission: `Notification.permission`
3. Make sure service worker is registered
4. On iOS, notifications work better as PWA (installed on home screen)

### Sound not playing:
1. Most browsers require user interaction first
2. Click the test sound button
3. Check `/app/static/assets/notification.wav` exists
4. Try playing sound manually in console

---

## 📦 Required Files:

- ✅ `manifest.json` - PWA manifest with correct icon paths
- ✅ `sw.js` - Service worker with notification/sound support
- ✅ `assets/pwa/*.png` - All PWA icon sizes
- ✅ `assets/notification.wav` - Notification sound file
- ✅ `streamlit_app.py` - Notification JavaScript code
- ✅ `.streamlit/config.toml` - Dark theme configuration

All files have been updated! 🎉

---

## 🚀 Deployment Checklist:

- [ ] Push all changes to repository
- [ ] Deploy to Streamlit Cloud
- [ ] Verify manifest.json loads at `/manifest.json`
- [ ] Verify service worker loads
- [ ] Test PWA installation on mobile
- [ ] Test notifications and sound
- [ ] Check icon displays correctly on home screen

---

## 💡 Tips:

1. **Always test as PWA (installed app)** - some features work better in installed mode
2. **iOS Safari** is more restrictive - test on both iOS and Android
3. **Notification permissions** are requested automatically after 3 seconds
4. **Sound autoplay** is blocked until user interaction - this is normal
5. **Dark theme** is now forced - users cannot change it

---

**Last Updated:** 2025-09-30
**Version:** 1.0.0
