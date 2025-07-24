import { Request } from 'express';

export interface AuthRequest extends Request {
  userId?: string;
}

export interface CreateUserData {
  email: string;
  name: string;
  password: string;
}

export interface LoginData {
  email: string;
  password: string;
}

export interface CreateTaskData {
  title: string;
  description?: string;
  priority?: 'low' | 'medium' | 'high';
  dueDate?: string;
}

export interface UpdateTaskData {
  title?: string;
  description?: string;
  completed?: boolean;
  priority?: 'low' | 'medium' | 'high';
  dueDate?: string;
}