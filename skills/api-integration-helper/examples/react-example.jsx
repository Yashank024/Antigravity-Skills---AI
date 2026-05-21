import React, { useState, useEffect } from 'react';

/**
 * UserProfile Example Component
 * Demonstrates state management, loading states, side effects, and modern Tailwind styling.
 */
const UserProfile = ({ userId }) => {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    const abortController = new AbortController();
    
    const fetchUser = async () => {
      setLoading(true);
      setError(null);
      try {
        // Simulated API call
        const response = await fetch(`https://api.example.com/users/${userId}`, {
          signal: abortController.signal
        });
        
        if (!response.ok) throw new Error('Failed to fetch user data');
        
        const data = await response.json();
        setUser(data);
      } catch (err) {
        if (err.name !== 'AbortError') {
          setError(err.message);
        }
      } finally {
        setLoading(false);
      }
    };

    fetchUser();
    
    return () => {
      abortController.abort();
    };
  }, [userId]);

  if (loading) {
    return (
      <div className="flex justify-center items-center h-48 bg-gray-50 dark:bg-gray-900 rounded-xl">
        <div className="text-blue-500 animate-pulse font-medium">Loading profile...</div>
      </div>
    );
  }

  if (error) {
    return (
      <div className="p-4 rounded-xl bg-red-50 dark:bg-red-900/20 border border-red-200 dark:border-red-800">
        <div className="text-red-600 dark:text-red-400 font-semibold flex items-center gap-2">
          <span>Error:</span> {error}
        </div>
      </div>
    );
  }

  if (!user) return null;

  return (
    <div className="max-w-sm rounded-2xl overflow-hidden shadow-lg bg-white dark:bg-gray-800 p-8 transition-transform duration-300 hover:-translate-y-2 border border-gray-100 dark:border-gray-700">
      <div className="relative">
        <div className="absolute inset-0 bg-gradient-to-tr from-blue-500 to-purple-500 rounded-full blur opacity-40"></div>
        <img 
          className="relative w-28 h-28 rounded-full mx-auto object-cover border-4 border-white dark:border-gray-800 shadow-sm" 
          src={user.avatarUrl || 'https://via.placeholder.com/150'} 
          alt={user.name} 
        />
      </div>
      
      <div className="text-center mt-6">
        <h3 className="font-bold text-2xl text-gray-900 dark:text-white mb-1">{user.name}</h3>
        <p className="text-gray-500 dark:text-gray-400 text-sm font-medium">{user.role || 'Developer'}</p>
      </div>
      
      <div className="mt-8 flex justify-center space-x-4 w-full">
        <button className="flex-1 bg-gradient-to-r from-blue-600 to-blue-700 hover:from-blue-700 hover:to-blue-800 text-white font-medium py-2.5 px-4 rounded-xl shadow-md shadow-blue-500/30 focus:outline-none focus:ring-2 focus:ring-blue-500 focus:ring-offset-2 dark:focus:ring-offset-gray-800 transition-all">
          Message
        </button>
      </div>
    </div>
  );
};

export default UserProfile;
