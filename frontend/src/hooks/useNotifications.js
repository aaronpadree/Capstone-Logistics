// import { useState, useEffect } from 'react';

// export function useNotifications() {
//   const [notifications, setNotifications] = useState([]); 
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState(null);

//   useEffect(() => {
//     async function fetchNotifications() {
//       try {
//         const response = await fetch('/api/inventory/notifications'); 
//         if (!response.ok) {
//           throw new Error('Failed to fetch notifications'); 
//         }
//         const data = await response.json();
//         setNotifications(data || []);
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     }

//     fetchNotifications();
//   }, []);

//   return { notifications, setNotifications, loading, error };
// }
import { useState, useEffect } from 'react';

export function useNotifications() {
  const [notifications, setNotifications] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let interval;

    const fetchNotifications = async () => {
      try {
        const response = await fetch('/api/inventory/notifications');
        if (!response.ok) {
          throw new Error('Failed to fetch notifications');
        }
        const data = await response.json();
        setNotifications(data || []);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };

    fetchNotifications(); 

    // Set up polling interval for real-time updates
    interval = setInterval(() => {
      fetchNotifications();
    }, 1000);

    // Clear the interval on unmount
    return () => clearInterval(interval);
  }, []);

  return { notifications, setNotifications, loading, error };
}
