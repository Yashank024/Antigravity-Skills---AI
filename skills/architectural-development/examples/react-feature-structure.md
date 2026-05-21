# Modular React Feature Structure

When scaffolding a scalable React or Next.js application, recommend the **Feature-Driven Structure**. Below is the recommended mental model for organizing the `src` directory.

```text
src/
├── app/                  # App-wide settings, routing, and global providers
│   ├── store.js          # Global state (if necessary)
│   └── index.jsx         # App entry point
│
├── features/             # Feature-based modules (The core of the app)
│   ├── auth/             # Example Feature: Authentication
│   │   ├── api/          # API requests related to auth
│   │   ├── components/   # UI components strictly for auth
│   │   ├── hooks/        # Custom hooks containing auth business logic
│   │   ├── utils/        # Auth-specific formatting/helpers
│   │   └── index.js      # Public API for the `auth` module (Export only what's needed)
│   │
│   └── dashboard/        # Example Feature: Dashboard
│       ├── api/
│       ├── components/
│       └── index.js
│
├── shared/               # Truly generic, cross-feature code
│   ├── components/       # e.g., PrimaryButton, Modal base
│   ├── hooks/            # e.g., useClickOutside, useWindowSize
│   └── utils/            # e.g., formatDate, validators
│
└── assets/               # Static files (images, global CSS)
```

## Why this works for Scalability
By keeping the API, UI, and logic for a specific feature (like `auth`) co-located, developers do not have to jump between 4 different root folders (`/components`, `/hooks`, `/api`, `/utils`) to understand one feature. The `index.js` acts as a barrel file to explicitly define the public contract of that feature.
