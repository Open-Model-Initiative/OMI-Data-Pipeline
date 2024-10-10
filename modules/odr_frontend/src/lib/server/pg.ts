import { get } from 'http';
import pg from 'pg';

export interface IDBUser {
	id: number;
	email: string;
	is_active: boolean;
	is_superuser: boolean;
	created_at: Date;
	updated_at: Date | null;
	user_type: 'user' | 'admin';
	name: string;
	emailVerified: boolean;
	image: string | null;
}

export interface IDBTeam {
	id: number;
	name: string;
	created_at: Date;
	updated_at: Date | null;
}

export interface IDBUserTeam {
	team_id: number;
	user_id: number;
	role: 'member' | 'admin';
	name: string;
}

export interface IFeatureToggle {
    id: number;
    feature_name: string;
    is_enabled: boolean;
    default_state: boolean;
}

export const pg_client_config = {
	host: process.env.POSTGRES_HOST,
	user: process.env.POSTGRES_USER,
	password: process.env.POSTGRES_PASSWORD,
	database: process.env.POSTGRES_DB,
	connectionTimeoutMillis: 2000
};

export const pgClient = new pg.Client(pg_client_config);

// Connect the client once when the module is loaded
pgClient.connect();

export const PG_API = {
	users: {
		get: async (id: number | string): Promise<IDBUser> => {
			const { rows } = await pgClient.query('SELECT * FROM users WHERE id=$1', [id]);
			return rows[0];
		},
		getAll: async (): Promise<IDBUser[]> => {
			const { rows } = await pgClient.query('SELECT * FROM users');
			return rows;
		}
	},
	teams: {
		get: async (id: number): Promise<IDBTeam> => {
			const { rows } = await pgClient.query('SELECT * FROM teams WHERE id=$1', [id]);
			return rows[0];
		},
		getAll: async (): Promise<IDBTeam[]> => {
			const { rows } = await pgClient.query('SELECT * FROM teams');
			return rows;
		},
		getUsers: async (team_id: number): Promise<IDBUserTeam[]> => {
			const { rows } = await pgClient.query('SELECT * FROM user_teams WHERE team_id=$1', [team_id]);
			return rows;
		},
		getAllUsers: async (): Promise<IDBUserTeam[]> => {
			const { rows } = await pgClient.query('SELECT * FROM user_teams');
			return rows;
		},
		getUser: async (user_id: number): Promise<IDBUserTeam[]> => {
			const { rows } = await pgClient.query(
				'SELECT * FROM user_teams t JOIN teams t2 on t2.id=t.team_id WHERE user_id=$1',
				[user_id]
			);
			return rows;
		}
	},
	featureToggles: {
        getAll: async (): Promise<IFeatureToggle[]> => {
            const { rows } = await pgClient.query('SELECT * FROM feature_toggles');
            return rows;
        }
    }
};

process.on('exit', () => {
	pgClient.end();
});
