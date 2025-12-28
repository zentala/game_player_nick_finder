import hashlib
import re
from django.conf import settings
from django.utils import timezone
from datetime import timedelta
from django.db.models import Q

def get_gravatar_url(email, size=40):
    email_hash = hashlib.md5(email.lower().encode('utf-8')).hexdigest()
    return f"https://www.gravatar.com/avatar/{email_hash}?s={size}&d=identicon"


# POKE System Utilities
def validate_poke_content(content):
    """
    Validate POKE content according to rules:
    - Max 100 characters
    - No URLs/links
    - No email addresses
    - Strip HTML tags
    """
    from django.utils.html import strip_tags
    
    errors = []
    
    # Check length
    max_length = getattr(settings, 'POKE_MAX_CONTENT_LENGTH', 100)
    if len(content) > max_length:
        errors.append(f"Content must be {max_length} characters or less")
    
    # Strip HTML tags
    clean_content = strip_tags(content)
    if clean_content != content:
        errors.append("HTML tags are not allowed")
    
    # Check for URLs/links
    url_pattern = r'(http|https|www\.|\.com|\.net|\.org|://)'
    if getattr(settings, 'POKE_CONTENT_FILTER_URLS', True):
        if re.search(url_pattern, content, re.IGNORECASE):
            errors.append("URLs and links are not allowed in POKE content")
    
    # Check for email addresses
    email_pattern = r'@'
    if getattr(settings, 'POKE_CONTENT_FILTER_EMAILS', True):
        if re.search(email_pattern, content):
            errors.append("Email addresses are not allowed in POKE content")
    
    # Profanity filter (basic - can be enhanced)
    if getattr(settings, 'POKE_PROFANITY_FILTER_ENABLED', True):
        profanity_list = getattr(settings, 'POKE_PROFANITY_WORDLIST', [])
        content_lower = content.lower()
        for word in profanity_list:
            if word.lower() in content_lower:
                errors.append("Inappropriate content is not allowed")
                break
    
    return errors, clean_content if clean_content != content else content


def can_send_poke(user, receiver_character):
    """
    Check if user can send POKE to receiver_character.
    Returns (can_send: bool, reason: str or None)
    """
    from app.models import Poke, PokeBlock, Character
    
    # Check if user has characters
    user_characters = Character.objects.filter(user=user)
    if not user_characters.exists():
        return False, "You need to create a character first to send POKEs"
    
    # Check if receiver is from different user
    if receiver_character.user == user:
        return False, "You cannot send POKE to your own character"
    
    # Check for blocks
    is_blocked = PokeBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character__user=user
    ).exists()
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # Rate limiting: Check daily limit per user
    max_per_day = getattr(settings, 'POKE_MAX_PER_USER_PER_DAY', 5)
    yesterday = timezone.now() - timedelta(days=1)
    today_poke_count = Poke.objects.filter(
        sender_character__user=user,
        sent_date__gte=yesterday
    ).count()
    if today_poke_count >= max_per_day:
        return False, f"You can send maximum {max_per_day} POKEs per 24 hours"
    
    # Cooldown: Check if POKE was sent to same character recently
    cooldown_days = getattr(settings, 'POKE_COOLDOWN_DAYS', 30)
    cooldown_date = timezone.now() - timedelta(days=cooldown_days)
    recent_poke = Poke.objects.filter(
        sender_character__user=user,
        receiver_character=receiver_character,
        sent_date__gte=cooldown_date
    ).exists()
    if recent_poke:
        return False, f"You can send only 1 POKE to the same character per {cooldown_days} days"
    
    # Check if POKE already exists (unique_together constraint)
    existing_poke = Poke.objects.filter(
        sender_character__user=user,
        receiver_character=receiver_character
    ).exists()
    if existing_poke:
        return False, "You have already sent a POKE to this character"
    
    # Check receiver's profile visibility (respect privacy settings)
    receiver_user = receiver_character.user
    if hasattr(receiver_user, 'profile_visibility'):
        if receiver_user.profile_visibility == 'PRIVATE':
            # For private profiles, we might want to restrict - but let's allow for now
            # and let user decide to block if unwanted
            pass
    
    return True, None


def can_send_message(sender_character, receiver_character):
    """
    Check if sender_character can send full Message to receiver_character.
    Full messaging is unlocked after mutual POKE exchange.
    """
    from app.models import Poke, PokeBlock
    
    # Check for blocks (even if POKE was exchanged, block can prevent messaging)
    is_blocked = PokeBlock.objects.filter(
        blocker_character=receiver_character,
        blocked_character=sender_character
    ).exists()
    if is_blocked:
        return False, "You have been blocked by this character"
    
    # Check if mutual POKE exists
    poke_a_to_b = Poke.objects.filter(
        sender_character=sender_character,
        receiver_character=receiver_character,
        status='RESPONDED'
    ).exists()
    
    poke_b_to_a = Poke.objects.filter(
        sender_character=receiver_character,
        receiver_character=sender_character,
        status__in=['PENDING', 'RESPONDED']
    ).exists()
    
    # Both POKEs exist and at least one is RESPONDED
    if (poke_a_to_b or poke_b_to_a):
        return True, None
    
    return False, "You must exchange POKEs before sending messages. Send a POKE first."
