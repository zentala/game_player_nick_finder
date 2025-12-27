# 002 - Technology Stack - Game Player Nick Finder

**Status**: 📋 Planning document - Target stack for future migration  
**Last Updated**: 2024

## Document Purpose
This document defines the complete technology stack for the Game Player Nick Finder application, including frontend framework, UI library, testing tools, and development workflow.

## Recommended Technology Stack

### Frontend Stack

#### Framework: Next.js 14+ (App Router)
**Why Next.js?**
- ✅ Server-side rendering (SSR) and static site generation (SSG)
- ✅ Excellent Cloudflare Pages integration
- ✅ Built-in API routes (can replace some Workers)
- ✅ Automatic code splitting and optimization
- ✅ TypeScript support out of the box
- ✅ Minimal configuration needed
- ✅ Great developer experience

**Alternative Considered**: Remix, but Next.js has better Cloudflare integration

#### Language: TypeScript
**Why TypeScript?**
- ✅ Type safety reduces bugs
- ✅ Better IDE support and autocomplete
- ✅ Easier refactoring
- ✅ Self-documenting code
- ✅ Industry standard

#### UI Library: Joy UI (MUI Joy)
**Why Joy UI over Material UI?**
- ✅ Modern, clean design system
- ✅ Better customization options
- ✅ Less opinionated than Material UI
- ✅ Built on MUI (mature ecosystem)
- ✅ Excellent TypeScript support
- ✅ Smaller bundle size than Material UI
- ✅ Better for gaming/social media aesthetics
- ✅ More flexible theming

**Comparison**:
- Material UI: More components, but heavier and more opinionated
- Joy UI: Modern, lightweight, flexible, perfect for custom designs
- Chakra UI: Good alternative, but Joy UI has better MUI ecosystem integration

#### Styling: Tailwind CSS (Optional, with Joy UI)
**Why Tailwind?**
- ✅ Utility-first approach = less code
- ✅ Rapid development
- ✅ Consistent design system
- ✅ Works well with Joy UI
- ✅ Easy customization

**Note**: Joy UI can work standalone, but Tailwind adds utility classes for rapid development

### Backend Stack (Cloudflare)

#### API: Cloudflare Workers (TypeScript)
- Serverless functions
- Edge computing
- Fast response times
- TypeScript support

#### Database: Cloudflare D1 (SQLite)
- Compatible with current SQLite
- Edge-optimized
- Simple migration path

#### Storage: Cloudflare R2
- S3-compatible
- Media files (avatars, screenshots)
- Cost-effective

#### Authentication: Cloudflare AUG
- OAuth providers
- Session management
- JWT tokens

### Testing Stack

#### E2E Testing: Playwright
**Why Playwright?**
- ✅ Cross-browser testing (Chromium, Firefox, WebKit)
- ✅ Fast and reliable
- ✅ Great debugging tools
- ✅ TypeScript support
- ✅ Mobile device emulation
- ✅ Screenshot and video recording
- ✅ Better than Cypress for modern apps

#### Unit Testing: Vitest
**Why Vitest?**
- ✅ Fast (Vite-based)
- ✅ TypeScript support
- ✅ Jest-compatible API
- ✅ Works great with Next.js

#### Component Testing: React Testing Library
- Component isolation testing
- User-centric testing approach
- Works with Vitest

### Development Tools

#### Package Manager: pnpm
**Why pnpm?**
- ✅ Faster than npm/yarn
- ✅ Disk space efficient
- ✅ Better monorepo support
- ✅ Strict dependency resolution

#### Build Tool: Next.js (built-in)
- Uses Turbopack (faster than Webpack)
- Automatic optimization
- No additional config needed

#### Linting: ESLint + TypeScript ESLint
- Code quality
- TypeScript-specific rules
- Next.js recommended config

#### Formatting: Prettier
- Consistent code style
- Automatic formatting

## Architecture Decision

### Current State → Target State

**Current**:
```
Django Templates + Bootstrap 5
→ Server-side rendered HTML
→ Limited interactivity
→ Hard to maintain
```

