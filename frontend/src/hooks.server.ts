import { safeTranslate } from '$lib/utils/i18n';
import { BASE_API_URL } from '$lib/utils/constants';
import type { User } from '$lib/utils/types';
import { redirect, type Handle, type RequestEvent, type HandleFetch } from '@sveltejs/kit';
import { setFlash } from 'sveltekit-flash-message/server';
import { getLocale, setLocale } from '$paraglide/runtime';
import { DEFAULT_LANGUAGE } from '$lib/utils/constants';

import { loadFeatureFlags } from '$lib/feature-flags';

async function ensureCsrfToken(event: RequestEvent): Promise<string> {
	let csrfToken = event.cookies.get('csrftoken') || '';
	if (!csrfToken) {
		const response = await fetch(`${BASE_API_URL}/csrf/`, {
			credentials: 'include',
			headers: { 'content-type': 'application/json' }
		});
		const data = await response.json();
		csrfToken = data.csrfToken;
		event.cookies.set('csrftoken', csrfToken, {
			httpOnly: false,
			sameSite: 'lax',
			path: '/',
			secure: true
		});
	}
	return csrfToken;
}

function logoutUser(event: RequestEvent) {
	event.cookies.delete('token', {
		path: '/'
	});
	const allauthSessionToken = event.cookies.get('allauth_session_token');
	if (allauthSessionToken) {
		event.cookies.delete('allauth_session_token', { path: '/' });
	}
	redirect(302, `/login?next=${event.url.pathname}`);
}

async function validateUserSession(event: RequestEvent): Promise<User | null> {
	const token = event.cookies.get('token');
	if (!token) return null;

	const allauthSessionToken = event.cookies.get('allauth_session_token');
	if (!allauthSessionToken) logoutUser(event);

	const res = await fetch(`${BASE_API_URL}/iam/current-user/`, {
		credentials: 'include',
		headers: {
			'content-type': 'application/json',
			Authorization: `Token ${token}`
		}
	});

	if (!res.ok) logoutUser(event);

	return res.json();
}

export const handle: Handle = async ({ event, resolve }) => {
	event.locals.featureFlags = loadFeatureFlags();

	await ensureCsrfToken(event);

	if (event.locals.user) return await resolve(event);

	const errorId = new URL(event.request.url).searchParams.get('error');
	if (errorId) {
		setLocale(event.cookies.get('PARAGLIDE_LOCALE') || DEFAULT_LANGUAGE);
		setFlash({ type: 'error', message: safeTranslate(errorId) }, event);
		redirect(302, '/login');
	}

	const user = await validateUserSession(event);
	if (user) {
		event.locals.user = user;
		const generalSettings = await fetch(`${BASE_API_URL}/settings/general/object/`, {
			credentials: 'include',
			headers: {
				'content-type': 'application/json',
				Authorization: `Token ${event.cookies.get('token')}`
			}
		});
		event.locals.settings = await generalSettings.json();
	}

	return await resolve(event);
};

export const handleFetch: HandleFetch = async ({ request, fetch, event: { cookies } }) => {
	const unsafeMethods = new Set(['POST', 'PUT', 'PATCH', 'DELETE']);
	const currentLang = cookies.get('PARAGLIDE_LOCALE') || DEFAULT_LANGUAGE;
	if (request.url.startsWith(BASE_API_URL)) {
		request.headers.set('Content-Type', 'application/json');
		request.headers.set('Accept-Language', currentLang);

		const token = cookies.get('token');
		const csrfToken = cookies.get('csrftoken');

		if (token) {
			request.headers.append('Authorization', `Token ${token}`);
		}

		if (unsafeMethods.has(request.method) && csrfToken) {
			request.headers.append('X-CSRFToken', csrfToken);
			request.headers.append('Cookie', `csrftoken=${csrfToken}`);
		}
	}

	if (request.url.startsWith(`${BASE_API_URL}/_allauth/app`)) {
		const allauthSessionToken = cookies.get('allauth_session_token');
		if (allauthSessionToken) {
			request.headers.append('X-Session-Token', allauthSessionToken);
		}
	}

	return fetch(request);
};
