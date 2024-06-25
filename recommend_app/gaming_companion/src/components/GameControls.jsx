import { BACKEND_URL } from '../utils';
import axios from 'axios';

const GameControls = ({ game, type }) => {
	const addGameToPlayed = async (game) => {
		await axios.post(`${BACKEND_URL}/playedlist`, game);
	};

	const removeGameFromPlayedlist = async (id) => {
		await axios.delete(`${BACKEND_URL}/playedlist/${id}`);
	};

	const moveToPlayedlist = async (game) => {
		await axios.post(`${BACKEND_URL}/playedlist`, game);
		await axios.delete(`${BACKEND_URL}/played/${game.id}`);
	};

	const removeFromPlayedlist = async (id) => {
		await axios.delete(`${BACKEND_URL}/played/${id}`);
	};

	const removeFromRecommend = async (id) => {
		await axios.delete(`${BACKEND_URL}/recommend/${id}`);
	};

	return (
		<div className="inner-card-controls">
			<button className="ctrl-btn" onClick={() => addGameToPlayed(game)}>
				<i className="fa-fw far fa-eye"></i>
			</button>

			<button className="ctrl-btn" onClick={() => removeGameFromPlayedlist(game.id)}>
				<i className="fa-fw fa fa-times"></i>
			</button>
		</div>
	);
};

export default GameControls;
