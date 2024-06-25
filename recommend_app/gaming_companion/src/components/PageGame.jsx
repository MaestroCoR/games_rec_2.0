import axios from 'axios';
import useSWR from 'swr';
import Rater from 'react-rater';
import 'react-rater/lib/react-rater.css';
import { Link, useParams } from 'react-router-dom';
import { BACKEND_URL } from '../utils';
import ReviewItem from './ReviewItem';
import useUser from '../hooks/useUser';
import { useState } from 'react';

const fetcher = (url) => axios.get(url).then((res) => res.data);

const PageGame = () => {
	const { game_id } = useParams();
	const { user, mutate: mutateUser } = useUser();
	const { data, error, mutate } = useSWR(`${BACKEND_URL}/games/${game_id}`, fetcher);

	const [reviewRate, setReviewRate] = useState();

	if (error) return <div>Error</div>;
	if (!data) return <div>Loading...</div>;

	const rating =
		data.ratings?.length > 0
			? data.ratings.reduce((acc, curr) => acc + curr.rating, 0) / data.ratings.length
			: 0;

	const isReviewed = data.reviews.some((review) => review.user_id === user?.id);

	const handleMakeReview = async (event) => {
		event.preventDefault();

		if (!user) {
			return;
		}

		if (!reviewRate) {
			alert('Please rate the game!');
			return;
		}

		const formData = new FormData(event.target);
		const data = {};
		for (let [key, value] of formData.entries()) {
			data[key] = value;
		}

		data['game_id'] = game_id;
		data['rating'] = reviewRate;

		try {
			console.log(data);
			await axios.post(`${BACKEND_URL}/reviews`, data);
			await mutate();
		} catch (error) {
			console.error(error);
		}
	};

	const inUserLibrary = user?.libraries.some((library) => library.game_id == game_id);
	const handleAddToLibrary = async () => {
		await axios.post(`${BACKEND_URL}/user_libraries/${game_id}`);
		await mutateUser();
	};

	const handleRemoveFromLibrary = async () => {
		await axios.delete(`${BACKEND_URL}/user_libraries/${game_id}`);
		await mutateUser();
	};

	const inUserWishlist = user?.wishlists.some((wishlist) => wishlist.game_id == game_id);
	const handleAddToWishlist = async () => {
		await axios.post(`${BACKEND_URL}/wishlists/${game_id}`);
		await mutateUser();
	};

	const handleRemoveFromWishlist = async () => {
		await axios.delete(`${BACKEND_URL}/wishlists/${game_id}`);
		await mutateUser();
	};

	const handleAddRate = async (rating) => {
		await axios.post(`${BACKEND_URL}/user_ratings/${game_id}`, { rating });
		await mutate();
	};

	return (
		<div className="container relative p-4 mx-auto">
			<div className="flex gap-8 max-sm:flex-col">
				<div className="sm:max-w-96">
					<div className="sticky top-0 w-full space-y-2">
						<img
							src={`https://shared.cloudflare.steamstatic.com/store_item_assets/steam/apps/${data.steam_id}/library_600x900_2x.jpg?t=1568756407`}
							onError={(e) => {
								e.target.onerror = null;
								e.target.src = 'https://via.placeholder.com/600x900';
							}}
							alt={`${data.title} Poster`}
							className="h-auto mx-auto rounded shadow-lg sm:max-w-full"
						/>
						<h1 className="text-4xl font-bold sm:hidden">{data.title}</h1>
						{!!user && (
							<div className="flex justify-center gap-2 max-sm:flex-col">
								{inUserLibrary ? (
									<button onClick={handleRemoveFromLibrary} className="btn bg-amber-400">
										Remove from library
									</button>
								) : (
									<button onClick={handleAddToLibrary} className="btn">
										Add to library
									</button>
								)}
								{inUserWishlist ? (
									<button onClick={handleRemoveFromWishlist} className="btn bg-amber-400">
										Remove from wishlist
									</button>
								) : (
									<button onClick={handleAddToWishlist} className="btn">
										Add to wishlist
									</button>
								)}
							</div>
						)}
						<div className="flex items-center justify-center text-4xl">
							<Rater
								total={5}
								rating={rating}
								onRate={({ rating }) => handleAddRate(rating)}
								interactive={!!user}
							/>
							<span className="text-3xl">{rating.toFixed(1)}</span>
						</div>
						<p>Release Date: {data.release_date}</p>
						<p>Genres: {data.genres}</p>
						<p className="text-justify">{data.short_description}</p>
					</div>
				</div>
				<div className="flex-1 pb-20 space-y-4">
					<h1 className="text-4xl font-bold max-sm:hidden">{data.title}</h1>
					<div dangerouslySetInnerHTML={{ __html: data.detailed_description }}></div>
					<div></div>
					<div className="border border-[var(--secondary)] p-2 rounded-sm">
						{!user ? (
							<p className="font-medium">
								Please{' '}
								<Link to={`/login`} className="font-semibold underline">
									authenticate
								</Link>{' '}
								to leave a review.
							</p>
						) : !isReviewed ? (
							<form onSubmit={handleMakeReview} className="flex flex-col gap-2">
								<label htmlFor="rating">Your rate</label>
								<div className="text-3xl">
									<Rater total={5} onRate={({ rating }) => setReviewRate(rating)} />
								</div>
								<label htmlFor="review">Your thoughts</label>
								<textarea
									name="review_text"
									id="review"
									required
									className="w-full p-2 border border-gray-300 rounded-md"
								/>
								<button className="btn">Make review</button>
							</form>
						) : (
							<p>You have already reviewed this game.</p>
						)}
					</div>
					<div className="space-y-4">
						{data.reviews?.length > 0 ? (
							data.reviews
								.sort((a) => (a.user_id === user?.id ? -1 : 1))
								.map((review) => <ReviewItem key={review.id} review={review} />)
						) : (
							<p>No reviews yet</p>
						)}
					</div>
				</div>
			</div>
		</div>
	);
};

export default PageGame;
