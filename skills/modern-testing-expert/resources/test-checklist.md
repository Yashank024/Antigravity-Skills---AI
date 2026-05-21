# Comprehensive Testing Checklist

## General JavaScript / TypeScript Unit Tests
- [ ] Are pure functions tested with variety of input permutations?
- [ ] Are null, undefined, and empty string edge cases handled?
- [ ] Are errors explicitly caught and tested using `expect(() => fn()).toThrow()`?

## React Component Testing (React Testing Library)
- [ ] Are queries prioritizing accessibility (e.g., `getByRole`, `getByLabelText`) over `getByTestId`?
- [ ] Is userEvent used instead of fireEvent for simulating interactions?
- [ ] Are asynchronous updates wrapped in `waitFor` or using `findBy*` queries?
- [ ] Is cleanup handled? (Note: RTL handles this automatically in modern setups, but verify side effects).

## Integration / Mocking
- [ ] Are native APIs (like `window.localStorage` or `navigator`) mocked if used?
- [ ] Are timers mocked (`vi.useFakeTimers()`) for testing `setTimeout` or intervals?
- [ ] Is network data mocked gracefully?
