<svelte:head>
	<title>Login | OMI Data Pipeline</title>
</svelte:head>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Authenticate.</h2>
		<form action="/auth/login" method="post">
			<div class="text-left flex flex-col gap-4">
				<label class="label">
					<span>Username</span>
					<input class="input" type="text" name="username" />
				</label>

				<label class="label">
					<span>Password</span>
					<input class="input" type="password" name="password" />
				</label>
			</div>
			<button
				class="btn bg-gradient-to-br variant-gradient-primary-secondary w-full mt-4"
				type="submit">Login</button
			>
		</form>
		<small class="text-sm"
			>Don't have an account? <a href="register" class="text-blue-500">Register</a></small
		>
	</div>
</div>
