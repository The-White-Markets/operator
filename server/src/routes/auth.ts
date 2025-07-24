import { Router, Request, Response } from 'express';
import { PrismaClient } from '@prisma/client';
import { z } from 'zod';
import { hashPassword, comparePassword, generateToken } from '../utils/auth';
import { CreateUserData, LoginData } from '../types';

const router = Router();
const prisma = new PrismaClient();

// Validation schemas
const registerSchema = z.object({
  email: z.string().email(),
  name: z.string().min(2).max(50),
  password: z.string().min(6)
});

const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1)
});

// Register route
router.post('/register', async (req: Request, res: Response) => {
  try {
    const validatedData = registerSchema.parse(req.body) as CreateUserData;
    
    // Check if user already exists
    const existingUser = await prisma.user.findUnique({
      where: { email: validatedData.email }
    });

    if (existingUser) {
      return res.status(400).json({ error: 'User already exists with this email' });
    }

    // Hash password and create user
    const hashedPassword = await hashPassword(validatedData.password);
    const user = await prisma.user.create({
      data: {
        email: validatedData.email,
        name: validatedData.name,
        password: hashedPassword
      },
      select: {
        id: true,
        email: true,
        name: true,
        createdAt: true
      }
    });

    // Generate token
    const token = generateToken(user.id);

    res.status(201).json({
      message: 'User created successfully',
      user,
      token
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'Validation failed', details: error.errors });
    }
    console.error('Registration error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

// Login route
router.post('/login', async (req: Request, res: Response) => {
  try {
    const validatedData = loginSchema.parse(req.body) as LoginData;

    // Find user
    const user = await prisma.user.findUnique({
      where: { email: validatedData.email }
    });

    if (!user) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Check password
    const isValidPassword = await comparePassword(validatedData.password, user.password);
    if (!isValidPassword) {
      return res.status(401).json({ error: 'Invalid credentials' });
    }

    // Generate token
    const token = generateToken(user.id);

    res.json({
      message: 'Login successful',
      user: {
        id: user.id,
        email: user.email,
        name: user.name,
        createdAt: user.createdAt
      },
      token
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ error: 'Validation failed', details: error.errors });
    }
    console.error('Login error:', error);
    res.status(500).json({ error: 'Internal server error' });
  }
});

export default router;