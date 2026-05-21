# Advanced Optimization Techniques

The following techniques bridge the gap between high-performance game developement and modern web/backend applications. Apply these proactively during heavy optimization passes.

## 1. Rendering & Visibility
- **Frustum Culling / Occlusion Culling**: Render only what is inside the camera view or viewport. Disable off-screen rendering. (In web: Intersection Observer, Virtualization).
- **Virtualization**: Do not render massive lists. If dealing with 10,000 items, render only the visible ones using libraries like `react-window` or `react-virtualized`.
- **Level of Detail (LOD)**: Load low-fidelity placeholders for distant/background elements or before interaction, switching to high-fidelity on demand.

## 2. Loading & Delivery
- **Lazy Loading**: If a resource is not immediately required, defer it. (Images, `React.lazy()` for components, deferred chunk loading).
- **Code Splitting**: Divide massive JS bundles into smaller chunks (`auth.js`, `dashboard.js`) avoiding single monolithic `bundle.js`.
- **Tree Shaking**: Strip away unused exports during build. Avoid heavy imports like full `lodash` in favor of specific path imports (`lodash/debounce`).
- **CDN Optimization & Asset Streaming**: Push static files (images, JS, CSS, 3D models) to edge servers. Stream map tiles or assets progressively instead of locking the UI.
- **Compression**: Use gzip/brotli for payloads. Compress static images automatically.

## 3. Data & State Management
- **Caching**: Store frequently requested data. Use memory caches, Redis, or simple browser-level caching to prevent repeated identical API calls.
- **Data Batching**: Combine multiple network loops. Instead of separate `GET /user`, `GET /orders`, and `GET /cart` loops, batch them or create a dedicated `GET /dashboard-data` endpoint.
- **Memoization**: Prevent repeating identical expensive calculations using React's `useMemo`, `useCallback`, or backend compute caches.
- **Progressive Loading**: Show data gradually (e.g., image blur-up previews turning into full renders).

## 4. Execution Control
- **Debouncing**: Delay rapid user events (search inputs, resize). 100 keystrokes = 1 API call.
- **Throttling**: Cap execution rate for continuous events (scroll handlers, mouse move).
- **Object Pooling**: Instead of constantly destroying and creating objects (causing garbage collection spikes), reuse them. Excellent for Canvas, WebGL, or particle generation.
- **Parallel Processing & Worker Threads**: Execute multiple independent async requests simultaneously via `Promise.all()`. Offload heavy compute to Web Workers or Node Worker Threads so the main thread remains unblocked.
- **Database Query Optimization & Indexing**: Detect and destroy N+1 queries. Use single JOIN queries. Add indexes for heavily searched columns (e.g., `userId`, `email`).
