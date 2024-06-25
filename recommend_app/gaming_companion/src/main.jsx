import React from 'react';
import ReactDOM from 'react-dom/client';
import App from './App.jsx';
import './index.css';
import { BrowserRouter } from 'react-router-dom';
import RecommendProvider from './hooks/useRecommend.jsx';

ReactDOM.createRoot(document.getElementById('root')).render(
	<React.StrictMode>
		<RecommendProvider>
			<BrowserRouter>
				<App />
			</BrowserRouter>
		</RecommendProvider>
	</React.StrictMode>,
);
