import { BACKEND_URL } from '../utils';
import axios from 'axios';
import useSWRInfinite from 'swr/infinite';
import GameCard from './GameCard';
import { useEffect, useState } from 'react';
import { useDebounce } from '../utils';
import { useSearchParams } from 'react-router-dom';

const fetcher = (url) => axios.get(url).then((res) => res.data);

const PageHome = () => {
	const [searchParams, setSearchParams] = useSearchParams();
	const [query, setQuery] = useState(searchParams.get('q') || '');
	const debouncedQuery = useDebounce(query, 500);

	useEffect(() => {
		if (debouncedQuery) {
			setSearchParams({ q: debouncedQuery }, { replace: true });
		} else {
			setSearchParams({}, { replace: true });
		}
	}, [debouncedQuery, setSearchParams]);

	const { data, error, size, setSize } = useSWRInfinite(
		(index) => `${BACKEND_URL}/games?page=${index + 1}&title=${debouncedQuery}`,
		fetcher,
	);

	const isLoadingInitialData = !data && !error;
	const isLoadingMore = isLoadingInitialData || (data && typeof data[size - 1] === 'undefined');

	console.log(data);
	return (
		<div className="container p-4 mx-auto space-y-4">
			<h1 className="text-4xl font-bold">Games</h1>
			<div className="mb-4">
				<input
					type="text"
					placeholder="Пошук гри за назвою"
					value={query}
					onChange={(e) => setQuery(e.target.value)}
					className="w-full p-2 border border-gray-300 rounded-md"
				/>
			</div>
			<div className="space-y-8 ">
				{data &&
					data.map((page, index) => (
						<div key={index} className="grid grid-cols-5 gap-8">
							{page.games?.map((game) => (
								<GameCard game={game} key={game.id} />
							))}
						</div>
					))}
			</div>
			<div className="w-full text-center">
				<button
					className="p-2 text-xl text-white transition-colors bg-green-500 rounded-md hover:bg-green-300"
					disabled={isLoadingMore}
					onClick={() => setSize(size + 1)}>
					{isLoadingMore ? 'Loading...' : 'Load more'}
				</button>
			</div>
		</div>
	);
};

export default PageHome;
