# Cloudflare + AUG Migration Architecture

## Document Purpose
This document describes the architectural approach for migrating the Game Player Nick Finder application to Cloudflare infrastructure with AUG (Application User Gateway) integration. It is intended for Tech Leads and mid-level developers who will be involved in the migration process.

## Executive Summary

The migration to Cloudflare will leverage:
- **Cloudflare Pages** for static frontend assets
- **Cloudflare Workers** for serverless backend API
- **Cloudflare D1** (SQLite) or **Cloudflare Durable Objects** for database
- **Cloudflare R2** for media storage (avatars, game icons)
- **Cloudflare AUG** for authentication and user management
- **Cloudflare Images** for image optimization

## Current Architecture

### Technology Stack
- **Backend**: Django 5.1.4 (Python 3.10+)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates + Bootstrap 5
- **Authentication**: django-allauth (Google OAuth)
- **Media Storage**: Local filesystem
- **Deployment**: Gunicorn + PM2 + Nginx

### Current Components
1. **Django Application**
   - Models: CustomUser, Character, Game, Message, Friend, FriendRequest
   - Views: Class-based and function-based views
   - Forms: Django forms with crispy-forms
   - API: Django REST Framework
   - Templates: Django template engine

2. **Database Schema**
   - CustomUser (UUID primary key)
   - Character (multiple per user, linked to games)
   - Game (with categories, voting system)
   - Message (character-to-character messaging with thread_id)
   - Friend/FriendRequest (user-level relationships)

3. **Key Features**
   - User registration and authentication
   - Character management (multiple characters per user)
   - Game management and voting
   - Messaging system (character-based)
   - Friend system (user-based, not fully implemented)

