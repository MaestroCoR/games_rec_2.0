import { Link } from 'react-router-dom';
import useUser from '../hooks/useUser';
import axios from 'axios';
import { BACKEND_URL } from '../utils';

const Header = () => {
	const { user, isLoading, isError } = useUser();

	const handleLogout = async () => {
		if (window.confirm('Are you sure you want to logout?')) {
			await axios.post(`${BACKEND_URL}/auth/logout`);
			window.location.href = '/';
		}
	};

	return (
		<header>
			<div className="container px-4 mx-auto">
				<div className="inner-content">
					<div className="brand">
						<Link to="/">GameCompanion</Link>
					</div>
					{user ? (
						<ul className="nav-links">
							<li>
								<Link to="/wantplaylist">Wantplaylist</Link>
							</li>
							<li>
								<li>
									<Link to="/played">Library</Link>
								</li>
								<button onClick={handleLogout} className="btn">
									Logout
								</button>
							</li>
						</ul>
					) : (
						<div className="flex gap-4">
							<ul className="nav-links">
								<li>
									<Link to="/recommend">Try recommendations</Link>
								</li>
							</ul>

							<Link to="/login" className="btn">
								Login
							</Link>

							<Link to="/register" className="btn">
								Register
							</Link>
						</div>
					)}
				</div>
			</div>
		</header>
	);
};

export default Header;
