import Rater from 'react-rater';

const ReviewItem = ({ review }) => {
	return (
		<div className="">
			<div className="flex items-center gap-4">
				<img
					src={
						'https://ui-avatars.com/api/?name='.split() + review.user.username.split('_').join('+')
					}
					alt={review.user.username}
					className="w-12 h-12 rounded-full"
				/>
				<div>
					<p className="font-bold">{review.user.username}</p>
					<p>{new Date(review.created_at).toLocaleString()}</p>
				</div>
			</div>
			<div>
				<Rater total={5} rating={review.rating} interactive={false} />
				<p>{review.review_text}</p>
			</div>
		</div>
	);
};

export default ReviewItem;