**Target**:
```
Next.js 14 (App Router) + TypeScript + Joy UI
→ Server-side rendering + Client-side interactivity
→ Component-based architecture
→ Type-safe
→ Modern UX
→ Easy to test with Playwright
```

### Migration Strategy

#### Phase 1: Setup New Frontend (Week 1)
1. Initialize Next.js 14 project with TypeScript
2. Install Joy UI and configure theme
3. Set up Tailwind CSS (optional)
4. Configure Playwright
5. Set up development environment

#### Phase 2: Component Migration (Weeks 2-3)
1. Create base components (Button, Input, Card, etc.) with Joy UI
2. Migrate existing pages one by one
3. Keep Django backend running during migration
4. Connect Next.js frontend to Django API

#### Phase 3: Full Migration (Weeks 4-6)
1. Migrate backend to Cloudflare Workers
2. Migrate database to Cloudflare D1
3. Deploy Next.js to Cloudflare Pages
4. Switch DNS

## Project Structure

```
game_player_nick_finder/
├── frontend/                    # Next.js application
│   ├── app/                    # Next.js App Router
│   │   ├── (auth)/             # Auth routes
│   │   ├── (dashboard)/        # Dashboard routes
│   │   ├── api/                # API routes (if needed)
│   │   └── layout.tsx          # Root layout
│   ├── components/             # React components
│   │   ├── ui/                 # Joy UI components
│   │   ├── features/           # Feature components
│   │   └── layouts/            # Layout components
│   ├── lib/                    # Utilities
│   │   ├── api/                # API client
│   │   ├── hooks/              # Custom hooks
│   │   └── utils/              # Helper functions
│   ├── styles/                 # Global styles
│   ├── tests/                  # Test files
│   │   ├── e2e/                # Playwright tests
│   │   ├── unit/                # Unit tests
│   │   └── components/          # Component tests
│   └── playwright.config.ts    # Playwright config
├── backend/                    # Cloudflare Workers (future)
│   └── src/
│       └── api/                # API handlers
├── shared/                     # Shared types/utilities
│   └── types/                  # TypeScript types
└── docs/                       # Documentation
```

## Code Example: Component Structure

### Joy UI Component Example

```typescript
// components/features/messaging/MessageBubble.tsx
import { Box, Typography, Avatar } from '@mui/joy';
import { Message } from '@/types';

interface MessageBubbleProps {
  message: Message;
  isOwn: boolean;
}

export function MessageBubble({ message, isOwn }: MessageBubbleProps) {
  return (
    <Box
      sx={{
        display: 'flex',
        gap: 1,
        flexDirection: isOwn ? 'row-reverse' : 'row',
        mb: 2,
      }}
    >
      <Avatar src={message.sender.avatar} />
      <Box
        sx={{
          bgcolor: isOwn ? 'primary.50' : 'neutral.100',
          p: 2,
          borderRadius: 2,
          maxWidth: '70%',
        }}
      >
        <Typography level="body-sm" fontWeight="lg">
          {message.sender.nickname}
          {message.identityRevealed && (
            <Typography level="body-xs" color="neutral">
              (@{message.sender.user.username})
            </Typography>
          )}
        </Typography>
        <Typography>{message.content}</Typography>
        <Typography level="body-xs" color="neutral">
          {formatTime(message.sentDate)}
        </Typography>
      </Box>
    </Box>
  );
}
```

### Playwright Test Example

```typescript
// tests/e2e/messaging.spec.ts
import { test, expect } from '@playwright/test';

test.describe('Messaging', () => {
  test('should send anonymous message', async ({ page }) => {
    await page.goto('/characters/character-123');
    await page.click('text=Send Message');
    
    // Select anonymous mode
    await page.click('input[value="anonymous"]');
    
    // Type message
    await page.fill('textarea[name="content"]', 'Hello!');
    
    // Send
    await page.click('button:has-text("Send")');
    
    // Verify message sent
    await expect(page.locator('.message-sent')).toBeVisible();
    await expect(page.locator('.message-sent')).toContainText('Hello!');
    
    // Verify anonymous indicator
    await expect(page.locator('.privacy-badge')).toContainText('Anonymous');
  });
});
```

