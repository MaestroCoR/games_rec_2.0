import useUser from '../hooks/useUser';
import GameCard from './GameCard';

const WantPlayList = () => {
	const { user, isLoading, isError } = useUser();
	return (
		<div className="container p-4 mx-auto space-y-4">
			<h1 className="text-4xl font-bold">Your wishlist</h1>
			{/* <div className="mb-4">
			<input
				type="text"
				placeholder="Пошук гри за назвою"
				value={query}
				onChange={(e) => setQuery(e.target.value)}
				className="w-full p-2 border border-gray-300 rounded-md"
			/>
		</div> */}
			<div className="space-y-8 ">
				{user?.wishlists.length > 0 ? (
					<div className="grid grid-cols-5 gap-8">
						{user.wishlists?.map((entry) => (
							<GameCard game={entry.game} key={entry.game_id} />
						))}
					</div>
				) : (
					<h2 className="no-games">No games</h2>
				)}
			</div>
			{/* <div className="w-full text-center">
			<button
				className="p-2 text-xl text-white transition-colors bg-green-500 rounded-md hover:bg-green-300"
				disabled={isLoadingMore}
				onClick={() => setSize(size + 1)}>
				{isLoadingMore ? 'Loading...' : 'Load more'}
			</button>
		</div> */}
		</div>
	);
};

export default WantPlayList;
