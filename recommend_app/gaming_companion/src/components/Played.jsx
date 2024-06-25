import useUser from '../hooks/useUser';
import GameCard from './GameCard';
import axios from 'axios';
import { BACKEND_URL } from '../utils';
import { useEffect, useState } from 'react';

const WantPlayList = () => {
	const { user, isLoading, isError } = useUser();
	const [recommendations, setRecommendations] = useState([]);

	useEffect(() => {
		user && fetchRecommendations();
	}, [user]);

	if (isLoading) return <h1>Loading...</h1>;
	if (isError) return <h1>Error</h1>;

	const fetchRecommendations = async () => {
		try {
			const response = await axios.post(`${BACKEND_URL}/recommend/games`, {
				game_ids: user?.libraries?.map((entry) => entry.game_id),
			});
			setRecommendations(response.data.recommendation);
		} catch (error) {
			console.error(error);
		}
	};

	return (
		<div className="container p-4 mx-auto space-y-4">
			<h1 className="text-4xl font-bold">Your library</h1>
			<div className="space-y-8 ">
				{user?.libraries.length > 0 ? (
					<div className="grid grid-cols-5 gap-8">
						{user.libraries?.map((entry) => (
							<GameCard game={entry.game} key={entry.game_id} />
						))}
					</div>
				) : (
					<h2 className="no-games">No games</h2>
				)}
			</div>
			<h1 className="text-3xl font-semibold">Others gamers like you playing</h1>
			<div className="space-y-8 ">
				{recommendations?.length > 0 ? (
					<div className="grid grid-cols-5 gap-8">
						{recommendations.map((game) => (
							<GameCard game={game} key={game.game_id} />
						))}
					</div>
				) : (
					<h2 className="no-games">No games</h2>
				)}
			</div>
		</div>
	);
};

export default WantPlayList;