## Development Workflow

### 1. Feature Development
1. Create feature branch
2. Write Playwright test first (TDD)
3. Implement feature
4. Run tests (unit + E2E)
5. Code review
6. Merge

### 2. Testing Workflow
```bash
# Run all tests
pnpm test

# Run Playwright tests
pnpm test:e2e

# Run Playwright in UI mode
pnpm test:e2e:ui

# Run specific test
pnpm test:e2e tests/e2e/messaging.spec.ts
```

### 3. Code Quality
- ESLint runs on save
- Prettier formats on save
- Pre-commit hooks run tests
- CI/CD runs full test suite

## Performance Optimization

### Next.js Optimizations
- Automatic code splitting
- Image optimization (next/image)
- Font optimization
- Static generation where possible

### Joy UI Optimizations
- Tree-shaking (only import used components)
- CSS-in-JS with minimal runtime
- Component lazy loading

### Bundle Size Targets
- Initial load: < 100KB (gzipped)
- Total bundle: < 500KB (gzipped)
- Lazy-loaded components: Load on demand

## Browser Support

- Chrome/Edge: Latest 2 versions
- Firefox: Latest 2 versions
- Safari: Latest 2 versions
- Mobile: iOS Safari, Chrome Mobile

## Accessibility

- WCAG AA compliance
- Keyboard navigation
- Screen reader support
- Joy UI components are accessible by default

## Security

- CSRF protection (Next.js built-in)
- XSS prevention (React built-in)
- Input validation
- Secure authentication (Cloudflare AUG)

## Deployment

### Cloudflare Pages
- Automatic deployments from Git
- Preview deployments for PRs
- Edge caching
- Global CDN

### Environment Variables
- Development: `.env.local`
- Production: Cloudflare Pages dashboard
- Secrets: Cloudflare Workers secrets

## Cost Estimation

### Development Tools
- **Next.js**: Free (open source)
- **Joy UI**: Free (open source)
- **Playwright**: Free (open source)
- **TypeScript**: Free (open source)

### Cloudflare Costs
- **Pages**: Free tier (unlimited requests)
- **Workers**: $5/month (10M requests)
- **D1**: Free tier (5GB storage, 5M reads)
- **R2**: $0.015/GB storage

**Total**: ~$5-20/month for small to medium traffic

## Migration Timeline

### Week 1: Setup
- Initialize Next.js project
- Install dependencies
- Set up Playwright
- Create base components

### Week 2-3: Component Library
- Create reusable UI components
- Set up theme and styling
- Implement authentication flow
- Write initial Playwright tests

### Week 4-6: Feature Migration
- Migrate character management
- Migrate messaging system
- Migrate friend system
- Migrate user profile

### Week 7-8: Polish & Testing
- Complete Playwright test coverage
- Performance optimization
- Bug fixes
- Documentation

## Recommendations

### ✅ Do
- Use TypeScript strictly (no `any`)
- Write Playwright tests for all user flows
- Use Joy UI components (don't reinvent)
- Follow Next.js best practices
- Keep components small and focused
- Write reusable hooks

### ❌ Don't
- Don't use Material UI (too heavy, too opinionated)
- Don't skip Playwright tests
- Don't use `any` in TypeScript
- Don't create custom components when Joy UI has them
- Don't mix styling approaches (stick to Joy UI + Tailwind)

## Conclusion

**Recommended Stack**:
- **Frontend**: Next.js 14 + TypeScript + Joy UI + Tailwind CSS
- **Testing**: Playwright (E2E) + Vitest (Unit) + React Testing Library
- **Backend**: Cloudflare Workers + D1 + R2 + AUG
- **Package Manager**: pnpm

This stack provides:
- ✅ Fast development (less code, more features)
- ✅ Type safety (fewer bugs)
- ✅ Modern UX (Joy UI)
- ✅ Easy testing (Playwright)
- ✅ Scalable architecture (Cloudflare)
- ✅ Cost-effective (mostly free tier)

---

**Document Version**: 1.0  
**Last Updated**: 2024  
**Maintained By**: Tech Lead, Solution Architect

