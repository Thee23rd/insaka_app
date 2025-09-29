# 📱 Insaka Conference PWA Setup Guide

## 🎯 What is PWA?

A Progressive Web App (PWA) allows users to install your conference app on their mobile devices like a native app. Users get:
- 📱 App icon on home screen
- 🚀 Fast loading and offline capabilities  
- 🔔 Push notifications
- 📲 Native app-like experience

## 🛠️ Current PWA Configuration

Your Insaka Conference app is now configured as a PWA with:

### 📋 Files Created:
- `manifest.json` - PWA configuration
- `sw.js` - Service worker for offline functionality
- `.streamlit/config.toml` - Streamlit PWA settings
- `generate_pwa_logos.py` - Logo generator script

### 🎨 Current Logo Setup:
- **Main Logo**: `assets/logos/insaka.jpg`
- **PWA Icons**: Will be generated in `assets/pwa/` folder
- **Theme Colors**: Zambian green (#198A00)

## 🔄 How to Change the PWA Logo

### Option 1: Use the Logo Generator Script

1. **Install Pillow** (if not already installed):
   ```bash
   pip install Pillow
   ```

2. **Run the generator**:
   ```bash
   python generate_pwa_logos.py
   ```

3. **The script will**:
   - Generate multiple icon sizes (48x48 to 512x512)
   - Create PNG icons in `assets/pwa/` folder
   - Update `manifest.json` with new icon paths
   - Use your existing logo from `assets/logos/insaka.jpg`

### Option 2: Manual Logo Replacement

1. **Replace the main logo**:
   - Put your new logo at `assets/logos/insaka.jpg`
   - Or update paths in `manifest.json` and `streamlit_app.py`

2. **Generate different sizes**:
   - Use online tools like [PWA Builder](https://www.pwabuilder.com/imageGenerator)
   - Create icons: 48x48, 72x72, 96x96, 144x144, 152x152, 167x167, 180x180, 192x192, 512x512

3. **Update manifest.json**:
   - Replace icon paths in the `icons` array
   - Update `screenshots` section if needed

### Option 3: Use Online PWA Icon Generator

1. Go to [PWA Builder Image Generator](https://www.pwabuilder.com/imageGenerator)
2. Upload your logo
3. Download the generated icon pack
4. Replace files in `assets/pwa/` folder
5. Update `manifest.json` paths if needed

## 🎨 Customizing PWA Appearance

### Colors
Update these in `manifest.json`:
```json
{
  "background_color": "#198A00",  // App background
  "theme_color": "#198A00"        // Status bar color
}
```

### App Name & Description
Update in `manifest.json`:
```json
{
  "name": "Insaka Conference 2025",
  "short_name": "Insaka",
  "description": "Zambian Mining and Investment Conference - Delegate Portal"
}
```

### App Behavior
Update display mode in `manifest.json`:
```json
{
  "display": "standalone",           // Full screen app
  "orientation": "portrait-primary", // Portrait only
  "scope": "/"                       // App scope
}
```

## 📱 Testing Your PWA

### Desktop Testing:
1. Open Chrome/Edge
2. Go to your app URL
3. Click the install button in address bar
4. Test the installed app

### Mobile Testing:
1. Open Chrome on Android/iOS
2. Go to your app URL
3. Tap "Add to Home Screen"
4. Install and test

### PWA Audit:
1. Open Chrome DevTools
2. Go to "Lighthouse" tab
3. Run "Progressive Web App" audit
4. Check for any issues

## 🚀 Deployment Notes

### Streamlit Cloud:
- PWA files will be served automatically
- Ensure all paths are relative (start with `/`)
- Test after deployment

### Custom Server:
- Ensure HTTPS is enabled (required for PWA)
- Set proper MIME types for manifest.json
- Test service worker registration

## 🔧 Troubleshooting

### Common Issues:

**Icons not showing:**
- Check file paths in manifest.json
- Ensure icons are PNG format
- Verify file sizes match manifest entries

**Install prompt not appearing:**
- Ensure HTTPS is enabled
- Check manifest.json is valid
- Verify service worker is registered

**App not working offline:**
- Check service worker is active
- Verify cache strategy in sw.js
- Test network throttling in DevTools

### Debug Commands:
```javascript
// Check service worker status
navigator.serviceWorker.getRegistrations()

// Check manifest
console.log('Manifest:', document.querySelector('link[rel="manifest"]'))

// Check PWA installability
window.addEventListener('beforeinstallprompt', (e) => {
  console.log('PWA installable:', e)
})
```

## 📞 Support

If you need help with PWA setup:
1. Check browser console for errors
2. Validate manifest.json at [manifest-validator.appspot.com](https://manifest-validator.appspot.com)
3. Test with [PWA Builder](https://www.pwabuilder.com)

## 🎉 Next Steps

After setting up your PWA:
1. **Test thoroughly** on different devices
2. **Customize branding** with your conference colors
3. **Add push notifications** for conference updates
4. **Optimize performance** for mobile users
5. **Share install instructions** with delegates

Your Insaka Conference app is now ready to be installed as a native-like experience on delegates' mobile devices! 🇿🇲📱✨

