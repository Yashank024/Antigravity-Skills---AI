# Architecture Planning Checklist

Before finalizing a project architecture proposal, ensure the following bases are covered:

## 1. Domain Separation
- [ ] Is the business logic clearly separated from UI rendering logic?
- [ ] Are features isolated (e.g., Auth shouldn't be tightly coupled inside Dashboard logic)?

## 2. Global State vs. Local State
- [ ] Has it been explicitly decided what data lives in global context vs. local component state? (Avoid dumping everything into Redux/Context).
- [ ] Is server state (API caching) separated from client UI state?

## 3. Performance Considerations
- [ ] Are route-level components configured for code-splitting / lazy loading?
- [ ] Are heavy third-party dependencies evaluated for dynamic importing?

## 4. DX (Developer Experience)
- [ ] Is the folder structure intuitive for a new developer joining the team?
- [ ] Are barrel files (`index.js`/`ts`) utilized to keep imports clean?
- [ ] Is there a clear place for testing (e.g., `__tests__` folders next to components)?
