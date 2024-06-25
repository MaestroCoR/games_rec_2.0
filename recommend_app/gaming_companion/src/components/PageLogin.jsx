import { Link, Navigate } from 'react-router-dom';
import useUser from '../hooks/useUser';
import axios from 'axios';
import { useState } from 'react';
import { BACKEND_URL } from '../utils';

const PageLogin = () => {
	const { user, isLoading, isError, mutate } = useUser();
	const [error, setError] = useState();

	const handleSubmit = async (event) => {
		event.preventDefault();
		const formData = new FormData(event.target);
		const data = {};

		for (let [key, value] of formData.entries()) {
			data[key] = value;
		}

		try {
			await axios.post(`${BACKEND_URL}/auth/login`, data);
			await mutate();
		} catch (error) {
			console.error(error);
			setError(error.response.data.message);
		}
	};

	console.log(user, error);
	if (!isLoading && user) {
		return <Navigate to="/" />;
	}

	return (
		<div className="container p-4 mx-auto">
			<div className="flex items-center justify-center py-64">
				<form
					onSubmit={handleSubmit}
					className="min-w-96 py-4 px-6 text-lg border border-[var(--secondary)] flex flex-col gap-4 shadow-xl rounded-md">
					<h3 className="text-2xl font-semibold">Login to GameCompanion</h3>
					{error && <div className="">{error?.response?.message}</div>}
					<div className="flex flex-col w-full">
						<label htmlFor="username">Username</label>
						<input
							id="username"
							name="username"
							type="text"
							required
							placeholder="example_nickname"
							className="w-full border border-[var(--secondary)] rounded-sm px-2 py-0.5"
						/>
					</div>
					<div className="flex flex-col w-full">
						<label htmlFor="password">Password</label>
						<input
							id="password"
							name="password"
							type="password"
							minLength={8}
							required
							placeholder="********"
							className="w-full border border-[var(--secondary)] rounded-sm px-2 py-0.5 "
						/>
					</div>
					<div className="w-full">
						<p className="text-lg text-black/70">
							I want to{' '}
							<Link to={`/register`} className="font-semibold underline">
								create account
							</Link>
							.
						</p>
					</div>
					<button className="self-center btn">Увійти</button>
				</form>
			</div>
		</div>
	);
};

export default PageLogin;
