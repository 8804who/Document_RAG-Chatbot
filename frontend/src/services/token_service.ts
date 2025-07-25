export function set_access_token(accessToken: string) {
    localStorage.setItem('access_token', accessToken);
}

export function get_token() {
    const accessToken = localStorage.getItem('access_token');
    return accessToken;
}

// Clear access token from localStorage and refresh token from cookies
export function clear_token() {
    localStorage.removeItem('access_token');
} 