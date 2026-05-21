import { render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { describe, it, expect, vi, beforeEach } from 'vitest';
import LoginForm from './LoginForm';

// Mocking an external API module
import * as api from '../utils/api';
vi.mock('../utils/api');

describe('LoginForm Component', () => {
  beforeEach(() => {
    vi.clearAllMocks();
  });

  it('renders login form correctly', () => {
    // Arrange & Act
    render(<LoginForm />);
    
    // Assert
    expect(screen.getByRole('heading', { name: /login/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/email/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/password/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /submit/i })).toBeInTheDocument();
  });

  it('shows validation errors on empty submission', async () => {
    const user = userEvent.setup();
    render(<LoginForm />);
    
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    expect(await screen.findByText(/email is required/i)).toBeInTheDocument();
    expect(api.loginUser).not.toHaveBeenCalled();
  });

  it('submits form successfully with valid credentials', async () => {
    const user = userEvent.setup();
    api.loginUser.mockResolvedValueOnce({ token: 'mock-jwt-token' });
    
    render(<LoginForm onSuccess={vi.fn()} />);
    
    await user.type(screen.getByLabelText(/email/i), 'test@example.com');
    await user.type(screen.getByLabelText(/password/i), 'password123');
    await user.click(screen.getByRole('button', { name: /submit/i }));
    
    await waitFor(() => {
      expect(api.loginUser).toHaveBeenCalledWith('test@example.com', 'password123');
    });
  });
});
