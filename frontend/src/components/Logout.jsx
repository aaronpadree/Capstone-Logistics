import { FontAwesomeIcon } from '@fortawesome/react-fontawesome';
import { faSignOutAlt } from '@fortawesome/free-solid-svg-icons';
import { useNavigate } from 'react-router-dom';
import { supabase } from '../config/supabaseClient';
import toast from 'react-hot-toast';

const Logout = () => {
  const navigate = useNavigate();

  const handleLogout = async () => {
    try {
      const { error } = await supabase.auth.signOut();
      if (error) throw error;
      
      // Clear all auth-related data from localStorage
      localStorage.removeItem("session");
      localStorage.removeItem("profile");
      
      toast.success("Logged out successfully");
      // Use replace: true to prevent going back to protected pages
      navigate("/login", { replace: true });
    } catch (error) {
      toast.error(error.message || "Error logging out");
    }
  };

  return (
    <li>
      <button 
        onClick={handleLogout}
        className="text-white hover:bg-green-800 text-[15px] flex items-center rounded px-4 py-3 transition-all cursor-pointer w-full"
      >
        <FontAwesomeIcon icon={faSignOutAlt} className="mr-2" />
        <span>Logout</span>
      </button>
    </li>
  );
};

export default Logout;