## Target Architecture (Cloudflare)

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    Cloudflare Edge Network                    │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐  │
│  │   Cloudflare │    │   Cloudflare  │    │   Cloudflare  │  │
│  │    Pages     │    │    Workers    │    │      AUG     │  │
│  │  (Frontend)  │◄───┤   (Backend)   │◄───┤  (Auth)      │  │
│  └──────────────┘    └──────────────┘    └──────────────┘  │
│         │                   │                      │         │
│         │                   │                      │         │
│         └───────────────────┼──────────────────────┘         │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │  Cloudflare D1  │                       │
│                    │   (Database)    │                       │
│                    └─────────────────┘                       │
│                             │                                │
│                    ┌────────▼────────┐                       │
│                    │  Cloudflare R2  │                       │
│                    │  (Media Storage) │                       │
│                    └─────────────────┘                       │
└─────────────────────────────────────────────────────────────┘
```

### Component Breakdown

#### 1. Cloudflare Pages (Frontend)
- **Purpose**: Host static frontend assets
- **Technology**: Pre-rendered HTML/CSS/JS or React/Vue if migrating
- **Build Process**: 
  - Option A: Keep Django templates, pre-render to static HTML
  - Option B: Migrate to React/Vue SPA with API calls
- **Deployment**: Git-based CI/CD via Cloudflare Pages

#### 2. Cloudflare Workers (Backend API)
- **Purpose**: Serverless backend replacing Django
- **Technology**: JavaScript/TypeScript or Python (via Pyodide)
- **Key Considerations**:
  - Workers have execution time limits (CPU time: 50ms free tier, 30s paid)
  - Need to handle Django ORM migration
  - Consider using D1 SQL queries directly or ORM-like library
- **API Endpoints**: RESTful API replacing Django views

#### 3. Cloudflare D1 (Database)
- **Purpose**: SQLite-based database (compatible with current SQLite)
- **Migration Path**: 
  - Export current SQLite database
  - Import to D1
  - Update schema if needed
- **Limitations**: 
  - SQLite compatibility (no PostgreSQL-specific features)
  - Read replicas for scaling
- **Alternative**: Consider Cloudflare Durable Objects for real-time features

#### 4. Cloudflare R2 (Media Storage)
- **Purpose**: Object storage for avatars, game icons
- **Migration**: 
  - Upload existing media files to R2
  - Update URLs in database
  - Configure CDN for fast delivery
- **Integration**: Cloudflare Images for automatic optimization

#### 5. Cloudflare AUG (Application User Gateway)
- **Purpose**: Authentication and user management
- **Features**:
  - OAuth providers (Google, Facebook, etc.)
  - User session management
  - JWT tokens
- **Migration**: Replace django-allauth with AUG

## Migration Strategy

### Phase 1: Preparation (Weeks 1-2)
**Goal**: Set up Cloudflare infrastructure and prepare migration tools

**Tasks**:
1. Create Cloudflare account and configure organization
2. Set up Cloudflare Pages project
3. Set up Cloudflare Workers project
4. Create D1 database instance
5. Create R2 bucket for media
6. Configure AUG for authentication
7. Create migration scripts for data export/import

**Deliverables**:
- Cloudflare infrastructure ready
- Migration scripts ready
- Test environment configured

### Phase 2: Database Migration (Week 3)
**Goal**: Migrate database schema and data to D1

**Tasks**:
1. Export current database schema
2. Convert Django models to D1-compatible schema
3. Export all data from current database
4. Import data to D1
5. Verify data integrity
6. Create database access layer (ORM replacement)

**Deliverables**:
- D1 database with all data migrated
- Database access layer implemented
- Data integrity verified

### Phase 3: Backend API Migration (Weeks 4-6)
**Goal**: Migrate Django backend to Cloudflare Workers

**Tasks**:
1. Identify all API endpoints
2. Create Workers for each endpoint group
3. Migrate authentication logic to AUG
4. Migrate business logic from Django views
5. Implement database queries using D1
6. Set up media upload/download via R2
7. Implement WebSocket support for real-time messaging (if needed)

**Deliverables**:
- All API endpoints working in Workers
- Authentication via AUG
- Media handling via R2

### Phase 4: Frontend Migration (Weeks 7-8)
**Goal**: Migrate frontend to Cloudflare Pages

**Tasks**:
1. Option A: Pre-render Django templates to static HTML
2. Option B: Migrate to SPA framework (React/Vue)
3. Update API calls to point to Workers
4. Update authentication flow to use AUG
5. Update media URLs to use R2
6. Test all user flows

**Deliverables**:
- Frontend deployed on Cloudflare Pages
- All features working end-to-end
- User flows tested

### Phase 5: Testing & Optimization (Week 9)
**Goal**: Comprehensive testing and performance optimization

**Tasks**:
1. End-to-end testing
2. Load testing
3. Performance optimization
4. Security audit
5. Fix bugs and issues
6. Documentation update

**Deliverables**:
- Application fully tested
- Performance optimized
- Documentation updated

### Phase 6: Cutover (Week 10)
**Goal**: Switch production traffic to Cloudflare

**Tasks**:
1. Final data sync
2. DNS cutover
3. Monitor for issues
4. Rollback plan ready
5. Post-migration verification

**Deliverables**:
- Application running on Cloudflare
- All systems operational

## Technical Challenges & Solutions

### Challenge 1: Django ORM to D1 Migration
**Problem**: Django ORM doesn't work in Workers environment
**Solution**: 
- Use D1's native SQL API
- Create lightweight ORM-like wrapper
- Or use existing libraries like `drizzle-orm` or `kysely`

### Challenge 2: Python Code in Workers
**Problem**: Workers primarily support JavaScript/TypeScript
**Solution**:
- Option A: Rewrite Python code to JavaScript/TypeScript
- Option B: Use Pyodide for Python execution (limited)
- Option C: Keep critical Python logic in separate service

### Challenge 3: Real-time Messaging
**Problem**: Workers don't support long-lived connections
**Solution**:
- Use Cloudflare Durable Objects for WebSocket connections
- Or use polling for message updates
- Or use Cloudflare Pub/Sub

### Challenge 4: File Uploads
**Problem**: Workers have size limits
**Solution**:
- Use R2's direct upload feature
- Generate pre-signed URLs for client-side uploads
- Process images via Cloudflare Images API

### Challenge 5: Session Management
**Problem**: Django sessions don't work in Workers
**Solution**:
- Use AUG for session management
- Or use JWT tokens stored in cookies
- Or use D1 for session storage

## Data Migration Plan

### Database Schema Mapping

| Django Model | D1 Table | Notes |
|-------------|----------|-------|
| CustomUser | users | UUID primary key preserved |
| Character | characters | UUID primary key preserved |
| Game | games | Auto-increment ID can stay or convert to UUID |
| GameCategory | game_categories | Auto-increment ID |
| Message | messages | UUID thread_id preserved |
| Friend | friends | User-to-user relationships |
| FriendRequest | friend_requests | User-to-user relationships |
| Vote | votes | Game voting system |
| EmailNotification | email_notifications | Notification history |

### Migration Script Structure

```javascript
// Example migration script structure
async function migrateDatabase() {
  // 1. Export from Django/SQLite
  const data = await exportFromDjango();
  
  // 2. Transform data if needed
  const transformed = transformData(data);
  
  // 3. Import to D1
  await importToD1(transformed);
  
  // 4. Verify
  await verifyMigration();
}
```

## API Endpoint Mapping

### Current Django URLs → Cloudflare Workers Routes

| Django URL | Worker Route | Method | Notes |
|-----------|--------------|--------|-------|
| `/api/v1/games/` | `/api/v1/games` | GET, POST | List/create games |
| `/api/v1/characters/` | `/api/v1/characters` | GET, POST | List/create characters |
| `/messages/` | `/api/v1/messages` | GET, POST | Message list/send |
| `/accounts/profile/` | `/api/v1/users/me` | GET, PUT | User profile |
| `/character/add/` | `/api/v1/characters` | POST | Create character |

## Security Considerations

1. **Authentication**: AUG handles OAuth and session management
2. **Authorization**: Implement role-based access control in Workers
3. **CSRF Protection**: Use Cloudflare's built-in CSRF protection
4. **Rate Limiting**: Use Cloudflare Rate Limiting
5. **DDoS Protection**: Cloudflare's automatic DDoS protection
6. **Data Encryption**: Use HTTPS everywhere (automatic with Cloudflare)

## Performance Optimization

1. **Caching**: Use Cloudflare Cache API for frequently accessed data
2. **CDN**: Automatic CDN for static assets
3. **Image Optimization**: Cloudflare Images for automatic optimization
4. **Database Indexing**: Ensure proper indexes in D1
5. **Lazy Loading**: Implement lazy loading for large datasets

## Monitoring & Observability

1. **Cloudflare Analytics**: Built-in analytics for Workers
2. **Logs**: Cloudflare Workers Logs
3. **Error Tracking**: Integrate with Sentry or similar
4. **Performance Monitoring**: Cloudflare Web Analytics
5. **Database Monitoring**: D1 query analytics

## Cost Estimation

### Cloudflare Pricing (Approximate)

| Service | Free Tier | Paid Tier | Estimated Monthly Cost |
|---------|-----------|-----------|------------------------|
| Pages | Unlimited | Included | $0-20 |
| Workers | 100k requests/day | $5/10M requests | $5-50 |
| D1 | 5GB storage, 5M reads | $0.001/GB storage, $1/25M reads | $0-30 |
| R2 | 10GB storage, 1M operations | $0.015/GB storage | $0-20 |
| AUG | Limited | Custom pricing | $0-50 |
| **Total** | | | **$5-170/month** |

*Costs depend on usage. Free tier may be sufficient for initial deployment.*

## Rollback Plan

1. **DNS Rollback**: Switch DNS back to original server
2. **Database Backup**: Keep original database as backup
3. **Code Rollback**: Maintain original Django codebase
4. **Data Sync**: If needed, sync data back from D1 to original DB

## Success Criteria

1. ✅ All features working on Cloudflare
2. ✅ Performance equal or better than current
3. ✅ Zero data loss during migration
4. ✅ All users can authenticate and use app
5. ✅ Media files accessible and optimized
6. ✅ API endpoints responding correctly
7. ✅ Real-time features working (if applicable)

## Next Steps

1. Review and approve this architecture document
2. Assign team members to migration phases
3. Set up Cloudflare accounts and infrastructure
4. Begin Phase 1: Preparation
5. Schedule regular migration status meetings

## References

- [Cloudflare Workers Documentation](https://developers.cloudflare.com/workers/)
- [Cloudflare D1 Documentation](https://developers.cloudflare.com/d1/)
- [Cloudflare Pages Documentation](https://developers.cloudflare.com/pages/)
- [Cloudflare R2 Documentation](https://developers.cloudflare.com/r2/)
- [Cloudflare AUG Documentation](https://developers.cloudflare.com/cloudflare-one/applications/configure-apps/)

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Author**: Solution Architect  
**Reviewers**: Tech Leads, Development Team

