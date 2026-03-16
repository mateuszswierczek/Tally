export interface AuthContext {
    token: string | null
    login: (token:string) => void
    logout: () => void
}

export function getToken() {
    return localStorage.getItem('token')
}