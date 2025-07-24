import axios, { AxiosError } from 'axios';
import { 
  Task, 
  CreateTaskData, 
  UpdateTaskData, 
  LoginData, 
  RegisterData, 
  AuthResponse,
  ApiError 
} from '../types';

const API_URL = import.meta.env.VITE_API_URL || 'http://localhost:3001/api';

// Create axios instance
const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Handle response errors
api.interceptors.response.use(
  (response) => response,
  (error: AxiosError<ApiError>) => {
    if (error.response?.status === 401) {
      localStorage.removeItem('token');
      localStorage.removeItem('user');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// Auth API
export const authAPI = {
  register: async (data: RegisterData): Promise<AuthResponse> => {
    const response = await api.post('/auth/register', data);
    return response.data;
  },

  login: async (data: LoginData): Promise<AuthResponse> => {
    const response = await api.post('/auth/login', data);
    return response.data;
  },
};

// Tasks API
export const tasksAPI = {
  getTasks: async (): Promise<Task[]> => {
    const response = await api.get('/tasks');
    return response.data;
  },

  getTask: async (id: string): Promise<Task> => {
    const response = await api.get(`/tasks/${id}`);
    return response.data;
  },

  createTask: async (data: CreateTaskData): Promise<Task> => {
    const response = await api.post('/tasks', data);
    return response.data;
  },

  updateTask: async (id: string, data: UpdateTaskData): Promise<Task> => {
    const response = await api.put(`/tasks/${id}`, data);
    return response.data;
  },

  deleteTask: async (id: string): Promise<void> => {
    await api.delete(`/tasks/${id}`);
  },
};

export default api;