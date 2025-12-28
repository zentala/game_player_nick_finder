# Before Production Deployment - Checklist

**Last Updated**: 2025-12-28
**Status**: ⛔ NOT READY FOR PRODUCTION
**Critical Blocker**: Email validation disabled (development mode only)

---

## 🚨 CRITICAL: Email Validation (HIGHEST PRIORITY)

### Why Email is Required in Production
- Password reset mechanism
- User account verification
- Account recovery
- Legal compliance (GDPR, SOC 2)
- Spam prevention and account ownership verification

### Implementation Tasks

#### Task 1: Update Production Settings
- [ ] **File**: `game_player_nick_finder/settings/production.py`
- [ ] **Enable email requirement**: Add `ACCOUNT_EMAIL_REQUIRED = True`
- [ ] **Enable email verification**: Add `ACCOUNT_EMAIL_VERIFICATION = 'mandatory'`
- [ ] **Ensure email uniqueness**: Add `ACCOUNT_EMAIL_UNIQUE = True`
- [ ] **Configure email backend**: Change from console to SendGrid/AWS SES/Resend

**Code to add**:
```python
# Email Configuration (Production)
ACCOUNT_EMAIL_REQUIRED = True                    # CRITICAL: Email required in production
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'         # User must verify email
ACCOUNT_EMAIL_UNIQUE = True                      # Email must be unique
ACCOUNT_USERNAME_REQUIRED = True                 # Username still required

# Email Backend (Choose one)
EMAIL_BACKEND = 'sendgrid_backend.SendgridBackend'  # or 'django_ses.SESBackend'
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY')

# Email Confirmation Settings
ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 7      # Token expires after 7 days
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5                # Prevent brute force
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300            # 5 minute lockout
```

**Reference**: Check current production settings
```bash
grep -n "ACCOUNT_EMAIL" game_player_nick_finder/settings/production.py
```

#### Task 2: Keep Development Settings Unchanged
- [ ] **File**: `game_player_nick_finder/settings/local.py`
- [ ] **Keep disabled**: `ACCOUNT_EMAIL_REQUIRED = False` (for development)
- [ ] **Keep console backend**: Existing console email backend
- [ ] **Reason**: Developers should not need email during development

#### Task 3: Database Migration
- [ ] **Create migration**: Run `python manage.py makemigrations` if field changes needed
- [ ] **Document migration**: In PR description
- [ ] **Test migration**: On staging environment
- [ ] **Backup production DB**: Before applying migration

#### Task 4: Update Email Templates
- [ ] **File**: `templates/account/email/` directory
- [ ] **Verify layout**: Check confirmation email template
- [ ] **Test rendering**: Send test email with real content
- [ ] **Check branding**: Logo, colors, links match production brand
- [ ] **Verify links**: Confirmation links work correctly

**Key templates to review**:
- `email_confirmation_message.txt` - Email body
- `email_confirmation_subject.txt` - Email subject
- Base email template styling

#### Task 5: Update Signup Tests
- [ ] **File**: `tests/e2e/auth/signup.spec.ts`
- [ ] **Update test flow**: Include email in signup form
- [ ] **Test email verification**: Simulate clicking confirmation link
- [ ] **Test duplicate email**: Verify error when email already used
- [ ] **Test email required**: Verify signup fails without email
- [ ] **Verify all signup tests pass**: Run `pnpm test:e2e tests/e2e/auth/signup.spec.ts`

**Test scenarios to add**:
```javascript
// Scenario: Signup requires email
await expect(signup button to be disabled if no email)

// Scenario: Email verification required
await expect(verification email sent)
await expect(cannot login until verified)

// Scenario: Duplicate email prevention
await expect(error message for duplicate email)
```

#### Task 6: Configure Email Service (SendGrid/AWS SES)
- [ ] **Create SendGrid account** OR **Configure AWS SES**
- [ ] **Get API credentials**: Store in environment variables
- [ ] **Test email sending**: Send test email from application
- [ ] **Set up email whitelisting**: Add domain to sender policy
- [ ] **Configure bounce handling**: Set up bounce/complaint notifications
- [ ] **Document setup**: Add instructions to deployment guide

