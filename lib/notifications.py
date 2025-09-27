"""
Notification System for Insaka Conference App
Handles notification tracking and display across all components
"""

import json
import os
from datetime import datetime
from typing import Dict, List, Optional

NOTIFICATIONS_FILE = "data/notifications.json"

def load_notifications() -> List[Dict]:
    """Load notifications from JSON file"""
    try:
        if os.path.exists(NOTIFICATIONS_FILE):
            with open(NOTIFICATIONS_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []
    except Exception:
        return []

def save_notifications(notifications: List[Dict]) -> bool:
    """Save notifications to JSON file"""
    try:
        os.makedirs(os.path.dirname(NOTIFICATIONS_FILE), exist_ok=True)
        with open(NOTIFICATIONS_FILE, "w", encoding="utf-8") as f:
            json.dump(notifications, f, indent=2, ensure_ascii=False)
        return True
    except Exception:
        return False

def add_notification(
    user_id: str,
    notification_type: str,
    title: str,
    message: str,
    priority: str = "Normal",
    data: Optional[Dict] = None
) -> bool:
    """Add a new notification for a user"""
    notifications = load_notifications()
    
    notification = {
        "id": len(notifications) + 1,
        "user_id": user_id,
        "type": notification_type,
        "title": title,
        "message": message,
        "priority": priority,
        "data": data or {},
        "read": False,
        "created_at": datetime.now().isoformat()
    }
    
    notifications.append(notification)
    return save_notifications(notifications)

def get_user_notifications(user_id: str, unread_only: bool = False) -> List[Dict]:
    """Get notifications for a specific user"""
    notifications = load_notifications()
    user_notifications = [n for n in notifications if n.get("user_id") == user_id]
    
    if unread_only:
        user_notifications = [n for n in user_notifications if not n.get("read", False)]
    
    # Sort by priority and date
    priority_order = {"Urgent": 4, "High": 3, "Normal": 2, "Low": 1}
    user_notifications.sort(
        key=lambda x: (priority_order.get(x.get("priority", "Normal"), 2), x.get("created_at", "")),
        reverse=True
    )
    
    return user_notifications

def mark_notification_read(notification_id: int) -> bool:
    """Mark a notification as read"""
    notifications = load_notifications()
    
    for notification in notifications:
        if notification.get("id") == notification_id:
            notification["read"] = True
            notification["read_at"] = datetime.now().isoformat()
            return save_notifications(notifications)
    
    return False

def mark_all_notifications_read(user_id: str) -> bool:
    """Mark all notifications as read for a user"""
    notifications = load_notifications()
    
    for notification in notifications:
        if notification.get("user_id") == user_id and not notification.get("read", False):
            notification["read"] = True
            notification["read_at"] = datetime.now().isoformat()
    
    return save_notifications(notifications)

def get_notification_count(user_id: str, unread_only: bool = True) -> int:
    """Get notification count for a user"""
    user_notifications = get_user_notifications(user_id, unread_only=unread_only)
    return len(user_notifications)

def get_notification_badge(count: int, max_show: int = 99) -> str:
    """Generate notification badge HTML"""
    if count > 0:
        if count > max_show:
            return f'<span style="background: #ff4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem; margin-left: 5px; font-weight: bold;">{max_show}+</span>'
        else:
            return f'<span style="background: #ff4444; color: white; border-radius: 50%; padding: 2px 6px; font-size: 0.7rem; margin-left: 5px; font-weight: bold;">{count}</span>'
    return ""

def create_test_notifications(user_id: str, count: int = 3) -> bool:
    """Create test notifications for demonstration"""
    for i in range(count):
        add_notification(
            user_id=user_id,
            notification_type="system",
            title=f"Test Notification {i+1}",
            message=f"This is a test notification #{i+1}",
            priority="Normal"
        )
    return True

def clear_all_notifications(user_id: str) -> bool:
    """Clear all notifications for a user"""
    notifications = load_notifications()
    filtered_notifications = [n for n in notifications if n.get("user_id") != user_id]
    return save_notifications(filtered_notifications)

def get_priority_color(priority: str) -> str:
    """Get color for notification priority"""
    colors = {
        "Urgent": "🔴",
        "High": "🟠", 
        "Normal": "🟡",
        "Low": "🟢"
    }
    return colors.get(priority, "🟡")

def cleanup_old_notifications(days_old: int = 30) -> bool:
    """Remove notifications older than specified days"""
    notifications = load_notifications()
    
    cutoff_date = datetime.now().timestamp() - (days_old * 24 * 60 * 60)
    
    filtered_notifications = []
    for notification in notifications:
        try:
            created_at = datetime.fromisoformat(notification.get("created_at", ""))
            if created_at.timestamp() > cutoff_date:
                filtered_notifications.append(notification)
        except:
            # Keep notifications with invalid dates
            filtered_notifications.append(notification)
    
    return save_notifications(filtered_notifications)

# Notification types and templates
NOTIFICATION_TYPES = {
    "announcement": {
        "icon": "📢",
        "color": "#198A00"
    },
    "news": {
        "icon": "📰",
        "color": "#2BA300"
    },
    "interaction": {
        "icon": "💬",
        "color": "#D10000"
    },
    "connection": {
        "icon": "🤝",
        "color": "#FF8800"
    },
    "meeting": {
        "icon": "📅",
        "color": "#0066CC"
    },
    "system": {
        "icon": "⚙️",
        "color": "#666666"
    }
}

def create_system_notification(user_id: str, title: str, message: str, notification_type: str = "system") -> bool:
    """Create a system notification"""
    return add_notification(
        user_id=user_id,
        notification_type=notification_type,
        title=title,
        message=message,
        priority="Normal"
    )

def create_interaction_notification(
    from_user_id: str,
    to_user_id: str,
    interaction_type: str,
    content: str = ""
) -> bool:
    """Create an interaction notification (like, comment, share, etc.)"""
    interaction_titles = {
        "like": "New Like",
        "comment": "New Comment",
        "share": "Post Shared",
        "mention": "You were mentioned"
    }
    
    title = interaction_titles.get(interaction_type, "New Interaction")
    message = f"Someone {interaction_type}d your content"
    
    if content:
        message += f": {content[:100]}..."
    
    return add_notification(
        user_id=to_user_id,
        notification_type="interaction",
        title=title,
        message=message,
        priority="Normal",
        data={"from_user_id": from_user_id, "interaction_type": interaction_type}
    )

def create_connection_notification(from_user_id: str, to_user_id: str, action: str) -> bool:
    """Create a connection-related notification"""
    action_titles = {
        "request": "Connection Request",
        "accepted": "Connection Accepted",
        "declined": "Connection Declined"
    }
    
    title = action_titles.get(action, "Connection Update")
    message = f"Connection {action} from another delegate"
    
    success = add_notification(
        user_id=to_user_id,
        notification_type="connection",
        title=title,
        message=message,
        priority="Normal",
        data={"from_user_id": from_user_id, "action": action}
    )
    
    # Trigger sound notification for PWA
    if success:
        trigger_sound_notification()
    
    return success

def trigger_sound_notification():
    """Trigger a sound notification for PWA functionality"""
    # This will be handled by JavaScript on the frontend
    pass

def get_sound_notification_script() -> str:
    """Generate JavaScript for simple, reliable sound notifications"""
    return """
    <script>
    // Super simple sound system that will definitely work
    let audioContext = null;
    let isAudioEnabled = false;
    
    // Initialize audio context on first user interaction
    function initAudio() {
        if (!audioContext && !isAudioEnabled) {
            try {
                audioContext = new (window.AudioContext || window.webkitAudioContext)();
                isAudioEnabled = true;
                console.log('🔊 Audio context initialized!');
            } catch (error) {
                console.log('❌ Audio context failed:', error);
            }
        }
    }
    
    function playNotificationSound() {
        console.log('🔊 Playing notification sound...');
        
        // Initialize audio if not done yet
        initAudio();
        
        if (!audioContext) {
            console.log('❌ No audio context available');
            showVisualAlert();
            return;
        }
        
        try {
            // Create a simple, loud beep
            const oscillator = audioContext.createOscillator();
            const gainNode = audioContext.createGain();
            
            oscillator.connect(gainNode);
            gainNode.connect(audioContext.destination);
            
            // Make it loud and attention-grabbing
            oscillator.frequency.value = 1000; // Higher frequency
            oscillator.type = 'square'; // Square wave is more piercing
            gainNode.gain.value = 0.5; // Louder volume
            
            // Play the beep
            oscillator.start();
            oscillator.stop(audioContext.currentTime + 0.2); // Longer beep
            
            console.log('✅ BEEP PLAYED!');
            
            // Play second beep after a short delay
            setTimeout(() => {
                try {
                    const osc2 = audioContext.createOscillator();
                    const gain2 = audioContext.createGain();
                    osc2.connect(gain2);
                    gain2.connect(audioContext.destination);
                    osc2.frequency.value = 1200; // Even higher frequency
                    osc2.type = 'square';
                    gain2.gain.value = 0.5;
                    osc2.start();
                    osc2.stop(audioContext.currentTime + 0.2);
                    console.log('✅ SECOND BEEP PLAYED!');
                } catch (e) {
                    console.log('❌ Second beep failed:', e);
                }
            }, 300);
            
        } catch (error) {
            console.log('❌ Beep failed:', error);
            showVisualAlert();
        }
    }
    
    function showVisualAlert() {
        console.log('👁️ Showing BRIGHT RED visual alert...');
        // Create a bright red flash that's impossible to miss
        const flash = document.createElement('div');
        flash.style.cssText = `
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            background: #ff0000;
            z-index: 99999;
            pointer-events: none;
            opacity: 1;
        `;
        document.body.appendChild(flash);
        
        // Flash multiple times
        let flashCount = 0;
        const flashInterval = setInterval(() => {
            flash.style.opacity = flash.style.opacity === '1' ? '0.3' : '1';
            flashCount++;
            if (flashCount >= 6) {
                clearInterval(flashInterval);
                setTimeout(() => {
                    if (document.body.contains(flash)) {
                        document.body.removeChild(flash);
                    }
                }, 500);
            }
        }, 200);
        
        console.log('✅ BRIGHT RED VISUAL ALERT SHOWN!');
    }
    
    function vibrateDevice() {
        console.log('📳 Attempting strong vibration...');
        if ('vibrate' in navigator) {
            try {
                // Very strong vibration pattern
                navigator.vibrate([300, 100, 300, 100, 300]);
                console.log('✅ STRONG VIBRATION PLAYED!');
            } catch (error) {
                console.log('❌ Vibration failed:', error);
            }
        } else {
            console.log('❌ Vibration not supported');
        }
    }
    
    function triggerNotificationFeedback() {
        console.log('🔔 TRIGGERING LOUD NOTIFICATION!');
        playNotificationSound();
        vibrateDevice();
        showVisualAlert(); // Always show visual alert too
    }
    
    // Make functions globally available immediately
    window.playNotificationSound = playNotificationSound;
    window.vibrateDevice = vibrateDevice;
    window.triggerNotificationFeedback = triggerNotificationFeedback;
    window.showVisualAlert = showVisualAlert;
    
    // Test function
    window.testNotificationSound = function() {
        console.log('🧪 TESTING LOUD NOTIFICATION...');
        triggerNotificationFeedback();
    };
    
    console.log('🔊 SIMPLE NOTIFICATION SYSTEM LOADED!');
    </script>
    """
