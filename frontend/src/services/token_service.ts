export function setAccessToken(accessToken: string) {
    localStorage.setItem('accessToken', accessToken);
}

export function getToken() {
    const accessToken = localStorage.getItem('accessToken');
    return accessToken;
}

export function clearToken() {
    localStorage.removeItem('accessToken');
} 