**SendGrid Setup** (recommended):
```bash
# 1. Create account at sendgrid.com
# 2. Generate API key
# 3. Set environment variable
export SENDGRID_API_KEY="SG.xxx..."

# 4. Test in Django shell
python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Body', 'noreply@yourdomain.com', ['test@example.com'])
1
```

#### Task 7: Update Deployment Docs
- [ ] **File**: `docs/deployment/DEPLOYMENT_GUIDE.md`
- [ ] **Add section**: "Email Configuration for Production"
- [ ] **Document**: All environment variables needed
- [ ] **Add checklist**: Pre-deployment email verification steps
- [ ] **Include**: Troubleshooting for email issues

---

## 🔐 Security & Configuration

### Settings Hardening

#### Task 1: Disable Debug Mode
- [ ] **File**: `game_player_nick_finder/settings/production.py`
- [ ] **Set**: `DEBUG = False` (ABSOLUTELY CRITICAL!)
- [ ] **Impact**: Hides error details from users, required for production
- [ ] **Verify**: Test that error pages don't show sensitive info

#### Task 2: Secret Key Management
- [ ] **Verify**: SECRET_KEY is NOT in version control
- [ ] **Use environment variable**: `SECRET_KEY = os.environ.get('SECRET_KEY')`
- [ ] **Generate new key**: For production (never reuse development key)
- [ ] **Rotate periodically**: Every 6 months recommended

#### Task 3: ALLOWED_HOSTS
- [ ] **File**: `game_player_nick_finder/settings/production.py`
- [ ] **Set specific domain**: `ALLOWED_HOSTS = ['yourdomain.com', 'www.yourdomain.com']`
- [ ] **Never use**: `ALLOWED_HOSTS = ['*']` in production
- [ ] **Verify**: Blocks requests to other hostnames

#### Task 4: HTTPS & Security Headers
- [ ] **Enable HTTPS**: `SECURE_SSL_REDIRECT = True`
- [ ] **Set HSTS**: `SECURE_HSTS_SECONDS = 31536000` (1 year)
- [ ] **HSTS includes subdomains**: `SECURE_HSTS_INCLUDE_SUBDOMAINS = True`
- [ ] **HSTS preload**: `SECURE_HSTS_PRELOAD = True`
- [ ] **Secure cookies**: `SESSION_COOKIE_SECURE = True`
- [ ] **CSRF secure**: `CSRF_COOKIE_SECURE = True`
- [ ] **CSRF trust origin**: `CSRF_TRUSTED_ORIGINS = ['https://yourdomain.com']`
- [ ] **X-Frame-Options**: `X_FRAME_OPTIONS = 'DENY'`
- [ ] **Content Security Policy**: Add CSP header middleware

**Security headers to add**:
```python
# In middleware or header configuration
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_SECURITY_POLICY = {
    'default-src': ("'self'",),
    'script-src': ("'self'", "cdn.jsdelivr.net"),
    'style-src': ("'self'", "cdn.jsdelivr.net", "'unsafe-inline'"),
}
```

#### Task 5: Admin URL Change
- [ ] **Do NOT use**: `/admin/` in production (too predictable)
- [ ] **File**: `game_player_nick_finder/urls.py`
- [ ] **Change to**: `/admin-panel-xyz/` or similar unpredictable path
- [ ] **Document**: Store in environment variable
- [ ] **Update login processes**: If any automated monitoring

#### Task 6: CORS & Allowed Origins
- [ ] **Disable CORS if not needed**: `CORS_ALLOWED_ORIGINS = []`
- [ ] **Or restrict**: Only to specific origins if API is used
- [ ] **Document**: Which origins are allowed and why

### Django Specific

- [ ] **Migrate to PostgreSQL**: Switch from SQLite (currently used)
- [ ] **Configure database connection**: Use environment variables for credentials
- [ ] **Enable database SSL**: If hosted remotely (PG_SSL = 'require')
- [ ] **Set up connection pooling**: If high traffic expected
- [ ] **Configure backups**: Automated daily backups

---

## 🧪 Testing (CRITICAL - Currently Only 27% Pass Rate)

### E2E Test Completion

**Current Status**: 123/456 tests pass (27%)
**Target**: 100% pass rate before production

