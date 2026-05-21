# Optimized File Structure Example

Reference this mapping when consolidating a messy repository into an optimized, modular architecture.

## 1. API Consolidation

**Before (Messy & Conflicting):**
```
src/
  api.js          (Uses fetch for users)
  auth.js         (Uses axios for login)
  userApi.js      (Uses fetch for users again)
```

**After (Optimized & Modular):**
```
src/
  services/
    apiConfig.js  (Unified axios instance with baseURL and interceptors)
    authApi.js    (Uses apiConfig)
    userApi.js    (Uses apiConfig)
```

## 2. Component Cleanup

**Before (Orphans & Dead Code):**
```
components/
  Header.jsx
  Header-old.jsx  (Unused)
  Header-v2.jsx   (Unused prototype)
```

**After (Clean):**
```
components/
  Header.jsx
```

## 3. Game-Dev Style Lazy Loading & Splitting

**Before (Monolithic / Blocking):**
```javascript
import HeavyChart from './HeavyChart';
import 3DModelViewer from './3DModelViewer';

function Dashboard() {
    return <div> <HeavyChart /> <3DModelViewer /> </div>
}
```

**After (Splitting / Culling / Progress Loading):**
```javascript
import React, { Suspense, lazy } from 'react';
// Lazy load resources only when needed
const HeavyChart = lazy(() => import('./HeavyChart'));
const ModelViewer = lazy(() => import('./3DModelViewer'));

function Dashboard() {
    return (
        <Suspense fallback={<LoadingSpinner />}>
            {/* Implement intersection observer to only render inside Viewport (Frustum Culling equivalent) */}
            <heavyChart />
            <ModelViewer />
        </Suspense>
    )
}
```
