<script lang="ts">
	//Rules
	//Username
	const username_min_length = 4;
	const username_max_length = 20;
	const valid_username = /^[a-zA-Z0-9]+$/;
	//Email
	const valid_email = /^[a-zA-Z0-9._%]+(?:\.[a-zA-Z0-9._%]+)*@[a-zA-Z0-9-]+\.[a-zA-Z]{2,}$/;
	//Password
	const password_min_length = 8;
	const contains_lowercase = /[a-z]/;
	const contains_uppercase = /[A-Z]/;
	const contains_number = /[0-9]/;
	// eslint-disable-next-line no-useless-escape
	const contains_special = /[!@#$%^&*()_+\-=\[\]{};':"\\|,.<>\/?]/;

	let password_input = '',
		password_confirmation_input = '',
		email_input = '',
		username_input = '';

	$: username_respects_min_length = username_input.length >= username_min_length;
	$: username_respects_max_length = username_input.length <= username_max_length;
	$: username_respects_valid_format = valid_username.test(username_input);
	$: username_is_valid =
		username_respects_min_length && username_respects_max_length && username_respects_valid_format;

	$: email_is_valid = valid_email.test(email_input);

	$: password_respects_length = password_input.length >= password_min_length;
	$: password_respects_lowercase = contains_lowercase.test(password_input);
	$: password_respects_uppercase = contains_uppercase.test(password_input);
	$: password_respects_number = contains_number.test(password_input);
	$: password_respects_special = contains_special.test(password_input);
	$: password_is_valid =
		password_respects_length &&
		password_respects_lowercase &&
		password_respects_uppercase &&
		password_respects_number &&
		password_respects_special;
	$: password_confirmation_is_valid =
		password_input === password_confirmation_input && password_is_valid;
</script>

<svelte:head>
	<title>Register | OMI Data Pipeline</title>
</svelte:head>

<div class="container h-full mx-auto flex justify-center items-center">
	<div class="space-y-10 text-center flex flex-col items-center">
		<h2 class="h2">Register.</h2>
		<form action="/auth/register" method="post">
			<div class="text-left flex flex-col gap-4">
				<label class="label">
					<span>Username</span>
					<input
						class="input"
						type="text"
						name="username"
						bind:value={username_input}
						class:input-success={username_is_valid}
						class:input-error={!username_is_valid}
					/>
				</label>
				<label class="label">
					<span>E-mail (Is valid?: {email_is_valid})</span>
					<input
						class="input"
						type="text"
						name="email"
						bind:value={email_input}
						class:input-success={email_is_valid}
						class:input-error={!email_is_valid}
					/>
				</label>

				<label class="label">
					<span>Password (Is Valid?: {password_is_valid} | {password_input})</span>
					<input
						class="input"
						type="password"
						name="password"
						bind:value={password_input}
						class:input-success={password_is_valid}
						class:input-error={!password_is_valid}
					/>
				</label>

				<label class="label">
					<span>Repeat Password (Matches?: {password_confirmation_is_valid})</span>
					<input
						class="input"
						type="password"
						name="password_confirmation"
						bind:value={password_confirmation_input}
						class:input-success={password_confirmation_is_valid}
						class:input-error={!password_confirmation_is_valid}
					/>
				</label>
			</div>
			<button
				class="btn bg-gradient-to-br variant-gradient-secondary-tertiary w-full mt-4"
				type="submit"
				disabled={!email_is_valid || !password_is_valid || !password_confirmation_is_valid}
				>Register</button
			>
		</form>
		<small class="text-sm"
			>Already have an account? <a href="/login" class="text-blue-500">Log in</a></small
		>
	</div>
</div>