- [ ] **Run all tests**: `pnpm test:e2e` (must all pass)
- [ ] **Load fixtures**: `pnpm load:fixtures` (required before testing)
- [ ] **Start dev server**: `python manage.py runserver 7600` (MUST use port 7600)
- [ ] **Run 3 times**: Ensure consistent passes (not flaky)
- [ ] **Document failures**: Any remaining failures in issue tracker

**Test Files to Verify**:
```
tests/e2e/auth/                 # Authentication & signup
tests/e2e/characters/           # Character CRUD & profiles
tests/e2e/friends/              # Friend system
tests/e2e/messaging/            # Messages & conversations
tests/e2e/pokes/                # POKE system
tests/e2e/blocking/             # Blocking system
tests/e2e/profile/              # User profile
tests/e2e/navigation/           # Navigation menu
```

### Security Testing

- [ ] **OWASP ZAP scan**: Run automated security scan
- [ ] **SQL injection test**: Try common injection patterns
- [ ] **XSS test**: Try script injection in forms
- [ ] **CSRF verification**: Verify CSRF tokens required
- [ ] **Password reset flow**: Verify secure token handling
- [ ] **Session security**: Verify session cookies are secure
- [ ] **Rate limiting**: Verify endpoints have rate limits (especially login, POKE)

### Performance Testing

- [ ] **Load test**: Simulate 100+ concurrent users
- [ ] **Database query optimization**: Verify no N+1 queries
- [ ] **Static files**: Verify CSS/JS minified and cached
- [ ] **Image optimization**: Verify images are optimized for web
- [ ] **Page load time**: Target < 3 seconds for main pages

### Accessibility Testing

- [ ] **WCAG 2.1 AA compliance**: Run automated audit
- [ ] **Keyboard navigation**: Verify all features work without mouse
- [ ] **Screen reader test**: Test with NVDA or JAWS
- [ ] **Color contrast**: Verify text is readable
- [ ] **Form labels**: All inputs have proper labels

---

## 📦 Database & Storage

### PostgreSQL Migration

- [ ] **Install PostgreSQL**: If not already available
- [ ] **Create production database**: With strong password
- [ ] **Configure connection**: In environment variables
- [ ] **Run migrations**: `python manage.py migrate`
- [ ] **Load data**: If migrating from SQLite, dump and restore
- [ ] **Verify data integrity**: Check record counts match
- [ ] **Enable backups**: Daily automated backups to S3/backup service
- [ ] **Test restore**: Practice restore from backup

### Media & Static Files

#### Static Files (CSS, JS)
- [ ] **Collect static files**: `python manage.py collectstatic`
- [ ] **Use CDN**: Cloudflare/AWS CloudFront for static asset delivery
- [ ] **Cache headers**: Set long cache expiry (1 year) for versioned files
- [ ] **Minification**: Verify all CSS/JS is minified

#### Media Files (Uploads)
- [ ] **Use S3 or equivalent**: Do NOT store on server filesystem
- [ ] **Configure boto3**: If using AWS S3
- [ ] **Set file permissions**: Private for user data, public for profiles
- [ ] **Enable versioning**: For S3 bucket (for recovery)
- [ ] **Implement cleanup**: Remove old/orphaned files regularly
- [ ] **Set CORS**: If front-end accesses files directly

**Configuration**:
```python
if not DEBUG:
    STORAGES = {
        'default': {
            'BACKEND': 'storages.backends.s3boto3.S3Boto3Storage',
            'OPTIONS': {
                'AWS_STORAGE_BUCKET_NAME': 'your-bucket-name',
                'AWS_S3_CUSTOM_DOMAIN': 'cdn.yourdomain.com',
            }
        }
    }
```

### Database Optimization

- [ ] **Add indexes**: For frequently queried fields
- [ ] **Analyze query performance**: Using Django Debug Toolbar in dev
- [ ] **Set up query caching**: Redis for cache backend
- [ ] **Configure connection pooling**: PgBouncer or Pgpool2
- [ ] **Vacuum & analyze**: Regular maintenance

---

## 📊 Monitoring & Logging

### Error Tracking

- [ ] **Set up Sentry**: For error aggregation and alerts
- [ ] **Configure environment**: `SENTRY_DSN` in production settings
- [ ] **Set release**: Version tracking in Sentry
- [ ] **Test error reporting**: Trigger test error, verify it appears in Sentry
- [ ] **Create alerts**: For critical errors (CRITICAL, ERROR levels)

