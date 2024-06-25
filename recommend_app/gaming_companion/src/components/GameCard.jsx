import { Link } from 'react-router-dom';
import { useRecommend } from '../hooks/useRecommend';

const GameCard = ({ game, controls }) => {
	const { pickGame, removeGame } = useRecommend();

	return (
		<div className="hover:ring-4 relative rounded-sm hover:ring-[var(--secondary)] transition-all duration-300 ease-in-out group">
			<Link to={`/game/${game.id}`}>
				<img
					src={`https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/${game.steam_id}/library_600x900_2x.jpg?t=1568756407`}
					onError={(e) => {
						e.target.onerror = null;
						e.target.src = 'https://via.placeholder.com/600x900';
					}}
					alt={`${game.title} Poster`}
				/>
			</Link>
			{controls ? (
				<div className="absolute z-10 flex w-1/2 p-2 mx-auto text-3xl text-white transition-opacity duration-300 ease-in-out translate-x-1/2 rounded-lg opacity-0 justify-evenly bottom-4 bg-black/80 group-hover:opacity-100 ">
					<button
						className="hover:text-[var(--secondary)] transition-colors"
						onClick={() => pickGame(game)}>
						<i className="fa-fw far fa-eye"></i>
					</button>

					<button
						className="hover:text-[var(--secondary)] transition-colors"
						onClick={() => removeGame(game)}>
						<i className="fa-fw fa fa-times"></i>
					</button>
				</div>
			) : null}
			<Link to={`/game/${game.id}`}>
				<p className="text-xl font-medium text-center">{game.title}</p>
			</Link>
		</div>
	);
};

export default GameCard;
