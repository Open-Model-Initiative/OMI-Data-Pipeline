<div class="flex flex-row gap-4">
	<nav class="list-nav text-primary-300 font-extrabold flex flex-row bg-surface-700 w-32">
		<ul class="w-full">
			<li>
				<a href="/admin/users">
					<span class="flex-auto">Users</span>
				</a>
			</li>
			<li>
				<a href="/admin/teams">
					<span class="flex-auto">Teams</span>
				</a>
			</li>
			<li>
				<a href="/admin/feature-toggles">
					<span class="flex-auto">Feature Toggles</span>
				</a>
			</li>
			<li>
				<a href="/admin/moderation">
					<span class="flex-auto">Image Moderation</span>
				</a>
			</li>
		</ul>
	</nav>
	<main class="w-full p-8">
		<slot />
	</main>
</div>