### Application Monitoring

- [ ] **Set up New Relic/DataDog**: For performance monitoring
- [ ] **Monitor CPU**: Alert if > 80% sustained
- [ ] **Monitor Memory**: Alert if > 85% used
- [ ] **Monitor Disk**: Alert if > 90% full
- [ ] **Monitor Database**: Connection pool utilization, slow queries
- [ ] **Set up dashboards**: Visualize key metrics

### Logging

- [ ] **Centralized logging**: CloudWatch, Loggly, or ELK stack
- [ ] **Log level**: Set to WARNING in production (not DEBUG)
- [ ] **Request logging**: Log all incoming requests (IP, method, path, status)
- [ ] **Error logging**: Full stack traces with context
- [ ] **Audit logging**: Log sensitive actions (user creation, permissions changes)
- [ ] **Log retention**: Keep for 30-90 days minimum

**Configuration**:
```python
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'WARNING',
            'class': 'logging.FileHandler',
            'filename': '/var/log/django/error.log',
        },
        'sentry': {
            'level': 'ERROR',
            'class': 'sentry_sdk.integrations.logging.EventHandler',
        },
    },
}
```

### Uptime Monitoring

- [ ] **Set up Pingdom/UptimeRobot**: External uptime monitoring
- [ ] **Configure health check endpoint**: `/health/` returns 200 if healthy
- [ ] **Monitor every 5 minutes**: More frequent = faster incident response
- [ ] **Set up SMS alerts**: For critical downtime
- [ ] **Document SLA**: Target uptime (e.g., 99.9%)

---

## ⚖️ Legal & Compliance

### Privacy & Terms

- [ ] **Write Privacy Policy**: Cover data collection, retention, usage
- [ ] **Write Terms of Service**: User obligations, liability limitations
- [ ] **Publish on website**: Add /privacy/ and /terms/ pages
- [ ] **Get legal review**: If handling sensitive data
- [ ] **GDPR compliance**: If EU users (data deletion, DPIA, DPA with vendor)
- [ ] **CCPA compliance**: If California users

### Cookies & Tracking

- [ ] **Cookie consent**: If using analytics (Google Analytics, Mixpanel)
- [ ] **Disclosure**: Clearly state what cookies are used
- [ ] **Opt-out**: Option to disable non-essential cookies
- [ ] **Privacy banner**: Sticky banner on first visit

### Data Protection

- [ ] **Encrypt at rest**: Database encryption, file encryption
- [ ] **Encrypt in transit**: HTTPS everywhere, TLS 1.2+
- [ ] **Data retention policy**: Define how long data is kept
- [ ] **Deletion policy**: How users can request account/data deletion
- [ ] **Export policy**: How users can export their data (GDPR right)

### Compliance Certifications

- [ ] **SOC 2 (if B2B)**: Security and controls certification
- [ ] **PCI DSS (if handling payments)**: Payment card security
- [ ] **ISO 27001 (if enterprise)**: Information security management
- [ ] **HIPAA (if health data)**: Health information security

---

## 🚀 Deployment Checklist

### Pre-Deployment

- [ ] **Staging environment**: Test deployment process on staging first
- [ ] **Backup production database**: Before deploying
- [ ] **Backup media files**: Before deploying
- [ ] **Document rollback plan**: How to quickly revert if problems
- [ ] **Notify team**: When deployment will occur
- [ ] **Schedule**: During low-traffic window (early morning/late night)
- [ ] **Have rollback ready**: Keep previous version available for quick revert

### Environment Variables

Ensure these are set in production:

- [ ] `DEBUG = False`
- [ ] `SECRET_KEY = <random 50 char key>`
- [ ] `ALLOWED_HOSTS = yourdomain.com,www.yourdomain.com`
- [ ] `DATABASE_URL = postgresql://user:pass@host/dbname`
- [ ] `SENDGRID_API_KEY = SG.xxxxx`
- [ ] `SENTRY_DSN = https://xxxxx`
- [ ] `AWS_ACCESS_KEY_ID = <key>`
- [ ] `AWS_SECRET_ACCESS_KEY = <secret>`
- [ ] `AWS_STORAGE_BUCKET_NAME = <bucket>`
- [ ] `SECURE_SSL_REDIRECT = True`
- [ ] `SESSION_COOKIE_SECURE = True`

