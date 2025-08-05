export type BaseEntity = {
  id: string;
  createdAt: number;
};

export type Entity<T> = {
  [K in keyof T]: T[K];
} & BaseEntity;

export type Meta = {
  page: number;
  total: number;
  totalPages: number;
};

export type User = Entity<{
  id: string;
  email: string;
  role: 'ADMIN' | 'USER';
  prefs: {
    pref: string;
  };
}>;

export type AuthResponse = {
  data: {
    username: string;
    email: string;
  };
};
