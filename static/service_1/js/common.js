// Меню, на случай если тупит hover при наведении у бутстрапа
(function () {
	const isDesktop = () => window.matchMedia('(min-width: 992px)').matches;
	function bindHoverMenus() {
		document.querySelectorAll('.navbar .dropdown').forEach(function (dd) {
			const toggle = dd.querySelector('[data-bs-toggle="dropdown"]');
			const menu = dd.querySelector('.dropdown-menu');
			if (!toggle || !menu) return;

			let bsDropdown = bootstrap.Dropdown.getOrCreateInstance(toggle, { popperConfig: { strategy: 'fixed' } });

			dd.addEventListener('mouseenter', () => { if (isDesktop()) bsDropdown.show(); });
			dd.addEventListener('mouseleave', () => { if (isDesktop()) bsDropdown.hide(); });
		});
	}

	bindHoverMenus();
	window.addEventListener('resize', bindHoverMenus);
})();
