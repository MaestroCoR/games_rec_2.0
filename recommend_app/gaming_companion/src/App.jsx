import './App.css';
import './lib/font-awesome/css/all.min.css';
import { Routes, Route } from 'react-router-dom';
import Header from './components/Header';
import PageHome from './components/PageHome';
import PageGame from './components/PageGame';
import PageLogin from './components/PageLogin';
import WantPlayList from './components/WantPlayList';
import Played from './components/Played';
import PageRegister from './components/PageRegister';
import Recommend from './components/Recommend';

function App() {
	return (
		<>
			<Header />
			<Routes>
				<Route path="/" element={<PageHome />} />
				<Route path="/login" element={<PageLogin />} />
				<Route path="/register" element={<PageRegister />} />
				<Route path="/game/:game_id" element={<PageGame />} />
				<Route path="/wantplaylist" element={<WantPlayList />} />
				<Route path="/played" element={<Played />} />
				<Route path="/recommend" element={<Recommend />} />
			</Routes>
		</>
	);
}

export default App;