### Deployment Process

- [ ] **Run migrations**: `python manage.py migrate --noinput`
- [ ] **Collect static files**: `python manage.py collectstatic --noinput`
- [ ] **Restart application**: Gracefully restart worker processes
- [ ] **Warm up cache**: Pre-populate cache with common queries
- [ ] **Monitor errors**: Watch Sentry for 30 minutes after deployment

### Health Checks

- [ ] **API health endpoint**: GET `/health/` returns 200 JSON
- [ ] **Database connectivity**: Can query at least one table
- [ ] **Static files serving**: CSS/JS files load correctly
- [ ] **Email sending**: Can send test email
- [ ] **Critical pages load**: Homepage, login, signup work

**Health check endpoint** (add to views):
```python
from django.http import JsonResponse
from django.views import View
from django.db import connection

class HealthCheckView(View):
    def get(self, request):
        try:
            with connection.cursor() as cursor:
                cursor.execute("SELECT 1")
            return JsonResponse({'status': 'healthy'})
        except Exception as e:
            return JsonResponse({'status': 'unhealthy', 'error': str(e)}, status=500)
```

---

## 📋 Post-Deployment

### First 24 Hours

- [ ] **Monitor error rate**: Check Sentry every hour
- [ ] **Monitor performance**: Check New Relic/DataDog
- [ ] **Test critical paths**: Manually test key user flows
- [ ] **Check logs**: Look for warnings/errors in application logs
- [ ] **Monitor database**: Check for slow queries or connection issues
- [ ] **Verify email**: Check that verification emails are being sent
- [ ] **User feedback**: Monitor for user-reported issues

### First Week

- [ ] **Performance baseline**: Measure and document
- [ ] **Error trending**: Ensure errors decreasing over time
- [ ] **Load testing**: Verify can handle expected load
- [ ] **Security scan**: Run security scan again
- [ ] **Backup verification**: Test database restore from production backup

### Ongoing Monitoring

- [ ] **Weekly review**: Check error trends, performance metrics
- [ ] **Monthly**: Review security logs, access patterns
- [ ] **Quarterly**: Security audit, dependency updates, architecture review
- [ ] **Annually**: Full penetration test, compliance review

---

## 📚 Related Documentation

- [CLAUDE.md - Email Configuration](../CLAUDE.md#special-configurations)
- [Django Deployment Checklist](https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/)
- [SendGrid Django Integration](https://github.com/suredev/django-sendgrid-v5)
- [OWASP Deployment Checklist](https://owasp.org/www-project-deployment-checklist/)
- [12-Factor App Methodology](https://12factor.net/)

---

## 🎯 Next Steps

1. **Immediate** (This Sprint):
   - [ ] Review this checklist with team
   - [ ] Estimate effort for each section
   - [ ] Assign ownership (who will work on what)

2. **Short-term** (Next 1-2 weeks):
   - [ ] Implement email validation settings
   - [ ] Update tests to require email
   - [ ] Set up email service (SendGrid/AWS SES)

3. **Medium-term** (2-4 weeks):
   - [ ] Complete all security hardening
   - [ ] Verify all E2E tests pass (27% → 100%)
   - [ ] Set up monitoring and logging

4. **Before Go-Live** (Final checks):
   - [ ] Run full security audit
   - [ ] Complete staging environment testing
   - [ ] Final checklist review
   - [ ] Get sign-off from Product Owner

---

## ⚠️ CRITICAL REMINDERS

- **EMAIL VALIDATION IS NOT OPTIONAL**: Must be enabled before production
- **DEBUG MUST BE FALSE**: Never deploy with DEBUG=True
- **TESTS MUST PASS**: Don't deploy if tests are failing
- **BACKUP BEFORE DEPLOY**: Always have a rollback plan
- **MONITOR AFTER DEPLOY**: Watch for errors and performance issues

**DO NOT DEPLOY TO PRODUCTION WITHOUT COMPLETING THIS CHECKLIST!**

---

**Checklist Version**: 1.0
**Last Updated**: 2025-12-28
**Maintained By**: Development Team
