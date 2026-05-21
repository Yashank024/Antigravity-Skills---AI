---
name: api-integration-helper
description: Assists with integrating REST or GraphQL APIs into frontend applications. Use when fetching data, handling loading/error states, or communicating with backends.
---

# API Integration Helper

This skill establishes strong data-fetching and state management patterns.

## Trigger Keywords

Activate this skill if the request mentions:
- api integration
- fetch data
- rest api
- graphql
- loading states
- error handling
- axios
- react query

## When to use

- Fetching user data, submitting forms, or syncing client state.
- Integrating third-party APIs.
- Setting up React Query or native `fetch` wrappers.

## Integration Workflow

1. **Complete State Management**: Always handle `loading`, `success`, and `error` states gracefully to provide good UX.
2. **Safety**: Use `AbortController` (or equivalent mechanisms) to cancel requests on component unmount and avoid setting state on unmounted components.
3. **Separation of Concerns**: Try to separate data fetching logic into custom hooks (e.g., `useData`, `useUser`) rather than cluttering UI components.
4. **Error Handling**: Log errors clearly and provide user-friendly fallback UIs.
