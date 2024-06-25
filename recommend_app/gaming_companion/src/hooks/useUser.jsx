import useSWR from 'swr';
import axios from 'axios';
import { BACKEND_URL } from '../utils';

const fetcher = (url) => axios.get(url, { withCredentials: true }).then((res) => res.data);

const useUser = () => {
	const { data, error, isLoading, mutate } = useSWR(`${BACKEND_URL}/auth/current_user`, fetcher, {
		focusThrottleInterval: 60000,
		shouldRetryOnError: false,
	});

	return {
		user: data,
		isLoading,
		isError: error,
		mutate,
	};
};

export default useUser;
