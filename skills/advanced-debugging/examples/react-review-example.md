# Code Review Example

**User Input:**
"Can you review my new React component? It fetches data and displays it."

```jsx
import React, { useState, useEffect } from 'react';

export default function UserList() {
  const [users, setUsers] = useState([]);
  
  useEffect(() => {
    fetch('/api/users')
      .then(res => res.json())
      .then(data => setUsers(data));
  }, []);

  return (
    <div>
      {users.map(u => <div><h1>{u.name}</h1><p dangerouslySetInnerHTML={{__html: u.bio}}></p></div>)}
    </div>
  );
}
```

---

**Agent Response:**

Here is a review of your `UserList` component. Overall, the structure makes sense, but there are a few critical issues regarding safety, component keys, and error handling.

### 🚨 Critical

**1. Security (XSS Vulnerability)**
You are using `dangerouslySetInnerHTML` for the user's bio. If users can input their own bios, this exposes your app to Cross-Site Scripting (XSS) attacks. 
*Fix:* Remove `dangerouslySetInnerHTML` and render it as a standard string. If HTML is required, use a sanitizer like `DOMPurify`.

**2. Missing React Keys**
When mapping over arrays in React, every element needs a unique `key` prop, otherwise React loses track of DOM elements during re-renders.
*Fix:* Add `key={u.id}` to the top-level `<div>` in the map.

### ⚠️ Warnings

**3. Unhandled Errors and Loading States**
If the network request fails, the component will crash silently or show a blank screen. It also doesn't indicate to the user that data is loading.
*Fix:* Wrap the fetch in a try/catch (or use `.catch()`) and add `loading` and `error` state variables.

### Suggested Refactor

Here is the updated, safer, and more robust version of your component:

```jsx
import React, { useState, useEffect } from 'react';

export default function UserList() {
  const [users, setUsers] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  
  useEffect(() => {
    const fetchUsers = async () => {
      try {
        const res = await fetch('/api/users');
        if (!res.ok) throw new Error('Failed to fetch users');
        const data = await res.json();
        setUsers(data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    
    fetchUsers();
  }, []);

  if (loading) return <p>Loading users...</p>;
  if (error) return <p className="text-red-500">Error: {error}</p>;

  return (
    <div className="flex flex-col gap-4">
      {users.map(u => (
        <div key={u.id} className="p-4 border rounded">
          <h2 className="text-xl font-bold">{u.name}</h2>
          {/* Render safely without dangerouslySetInnerHTML */}
          <p className="text-gray-700">{u.bio}</p>
        </div>
      ))}
    </div>
  );
}
```
