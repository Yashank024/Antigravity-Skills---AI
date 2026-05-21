---
name: modern-testing-expert
description: Writes unit and integration tests for modern JavaScript/TypeScript and React applications using Jest or Vitest. Emphasizes Test-Driven Development (TDD) and React Testing Library best practices.
---

# Modern Testing Expert

This skill provides expertise in writing robust, maintainable tests for front-end and full-stack JavaScript applications.

## Trigger Keywords

Activate this skill if the request mentions:
- test
- test this
- testing
- testing expertise
- generate tests
- test coverage
- unit test
- integration test
- test driven development
- tdd
- react testing library
- vitest
- jest
- mock api

## When to use

- Adding tests to new or existing React components.
- Writing unit tests for helper functions or hooks.
- Handling mocked API responses in test suites.
- Fixing or updating failing tests.

## Testing Pattern: Plan → Validate → Execute

Always follow this pattern before and during test creation:
1. **Plan**: Identify what needs to be tested (the happy path, edge cases, error states, and loading states).
2. **Validate**: Check the component's props, state behavior, and external dependencies (like API calls or contexts).
3. **Execute**: Write the test using the Arrange-Act-Assert methodology. Run the test to ensure it passes.

## Testing Workflow Checklist

When writing tests, adhere to these best practices:
- [ ] **Arrange-Act-Assert**: Structure every test clearly into these three phases.
- [ ] **Test Behavior, Not Implementation**: For React components, test what the user sees and interacts with using `@testing-library/react` (e.g., `findByRole`, `click`). Do not test internal component state directly.
- [ ] **Coverage**: Ensure you cover the happy path, at least one error path, and boundary conditions/edge cases.
- [ ] **Mocking**: properly mock out external side effects (network requests with MSW or Jest/Vitest mocks). Always clear mocks between tests (`afterEach(() => vi.clearAllMocks())`).
- [ ] **Accessibility**: Use appropriate ARIA roles for querying elements to simultaneously validate accessibility.
