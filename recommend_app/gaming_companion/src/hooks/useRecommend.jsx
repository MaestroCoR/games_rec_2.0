import { createContext, useContext, useMemo, useState } from 'react';

const RecommendContext = createContext();

const RecommendProvider = ({ children }) => {
	const [pickedGames, setPickedGames_] = useState([]);

	const setPickedGames = (games) => {
		setPickedGames_(games);
	};

	console.log(pickedGames);

	// Memoized value of the  context
	const contextValue = useMemo(
		() => ({
			pickedGames,
			setPickedGames,
			pickGame: async (game) => {
				setPickedGames((prev) => [...prev, game]);
			},
			removeGame: async (game) => {
				setPickedGames((prev) => prev.filter((pickedGame) => pickedGame.id !== game.id));
			},
		}),
		[pickedGames],
	);

	// Provide the  context to the children components
	return <RecommendContext.Provider value={contextValue}>{children}</RecommendContext.Provider>;
};

export const useRecommend = () => {
	const context = useContext(RecommendContext);
	if (!context) {
		throw new Error('useRecommend must be used within an RecommendProvider');
	}
	return context;
};

export default RecommendProvider;
