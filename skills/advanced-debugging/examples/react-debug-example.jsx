import React, { useState, useEffect, useCallback } from 'react';

// INCORRECT VERSION: Causes an infinite loop because `fetchData` is recreated on every render,
// triggering the `useEffect`, which updates state, causing a re-render.
/*
const BuggyComponent = ({ userId }) => {
  const [data, setData] = useState(null);

  const fetchData = async () => {
    const response = await fetch(`/api/user/${userId}`);
    const result = await response.json();
    setData(result);
  };

  useEffect(() => {
    fetchData();
  }, [fetchData]); // 🔴 Danger: fetchData reference changes every render
  
  return <div>{data?.name}</div>;
};
*/

// CORRECT VERSION: Uses useCallback to memoize the function, ensuring its reference
// remains stable unless its dependencies (userId) change.
const FixedComponent = ({ userId }) => {
  const [data, setData] = useState(null);
  const [error, setError] = useState(null);

  // 1. ISOLATE: The infinite loop comes from the useEffect dependency.
  // 2. HYPOTHESIS: `fetchData` is unstable. We must memoize it.
  
  const fetchData = useCallback(async () => {
    try {
      const response = await fetch(`/api/user/${userId}`);
      if (!response.ok) throw new Error('Network response was not ok');
      const result = await response.json();
      setData(result);
    } catch (err) {
      setError(err.message);
    }
  }, [userId]); // Stable reference

  useEffect(() => {
    fetchData();
  }, [fetchData]); // Now safe

  // 3. VERIFY: Component now only fetches when userId changes.

  if (error) return <div>Error: {error}</div>;
  if (!data) return <div>Loading...</div>;

  return <div>{data.name}</div>;
};

export default FixedComponent;
