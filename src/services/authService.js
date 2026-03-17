const API_URL = 'http://localhost:3000/api';

const mockUsers = [];

export async function loginUser(email, password) {
    try {
        const res = await fetch(`${API_URL}/login`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ email, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || 'Login failed');
        return data;
    } catch (err) {
        const found = mockUsers.find(u => u.email === email && u.password === password);
        if (found) {
            return { token: 'mock-token-' + Date.now(), user: { email: found.email, name: found.name } };
        }
        throw new Error('Invalid email or password');
    }
}

export async function registerUser(name, email, password) {
    try {
        const res = await fetch(`${API_URL}/register`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name, email, password })
        });
        const data = await res.json();
        if (!res.ok) throw new Error(data.message || 'Registration failed');
        return data;
    } catch (err) {
        const exists = mockUsers.find(u => u.email === email);
        if (exists) throw new Error('Email already in use');
        const newUser = { name, email, password };
        mockUsers.push(newUser);
        return { token: 'mock-token-' + Date.now(), user: { email, name } };
    }
}

export function logoutUser() {
    return Promise.resolve({ success: true });
}
