import { writable } from 'svelte/store';
import { goto as _goto } from '$app/navigation';
import * as m from '$paraglide/messages';

interface Breadcrumb {
	label: string;
	href: string;
	icon?: string;
}

const homeCrumb: Breadcrumb = { label: m.home(), href: '/', icon: 'fa-regular fa-compass' };

const createBreadcrumbs = (initialValue: Breadcrumb[]) => {
	const breadcrumbs = writable<Breadcrumb[]>(initialValue);

	function push(crumb: Breadcrumb) {
		breadcrumbs.update((value) => {
			return [...value, crumb];
		});
	}

	function replace(crumb: Breadcrumb) {
		breadcrumbs.update(() => {
			return [homeCrumb, crumb];
		});
	}

	function slice(index: number) {
		breadcrumbs.update((value) => {
			return value.slice(0, index + 1);
		});
	}

	return {
		...breadcrumbs,
		push,
		replace,
		slice
	};
};

export const breadcrumbs = createBreadcrumbs([homeCrumb]);

export function goto(
	url: string,
	_opts: { crumbs: typeof breadcrumbs; label: string; breadcrumbAction: 'push' }
) {
	const opts = {
		crumbs: breadcrumbs,
		label: '',
		breadcrumbAction: 'replace',
		..._opts
	};

	const { crumbs, label, breadcrumbAction } = opts;
	const crumb = { label, href: url };
	crumbs[breadcrumbAction](crumb);
	return _goto(url, opts);
}
