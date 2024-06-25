import { useState } from 'react';
import GameCard from './GameCard';
import axios from 'axios';
import { BACKEND_URL } from '../utils';
import { useRecommend } from '../hooks/useRecommend';

const Recommend = () => {
	const { pickedGames } = useRecommend();
	const [query, setQuery] = useState('');
	const [results, setResults] = useState([]);
	const [recommendedResults, setRecommendedResults] = useState([]);

	const onChange = (e) => {
		e.preventDefault();
		setQuery(e.target.value);

		if (e.target.value.trim() === '') {
			setResults([]);
			return;
		}

		fetch(`${BACKEND_URL}/games?title=${e.target.value}`, {
			method: 'GET',
			headers: { 'Content-Type': 'application/json' },
		})
			.then((res) => {
				if (!res.ok) {
					throw new Error(`HTTP error! status: ${res.status}`);
				}
				return res.json();
			})
			.then((data) => {
				setResults(data.games);
			})
			.catch((error) => {
				console.error('Error fetching data:', error);
				setResults([]);
			});
	};

	const handleSubmit = (event) => {
		event.preventDefault();

		// Отримання id з об'єктів recommend
		const ids = pickedGames
			.map((item) => item.id) // Отримання id з кожного об'єкта
			.filter((id) => (typeof id === 'string' ? id.trim() !== '' : id !== undefined)); // Фільтрування пустих id

		console.log(ids);

		// Відправка POST-запиту з id на сервер
		axios
			.post(`${BACKEND_URL}/recommend/games`, { game_ids: ids })
			.then((response) => {
				console.log(response.data);
				// Оновлення стану з отриманими рекомендаціями
				setRecommendedResults(response.data.recommendation);
			})
			.catch((error) => {
				console.error('Error:', error);
			});
	};
	return (
		<div className="container p-4 mx-auto">
			<div className="flex flex-col gap-8 md:flex-row">
				<div className="md:w-1/2">
					<div className="mb-4">
						<input
							type="text"
							placeholder="Пошук гри"
							value={query}
							onChange={onChange}
							className="w-full p-2 border border-gray-300 rounded-md"
						/>
						{results.length > 0 && (
							<div className="grid max-w-full grid-cols-4 gap-4 mt-2 bg-white rounded-lg shadow-lg">
								{results.map((game) => (
									<GameCard game={game} key={game.id} controls={true} />
								))}
							</div>
						)}
					</div>
					<div className="mt-8">
						<div className="mb-4 header">
							<h1 className="text-2xl font-bold">Taken for recommendation</h1>
						</div>
						{pickedGames.length > 0 ? (
							<div>
								<div className="grid grid-cols-1 gap-4 mb-4 sm:grid-cols-3">
									{pickedGames.map((game) => (
										<GameCard game={game} key={game.id} type="recommend" />
									))}
								</div>
								<button
									onClick={handleSubmit}
									className="px-4 py-2 text-white bg-blue-500 rounded-md">
									Recommend
								</button>
							</div>
						) : (
							<h2 className="text-xl text-gray-500">No games</h2>
						)}
					</div>
				</div>
				<div className="w-full md:w-1/2">
					<div className="mt-8 md:mt-0">
						<div className="mb-4 header">
							<h1 className="text-2xl font-bold">Recommended Games</h1>
						</div>
						{recommendedResults.length > 0 ? (
							<div>
								<div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
									{recommendedResults.map((game) => (
										<GameCard game={game} key={game.id} controls={true} />
									))}
								</div>
							</div>
						) : (
							<h2 className="text-xl text-gray-500">No games</h2>
						)}
					</div>
				</div>
			</div>
		</div>
	);
};

export default Recommend;
